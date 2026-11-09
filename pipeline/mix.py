#!/usr/bin/env python3
"""Soundtrack mixer: narration + music moods + ambience beds + SFX, ducked and loudness-normalised (-14 LUFS).

Usage:  python3 /home/claude/pipeline/mix.py PROJECT_DIR
Reads PROJECT_DIR/story.json cues (music / amb / sfx per beat) and PROJECT_DIR/audio/{narration.wav,timeline.json}
Writes PROJECT_DIR/audio/mix.wav (48 kHz stereo). Generated beds are cached in PROJECT_DIR/audio/cache_music.
"""
import json, os, sys, hashlib, fcntl
import numpy as np, soundfile as sf, pyloudnorm as pyln
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sound as S

SR = S.SR
PIPE = os.path.dirname(os.path.abspath(__file__))
db = lambda d: 10 ** (d / 20)


def cached(cdir, tag, fn):
    f = os.path.join(cdir, hashlib.sha1(tag.encode()).hexdigest()[:16] + ".npy")
    if os.path.exists(f): return np.load(f)
    x = fn(); np.save(f, x.astype(np.float32)); return x


def add(track, sig, t, gain=1.0):
    s = int(round(t * SR))
    if s < 0: sig = sig[-s:]; s = 0
    e = min(len(track), s + len(sig))
    if e > s: track[s:e] += sig[: e - s] * gain


def main(proj):
    story = json.load(open(os.path.join(proj, "story.json"), encoding="utf-8"))
    tl = json.load(open(os.path.join(proj, "audio", "timeline.json")))
    cdir = os.path.join(proj, "audio", "cache_music"); os.makedirs(cdir, exist_ok=True)
    voice, sr = sf.read(os.path.join(proj, "audio", "narration.wav"), dtype="float32")
    assert sr == SR
    total = tl["duration"] + float(story.get("outro", 0))
    n = int(total * SR) + SR
    key = story.get("key", "A"); seed = int(story.get("seed", 1))
    lock = open(os.path.join(PIPE, "cpu.lock"), "w"); print("waiting for CPU lock…", flush=True); fcntl.flock(lock, fcntl.LOCK_EX)
    # ---- change points
    music_pts, amb_pts = [], []
    for b, tb in zip(story["beats"], tl["beats"]):
        if "music" in b: music_pts.append((tb["start"] + float(b.get("music_at", 0)), b["music"]))
        if "amb" in b: amb_pts.append((tb["start"], list(b["amb"])))
    if not music_pts or music_pts[0][0] > 0.01: music_pts.insert(0, (0.0, music_pts[0][1] if music_pts else "mystery"))
    music = np.zeros((n, 2), np.float32); amb = np.zeros((n, 2), np.float32); sfx = np.zeros((n, 2), np.float32)
    XF = 2.5
    for i, (t0, m) in enumerate(music_pts):
        t1 = music_pts[i + 1][0] if i + 1 < len(music_pts) else total
        d = t1 - t0 + XF
        x = cached(cdir, f"m|{m}|{d:.2f}|{key}|{seed+i}", lambda: S.mood(m, d, key, seed + i))
        x = S.fade(x, XF if i else 0.5, XF + 0.5 if i + 1 < len(music_pts) else 4.0)
        add(music, x, t0 - (XF / 2 if i else 0), db(float(story.get("mood_gain", {}).get(m, 0))))
    for i, (t0, names) in enumerate(amb_pts):
        t1 = amb_pts[i + 1][0] if i + 1 < len(amb_pts) else total
        d = t1 - t0 + XF
        for nm in names:
            g = 0.0
            if isinstance(nm, dict): g = float(nm.get("gain", 0)); nm = nm["name"]
            x = cached(cdir, f"a|{nm}|{d:.2f}|{seed+i}", lambda: S.AMB[nm](d, seed + i))
            add(amb, S.fade(x, XF, XF + 1), t0 - XF / 2, db(g))
    for b, tb in zip(story["beats"], tl["beats"]):
        for c in b.get("sfx", []):
            nm = c["name"]; args = c.get("args", {})
            x = cached(cdir, f"s|{nm}|{json.dumps(args, sort_keys=True)}", lambda: S.SFX[nm](**args))
            if "pan" in c:
                p = float(c["pan"]); x = x * np.array([min(1, 1 - p), min(1, 1 + p)], np.float32)
            add(sfx, x, tb["start"] + float(c.get("at", 0)), db(float(c.get("gain", 0))))
    # ---- ducking envelope from narration
    v = np.zeros(n, np.float32); v[: len(voice)] = voice[:n]
    win = int(0.05 * SR); e = np.sqrt(np.convolve(v ** 2, np.ones(win) / win, "same"))
    act = (e > 0.02).astype(np.float32)
    k = int(0.35 * SR); act = np.convolve(act, np.ones(k) / k, "same")  # smooth attack/release
    act = np.clip(act * 1.5, 0, 1)
    duck_m = db(-8 * 1.0) ** act; duck_a = db(-5) ** act
    gm, ga, gs = db(float(story.get("music_gain", -15))), db(float(story.get("amb_gain", -21))), db(float(story.get("sfx_gain", -9)))
    mix = music * (gm * duck_m)[:, None] + amb * (ga * duck_a)[:, None] + sfx * gs + v[:, None]
    mix = mix[: int(total * SR)]
    fcntl.flock(lock, fcntl.LOCK_UN)
    # ---- loudness + limiter
    meter = pyln.Meter(SR); L = meter.integrated_loudness(mix)
    mix = mix * db(-14 - L)
    pk = np.abs(mix).max()
    if pk > 0.89:
        over = np.abs(mix) > 0.7
        mix[over] = np.sign(mix[over]) * (0.7 + 0.19 * np.tanh((np.abs(mix[over]) - 0.7) / 0.19))
    L2 = meter.integrated_loudness(mix)
    sf.write(os.path.join(proj, "audio", "mix.wav"), mix.astype(np.float32), SR, subtype="PCM_16")
    print(f"mix.wav {total/60:.2f} min, loudness {L2:.1f} LUFS, peak {np.abs(mix).max():.2f}")


if __name__ == "__main__":
    main(sys.argv[1])
