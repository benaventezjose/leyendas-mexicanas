"""Procedural sound library (48 kHz): music moods, ambiences and SFX. Everything is synthesised locally.
Import:  sys.path.insert(0, '/home/claude/pipeline'); import sound
Every generator returns a float32 stereo array of shape (n, 2), peak-normalised to ~0.9 unless stated.
"""
import numpy as np, zlib
from scipy.signal import butter, sosfilt, lfilter, oaconvolve

SR = 48000
NOTE = {n: i for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}

def hz(note):
    """'A3' -> 220.0 ; supports sharps like 'G#2'."""
    name, octv = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((NOTE[name] - 9) / 12 + (octv - 4))

def rng(seed): return np.random.default_rng(seed)
def secs(d): return int(d * SR)
def stereo(x, pan=0.0):
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    return np.stack([x * l * 1.414, x * r * 1.414], 1).astype(np.float32)
def norm(x, peak=0.9):
    m = np.abs(x).max()
    return (x / m * peak).astype(np.float32) if m > 0 else x.astype(np.float32)
def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "bandpass", fs=SR, output="sos"), x, axis=0)
def lp(x, f, order=2): return sosfilt(butter(order, f, "lowpass", fs=SR, output="sos"), x, axis=0)
def hp(x, f, order=2): return sosfilt(butter(order, f, "highpass", fs=SR, output="sos"), x, axis=0)
def env_ad(n, a, d):
    e = np.ones(n, np.float32); na = min(n, secs(a))
    if na: e[:na] = np.linspace(0, 1, na)
    t = np.arange(n - na) / SR; e[na:] = np.exp(-t / max(d, 1e-3)); return e
def fade(x, fi=0.05, fo=0.05):
    x = x.copy(); a, b = min(len(x), secs(fi)), min(len(x), secs(fo))
    if a: x[:a] *= np.linspace(0, 1, a)[:, None] if x.ndim == 2 else np.linspace(0, 1, a)
    if b: x[-b:] *= np.linspace(1, 0, b)[:, None] if x.ndim == 2 else np.linspace(1, 0, b)
    return x
def pink(n, seed=0):
    w = rng(seed).standard_normal(n)
    b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]; a = [1, -2.494956002, 2.017265875, -0.522189400]
    return lfilter(b, a, w).astype(np.float32) * 8
def brown(n, seed=0):
    x = np.cumsum(rng(seed).standard_normal(n)); x = hp(x, 15); return norm(x, 0.9)

_IR = {}
def reverb(x, size=2.8, wet=0.35, seed=3, predelay=0.02):
    """Stereo convolution reverb (x mono or stereo)."""
    if x.ndim == 1: x = stereo(x)
    key = (round(size, 2), seed)
    if key not in _IR:
        n = secs(size); t = np.arange(n) / SR; r = rng(seed)
        irs = []
        for ch in range(2):
            ir = r.standard_normal(n) * np.exp(-t / (size / 6.9))
            ir = lp(ir, 6500); ir[: secs(predelay)] = 0; irs.append(ir / np.sqrt((ir ** 2).sum()))
        _IR[key] = irs
    y = np.zeros((len(x) + secs(size), 2), np.float32)
    for ch in range(2):
        c = oaconvolve(x[:, ch], _IR[key][ch]); m = min(len(c), len(y)); y[:m, ch] = c[:m]
    y *= wet * 2.2
    y[: len(x)] += x * (1 - wet)
    return y.astype(np.float32)

# ------------------------------------------------------------------ instruments
def pluck(freq, dur=2.5, bright=0.6, seed=0):
    """Karplus-Strong nylon-guitar-like pluck (mono)."""
    n = secs(dur); N = max(2, int(SR / freq))
    exc = np.zeros(n); burst = rng(seed).uniform(-1, 1, N)
    burst = lp(burst, 1500 + 5000 * bright) if N > 12 else burst
    exc[:N] = burst
    g = 0.996 - 0.004 * (freq / 1000)
    a = np.zeros(N + 2); a[0] = 1; a[N] = -g * 0.5; a[N + 1] = -g * 0.5
    y = lfilter([1.0], a, exc)
    y = lp(y, 3500 + 3000 * bright) * env_ad(n, 0.002, dur * 0.45)
    return norm(y, 0.8)

def piano(freq, dur=3.0, seed=0):
    n = secs(dur); t = np.arange(n) / SR; y = np.zeros(n)
    for k, amp in enumerate([1, 0.55, 0.3, 0.18, 0.1, 0.06], 1):
        f = freq * k * (1 + 0.0004 * k * k)
        y += amp * np.sin(2 * np.pi * f * t) * np.exp(-t * (0.9 + 0.6 * k))
    y *= env_ad(n, 0.004, dur)
    return norm(y, 0.8)

def bell(freq=220, dur=6.0):
    n = secs(dur); t = np.arange(n) / SR; y = np.zeros(n)
    for p, amp, dec in [(0.5, 0.6, 2.5), (1, 1, 1.8), (1.19, 0.5, 1.4), (1.56, 0.4, 1.1), (2.0, 0.35, 0.9), (2.51, 0.25, 0.6), (3.01, 0.2, 0.45), (4.1, 0.12, 0.3)]:
        y += amp * np.sin(2 * np.pi * freq * p * t + p) * np.exp(-t / (dec * dur / 5))
    y[: secs(0.003)] *= np.linspace(0, 1, secs(0.003))
    return norm(y, 0.8)

def pad(freqs, dur, seed=0, cutoff=900, detune=0.12):
    """Warm string-like pad: detuned saws -> lowpass, slow attack/release."""
    n = secs(dur); t = np.arange(n) / SR; r = rng(seed)
    L = np.zeros(n); Rr = np.zeros(n)
    for f in freqs:
        for d in (-detune, 0, detune):
            ff = f * 2 ** (d / 12); ph = r.uniform(0, 1)
            saw = 2 * ((ff * t + ph) % 1) - 1
            lfo = 0.75 + 0.25 * np.sin(2 * np.pi * r.uniform(0.05, 0.15) * t + r.uniform(0, 6))
            if d < 0: L += saw * lfo
            elif d > 0: Rr += saw * lfo
            else: L += saw * lfo * 0.5; Rr += saw * lfo * 0.5
    x = np.stack([L, Rr], 1); x = lp(x, cutoff, 2)
    x = fade(x, min(3, dur / 3), min(3, dur / 3))
    return norm(x, 0.8)

def drone(root_hz, dur, seed=0, dark=True):
    n = secs(dur); t = np.arange(n) / SR; r = rng(seed)
    y = np.zeros(n)
    for mult, amp in [(0.5, 0.9), (1, 1), (1.5, 0.35), (2, 0.3), (3, 0.08)]:
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * r.uniform(0.02, 0.08) * t + r.uniform(0, 6))
        y += amp * np.sin(2 * np.pi * root_hz * mult * t + 0.3 * np.sin(2 * np.pi * 0.07 * t)) * lfo
    noise = lp(pink(n, seed), 300 if dark else 900) * 0.15
    x = stereo(y + noise)
    x[:, 1] = np.roll(x[:, 1], secs(0.013))
    return fade(norm(x, 0.8), 2, 2)

# ------------------------------------------------------------------ SFX
def sfx_thunder(dur=6.0, seed=1):
    n = secs(dur); b = brown(n, seed); t = np.arange(n) / SR
    crack = hp(rng(seed).standard_normal(n), 800) * np.exp(-t / 0.12) * 0.7
    rumble = lp(b, 180) * (env_ad(n, 0.25, dur / 3) * (1 + 0.6 * np.sin(2 * np.pi * 1.7 * t)))
    return reverb(norm(crack + rumble * 1.4), 3.0, 0.3)
def sfx_boom(dur=4.0):
    n = secs(dur); t = np.arange(n) / SR
    f = 75 * np.exp(-t / 0.5) + 32; ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t / 1.0) + lp(rng(2).standard_normal(n), 400) * np.exp(-t / 0.15) * 0.6
    return reverb(norm(y), 3.2, 0.35)
def sfx_riser(dur=4.0, seed=4):
    n = secs(dur); t = np.arange(n) / SR; u = t / dur
    noise = rng(seed).standard_normal(n); out = np.zeros(n); seg = secs(0.05)
    for i in range(0, n, seg):
        f = 300 + 5000 * u[i] ** 2
        out[i:i + seg] = bp(noise[i:i + seg], f * 0.8, min(f * 1.25, 20000), 1)
    tone = np.sin(2 * np.pi * np.cumsum(110 + 330 * u ** 2) / SR) * 0.4
    y = (out * 0.8 + tone) * u ** 2
    y[-secs(0.05):] *= np.linspace(1, 0, secs(0.05))
    return reverb(norm(y), 2.0, 0.3)
def sfx_whoosh(dur=1.2, seed=5):
    n = secs(dur); t = np.arange(n) / SR; u = t / dur
    e = np.sin(np.pi * u) ** 2
    y = bp(rng(seed).standard_normal(n), 250, 2600, 2) * e
    x = stereo(y); x[:, 0] *= 1 - u; x[:, 1] *= u
    return norm(x)
def sfx_sting(dur=3.0, seed=6, root="A2"):
    f0 = hz(root); fr = [f0 * 2, f0 * 2 * 2 ** (1 / 12), f0 * 3 * 2 ** (6 / 12) / 2, f0 * 4 * 2 ** (11 / 12) / 2]
    n = secs(dur); t = np.arange(n) / SR; y = np.zeros(n)
    for f in fr:
        y += (2 * ((f * t) % 1) - 1) * (1 + 0.3 * np.sin(2 * np.pi * 7 * t))
    y = lp(y, 2500) * env_ad(n, 0.01, dur / 3)
    return reverb(norm(y), 3.0, 0.4)
def sfx_heartbeat(dur=8.0, bpm=70):
    n = secs(dur); y = np.zeros(n); per = 60 / bpm
    for k in range(int(dur / per) + 1):
        for off, amp in ((0, 1.0), (0.24, 0.7)):
            s = secs(k * per + off); m = secs(0.18)
            if s + m < n:
                t = np.arange(m) / SR
                y[s:s + m] += amp * np.sin(2 * np.pi * (55 * np.exp(-t / 0.08) + 35) * t) * np.exp(-t / 0.05)
    return stereo(norm(lp(y, 150)))
def sfx_hooves(dur=6.0, bpm=110, seed=7, distance=0.0):
    n = secs(dur); y = np.zeros(n); r = rng(seed); per = 60 / bpm
    for k in range(int(dur / per) + 1):
        for off in (0, 0.11, 0.22):
            s = max(0, secs(k * per + off + r.uniform(-0.01, 0.01))); m = secs(0.07)
            if s + m < n:
                t = np.arange(m) / SR
                hit = bp(r.standard_normal(m), 400, 2500) * np.exp(-t / 0.012) + np.sin(2 * np.pi * 140 * t) * np.exp(-t / 0.02) * 0.6
                y[s:s + m] += hit * r.uniform(0.6, 1)
    if distance: y = lp(y, 2500 - 2000 * distance)
    return reverb(norm(y), 1.5, 0.25 + 0.3 * distance)
def sfx_footsteps(dur=6.0, rate=1.7, seed=8, surface="stone"):
    n = secs(dur); y = np.zeros(n); r = rng(seed)
    for k in range(int(dur * rate)):
        s = max(0, secs(k / rate + r.uniform(-0.03, 0.03))); m = secs(0.12)
        if s + m < n:
            t = np.arange(m) / SR
            hit = lp(r.standard_normal(m), 900 if surface == "stone" else 500) * np.exp(-t / 0.03) + np.sin(2 * np.pi * 90 * t) * np.exp(-t / 0.03) * 0.5
            y[s:s + m] += hit * r.uniform(0.6, 1)
    return reverb(norm(y), 1.8, 0.3)
def sfx_owl(seed=9):
    out = np.zeros(secs(2.2))
    for st, d in ((0, 0.45), (0.7, 0.3), (1.15, 0.6)):
        m = secs(d); t = np.arange(m) / SR
        f = 390 * (1 - 0.06 * t / d)
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 1.5
        out[secs(st):secs(st) + m] += tone
    return reverb(norm(out), 2.5, 0.45)
def sfx_howl(dur=3.5, seed=10):
    n = secs(dur); t = np.arange(n) / SR; u = t / dur
    f = 380 + 300 * np.sin(np.pi * np.minimum(u * 1.4, 1)) - 120 * u + 6 * np.sin(2 * np.pi * 5.5 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = (np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph)) * np.sin(np.pi * u) ** 0.8
    return reverb(norm(y), 3.5, 0.55)
def sfx_clock(dur=8.0, rate=1.0):
    n = secs(dur); y = np.zeros(n)
    for k in range(int(dur * rate)):
        s = secs(k / rate); m = secs(0.03); t = np.arange(m) / SR
        f = 2200 if k % 2 == 0 else 1700
        if s + m < n: y[s:s + m] += np.sin(2 * np.pi * f * t) * np.exp(-t / 0.004)
    return reverb(norm(y), 1.2, 0.25)
def sfx_door(seed=11):
    n = secs(2.2); t = np.arange(n) / SR; r = rng(seed)
    f = 110 + 60 * np.sin(2 * np.pi * 0.7 * t) + np.cumsum(r.standard_normal(n)) * 0.02
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    y = bp(saw, 300, 2500) * np.sin(np.pi * np.minimum(t / 1.8, 1)) * (t < 1.8)
    th = secs(1.85); m = secs(0.3); tt = np.arange(m) / SR
    y[th:th + m] += np.sin(2 * np.pi * 70 * tt) * np.exp(-tt / 0.06) * 2
    return reverb(norm(y), 2.0, 0.35)
def sfx_knock(times=3, seed=12):
    n = secs(0.35 * times + 0.6); y = np.zeros(n); r = rng(seed)
    for k in range(times):
        s = secs(k * 0.33); m = secs(0.15); t = np.arange(m) / SR
        y[s:s + m] += (np.sin(2 * np.pi * 170 * t) + 0.5 * lp(r.standard_normal(m), 1200)) * np.exp(-t / 0.025)
    return reverb(norm(y), 1.6, 0.35)
def sfx_chains(dur=2.5, seed=13):
    n = secs(dur); y = np.zeros(n); r = rng(seed)
    for _ in range(int(dur * 9)):
        s = secs(r.uniform(0, dur - 0.2)); m = secs(0.15); t = np.arange(m) / SR
        f = r.uniform(1800, 4200)
        y[s:s + m] += sum(np.sin(2 * np.pi * f * p * t) * np.exp(-t / 0.03) for p in (1, 1.47, 2.09)) * r.uniform(0.3, 1)
    return reverb(norm(hp(y, 600)), 1.8, 0.35)
def sfx_coins(dur=1.5, seed=14):
    return sfx_chains(dur, seed)
def sfx_splash(seed=15):
    n = secs(2.5); t = np.arange(n) / SR; r = rng(seed)
    y = lp(r.standard_normal(n), 3000) * np.exp(-t / 0.25)
    for _ in range(25):
        s = secs(r.uniform(0.1, 1.8)); m = secs(0.04); tt = np.arange(m) / SR; f = r.uniform(500, 1400)
        y[s:s + m] += np.sin(2 * np.pi * (f + 8000 * tt) * tt) * np.exp(-tt / 0.01) * 0.3
    return reverb(norm(y), 1.8, 0.3)
def sfx_whisper(dur=3.0, seed=16, pan=0.0):
    n = secs(dur); t = np.arange(n) / SR; r = rng(seed)
    noise = r.standard_normal(n); syl = np.clip(np.sin(2 * np.pi * r.uniform(3.5, 5.5) * t + np.sin(2 * np.pi * 0.7 * t)), 0, 1) ** 2
    y = bp(noise, 1500, 5500) * syl * np.sin(np.pi * t / dur)
    return reverb(stereo(norm(y), pan), 2.5, 0.5)
def sfx_gust(dur=4.0, seed=17):
    n = secs(dur); u = np.arange(n) / n
    y = bp(pink(n, seed), 200, 1800) * np.sin(np.pi * u) ** 2
    return stereo(norm(y))
def sfx_bell(freq=196, dur=7.0): return reverb(bell(freq, dur), 4.0, 0.4)
def sfx_fire(dur=5.0, seed=18): return amb_fire(dur, seed)

SFX = {"thunder": sfx_thunder, "boom": sfx_boom, "riser": sfx_riser, "whoosh": sfx_whoosh, "sting": sfx_sting,
       "heartbeat": sfx_heartbeat, "hooves": sfx_hooves, "footsteps": sfx_footsteps, "owl": sfx_owl, "howl": sfx_howl,
       "clock": sfx_clock, "door": sfx_door, "knock": sfx_knock, "chains": sfx_chains, "coins": sfx_coins,
       "splash": sfx_splash, "whisper": sfx_whisper, "gust": sfx_gust, "bell": sfx_bell, "fire": sfx_fire}

# ------------------------------------------------------------------ ambiences (looping beds)
def amb_wind(dur, seed=20):
    n = secs(dur); t = np.arange(n) / SR; p = pink(n, seed)
    lo = bp(p, 150, 600); hi = bp(p, 600, 2500)
    m1 = 0.5 + 0.5 * np.sin(2 * np.pi * 0.06 * t + 1) * np.sin(2 * np.pi * 0.023 * t)
    y = lo * (0.6 + 0.4 * m1) + hi * 0.5 * m1 ** 2
    x = stereo(y); x[:, 1] = np.roll(x[:, 1], secs(0.3)); return norm(x)
def amb_river(dur, seed=21):
    n = secs(dur); r = rng(seed); w = r.standard_normal(n)
    y = bp(w, 300, 2800) * (0.7 + 0.3 * lp(np.abs(r.standard_normal(n)), 8) * 3)
    y += lp(pink(n, seed), 250) * 0.5
    x = stereo(y); x[:, 1] = np.roll(x[:, 1], secs(0.21)); return norm(x)
def amb_rain(dur, seed=22):
    n = secs(dur); r = rng(seed)
    y = bp(r.standard_normal(n), 900, 9000) * 0.6 + lp(pink(n, seed), 400) * 0.3
    drops = np.zeros(n); idx = r.integers(0, n, int(dur * 40)); drops[idx] = r.uniform(0.3, 1, len(idx))
    y += bp(drops, 2000, 7000) * 4
    x = stereo(y); x[:, 1] = np.roll(x[:, 1], secs(0.17)); return norm(x)
def amb_crickets(dur, seed=23):
    n = secs(dur); t = np.arange(n) / SR; r = rng(seed); x = np.zeros((n, 2))
    for k in range(5):
        f = r.uniform(3800, 5200); rate = r.uniform(12, 22); gate_rate = r.uniform(0.4, 1.0); pan = r.uniform(-0.8, 0.8)
        chirp = np.sin(2 * np.pi * f * t) * (np.sin(2 * np.pi * rate * t) > 0.3) * (np.sin(2 * np.pi * gate_rate * t + r.uniform(0, 6)) > 0)
        x += stereo(lp(chirp, 7000) * r.uniform(0.3, 1), pan)
    return norm(x)
def amb_fire(dur, seed=24):
    n = secs(dur); r = rng(seed); y = lp(pink(n, seed), 500) * 0.5
    cr = np.zeros(n); idx = r.integers(0, n, int(dur * 25)); cr[idx] = r.uniform(0.2, 1, len(idx)) * np.sign(r.standard_normal(len(idx)))
    y += bp(cr, 800, 6000) * 6
    return stereo(norm(y))
def amb_sea(dur, seed=25):
    n = secs(dur); t = np.arange(n) / SR; p = pink(n, seed)
    sw = 0.35 + 0.65 * np.clip(np.sin(2 * np.pi * t / 7.5), 0, 1) ** 2
    y = lp(p, 900) * sw + bp(p, 1500, 6000) * sw ** 3 * 0.4
    x = stereo(y); x[:, 1] = np.roll(x[:, 1], secs(1.1)); return norm(x)
def amb_room(dur, seed=26):
    """Quiet interior: low hum + air."""
    n = secs(dur); t = np.arange(n) / SR
    y = 0.4 * np.sin(2 * np.pi * 60 * t) + 0.15 * np.sin(2 * np.pi * 120 * t) + lp(pink(n, seed), 400) * 0.6
    return stereo(norm(y, 0.5))
def amb_drips(dur, seed=27):
    n = secs(dur); r = rng(seed); y = lp(pink(n, seed), 200) * 0.3
    for _ in range(int(dur / 1.6)):
        s = secs(r.uniform(0, max(0.1, dur - 0.3))); m = secs(0.2); tt = np.arange(m) / SR; f = r.uniform(900, 1600)
        y[s:s + m] += np.sin(2 * np.pi * (f + 2500 * tt) * tt) * np.exp(-tt / 0.02)
    return reverb(norm(y), 2.5, 0.5)
def amb_clock(dur, seed=28): return norm(sfx_clock(dur)[:secs(dur)], 0.5)
def amb_night(dur, seed=29):
    return norm(amb_crickets(dur, seed) * 0.6 + amb_wind(dur, seed) * 0.5)
def amb_city(dur, seed=30):
    """Colonial city at night: wind in streets, distant dogs, far bells."""
    x = amb_wind(dur, seed) * 0.6; r = rng(seed)
    for _ in range(int(dur / 25)):
        h = sfx_howl(2.5, int(r.integers(100))) * 0.25; h = lp(h, 1200); s = secs(r.uniform(0, max(0.1, dur - 4)))
        x[s:s + len(h)] += h[: len(x) - s]
    return norm(x)

AMB = {"wind": amb_wind, "river": amb_river, "rain": amb_rain, "crickets": amb_crickets, "fire": amb_fire, "sea": amb_sea,
       "room": amb_room, "drips": amb_drips, "clock": amb_clock, "night": amb_night, "city": amb_city}

# ------------------------------------------------------------------ music moods
SCALES = {"minor": [0, 2, 3, 5, 7, 8, 10], "harmonic": [0, 2, 3, 5, 7, 8, 11], "phrygian": [0, 1, 4, 5, 7, 8, 10]}

def scale_notes(key, scale, octv, count=8):
    base = NOTE[key]; out = []
    for i in range(count):
        st = SCALES[scale][i % 7] + 12 * (i // 7)
        out.append(440 * 2 ** ((base + st - 9) / 12 + (octv - 4)))
    return out

def mood(name, dur, key="A", seed=0):
    """Music bed for a mood: calm, mystery, sad, tension, dread, climax, hope, silence."""
    n = secs(dur)
    if name == "silence" or dur <= 0: return np.zeros((n, 2), np.float32)
    r = rng(seed + zlib.crc32(name.encode()) % 1000)
    root = hz(key + "2"); out = np.zeros((n + secs(5), 2), np.float32)
    def place(sig, t, g=1.0, pan=0.0):
        s = secs(t)
        if s >= len(out): return
        sig = stereo(sig, pan) if sig.ndim == 1 else sig
        e = min(len(out), s + len(sig)); out[s:e] += sig[: e - s] * g
    minor = scale_notes(key, "minor", 3, 15); harm = scale_notes(key, "harmonic", 3, 15)
    tri_i = [root, root * 2 ** (3 / 12), root * 2 ** (7 / 12)]
    if name in ("calm", "sad", "hope", "mystery"):
        prog = {"calm": [0, 5, 3, 4], "sad": [0, 3, 5, 4], "hope": [2, 5, 0, 4], "mystery": [0, 5, 0, 6]}[name]
        chord_len = 8.0 if name != "mystery" else 10.0
        sc = harm if name == "mystery" else minor
        t = 0.0; ci = 0
        while t < dur:
            deg = prog[ci % len(prog)]
            ch = [sc[deg] / 2, sc[deg + 2] / 2, sc[deg + 4] / 2]
            place(pad(ch, chord_len + 3, seed + ci, cutoff=700 if name == "mystery" else 1100), t, 0.35)
            bpm = {"calm": 66, "sad": 58, "hope": 72, "mystery": 52}[name]; beat = 60 / bpm
            notes = [sc[deg], sc[deg + 2], sc[deg + 4], sc[deg + 7], sc[deg + 4], sc[deg + 2]]
            k = 0; tt = t
            while tt < t + chord_len - 0.1 and tt < dur:
                if name != "mystery" or r.random() < 0.45:
                    f = notes[k % len(notes)] * (2 if r.random() < 0.15 else 1)
                    place(pluck(f, 3.0, 0.45, seed + k), tt, 0.32 * r.uniform(0.7, 1), r.uniform(-0.4, 0.4))
                k += 1; tt += beat * (1 if name != "mystery" else 2)
            if name in ("sad", "mystery") and r.random() < 0.5:
                place(piano(sc[deg + 7] * 2, 4, seed + ci), t + chord_len / 2, 0.18, 0.2)
            t += chord_len; ci += 1
        place(drone(root / 2, dur + 2, seed), 0, 0.25)
    elif name in ("tension", "climax"):
        bpm = 84 if name == "tension" else 100; beat = 60 / bpm
        place(drone(root / 2, dur + 2, seed), 0, 0.45)
        place(pad([root, root * 2 ** (1 / 12), root * 2 ** (7 / 12)], dur + 2, seed, cutoff=600), 0, 0.3)
        t = 0.0; k = 0
        while t < dur:
            f = root * (1 if (k // 8) % 2 == 0 else 2 ** (1 / 12))
            place(pluck(f, 0.8, 0.3, k) * 0.8, t, 0.5 if k % 2 == 0 else 0.3)
            if name == "climax" and k % 4 == 0:
                place(sfx_boom(2.5) * 0.5, t, 0.5)
            if k % 16 == 15 and name == "tension":
                place(piano(harm[6] * 2, 2.5, k), t, 0.15, -0.3)
            t += beat / 2; k += 1
    elif name == "dread":
        place(drone(root / 2, dur + 2, seed), 0, 0.6)
        x = pad([root * 2, root * 2 * 2 ** (6 / 12), root * 2 * 2 ** (11 / 12)], dur + 2, seed + 1, cutoff=500, detune=0.3)
        place(x, 0, 0.28)
        t = r.uniform(4, 9)
        while t < dur - 2:
            place(sfx_sting(4.0, int(r.integers(100)), key + "2") * 0.18, t, 0.6); t += r.uniform(14, 26)
        t = r.uniform(8, 14)
        while t < dur - 2:
            place(piano(harm[int(r.integers(0, 7))] * r.choice([1, 2]), 5, int(t)), t, 0.14, r.uniform(-0.5, 0.5)); t += r.uniform(7, 15)
    out = reverb(out, 3.5, 0.32, seed=5)[:n]
    return fade(norm(out, 0.85), 1.5, 2.5)
