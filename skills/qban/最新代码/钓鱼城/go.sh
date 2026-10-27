cd /workspace/work/diaoyu_boyi
NF=$(python3 render.py info | awk '{print $4}'); N=$(( (NF + 299) / 300 ))
rm -f list.txt; for i in $(seq 0 $((N-1))); do echo "file 'c$i.mp4'" >> list.txt; done
ffmpeg -y -v error -f concat -safe 0 -i list.txt -c copy /tmp/dyb_out.mp4
ffmpeg -y -v error -i /tmp/dyb_out.mp4 -i sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ac 2 -ar 48000 -shortest \
  -metadata title="钓鱼城为什么守得住36年" -movflags +faststart /tmp/dyb_final.mp4 && cp /tmp/dyb_final.mp4 "钓鱼城为什么守得住36年.mp4"
ffprobe -v error -show_entries stream=codec_name,codec_type,width,height,channels,sample_rate:format=duration -of compact "钓鱼城为什么守得住36年.mp4"
