cd "$(dirname "$0")"
rm -f part*.done
N=${N:-4}
for i in $(seq 0 $((N-1))); do python3 render.py $i $N > log$i.txt 2>&1 & done
wait
: > list.txt; for i in $(seq 0 $((N-1))); do echo "file part$i.mp4" >> list.txt; done
ffmpeg -y -v error -f concat -i list.txt -c copy silent.mp4
ffmpeg -y -v error -i silent.mp4 -i bgm_ext.wav -map 0:v -map 1:a -c:v libx264 -profile:v high -level 4.1 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 44100 -af "afade=t=out:st=113.6:d=2" -shortest -movflags +faststart /tmp/bq_war.mp4 && cp /tmp/bq_war.mp4 白起的一生_战争风.mp4
echo done > ALL.done
