cd /workspace/work/mingwall
NF=$(/usr/bin/python3 render.py info | head -1 | awk '{print $4}')
N=4
step=$(( (NF + N - 1) / N ))
rm -f list.txt
for i in $(seq 0 $((N-1))); do
  a=$((i*step)); b=$(((i+1)*step)); [ $b -gt $NF ] && b=$NF
  /usr/bin/python3 render.py seg $a $b p$i.mp4 > l$i.log 2>&1 &
  echo "file 'p$i.mp4'" >> list.txt
done
/usr/bin/python3 sfx.py > s.log 2>&1 &
wait
ffmpeg -y -v error -f concat -safe 0 -i list.txt -c copy out.mp4
O="南京明城墙：为什么不修成正方形.mp4"
ffmpeg -y -v error -i out.mp4 -i sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart /tmp/mux.mp4 && cp /tmp/mux.mp4 "$O"
ffprobe -v error -show_entries stream=codec_type:format=duration -of csv=p=0 "$O"
grep -h -i error l*.log s.log; echo END
