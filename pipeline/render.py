#!/usr/bin/env python3
"""Scene renderer: illustrated layers + camera moves + parallax + animated FX -> 1080p30 MP4.

Usage:
  python3 /home/claude/pipeline/render.py PROJ                  # render changed scenes, then assemble PROJ/out/final.mp4
  python3 /home/claude/pipeline/render.py PROJ --stills 3,60.5   # write check frames at those global times -> PROJ/check/
  python3 /home/claude/pipeline/render.py PROJ --contact         # contact sheet of every scene's middle frame -> PROJ/check/contact_*.jpg
  python3 /home/claude/pipeline/render.py PROJ --only s012,s013  # force re-render of some scenes
  python3 /home/claude/pipeline/render.py PROJ --scenes-only     # render scenes, skip final assembly
Needs PROJ/story.json and PROJ/audio/timeline.json (run tts.py first). Uses PROJ/audio/mix.wav if present.
See /home/claude/pipeline/README.md for the scene format.
"""
import json, sys, os, math, hashlib, subprocess, fcntl, time, argparse, zlib
import numpy as np, cv2

PIPE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1920, 1080, 30
VERSION = "r9"
CACHE = os.path.join(PIPE, "cache"); os.makedirs(CACHE, exist_ok=True)

# ---------------------------------------------------------------- helpers
def ease(u, kind="inout"):
    u = min(max(u, 0.0), 1.0)
    if kind == "linear": return u
    if kind == "in": return u * u
    if kind == "out": return 1 - (1 - u) ** 2
    return 0.5 - 0.5 * math.cos(math.pi * u)

def smooth_noise(t, seed, speed=1.0):
    r = np.random.default_rng(seed)
    fr = r.uniform(0.3, 1.7, 4) * speed; ph = r.uniform(0, 6.28, 4)
    return float(sum(math.sin(t * f * 6.283 + p) for f, p in zip(fr, ph)) / 4)

def mat3(m2):
    m = np.eye(3); m[:2] = m2; return m

def T(dx, dy): return np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1.0]])
def S(s, cx, cy): return T(cx, cy) @ np.array([[s, 0, 0], [0, s, 0], [0, 0, 1.0]]) @ T(-cx, -cy)
def R(deg, cx, cy):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return T(cx, cy) @ np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]]) @ T(-cx, -cy)

GRADES = {
    "none":   dict(sat=1.00, gain=(1, 1, 1), lift=(0, 0, 0), gamma=1.0, contrast=1.0),
    "night":  dict(sat=0.80, gain=(0.86, 0.96, 1.08), lift=(4, 8, 16), gamma=1.08, contrast=1.06),
    "moon":   dict(sat=0.70, gain=(0.90, 1.00, 1.10), lift=(6, 10, 18), gamma=1.00, contrast=1.05),
    "cold":   dict(sat=0.60, gain=(0.88, 0.98, 1.10), lift=(5, 9, 14), gamma=1.05, contrast=1.08),
    "warm":   dict(sat=1.05, gain=(1.08, 0.98, 0.86), lift=(10, 6, 2), gamma=1.00, contrast=1.05),
    "candle": dict(sat=1.00, gain=(1.12, 0.95, 0.78), lift=(8, 4, 2), gamma=1.05, contrast=1.10),
    "sepia":  dict(sat=0.35, gain=(1.08, 0.98, 0.80), lift=(18, 12, 6), gamma=0.98, contrast=1.00),
    "blood":  dict(sat=0.90, gain=(1.15, 0.80, 0.78), lift=(12, 2, 4), gamma=1.05, contrast=1.12),
    "bw":     dict(sat=0.00, gain=(1, 1, 1), lift=(6, 6, 6), gamma=1.05, contrast=1.12),
}

def grade_ops(g):
    if isinstance(g, str): g = GRADES.get(g, GRADES["none"])
    g = {**GRADES["none"], **g}
    s = float(g["sat"]); lw = np.array([0.114, 0.587, 0.299])  # BGR luma weights
    M = np.eye(3) * s + (1 - s) * np.tile(lw, (3, 1))
    gainb = np.array(g["gain"][::-1], float); liftb = np.array(g["lift"][::-1], float)
    x = np.arange(256) / 255.0
    lut = np.zeros((1, 256, 3), np.uint8)
    for c in range(3):
        y = liftb[c] / 255 + (x ** g["gamma"]) * (gainb[c] - liftb[c] / 255)
        y = 0.5 + (y - 0.5) * g["contrast"]
        lut[0, :, c] = np.clip(y * 255, 0, 255).astype(np.uint8)
    return (None if abs(s - 1) < 1e-3 else M.astype(np.float32)), lut

def load_rgba(path, art_size):
    if path.startswith("#"):
        hx = path.lstrip("#"); rgb = [int(hx[i:i + 2], 16) for i in (0, 2, 4)]
        im = np.zeros((art_size[1], art_size[0], 4), np.uint8); im[:, :, 0] = rgb[2]; im[:, :, 1] = rgb[1]; im[:, :, 2] = rgb[0]; im[:, :, 3] = 255
        return im
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if im is None: raise FileNotFoundError(path)
    if im.ndim == 2: im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGRA)
    if im.shape[2] == 3: im = cv2.cvtColor(im, cv2.COLOR_BGR2BGRA)
    if (im.shape[1], im.shape[0]) != tuple(art_size):
        im = cv2.resize(im, tuple(art_size), interpolation=cv2.INTER_AREA)
    return im

def fog_texture(seed, shape=(576, 1024)):
    f = os.path.join(CACHE, f"fog_{seed}.npy")
    if os.path.exists(f): return np.load(f)
    r = np.random.default_rng(seed)
    n = r.standard_normal(shape)
    fy = np.fft.fftfreq(shape[0])[:, None]; fx = np.fft.fftfreq(shape[1])[None, :]
    k = np.sqrt(fx ** 2 + (fy * shape[0] / shape[1]) ** 2) + 1e-4
    spec = np.fft.fft2(n) / (k ** 1.6) * np.exp(-(k / 0.05) ** 2)
    x = np.real(np.fft.ifft2(spec)); x = (x - x.min()) / (x.max() - x.min())
    x = x.astype(np.float32); np.save(f, x); return x

VIGNETTE = None
def vignette(strength):
    global VIGNETTE
    key = round(strength, 3)
    if VIGNETTE is None or VIGNETTE[0] != key:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 * 0.85 + ((yy - H / 2) / (H / 2)) ** 2 * 0.75)
        v = 1 - strength * np.clip((d - 0.35) / 0.95, 0, 1) ** 1.6
        VIGNETTE = (key, cv2.cvtColor((v * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR))
    return VIGNETTE[1]

# ---------------------------------------------------------------- text cards
TEXT_STYLES = {
 "title":   lambda a, b: f'''<text x="960" y="560" text-anchor="middle" font-family="Cinzel" font-weight="700" font-size="112" letter-spacing="6" fill="#f3e6c8" filter="url(#glow)">{a}</text>
  <text x="960" y="650" text-anchor="middle" font-family="IM FELL English" font-style="italic" font-size="50" fill="#d8c39a">{b}</text>
  <rect x="660" y="430" width="600" height="2" fill="#c9a46a" opacity="0.8"/><rect x="660" y="690" width="600" height="2" fill="#c9a46a" opacity="0.8"/>''',
 "chapter": lambda a, b: f'''<text x="960" y="500" text-anchor="middle" font-family="Cinzel" font-size="36" letter-spacing="12" fill="#c9a46a">{a}</text>
  <text x="960" y="600" text-anchor="middle" font-family="IM FELL English" font-size="84" fill="#f1e8d6" filter="url(#glow)">{b}</text>
  <rect x="860" y="530" width="200" height="2" fill="#c9a46a"/>''',
 "big":     lambda a, b: f'''<text x="960" y="600" text-anchor="middle" font-family="Anton" font-size="170" letter-spacing="4" fill="#ffffff" stroke="#000" stroke-width="10" paint-order="stroke" filter="url(#shadow)">{a}</text>
  <text x="960" y="700" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="54" fill="#ffd34d" stroke="#000" stroke-width="6" paint-order="stroke">{b}</text>''',
 "date":    lambda a, b: f'''<text x="120" y="950" font-family="IM FELL English" font-style="italic" font-size="50" fill="#efe3c6" filter="url(#shadow)">{a}</text>
  <text x="120" y="1000" font-family="Cinzel" font-size="28" letter-spacing="6" fill="#c9a46a">{b}</text>''',
 "quote":   lambda a, b: f'''<text x="960" y="560" text-anchor="middle" font-family="IM FELL English" font-style="italic" font-size="70" fill="#f4ecdc" filter="url(#glow)">«{a}»</text>
  <text x="960" y="640" text-anchor="middle" font-family="Cinzel" font-size="30" letter-spacing="8" fill="#c9a46a">{b}</text>''',
 "whisper": lambda a, b: f'''<text x="960" y="900" text-anchor="middle" font-family="IM FELL English" font-style="italic" font-size="56" fill="#dfe8ee" opacity="0.85" filter="url(#glow)">{a}</text>''',
 "caption": lambda a, b: f'''<rect x="0" y="880" width="1920" height="150" fill="url(#band)"/>
  <text x="960" y="975" text-anchor="middle" font-family="Oswald" font-weight="700" font-size="60" fill="#ffffff" stroke="#000" stroke-width="5" paint-order="stroke">{a}</text>''',
}
SVG_DEFS = '''<defs><filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/>
<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="shadow" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity="0.85"/></filter>
<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.75"/></linearGradient></defs>'''

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text_cards(specs, outdir):
    os.makedirs(outdir, exist_ok=True); need = []; paths = {}
    for sp in specs:
        a, _, b = sp["str"].partition("|"); style = sp.get("style", "caption")
        body = TEXT_STYLES.get(style, TEXT_STYLES["caption"])(esc(a.strip()), esc(b.strip()))
        dy = {"top": -330, "center": 0, "bottom": 300}.get(sp.get("pos"), 0) if style not in ("date", "caption", "whisper") else 0
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">{SVG_DEFS}<g transform="translate(0,{dy})">{body}</g></svg>'
        h = hashlib.sha1(svg.encode()).hexdigest()[:14]
        p = os.path.join(outdir, f"txt_{h}.png"); paths[id(sp)] = p
        if not os.path.exists(p):
            open(p[:-4] + ".svg", "w", encoding="utf-8").write(svg); need.append(p[:-4] + ".svg")
    if need:
        subprocess.run(["node", os.path.join(PIPE, "render_svg.js"), *need], check=True, stdout=subprocess.DEVNULL)
    return paths

# ---------------------------------------------------------------- scene model
class Layer:
    def __init__(self, spec, art_size, base):
        self.spec = spec
        src = spec["src"]
        self.img = load_rgba(src if src.startswith("#") else os.path.join(base, src), art_size)
        self.depth = float(spec.get("depth", 1.0))
        self.anim = spec.get("anim", [])
        if isinstance(self.anim, dict): self.anim = [self.anim]
        op = spec.get("opacity", 1.0)
        self.op = (float(op), float(op)) if not isinstance(op, list) else (float(op[0]), float(op[1]))
        self.blend = spec.get("blend", "normal")
        self.fade_in = float(spec.get("fade_in", 0)); self.fade_out = float(spec.get("fade_out", 0))
        self.appear = float(spec.get("appear_at", 0)); self.vanish = spec.get("vanish_at")
        self._split()

    def _split(self):
        self.rgb = np.ascontiguousarray(self.img[:, :, :3]); self.alpha = np.ascontiguousarray(self.img[:, :, 3])
        self.opaque = bool((self.alpha == 255).all())

    def static(self):
        return not self.anim and self.op == (1.0, 1.0) and self.blend == "normal" and not self.fade_in and not self.appear and self.vanish is None and not self.fade_out

    def merge(self, other):
        a = other.img[:, :, 3:4].astype(np.float32) / 255
        rgb = self.img[:, :, :3] * (1 - a) + other.img[:, :, :3] * a
        al = self.img[:, :, 3:4] / 255 * (1 - a) + a
        self.img = np.concatenate([rgb, al * 255], 2).round().astype(np.uint8)
        self._split()

    def opacity(self, t, dur):
        u = t / dur if dur > 0 else 0
        o = self.op[0] + (self.op[1] - self.op[0]) * ease(u, "linear")
        if t < self.appear: return 0.0
        if self.fade_in: o *= min(1.0, (t - self.appear) / self.fade_in)
        if self.vanish is not None:
            if t >= float(self.vanish) + max(self.fade_out, 1e-6): return 0.0
            if self.fade_out and t > float(self.vanish): o *= 1 - (t - float(self.vanish)) / self.fade_out
        elif self.fade_out and t > dur - self.fade_out: o *= max(0.0, (dur - t) / self.fade_out)
        for a in self.anim:
            if a.get("type") == "flicker":
                o *= 1 - float(a.get("amp", 0.25)) * (0.5 + 0.5 * smooth_noise(t, 11, float(a.get("speed", 6))))
        return max(0.0, min(1.0, o))

    def local(self, t, dur, AW, AH):
        M = np.eye(3); u = t / dur if dur > 0 else 0
        for a in self.anim:
            ty = a.get("type"); px, py = a.get("pivot", [0.5, 0.5])
            if ty == "drift":
                e = ease(u, a.get("ease", "linear"))
                M = T(float(a.get("dx", 0)) * AW * e, float(a.get("dy", 0)) * AH * e) @ M
            elif ty == "float":
                M = T(0, float(a.get("amp", 0.008)) * AH * math.sin(6.283 * t / float(a.get("period", 5)))) @ M
            elif ty == "sway":
                M = R(float(a.get("deg", 1.5)) * math.sin(6.283 * t / float(a.get("period", 6))), px * AW, py * AH) @ M
            elif ty == "pulse":
                M = S(1 + float(a.get("amp", 0.02)) * math.sin(6.283 * t / float(a.get("period", 3))), px * AW, py * AH) @ M
            elif ty == "scale":
                e = ease(u, a.get("ease", "inout"))
                M = S(float(a.get("from", 1)) + (float(a.get("to", 1.2)) - float(a.get("from", 1))) * e, px * AW, py * AH) @ M
            elif ty == "shake":
                amp = float(a.get("amp", 0.003)) * AW
                M = T(amp * smooth_noise(t, 3, 4), amp * smooth_noise(t, 5, 4)) @ M
        return M


class Scene:
    def __init__(self, sid, spec, f0, f1, story, base, idx):
        self.id, self.spec, self.f0, self.f1, self.idx = sid, spec, f0, f1, idx
        self.n = f1 - f0; self.dur = self.n / FPS; self.base = base; self.story = story
        self.art_size = tuple(story.get("art_size", [2400, 1350]))
        self.loaded = False

    def key(self, prev_key=""):
        files = []
        for l in self.spec.get("layers", []):
            p = os.path.join(self.base, l["src"]) if not l["src"].startswith("#") else None
            files.append((l["src"], os.path.getmtime(p) if p and os.path.exists(p) else 0, os.path.getsize(p) if p and os.path.exists(p) else 0))
        glob = {k: self.story.get(k) for k in ("grade", "vignette", "grain", "art_size")}
        tr = self.spec.get("transition", "cut")
        blob = json.dumps([VERSION, self.spec, files, self.n, glob, prev_key if tr == "xfade" else ""], sort_keys=True, default=str)
        return hashlib.sha1(blob.encode()).hexdigest()[:12]

    def load(self):
        if self.loaded: return
        AW, AH = self.art_size
        layers = []
        for ls in self.spec.get("layers", []):
            L = Layer(ls, self.art_size, self.base)
            if layers and L.static() and layers[-1].static() and abs(L.depth - layers[-1].depth) < 1e-6:
                layers[-1].merge(L)
            else:
                layers.append(L)
        if not layers: layers = [Layer({"src": "#000000"}, self.art_size, self.base)]
        self.layers = layers
        cam = self.spec.get("cam")
        if cam is None:
            r = np.random.default_rng(self.idx * 7 + 1); k = self.idx % 4
            if k == 0: cam = {"from": [0.5, 0.5, 1.0], "to": [0.5, 0.48, 1.10]}
            elif k == 1: cam = {"from": [0.45, 0.5, 1.12], "to": [0.55, 0.5, 1.12]}
            elif k == 2: cam = {"from": [0.5, 0.5, 1.14], "to": [0.5, 0.5, 1.02]}
            else: cam = {"from": [0.55, 0.52, 1.12], "to": [0.45, 0.5, 1.12]}
        self.cam = cam
        self.fx = [({"type": f} if isinstance(f, str) else f) for f in self.spec.get("fx", [])]
        g = self.spec.get("grade", self.story.get("grade", "none"))
        self.cmat, self.lut = grade_ops(g)
        self.texts = self.spec.get("text", [])
        if isinstance(self.texts, dict): self.texts = [self.texts]
        if self.texts:
            paths = text_cards(self.texts, os.path.join(self.base, "out", "text"))
            self.text_imgs = []
            for sp in self.texts:
                im = cv2.imread(paths[id(sp)], cv2.IMREAD_UNCHANGED)
                ys, xs = np.where(im[:, :, 3] > 0)
                if len(ys) == 0: continue
                y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
                at = sp.get("at", [0, self.dur])
                self.text_imgs.append((im[y0:y1, x0:x1].copy(), y0, x0, float(at[0]), float(at[1])))
        else:
            self.text_imgs = []
        self.parts = {}
        self.loaded = True

    def unload(self):
        self.layers = None; self.text_imgs = None; self.loaded = False

    # camera matrix art->out for a layer of given depth
    def camera(self, t, depth, shake=(0, 0)):
        AW, AH = self.art_size
        u = t / self.dur if self.dur > 0 else 0
        e = ease(u, self.cam.get("ease", "inout"))
        a, b = self.cam.get("from", [0.5, 0.5, 1.0]), self.cam.get("to", [0.5, 0.5, 1.0])
        cx = a[0] + (b[0] - a[0]) * e; cy = a[1] + (b[1] - a[1]) * e; z = a[2] + (b[2] - a[2]) * e
        cx = 0.5 + (cx - 0.5) * depth; cy = 0.5 + (cy - 0.5) * depth
        z = max(1.0, z ** depth if depth > 0 else 1.0)
        vw = AW / z; vh = vw * H / W
        if vh > AH: vh = AH; vw = vh * W / H
        x0 = min(max(cx * AW - vw / 2, 0), AW - vw); y0 = min(max(cy * AH - vh / 2, 0), AH - vh)
        s = W / vw
        return np.array([[s, 0, -x0 * s + shake[0]], [0, s, -y0 * s + shake[1]], [0, 0, 1.0]])

    def frame(self, i):
        """Render local frame i (0..n-1, may exceed n for xfade continuation)."""
        t = i / FPS; dur = self.dur
        AW, AH = self.art_size
        shake = (0.0, 0.0); bright, bias = 1.0, 0.0
        for f in self.fx:
            ty = f["type"]; at = f.get("at")
            env = 1.0
            if ty == "shake":
                if at: env = 1.0 if at[0] <= t <= at[1] else 0.0
                amp = float(f.get("amp", 6))
                shake = (shake[0] + env * amp * smooth_noise(t, 21, 5), shake[1] + env * amp * smooth_noise(t, 23, 5))
        out = None
        for L in self.layers:
            o = L.opacity(t, dur)
            if o <= 0.003 and out is not None: continue
            M = (self.camera(t, L.depth, shake) @ L.local(t, dur, AW, AH))[:2].astype(np.float32)
            if out is None:
                out = cv2.warpAffine(L.rgb, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
                if not L.opaque or o < 1:
                    a = cv2.warpAffine(L.alpha, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
                    if o < 1: a = cv2.convertScaleAbs(a, alpha=o)
                    out = cv2.multiply(out, cv2.cvtColor(a, cv2.COLOR_GRAY2BGR), scale=1 / 255)
                continue
            c = cv2.warpAffine(L.rgb, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            a = cv2.warpAffine(L.alpha, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            if o < 1: a = cv2.convertScaleAbs(a, alpha=o)
            a3 = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
            if L.blend == "screen":
                ce = cv2.multiply(c, a3, scale=1 / 255)
                out = cv2.bitwise_not(cv2.multiply(cv2.bitwise_not(out), cv2.bitwise_not(ce), scale=1 / 255))
            elif L.blend == "add":
                out = cv2.add(out, cv2.multiply(c, a3, scale=1 / 255))
            elif L.blend == "multiply":
                cm = cv2.add(cv2.multiply(c, a3, scale=1 / 255), cv2.bitwise_not(a3))
                out = cv2.multiply(out, cm, scale=1 / 255)
            else:
                out = cv2.add(cv2.multiply(out, cv2.bitwise_not(a3), scale=1 / 255), cv2.multiply(c, a3, scale=1 / 255))
        # ---- fx overlays
        for f in self.fx:
            ty = f["type"]; at = f.get("at")
            if ty == "fog": out = fx_fog(out, t, f)
            elif ty in ("dust", "embers", "fireflies", "ash"): out = fx_particles(out, t, f, self.idx)
            elif ty == "rain": out = fx_rain(out, t, f, self.idx)
            elif ty == "flicker":
                bright *= 1 + float(f.get("amp", 0.06)) * smooth_noise(t, 31, float(f.get("speed", 3)))
            elif ty == "lightning":
                for t0 in (at or [dur * 0.4]):
                    for off, pw in ((0, 1.0), (0.13, 0.6)):
                        d = t - t0 - off
                        if 0 <= d < 0.35:
                            k = pw * math.exp(-d / 0.07)
                            bright *= 1 + 1.2 * k; bias += 45 * k
            elif ty == "pulse":
                bpm = float(f.get("bpm", 60)); ph = (t * bpm / 60) % 1.0
                beat = math.exp(-ph / 0.08) + 0.6 * math.exp(-max(0, ph - 0.22) / 0.08) * (ph > 0.22)
                bright *= 1 - float(f.get("amp", 0.12)) * (1 - min(1, beat))
            elif ty == "darken":
                bright *= float(f.get("amount", 0.6))
        # ---- grade + vignette
        if self.cmat is not None: out = cv2.transform(out, self.cmat)
        out = cv2.LUT(out, self.lut)
        vs = float(self.spec.get("vignette", self.story.get("vignette", 0.55)))
        if vs > 0: out = cv2.multiply(out, vignette(vs), scale=1 / 255)
        # ---- text
        for (im, y0, x0, a0, a1) in self.text_imgs:
            if not (a0 <= t <= a1): continue
            fa = min(1.0, (t - a0) / 0.45, (a1 - t) / 0.45)
            if fa <= 0: continue
            h, w = im.shape[:2]
            reg = out[y0:y0 + h, x0:x0 + w]
            a = im[:, :, 3]
            if fa < 1: a = cv2.convertScaleAbs(a, alpha=fa)
            a3 = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
            out[y0:y0 + h, x0:x0 + w] = cv2.add(cv2.multiply(reg, cv2.bitwise_not(a3), scale=1 / 255), cv2.multiply(im[:, :, :3], a3, scale=1 / 255))
        # ---- transitions in / out
        tr = self.spec.get("transition", "cut")
        if tr == "fade":
            bright *= min(1.0, t / float(self.spec.get("transition_len", 0.7)))
        elif tr == "flash":
            d = float(self.spec.get("transition_len", 0.35))
            if t < d: k = 1 - t / d; bright *= 1 + 1.5 * k; bias += 160 * k
        if self.spec.get("out") == "fade":
            d = float(self.spec.get("out_len", 0.8))
            if t > dur - d: bright *= max(0.0, (dur - t) / d)
        if bright != 1.0 or bias != 0.0:
            out = cv2.convertScaleAbs(out, alpha=bright, beta=bias)
        return out


# ---------------------------------------------------------------- fx implementations
_FOG = {}
def fx_fog(out, t, f):
    seed = int(f.get("seed", 1))
    if seed not in _FOG:
        _FOG[seed] = (fog_texture(seed), fog_texture(seed + 100))
        yy = np.linspace(0, 1, 270, dtype=np.float32)[:, None]
        _FOG[(seed, "low")] = np.clip((yy - 0.25) / 0.6, 0.15, 1.0) ** 1.2
    A, B = _FOG[seed]
    sp = float(f.get("speed", 1.0))
    h, w = 270, 480
    ma = np.float32([[0.5, 0, -t * 9 * sp], [0, 0.5, -t * 1.5 * sp]])
    mb = np.float32([[0.35, 0, t * 6 * sp], [0, 0.35, t * 0.8 * sp]])
    a = cv2.warpAffine(A, ma, (w, h), borderMode=cv2.BORDER_WRAP)
    b = cv2.warpAffine(B, mb, (w, h), borderMode=cv2.BORDER_WRAP)
    m = np.clip((a * 0.6 + b * 0.6 - 0.45) * 1.9, 0, 1)
    if f.get("low", True): m = m * _FOG[(seed, "low")]
    m8 = np.clip(m * (255 * float(f.get("strength", 0.35))), 0, 255).astype(np.uint8)
    m8 = cv2.cvtColor(cv2.resize(m8, (W, H), interpolation=cv2.INTER_LINEAR), cv2.COLOR_GRAY2BGR)
    col = f.get("color", [190, 205, 220])
    fogc = cv2.multiply(m8, (col[2], col[1], col[0], 0), scale=1 / 255)
    return cv2.bitwise_not(cv2.multiply(cv2.bitwise_not(out), cv2.bitwise_not(fogc), scale=1 / 255))

_PART = {}
def fx_particles(out, t, f, idx):
    ty = f["type"]
    key = (ty, idx, f.get("count"))
    if key not in _PART:
        r = np.random.default_rng(zlib.crc32(repr(key).encode()))
        n = int(f.get("count", {"dust": 70, "embers": 80, "fireflies": 40, "ash": 90}[ty]))
        _PART[key] = dict(x=r.random(n), y=r.random(n), s=r.uniform(0.6, 2.2, n), v=r.uniform(0.4, 1.0, n), ph=r.uniform(0, 6.28, n))
    P = _PART[key]
    hw, hh = W // 2, H // 2
    if ty == "dust":
        x = (P["x"] + t * 0.006 * P["v"] + 0.01 * np.sin(t * 0.5 + P["ph"])) % 1; y = (P["y"] + t * 0.004 * P["v"]) % 1
        b = 0.55 + 0.45 * np.sin(t * 1.3 + P["ph"]); col = f.get("color", [255, 220, 170]); sz = P["s"]
    elif ty == "embers":
        x = (P["x"] + 0.02 * np.sin(t * 0.9 + P["ph"]) + t * 0.004) % 1; y = (P["y"] - t * 0.07 * P["v"]) % 1
        b = 0.5 + 0.5 * np.sin(t * 7 * P["v"] + P["ph"]); col = f.get("color", [255, 140, 50]); sz = P["s"] * 1.1
    elif ty == "ash":
        x = (P["x"] + 0.03 * np.sin(t * 0.4 + P["ph"]) + t * 0.01) % 1; y = (P["y"] + t * 0.025 * P["v"]) % 1
        b = 0.7 + 0 * P["v"]; col = f.get("color", [200, 200, 200]); sz = P["s"]
    else:  # fireflies
        x = (P["x"] + 0.03 * np.sin(t * 0.3 + P["ph"])) % 1; y = (P["y"] + 0.02 * np.cos(t * 0.25 + P["ph"] * 2)) % 1
        b = np.clip(np.sin(t * 1.1 * P["v"] + P["ph"]) * 1.6 - 0.4, 0, 1); col = f.get("color", [210, 255, 140]); sz = P["s"] * 1.3
    ov = np.zeros((hh, hw), np.uint8)
    for xi, yi, bi, si in zip(x, y, b, sz):
        if bi > 0.02: cv2.circle(ov, (int(xi * hw), int(yi * hh)), max(1, int(si)), int(255 * bi), -1, cv2.LINE_AA)
    glow = cv2.GaussianBlur(ov, (0, 0), 2.5)
    ov = cv2.max(ov, cv2.convertScaleAbs(glow, alpha=1.6))
    ov = cv2.resize(ov, (W, H), interpolation=cv2.INTER_LINEAR)
    k = float(f.get("strength", 0.8))
    oc = cv2.merge([cv2.convertScaleAbs(ov, alpha=k * v / 255) for v in col[::-1]])
    return cv2.add(out, oc)

def fx_rain(out, t, f, idx):
    key = ("rain", idx)
    if key not in _PART:
        r = np.random.default_rng(idx + 99); n = int(f.get("count", 260))
        _PART[key] = dict(x=r.random(n), y=r.random(n), v=r.uniform(0.8, 1.3, n), l=r.uniform(0.03, 0.07, n))
    P = _PART[key]
    ov = np.zeros((H, W), np.uint8); slant = float(f.get("slant", 0.15))
    y = (P["y"] + t * 1.6 * P["v"]) % 1.2 - 0.1; x = (P["x"] + y * slant) % 1
    for xi, yi, li in zip(x, y, P["l"]):
        cv2.line(ov, (int(xi * W), int(yi * H)), (int((xi + li * slant) * W), int((yi + li) * H)), 255, 1, cv2.LINE_AA)
    k = float(f.get("strength", 0.35)); col = f.get("color", [190, 200, 215])
    oc = cv2.merge([cv2.convertScaleAbs(ov, alpha=k * v / 255) for v in col[::-1]])
    return cv2.add(out, oc)

# ---------------------------------------------------------------- timeline -> scenes
def build_scenes(proj):
    story = json.load(open(os.path.join(proj, "story.json"), encoding="utf-8"))
    tl = json.load(open(os.path.join(proj, "audio", "timeline.json")))
    beats = story["beats"]; tb = tl["beats"]
    assert len(beats) == len(tb), "story.json changed since tts.py ran: re-run tts.py"
    total = tl["duration"] + float(story.get("outro", 0))
    scenes, idx = [], 0
    for bi, (b, tbe) in enumerate(zip(beats, tb)):
        start = tbe["start"]; end = tbe["end"] if bi < len(beats) - 1 else total
        specs = b.get("scenes") or [b["scene"]] if (b.get("scenes") or b.get("scene")) else []
        if not specs:
            raise ValueError(f"beat {tbe['id']} has no scenes")
        fixed = sum(float(s["dur"]) for s in specs if "dur" in s)
        wsum = sum(float(s.get("weight", 1)) for s in specs if "dur" not in s)
        free = max(0.0, (end - start) - fixed)
        t = start
        for s in specs:
            d = float(s["dur"]) if "dur" in s else free * float(s.get("weight", 1)) / (wsum or 1)
            f0 = round(t * FPS); t += d; f1 = round(t * FPS)
            if s is specs[-1]: f1 = round(end * FPS)
            if f1 > f0:
                idx += 1
                scenes.append(Scene(s.get("id", f"s{idx:03d}"), s, f0, f1, story, proj, idx))
    return story, tl, scenes, total

# ---------------------------------------------------------------- encode
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-g", "60", "-pix_fmt", "yuv420p", "-r", str(FPS)]

def render_scene(sc, prev, path, grain):
    sc.load()
    if prev is not None and sc.spec.get("transition") == "xfade": prev.load()
    tmp = path[:-4] + ".part.mp4"
    vf = (f"noise=alls={grain}:allf=t," if grain else "") + "format=yuv420p"
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-vf", vf, *ENC, tmp], stdin=subprocess.PIPE)
    xf = int(float(sc.spec.get("transition_len", 0.8)) * FPS) if (prev is not None and sc.spec.get("transition") == "xfade") else 0
    for i in range(sc.n):
        fr = sc.frame(i)
        if i < xf:
            pf = prev.frame(prev.n + i)
            fr = cv2.addWeighted(pf, 1 - (i + 1) / (xf + 1), fr, (i + 1) / (xf + 1), 0)
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    if p.wait() != 0: raise RuntimeError("ffmpeg failed on " + sc.id)
    os.replace(tmp, path)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("proj")
    ap.add_argument("--stills"); ap.add_argument("--contact", action="store_true")
    ap.add_argument("--only"); ap.add_argument("--scenes-only", action="store_true")
    a = ap.parse_args(); proj = os.path.abspath(a.proj)
    story, tl, scenes, total = build_scenes(proj)
    grain = int(story.get("grain", 0))
    chk = os.path.join(proj, "check"); os.makedirs(chk, exist_ok=True)
    print(f"{len(scenes)} scenes, {total/60:.2f} min")
    if a.stills:
        for ts in [float(x) for x in a.stills.split(",")]:
            fi = int(ts * FPS)
            for k, sc in enumerate(scenes):
                if sc.f0 <= fi < sc.f1:
                    sc.load(); fr = sc.frame(fi - sc.f0)
                    xf = int(float(sc.spec.get("transition_len", 0.8)) * FPS)
                    if sc.spec.get("transition") == "xfade" and k and fi - sc.f0 < xf:
                        pv = scenes[k - 1]; pv.load(); i = fi - sc.f0
                        fr = cv2.addWeighted(pv.frame(pv.n + i), 1 - (i + 1) / (xf + 1), fr, (i + 1) / (xf + 1), 0)
                    out = os.path.join(chk, f"still_{ts:08.2f}_{sc.id}.jpg"); cv2.imwrite(out, fr, [cv2.IMWRITE_JPEG_QUALITY, 90]); print(out)
                    break
        return
    if a.contact:
        tiles = []
        for sc in scenes:
            sc.load(); fr = sc.frame(sc.n // 2); sc.unload()
            th = cv2.resize(fr, (480, 270), interpolation=cv2.INTER_AREA)
            cv2.rectangle(th, (0, 0), (150, 30), (0, 0, 0), -1)
            cv2.putText(th, f"{sc.id} {sc.f0/FPS:.0f}s", (5, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            tiles.append(th)
        per = 24
        for pg in range(0, len(tiles), per):
            grp = tiles[pg:pg + per]
            while len(grp) % 4: grp.append(np.zeros_like(tiles[0]))
            rows = [np.hstack(grp[i:i + 4]) for i in range(0, len(grp), 4)]
            f = os.path.join(chk, f"contact_{pg // per + 1:02d}.jpg"); cv2.imwrite(f, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85]); print(f)
        return
    sdir = os.path.join(proj, "out", "scenes"); os.makedirs(sdir, exist_ok=True)
    only = set(a.only.split(",")) if a.only else set()
    lock = open(os.path.join(PIPE, "cpu.lock"), "w")
    print("waiting for CPU lock…", flush=True); fcntl.flock(lock, fcntl.LOCK_EX)
    t0 = time.time(); files = []; prev_key = ""
    for k, sc in enumerate(scenes):
        key = sc.key(prev_key); prev_key = key
        path = os.path.join(sdir, f"{sc.id}_{key}.mp4"); files.append(path)
        if os.path.exists(path) and sc.id not in only: continue
        for old in os.listdir(sdir):
            if old.startswith(sc.id + "_") and old != os.path.basename(path): os.remove(os.path.join(sdir, old))
        ts = time.time()
        render_scene(sc, scenes[k - 1] if k else None, path, grain)
        if k: scenes[k - 1].unload()
        print(f"  {sc.id} {sc.dur:5.1f}s rendered in {time.time()-ts:5.1f}s", flush=True)
    sc_ids = {os.path.basename(f) for f in files}
    for old in os.listdir(sdir):
        if old.endswith(".mp4") and old not in sc_ids: os.remove(os.path.join(sdir, old))
    print(f"scenes done in {time.time()-t0:.0f}s")
    if a.scenes_only: fcntl.flock(lock, fcntl.LOCK_UN); return
    lst = os.path.join(proj, "out", "concat.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    vid = os.path.join(proj, "out", "video_only.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid], check=True)
    mix = os.path.join(proj, "audio", "mix.wav")
    if not os.path.exists(mix): mix = os.path.join(proj, "audio", "narration.wav"); print("WARNING: no mix.wav, using narration only")
    final = os.path.join(proj, "out", "final.mp4"); tmp = final[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", vid, "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", tmp], check=True)
    os.replace(tmp, final)
    fcntl.flock(lock, fcntl.LOCK_UN)
    print("FINAL", final)

if __name__ == "__main__":
    main()
