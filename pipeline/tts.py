#!/usr/bin/env python3
"""Spanish narration builder (Kokoro TTS, local, offline).

Usage:  python3 /home/claude/pipeline/tts.py PROJECT_DIR

Reads  PROJECT_DIR/story.json  (see /home/claude/pipeline/README.md for the format)
Writes PROJECT_DIR/audio/narration.wav   48 kHz mono narration
       PROJECT_DIR/audio/timeline.json   start/end of every beat and sentence (seconds)
       PROJECT_DIR/subs.srt              Spanish subtitles for YouTube upload
Sentences are cached in PROJECT_DIR/audio/cache, so re-running only re-synthesises changed text.
"""
import json, sys, os, re, hashlib, fcntl, time
import numpy as np, soundfile as sf
from scipy.signal import resample_poly, fftconvolve

PIPE = os.path.dirname(os.path.abspath(__file__))
SR_K = 24000
SR_OUT = 48000
_k = None


def kokoro():
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(os.path.join(PIPE, "models/kokoro-v1.0.onnx"), os.path.join(PIPE, "models/voices-v1.0.bin"))
    return _k


def split_sentences(text):
    text = re.sub(r"\s+", " ", text.strip())
    parts = re.findall(r'[^.!?…]+(?:[.!?…]+["»”’]?|$)', text)
    out = [p.strip() for p in parts if p.strip(" .")]
    return out or [text]


def trim(x, thr=0.006, pad=0.03):
    idx = np.where(np.abs(x) > thr)[0]
    if len(idx) == 0:
        return x
    p = int(pad * SR_K)
    return x[max(0, idx[0] - p): min(len(x), idx[-1] + p)]


LANG = "es-419"  # Latin-American Spanish phonemes (seseo, yeísmo) — right for Mexican narration

def synth(text, voice, speed, cache):
    h = hashlib.sha1(f"{voice}|{speed}|{text}|{LANG}".encode()).hexdigest()[:16]
    f = os.path.join(cache, h + ".wav")
    if os.path.exists(f):
        x, _ = sf.read(f, dtype="float32")
        return x
    s, sr = kokoro().create(text, voice=voice, speed=speed, lang=LANG)
    assert sr == SR_K
    s = trim(np.asarray(s, dtype=np.float32))
    sf.write(f + ".tmp.wav", s, SR_K)
    os.replace(f + ".tmp.wav", f)
    return s


def echo_fx(x, sr):
    """Ghostly voice: long reverb tail + faint delayed repeat."""
    n = int(2.2 * sr)
    t = np.arange(n) / sr
    rng = np.random.default_rng(7)
    ir = rng.standard_normal(n) * np.exp(-t / 0.55)
    ir[0] = 6.0
    ir /= np.abs(ir).sum() ** 0.5
    wet = np.zeros(len(x) + n, np.float32); w = fftconvolve(x, ir); wet[: min(len(wet), len(w))] = w[: len(wet)]
    out = np.zeros(len(x) + n, np.float32)
    out[: len(x)] += x * 0.75
    out += wet / (np.abs(wet).max() + 1e-9) * np.abs(x).max() * 0.55
    d = int(0.32 * sr)
    out[d: d + len(x)] += x * 0.25
    return out


def wrap_lines(s, width=42):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def srt_chunks(sentence, t0, t1, maxc=84):
    if len(sentence) <= maxc:
        return [(sentence, t0, t1)]
    # split at commas / semicolons / spaces into chunks <= maxc
    pieces, cur = [], ""
    for tok in re.split(r"(?<=[,;:])\s+", sentence):
        if len(cur) + len(tok) + 1 <= maxc:
            cur = (cur + " " + tok).strip()
        else:
            if cur:
                pieces.append(cur)
            while len(tok) > maxc:
                cut = tok.rfind(" ", 0, maxc)
                cut = cut if cut > 20 else maxc
                pieces.append(tok[:cut].strip()); tok = tok[cut:].strip()
            cur = tok
    if cur:
        pieces.append(cur)
    total = sum(len(p) for p in pieces)
    out, t = [], t0
    for p in pieces:
        d = (t1 - t0) * len(p) / total
        out.append((p, t, t + d)); t += d
    return out


def fmt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main(proj):
    story = json.load(open(os.path.join(proj, "story.json"), encoding="utf-8"))
    adir = os.path.join(proj, "audio"); cache = os.path.join(adir, "cache")
    os.makedirs(cache, exist_ok=True)
    dvoice = story.get("voice", "em_alex"); dspeed = float(story.get("speed", 0.88))
    gap = float(story.get("sentence_gap", 0.28))
    lock = open(os.path.join(PIPE, "cpu.lock"), "w")
    print("waiting for CPU lock…", flush=True); fcntl.flock(lock, fcntl.LOCK_EX)
    t_start = time.time()
    chunks, cur = [], 0.0
    timeline = {"beats": [], "sr": SR_OUT}
    srt = []
    for bi, b in enumerate(story["beats"]):
        bid = b.get("id", f"b{bi+1:03d}")
        pre = float(b.get("pre", 0.0))
        bstart = cur
        if pre:
            chunks.append(np.zeros(int(pre * SR_K), np.float32)); cur += pre
        voice = b.get("voice", dvoice); speed = float(b.get("speed", dspeed))
        sents = split_sentences(b["text"]) if b.get("text", "").strip() else []
        sent_t = []
        for si, s in enumerate(sents):
            x = synth(s, voice, speed, cache)
            if b.get("fx") == "eco":
                x = echo_fx(x, SR_K)
            x = x * float(b.get("gain", 1.0))
            t0 = cur
            chunks.append(x); cur += len(x) / SR_K
            sent_t.append({"text": s, "start": round(t0, 3), "end": round(cur, 3)})
            for (p, a, z) in srt_chunks(s, t0, cur):
                srt.append((p, a, z))
            g = gap * (2.2 if s.endswith("…") or s.endswith("...") else 1.0) if si < len(sents) - 1 else 0
            if g:
                chunks.append(np.zeros(int(g * SR_K), np.float32)); cur += g
        pause = float(b.get("pause", 0.55))
        chunks.append(np.zeros(int(pause * SR_K), np.float32)); cur += pause
        timeline["beats"].append({"id": bid, "start": round(bstart, 3), "end": round(cur, 3),
                                  "voice_start": sent_t[0]["start"] if sent_t else None,
                                  "sentences": sent_t})
        print(f"{bid}: {bstart:7.2f}–{cur:7.2f}s  {len(sents)} sentences", flush=True)
    fcntl.flock(lock, fcntl.LOCK_UN)
    audio = np.concatenate(chunks) if chunks else np.zeros(SR_K, np.float32)
    audio = resample_poly(audio, SR_OUT, SR_K).astype(np.float32)
    pk = np.abs(audio).max() + 1e-9
    audio = audio / pk * 0.89
    sf.write(os.path.join(adir, "narration.wav"), audio, SR_OUT)
    timeline["duration"] = round(len(audio) / SR_OUT, 3)
    json.dump(timeline, open(os.path.join(adir, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    with open(os.path.join(proj, "subs.srt"), "w", encoding="utf-8") as f:
        for i, (p, a, z) in enumerate(srt, 1):
            f.write(f"{i}\n{fmt(a)} --> {fmt(z)}\n" + "\n".join(wrap_lines(p)) + "\n\n")
    words = sum(len(b.get("text", "").split()) for b in story["beats"])
    print(f"DONE narration {timeline['duration']/60:.2f} min, {words} words, synth {time.time()-t_start:.0f}s")


if __name__ == "__main__":
    main(sys.argv[1])
