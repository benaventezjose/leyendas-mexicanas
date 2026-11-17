#!/usr/bin/env python3
"""Vertical 1080x1920 Short for La Calle de la Quemada, cut from the long video with new narration.
Shots are re-framed 9:16 crops of the long video (with slow pan), 3 white-flash scares,
big words + burned captions via ASS, end card. Usage: python3 build_short.py"""
import json, os, subprocess

P = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(P, "src/long.mp4")
FONTS = "/home/claude/pipeline/fonts"
os.makedirs(os.path.join(P, "shots"), exist_ok=True)
os.makedirs(os.path.join(P, "out"), exist_ok=True)

# (start, end, source start second (ss), crop centre x 0..1, flash)
SHOTS = [
    (0.0, 1.8, 7.0, .50, 0), (1.8, 3.4, 11.5, .60, 0), (3.4, 5.6, 16.5, .55, 0), (5.6, 8.73, 22.5, .36, 1),
    (8.73, 11.2, 60.0, .72, 0), (11.2, 13.0, 151.0, .50, 0), (13.0, 14.98, 109.0, .50, 0),
    (14.98, 17.3, 173.0, .45, 0), (17.3, 20.0, 187.5, .50, 0), (20.0, 22.2, 224.0, .50, 0), (22.2, 24.31, 141.0, .50, 0),
    (24.31, 26.18, 272.5, .50, 1), (26.18, 27.78, 284.5, .38, 0), (27.78, 30.21, 286.5, .74, 0),
    (30.21, 32.4, 300.0, .50, 0), (32.4, 34.37, 292.5, .50, 0), (34.37, 36.81, 360.5, .50, 0),
    (36.81, 38.8, 348.0, .50, 0), (38.8, 40.88, 227.0, .48, 0), (40.88, 43.97, 380.0, .50, 0),
    (43.97, 46.9, 384.5, .50, 0), (46.9, 48.99, 477.2, .45, 1),
]
END_START, TOTAL = 48.99, 56.68

SW, SH = 2208, 1242          # source upscaled 1.15x so the 9:16 window can pan
CW = 699                     # crop width for 9:16 at SH


def run(cmd):
    subprocess.run(cmd, check=True)


files = []
for i, (a, b, st, cx, flash) in enumerate(SHOTS):
    d = round(b - a, 3)
    out = os.path.join(P, f"shots/s{i:02d}.mp4")
    x0 = min(max(cx * SW - CW / 2 - 35 * (1 if i % 2 else -1), 0), SW - CW)
    x1 = min(max(cx * SW - CW / 2 + 35 * (1 if i % 2 else -1), 0), SW - CW)
    vf = (f"scale={SW}:{SH},crop={CW}:{SH}:'{x0:.1f}+({x1 - x0:.1f})*t/{d}':0,"
          f"scale=1080:1920:flags=lanczos,setsar=1,fps=30")
    if flash:
        vf += ",fade=in:st=0:d=0.45:color=white"
    if not os.path.exists(out) or os.environ.get("REBUILD"):
      run(["ffmpeg", "-v", "error", "-y", "-ss", str(st), "-t", str(d), "-i", SRC,
         "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", out])
    files.append(out)

# end card: blurred ceiba frame, slow push in
d = round(TOTAL - END_START, 3)
out = os.path.join(P, "shots/end.mp4")
run(["ffmpeg", "-v", "error", "-y", "-ss", "33.2", "-t", str(d), "-i", SRC, "-vf",
     f"scale={SW}:{SH},crop={CW}:{SH}:{SW/2-CW/2:.0f}:0,scale=1080:1920,setsar=1,fps=30,gblur=sigma=18,"
     f"eq=brightness=-0.12,fade=in:st=0:d=0.5", "-an", "-c:v", "libx264", "-preset", "veryfast",
     "-crf", "16", "-pix_fmt", "yuv420p", out])
files.append(out)

with open(os.path.join(P, "shots/list.txt"), "w") as f:
    for x in files:
        f.write(f"file '{x}'\n")


# ---- ASS: captions (short chunks) + big words + end card text
def ts(t):
    cs = int(round(t * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


tl = json.load(open(os.path.join(P, "audio/timeline.json")))
ev = []
for bt in tl["beats"]:
    for s in bt["sentences"]:
        words = s["text"].split()
        chunks, cur = [], []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 18 or w.endswith((",", "…", ".", "?")):
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
        n = sum(len(" ".join(c)) for c in chunks)
        t = s["start"]
        for c in chunks:
            txt = " ".join(c)
            dd = (s["end"] - s["start"]) * len(txt) / n
            ev.append(f"Dialogue: 0,{ts(t)},{ts(t + dd)},Cap,,0,0,0,,{txt.upper()}")
            t += dd

BIG = [(5.7, 8.6, "UN VELO|BLANCO"), (24.4, 27.6, "LOS|DUELOS"), (37.4, 40.8, "SIEMPRE HABRÁ|ALGUIEN"),
       (46.95, 48.95, "¿QUÉ HABÍA|DETRÁS DEL VELO?")]
for a, b, s in BIG:
    l1, l2 = s.split("|")
    ev.append(f"Dialogue: 1,{ts(a)},{ts(b)},Big,,0,0,0,,{{\\pos(540,820)\\fad(150,200)\\fscx115\\fscy115\\t(0,250,\\fscx100\\fscy100)}}{l1}\\N{{\\c&H2EC8F5&}}{l2}")

ev.append(f"Dialogue: 2,{ts(END_START + 0.3)},{ts(TOTAL)},End,,0,0,0,,{{\\pos(540,560)\\fad(400,0)}}VIDEO COMPLETO\\NEN EL CANAL")
ev.append(f"Dialogue: 2,{ts(END_START + 0.8)},{ts(TOTAL)},Title,,0,0,0,,{{\\pos(540,980)\\fad(400,0)}}La Calle\\Nde la Quemada\\N{{\\fs54}}la mujer que se escondió\\Ndetrás de un velo")
ev.append(f"Dialogue: 2,{ts(END_START + 1.4)},{ts(TOTAL)},Sub,,0,0,0,,{{\\pos(540,1180)\\fad(300,0)}}SUSCRÍBETE")

ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Oswald,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,1,0,0,0,100,100,1,0,1,6,3,2,90,90,560,1
Style: Big,Anton,150,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,2,0,1,8,6,5,60,60,0,1
Style: End,Anton,118,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,2,0,1,7,5,5,60,60,0,1
Style: Title,Cinzel,92,&H002EC8F5,&H00FFFFFF,&H00000000,&HA0000000,1,0,0,0,100,100,2,0,1,5,4,5,60,60,0,1
Style: Sub,Oswald,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H002020C8,1,0,0,0,100,100,3,0,3,18,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"
open(os.path.join(P, "short.ass"), "w", encoding="utf-8").write(ass)

final = os.path.join(P, "out/final.mp4")
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(P, "shots/list.txt"),
     "-i", os.path.join(P, "audio/mix.wav"),
     "-vf", f"vignette=PI/5,subtitles={os.path.join(P, 'short.ass')}:fontsdir={FONTS}",
     "-map", "0:v", "-map", "1:a", "-t", str(TOTAL), "-c:v", "libx264", "-preset", "medium", "-crf", "19",
     "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", final])
print("done", final)
