#!/bin/bash
# One-time setup of the production pipeline in a fresh workspace. Safe to re-run.
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
P=/home/claude/pipeline
if [ ! -e "$P" ]; then ln -s "$REPO/pipeline" "$P"; fi
pip install --break-system-packages -q kokoro-onnx soundfile opencv-python-headless pyloudnorm scipy numpy 2>&1 | grep -v WARNING || true
mkdir -p "$P/models" "$P/cache"
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "$P/models/$f" ] || curl -sSL --retry 3 -o "$P/models/$f" "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done
if [ ! -d "$P/node/node_modules/@resvg/resvg-js" ]; then
  mkdir -p "$P/node" && cd "$P/node" && npm init -y >/dev/null && npm i --silent @resvg/resvg-js
fi
which ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
python3 -c "import kokoro_onnx, cv2, pyloudnorm, soundfile; print('pipeline ready')"
