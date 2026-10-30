cd "$(dirname "$0")"
rm -f part*.done part*.mp4
NP=2
for i in $(seq 0 $((NP-1))); do python3 render.py $i $NP > log$i.txt 2>&1 & done
python3 sfx.py > logsfx.txt 2>&1
wait
: > list.txt; for i in $(seq 0 $((NP-1))); do echo "file part$i.mp4" >> list.txt; done
ffmpeg -y -v error -f concat -i list.txt -c copy video.mp4
ffmpeg -y -v error -i video.mp4 -i sfx.wav -c:v copy -c:a aac -b:a 160k -shortest 杨振宁_玉溪风.mp4
echo done
