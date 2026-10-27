cd "$(dirname "$0")"
rm -f part*.done
for i in 0 1 2 3; do python3 render.py $i 4 > log$i.txt 2>&1 & done
wait
printf "file part0.mp4\nfile part1.mp4\nfile part2.mp4\nfile part3.mp4\n" > list.txt
ffmpeg -y -v error -f concat -i list.txt -c copy out.mp4
