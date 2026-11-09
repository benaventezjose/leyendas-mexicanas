# Daily run — one new "Leyendas Mexicanas" video, scheduled on YouTube for 9:00 am (America/Mexico_City)

You are producing ONE complete ~12-minute Spanish YouTube video about a Mexican legend, end to end, with no one
watching, then scheduling it through Metricool. Do the work yourself in this session (no subagents).

## 0. Setup (≈3 min)
```
cd <this repo> && ./setup.sh
```
This links the pipeline to /home/claude/pipeline, installs deps and downloads the voice model.
Read `pipeline/README.md` fully: it documents tts.py, render_svg.js, render.py, mix.py, sound.py and art.py.
Look at one finished example in `examples/` (story.json, make_art.py, chars.py, script.md, metadata.md) to match
the channel's level of quality and structure. Do not edit `pipeline/` unless a real bug blocks you; if you fix one,
commit the fix with a clear message.

## 1. Pick the legend
Open `legends.json`. Take the FIRST entry of `backlog` (skip it only if you find it is not really a Mexican legend
or cannot be told in a YouTube-friendly way; then take the next and say why in your report). Never repeat a legend
in `done`. Project folder: `/home/claude/videos/<slug>/` (slug: lowercase, hyphens, no accents).
Do 3–5 quick web searches to get the details, the region, the historical facts and the main variants right.

## 2. Script (Spanish, Mexican storytelling voice) → `script.md`
- 1,750–2,050 words; after tts.py the narration must land between 10:30 and 13:30 (aim ~12 min). Edit and re-run if not.
- Retention: cold open in the first 15–20 s with the most chilling moment in medias res + an open loop paid off only
  at the end; title card by ~0:25; 4–5 chapters with escalating tension; a mini-reveal or scare every 60–90 s;
  short sentences, second person ("imagina que…"), concrete sensory detail; one short subscribe line at ~40%;
  ending: payoff, chilling last line, a question for the comments, and a tease of the NEXT legend in the backlog.
  No "hola amigos, bienvenidos".
- Frame it as legend ("cuentan que…"); facts about real places/people/dates must be accurate; separate history from
  legend. YouTube-friendly: imply violence, never gore; no method details for suicide; children's deaths only implied.
- TTS rules: numbers and years in words, no abbreviations, no parentheses, no English words; "…" = dramatic pause.
  Narrator em_alex speed 0.88; female characters ef_dora; other men em_santa; ghosts/devils "fx":"eco".

## 3. Build (follow pipeline/README.md)
story.json beats + scenes + sound cues → `tts.py` → art (make_art.py → render_svg.js) → `render.py --contact`
(LOOK at every contact sheet and fix weak frames) → `--stills` at key moments → `mix.py` → full `render.py` ONCE.
- 80–120 shots, each 4–10 s; ≥30 distinct illustrations, each reused at most ~3 times with different framing.
- Every scene moves (camera + parallax/animated layer/fog/particles/flicker…); xfade/fade at chapters; 4–6 flash
  scares with sting/boom; "big" text for 3–5 key words; chapter cards; date/place cards.
- Draw hero characters custom with real detail (faces, hair, hands, cloth folds, rim light); the generic
  figure()/ghost_woman() helpers look crude. Render each art file and Read the PNG; improve anything crude.
- Look of the channel: moonlit shadow-theatre illustration, night blues/teals, warm amber light, red only for danger.

## 4. Thumbnail and metadata
- `thumb_a.png` 1280x720 (art.thumb + thumb_text, export `--width 1280`): one close, high-contrast subject,
  2–3 huge words, bottom-right corner clear. Check it still reads at 320x180.
- `metadata.md`: title (≤100 chars), description in Spanish (2–3 hook lines, short summary, chapters from
  audio/timeline.json starting at 0:00, ≥3 chapters, comment question, "Próximo video: …", one line saying it is a
  traditional legend told for entertainment with a synthesized narration voice, 3 hashtags), 15–25 tags.

## 5. Final checks (all must pass before scheduling)
ffprobe: 1920x1080, has audio, duration 10:30–13:30; loudness ≈ -14 LUFS (mix.py prints it); extract 6 frames
spread across the video and look at them; subs.srt runs to the end. If something fails, fix it.

## 6. Host the files (public download links for Metricool)
GitHub releases cannot be created from these sessions, so the video goes on its own branch (files there must stay
under GitHub's 100 MB limit):
```
cd /home/claude/videos/<slug>
ffmpeg -y -i out/final.mp4 -c:v libx264 -preset medium -b:v 850k -maxrate 1300k -bufsize 2600k -pix_fmt yuv420p \
       -c:a aac -b:a 96k -movflags +faststart <slug>.mp4        # must be < 95 MB; if not, lower -b:v and redo
ffmpeg -y -i thumb_a.png -q:v 2 <slug>.jpg                       # thumbnail as JPG
BR=video/$(date +%Y-%m-%d)-<slug>
cd <repo> && git checkout --orphan $BR && git rm -rq --cached . && cp /home/claude/videos/<slug>/<slug>.{mp4,jpg} .
git add <slug>.mp4 <slug>.jpg && git commit -m "Video <slug>" && git push origin $BR && git checkout -f main
```
Video URL: `https://raw.githubusercontent.com/benaventezjose/leyendas-mexicanas/$BR/<slug>.mp4` (thumbnail: same
with .jpg). Check with `curl -sIL <url> | grep -iE "^HTTP|content-length"` that it ends in 200 with the full size.
(Old video branches pile up; the owner deletes them from GitHub now and then. Mention the count in the report.)

## 7. Schedule on YouTube through Metricool
Call createScheduledPost with blogId "7820990" (brand "_scorify", which also holds unrelated Instagram/TikTok
accounts: providers must be ONLY `[{"network":"youtube"}]`, never instagram or tiktok).
- date / publicationDate: today 09:00:00, timezone America/Mexico_City. If it is already past 08:45, use now + 30 min.
- text: the full description from metadata.md (≤5000 chars).
- media: [video URL]; videoThumbnailUrl: thumbnail URL. If the call is rejected with VIDEO_THUMBNAIL_NOT_APPLICABLE,
  retry once without videoThumbnailUrl (and say so in the report).
- youtubeData: {"title": <title>, "type": "video", "privacy": "public", "tags": [...], "category": "ENTERTAINMENT",
  "madeForKids": false, "isAiGeneratedContent": true}
- autoPublish true, draft false. Keep the returned plannerUrl.
Then confirm it with getScheduledPosts (brandId 7820990, today, America/Mexico_City).

## 8. Record and push
- Move the legend from `backlog` to `done` in legends.json with {"slug","title","published": "<date> 09:00",
  "planner_url"}. Add 3–5 new, distinct Mexican legends to the end of the backlog if it has fewer than 15 left.
- Copy script.md, metadata.md, story.json and make_art.py (and chars.py if any) to `published/<date>-<slug>/`.
- Commit ("Video <date>: <title>") and push to main (fetch first).

## 9. Report
Send the user a short message (SendUserMessage): the title, length, scheduled time, the Metricool planner link,
the video's raw URL, and anything weak or skipped. If the run cannot finish (e.g. Metricool refuses the upload),
do NOT post anything half-done: report exactly what failed and leave the video branch in place.
