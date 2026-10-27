cd /workspace/work/maling_boyi
NF=$(python3 render.py info | awk '{print $4}'); CH=300; N=$(( (NF + CH - 1) / CH ))
for i in $(seq 0 $((N-1))); do [ -f c$i.done ] || echo $i; done | xargs -P 2 -I{} sh -c 'a=$(({}*'$CH')); b=$(({}*'$CH'+'$CH')); [ $b -gt '$NF' ] && b='$NF'; python3 render.py seg $a $b c{}.mp4 > c{}.log 2>&1 && touch c{}.done'
echo ALLDONE $(ls c*.done | wc -l) / $N >> render_loop.log
