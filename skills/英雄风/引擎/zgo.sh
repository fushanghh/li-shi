cd "$(dirname "$0")"
rm -f part*.done
python3 zrender.py 0 2 > log0.txt 2>&1 &
python3 zrender.py 1 2 > log1.txt 2>&1 &
wait
printf "file part0.mp4\nfile part1.mp4\n" > list.txt
ffmpeg -y -v error -f concat -i list.txt -c copy silent.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 silent.mp4)
ST=$(python3 -c "print($D-2)")
ffmpeg -y -v error -i silent.mp4 -i bgm_ext.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 44100 -af "afade=t=out:st=$ST:d=2" -t $D -movflags +faststart /tmp/zzt.mp4 && cp /tmp/zzt.mp4 ../左宗棠_收复新疆_战争风燃剪.mp4
echo done > ALL.done
