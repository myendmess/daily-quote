#!/usr/bin/env bash
# Render a 1080x1920 vertical "Short" from the daily quote, with background music.
# Inputs (in the working directory): quote.txt, author.txt (raw text).
# Music: a random *.mp3 from assets/music/ (falls back to silence if none).
# Output: out.mp4
set -euo pipefail

# ffmpeg is preinstalled on GitHub-hosted ubuntu runners; install if missing.
if ! command -v ffmpeg >/dev/null 2>&1; then
  sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg
fi

# drawtext does not auto-wrap, so wrap on spaces to fit the frame width.
fold -s -w 26 quote.txt > quote_wrapped.txt
printf '— %s' "$(cat author.txt)" > author_line.txt

FONT_BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DUR=15

VF="drawtext=fontfile=${FONT_BOLD}:textfile=quote_wrapped.txt:fontcolor=white:fontsize=66:line_spacing=18:x=(w-text_w)/2:y=(h-text_h)/2-120,drawtext=fontfile=${FONT_REG}:textfile=author_line.txt:fontcolor=0xffd166:fontsize=46:x=(w-text_w)/2:y=(h-text_h)/2+280"

# Pick a random background track if any exist.
shopt -s nullglob
tracks=(assets/music/*.mp3)
shopt -u nullglob

if [ ${#tracks[@]} -gt 0 ]; then
  track="${tracks[RANDOM % ${#tracks[@]}]}"
  echo "Using music: $track"
  ffmpeg -y \
    -f lavfi -i "color=c=0x0d1b2a:s=1080x1920:d=${DUR}" \
    -i "$track" \
    -map 0:v -map 1:a \
    -vf "$VF" \
    -af "afade=t=out:st=$((DUR-2)):d=2" \
    -t ${DUR} -r 30 -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k out.mp4
else
  echo "No music in assets/music/ — rendering with silent audio."
  ffmpeg -y \
    -f lavfi -i "color=c=0x0d1b2a:s=1080x1920:d=${DUR}" \
    -f lavfi -i "anullsrc=channel_layout=stereo:sample_rate=44100" \
    -map 0:v -map 1:a \
    -vf "$VF" \
    -t ${DUR} -r 30 -c:v libx264 -pix_fmt yuv420p -c:a aac out.mp4
fi

echo "Rendered out.mp4"
