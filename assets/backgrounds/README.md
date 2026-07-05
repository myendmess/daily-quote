# Background clips (Phase 2)

Drop background clips here and a later workflow update will pick one at random,
crop it to vertical, loop it to the video length, and draw the quote on top
(with a dark scrim so the text stays readable).

## Recommended format for Shorts

| Property    | Recommended                                  | Why |
| ----------- | -------------------------------------------- | --- |
| Container   | **MP4 (H.264 + AAC/none)**                   | Universal, small, high quality. **Not GIF** — a 1080×1920 GIF is huge and grainy. |
| Aspect      | **9:16 vertical, 1080×1920**                 | Native Short size; landscape gets cropped to fill (center-safe). |
| Duration    | **10–15 s**, ideally a seamless loop         | Video is 15 s; shorter clips are looped. |
| Frame rate  | 30 fps                                        | Matches the render. |
| File size   | **< ~8 MB each** (bitrate ~3–5 Mbps)         | These live in git; big files bloat the repo. |
| Motion      | **Slow / calm** (water, clouds, mountain pans, skylines) | Fast motion fights the text; slow footage reads best. |
| Center area | Keep it relatively plain                     | The quote sits centered; a busy center hurts legibility even with the scrim. |

## Naming

Lowercase, no spaces or `&`: `calm-water.mp4`, `mountain-pan.mp4`, `city-skyline.mp4`.

## How to add them

Either commit them here yourself, or drop them in a Google Drive folder and I'll
copy + commit them (same as the music track). Aim for **3–5 clips** to start so
the daily pick has variety.
