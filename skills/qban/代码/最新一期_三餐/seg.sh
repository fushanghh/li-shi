cd /workspace/work/meals
NF=6762; N=96; step=$(( (NF + N - 1) / N ))
S=$(date +%s)
while [ $(( $(date +%s) - S )) -lt 95 ]; do
 todo=(); for i in $(seq 0 $((N-1))); do [ -f c$i.done ] || todo+=($i); done
 [ ${#todo[@]} -eq 0 ] && break
 for i in "${todo[@]:0:2}"; do a=$((i*step)); b=$(((i+1)*step)); [ $b -gt $NF ] && b=$NF
  ( python3 render.py seg $a $b c$i.mp4 > c$i.log 2>&1 && touch c$i.done ) & done; wait
done
ls c*.done 2>/dev/null | wc -l
