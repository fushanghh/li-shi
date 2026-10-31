#!/bin/bash
# 一键重建：《随份子从哪儿来》 1440×1080 24fps
set -e; cd "$(dirname "$0")"
pip install -q numpy scipy cairocffi pillow soundfile
python3 film.py --part 0 --parts 2 & python3 film.py --part 1 --parts 2 & wait
python3 audio.py
cd out && printf "file 'part0.mp4'\nfile 'part1.mp4'\n" > list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c copy /tmp/v.mp4
ffmpeg -y -loglevel error -i /tmp/v.mp4 -i mix.wav -vf fps=24 -c:v libx264 -profile:v high -level 4.1 -crf 21 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart /tmp/f.mp4
cp /tmp/f.mp4 随份子从哪儿来.mp4
