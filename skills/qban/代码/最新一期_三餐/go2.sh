cd /workspace/work/meals
python3 -c "import cairocffi" 2>/dev/null || { pip install -q cairocffi pyshp scipy numpy pillow; mkdir -p ~/.fonts; cp /workspace/skills-assets/history-video/字体/*.otf ~/.fonts/; fc-cache -f; }
NF=$(python3 render.py info | head -1 | awk '{print $4}')
N=10
step=$(( (NF + N - 1) / N ))
rm -f list.txt
run() { i=$1; a=$((i*step)); b=$(((i+1)*step)); [ $b -gt $NF ] && b=$NF
  if [ ! -f c$i.done ]; then python3 render.py seg $a $b c$i.mp4 > c$i.log 2>&1 && touch c$i.done; fi; }
for i in $(seq 0 $((N-1))); do echo "file 'c$i.mp4'" >> list.txt; done
for i in 0 2 4 6 8; do run $i & run $((i+1)) & wait; done
[ -f sfx.wav ] || python3 sfx.py > s.log 2>&1
ls c*.done | wc -l
ffmpeg -y -v error -f concat -safe 0 -i list.txt -c copy out.mp4
O="古人一天吃几顿_一日三餐的由来.mp4"
ffmpeg -y -v error -i out.mp4 -i sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart /tmp/mux.mp4 && cp /tmp/mux.mp4 "$O"
ffprobe -v error -show_entries stream=codec_type:format=duration -of csv=p=0 "$O"
echo END
