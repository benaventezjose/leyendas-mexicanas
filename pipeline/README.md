# Leyendas Mexicanas — shared video pipeline

Everything runs locally in this workspace (no internet needed except optional web research).
Output: 1920x1080, 30 fps, H.264 + AAC, -14 LUFS, Spanish narration, Spanish .srt subtitles.

Working example (tiny, 22 s): `/home/claude/videos/_test/` → `story.json`, `make_art.py`, `out/final.mp4`.

## Folder layout per video
```
/home/claude/videos/<slug>/
  story.json        # the whole video: narration beats + scenes + sound cues
  make_art.py       # python that writes art/*.svg (use /home/claude/pipeline/art.py helpers)
  art/*.svg, *.png  # illustrations, canvas 2400x1350 (16:9, 1.25x frame so the camera can move)
  thumb_a.svg/.png, thumb_b.svg/.png   # two thumbnail variants (1280x720 PNG)
  metadata.md       # YouTube title, description with chapters, tags
  subs.srt          # written by tts.py
  audio/            # narration.wav, timeline.json, mix.wav
  out/final.mp4     # the video
  check/            # stills / contact sheets for checking
```

## Commands (in order)
```
python3 /home/claude/pipeline/tts.py      PROJ   # narration + timeline + subs.srt (cached per sentence)
python3 make_art.py && node /home/claude/pipeline/render_svg.js art/*.svg      # illustrations -> PNG
python3 /home/claude/pipeline/render.py   PROJ --contact            # contact sheet of every scene (check/contact_XX.jpg)
python3 /home/claude/pipeline/render.py   PROJ --stills 12.5,95,300 # full-size check frames at global seconds
python3 /home/claude/pipeline/mix.py      PROJ   # music + ambience + sfx + voice -> audio/mix.wav
python3 /home/claude/pipeline/render.py   PROJ   # render changed scenes and assemble out/final.mp4
node /home/claude/pipeline/render_svg.js thumb_a.svg thumb_b.svg --width 1280
```
tts.py, mix.py and the full render take a shared CPU lock (`/home/claude/pipeline/cpu.lock`): only one runs at a
time across all videos, so a call may first wait. That's expected; don't kill it. A full render of a 12-minute
video takes roughly 8–15 minutes of CPU. Render the full video ONCE when everything checks out; use --contact and
--stills to check. Scenes are cached: re-running render.py re-renders only scenes whose spec or art changed.

## story.json
```json
{
  "title": "…", "voice": "em_alex", "speed": 0.88, "sentence_gap": 0.28,
  "key": "A",            // musical key for the score (A, D, E, C, G…)
  "seed": 1,
  "grade": "night",      // default colour grade: none night moon cold warm candle sepia blood bw
  "vignette": 0.55, "outro": 4.0,          // seconds of picture+music after the last line
  "music_gain": -15, "amb_gain": -21, "sfx_gain": -9,   // dB, defaults shown
  "beats": [ BEAT, BEAT, … ]
}
```
### BEAT = one chunk of narration (1–4 sentences) and what is on screen while it plays
```json
{
  "id": "b001",
  "text": "Spanish narration…",       // may be "" for a silent visual beat (then set "pause")
  "voice": "ef_dora", "speed": 0.8,    // optional override (character lines). Voices: em_alex (male narrator),
                                       //   em_santa (male, other character), ef_dora (female)
  "fx": "eco",                         // optional ghostly echo on this beat's voice (for ghost lines)
  "pre": 1.0,                          // optional silence before the text (lets a visual / sting land)
  "pause": 0.55,                       // silence after the beat (default 0.55)
  "music": "dread", "music_at": 0.0,   // switch score mood at this beat: calm mystery sad hope tension dread climax silence
  "amb": ["wind", {"name":"river","gain":-4}],   // ambience beds from here on (replaces previous): wind river rain
                                       //   crickets fire sea room drips clock night city ; [] = none
  "sfx": [{"name":"thunder","at":0.3,"gain":-3,"pan":0.0,"args":{}}],
       // at = seconds from beat start (negative allowed, e.g. riser at -4 to land on the beat).
       // names: thunder boom riser whoosh sting heartbeat hooves footsteps owl howl clock door knock chains coins
       //        splash whisper gust bell fire.  args examples: {"dur":6} riser/hooves/heartbeat/footsteps/clock/whisper,
       //        {"bpm":90} heartbeat/hooves, {"distance":0.6} hooves, {"freq":160} bell, {"times":3} knock
  "scenes": [ SCENE, … ]               // split the beat's duration between scenes by "weight" (default 1) or fixed "dur"
}
```
### SCENE
```json
{
  "layers": [                                       // bottom → top, PNGs on the 2400x1350 canvas
    {"src": "art/rio_bg.png"},                      // first layer should be opaque
    {"src": "art/llorona.png", "depth": 1.1, "blend": "screen",      // normal | screen (ghosts, light) | add | multiply
     "opacity": [0, 0.9], "fade_in": 1.0, "appear_at": 2.0, "vanish_at": 6.0, "fade_out": 0.5,
     "anim": [{"type": "float", "amp": 0.006, "period": 5}]},
    {"src": "art/rio_fg.png", "depth": 1.35}        // depth > 1 moves more than the camera = parallax foreground
  ],
  "cam": {"from": [0.45, 0.55, 1.0], "to": [0.6, 0.5, 1.3], "ease": "inout"},
       // [centre x, centre y, zoom] in art-normalised coords; zoom 1 = whole canvas, 1.25 = 1:1 pixels,
       // up to ~1.8 still OK. Omit cam for an automatic gentle move. Ease: inout linear in out.
  "fx": ["fog", {"type": "fog", "strength": 0.4, "color": [190,205,220], "low": true, "speed": 1.0, "seed": 2},
         "dust", "embers", "ash", "fireflies", {"type": "rain", "strength": 0.35},
         {"type": "flicker", "amp": 0.06}, {"type": "lightning", "at": [1.2, 4.0]},
         {"type": "shake", "amp": 6, "at": [0.0, 1.5]}, {"type": "pulse", "bpm": 70, "amp": 0.12}, {"type": "darken", "amount": 0.6}],
  "grade": "cold",                                  // per-scene override
  "text": [{"str": "CAPÍTULO I|El río", "style": "chapter", "at": [0.5, 4.5]}],
       // styles: title ("TITLE|subtitle"), chapter ("CAPÍTULO I|Name"), big ("WORD|small yellow line"),
       //         date ("Ciudad de México, 1634|note"), quote ("spoken line|who"), whisper, caption.  pos: top|center|bottom
  "transition": "cut",                              // cut | fade (from black) | xfade (crossfade from previous) | flash (white)
  "transition_len": 0.8,
  "out": "fade", "out_len": 1.0,                    // optional fade to black at the end of this scene
  "weight": 1, "dur": 3.0,                          // share of the beat, or fixed seconds
  "vignette": 0.6
}
```
Layer `anim` types (applied in art space, before the camera): `drift {dx,dy,ease}` (fractions of canvas, over the
scene) · `float {amp,period}` · `sway {deg,period,pivot:[x,y]}` (trees, hanging lamps, cloth) · `pulse {amp,period,pivot}`
· `scale {from,to,pivot,ease}` (something approaching) · `shake {amp}` · `flicker {amp,speed}` (opacity, candles/ghosts).

## Art (art.py helpers, 2400x1350 canvas)
`svg(*parts)` · `sky(top,bottom,mid)` · `stars(n,seed,ymax)` · `moon(cx,cy,r,phase)` · `ridge(y,amp,color,seed)` ·
`water(y0,y1)` · `reflection(cx,y0,y1)` · `reeds(x0,x1,y)` · `tree(x,y,size,seed,color,kind=bare|willow|ahuehuete)` ·
`glow(x,y,r,kind=warm|red|white|moon)` · `candle(x,y)` · `lamp(x,y)` · `window(x,y,w,h,lit)` · `facade(x,y_base,w,h)` ·
`church(x,y_base,scale)` · `cobbles(y0)` · `papel_picado(y)` · `figure(x,y,h,hat,dress,pose,rim,eyes,veil,hair)` (rough
generic silhouette) · `ghost_woman(x,y,h)` (rough) · `thumb(*parts)` + `thumb_text("NO\nVOLTEES")` for thumbnails.
Filters available inside every svg(): `url(#blur1..4)`, `url(#glow)`, `url(#ghost)`, `url(#paper)`, gradients
`url(#moonglow|warmglow|redglow|whiteglow)`. resvg supports gradients, masks, clipPath, feGaussianBlur, feTurbulence,
feDropShadow, feColorMatrix, text with fonts: Anton, Cinzel, IM FELL English, Rye, Oswald, Lora, Poppins.

The helpers are for backgrounds and quick extras. **Hero characters and key props must be drawn custom** with
real detail (hand-written paths: faces with hollow eyes, hair strands, folds in cloth, hands, horse anatomy…),
lit with rim light and glows. Always render and LOOK at your art (Read the PNG) and fix what looks crude.
Draw transparent PNG layers (no background rect) for things that move separately from the background.

## Look of the channel
Moonlit shadow-theatre illustration: deep night blues/teals, warm amber candle/lamp light, red only for danger,
silhouettes with rim light, layered fog, strong vignette. Mexican specificity: colonial architecture, cantera stone,
ahuehuetes, magueyes, nopales, cempasúchil, rebozos, sombreros, papel picado, adobe, chinampas, volcanoes.
