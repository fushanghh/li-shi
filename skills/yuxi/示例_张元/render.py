import sys, json, subprocess, math
import scenes as S
from kit import *
from script import L
FPS = 30; GAP = 0.25; LEAD = 0.25
dur = json.load(open('dur.json'))
starts = []; t = LEAD
for d in dur: starts.append(t); t += d + GAP
TOTAL = t + 1.2
seg = []  # 场景边界
for i, x in enumerate(L):
    s0 = 0 if i == 0 else starts[i] - GAP * 0.5
    s1 = starts[i + 1] - GAP * 0.5 if i + 1 < len(L) else TOTAL
    seg.append((s0, s1))
# 计数器状态
def count_at(tt):
    n = 0; last = -99
    for i, x in enumerate(L):
        if x[3] is not None:
            hit = starts[i] + dur[i] * 0.8
            if tt >= hit: n = x[3]; last = hit
    return n, last

def frame(tt):
    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(sf)
    i = max(k for k in range(len(L)) if seg[k][0] <= tt)
    key, yr, small, cnt, sub = L[i]
    s0, s1 = seg[i]; d = s1 - s0; lt = tt - s0; p = cl(lt / d)
    z0, z1, fx, fy = S.CAM.get(key, (1.0, 1.08, 960, 540))
    z = lerp(z0, z1, ease(p))
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx + (fx - W / 2) * (1 - 1 / z) * 0 , -fy)
    c.translate((fx - W / 2) * 0 + (W / 2 - fx) * 0, 0)
    c.restore()
    # 焦点缩放：保持焦点在画面同一处
    c.save(); c.translate(fx, fy); c.scale(z, z); c.translate(-fx, -fy)
    S.CNT[0] = None
    getattr(S, 'S_' + key)(c, lt, d, p)
    c.restore()
    vignette(c, 0.7)
    if S.CNT[0] is not None: S.draw_cnt(c, S.CNT[0])
    # UI
    ta = ease(lt / 0.4) * (1 - ease((lt - d + 0.25) / 0.25)) if yr else 0
    tag(c, yr, small, ta)
    if key != 'title':
        center = key in ('count', 'stone', 'heart', 'end', 'gone')
        subs(c, sub, tt - starts[i], dur[i], center=center, y=(120 if not center else 260))
    n, last = count_at(tt)
    if n > 0 and key not in ('count', 'stone', 'heart', 'end'):
        counter(c, n, cl(1 - (tt - last) / 0.6) if tt - last < 0.6 else 0)
    # 场景开头淡入
    k = cl(lt / 0.18)
    if k < 1 and i > 0: c.set_source_rgba(0, 0, 0, 1 - k); c.paint()
    if tt > TOTAL - 0.8: c.set_source_rgba(0, 0, 0, cl((tt - TOTAL + 0.8) / 0.8)); c.paint()
    return sf

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for a in sys.argv[2:]:
            tt = float(a); frame(tt).write_to_png(f'st_{a}.png')
        sys.exit()
    part, nparts = int(sys.argv[1]), int(sys.argv[2])
    N = int(TOTAL * FPS); a = N * part // nparts; b = N * (part + 1) // nparts
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', f'part{part}.mp4'], stdin=subprocess.PIPE)
    for f in range(a, b):
        sf = frame(f / FPS); p.stdin.write(bytes(sf.get_data()))
    p.stdin.close(); p.wait(); open(f'part{part}.done', 'w').write('ok')
