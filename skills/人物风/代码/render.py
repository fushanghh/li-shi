import sys, subprocess, math, random
import scenes as S
from kit import *
from script import L, durs, CLIMAX
FPS = 30; GAP = 0.25; LEAD = 0.25
dur = durs()
starts = []; t = LEAD
for i, d in enumerate(dur):
    starts.append(t); t += d + (0.08 if L[i][0] in CLIMAX else GAP)
TOTAL = t + 1.5
seg = []
for i, x in enumerate(L):
    s0 = 0 if i == 0 else starts[i] - GAP * 0.5
    s1 = starts[i + 1] - GAP * 0.5 if i + 1 < len(L) else TOTAL
    seg.append((s0, s1))

def scene_at(tt):
    return max(k for k in range(len(L)) if seg[k][0] <= tt)

def count_at(tt):
    n = 0; last = -99
    for i, x in enumerate(L):
        if x[3] is not None:
            hit = starts[i] + 0.3
            if tt >= hit: n = x[3]; last = hit
    return n, last

NOCNT = ('title', 'open', 'open2', 'open3', 'end', 'end2', 'letter2', 'tears', 'first', 'home', 'citizen')

def frame(tt):
    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(sf)
    i = scene_at(tt)
    key, yr, small, cnt, sub = L[i][:5]
    s0, s1 = seg[i]; d = s1 - s0; lt = tt - s0; p = cl(lt / d)
    z0, z1, fx, fy = S.CAM.get(key, (1.0, 1.08, 960, 540))
    z = lerp(z0, z1, ease(p))
    S.FX['shake'] = 0; S.FX['flash'] = 0; S.FX['white'] = 0
    # 先画场景到临时层以获取FX，再施加抖动
    c.save()
    c.translate(fx, fy); c.scale(z, z); c.translate(-fx, -fy)
    getattr(S, 'S_' + key)(c, lt, d, p)
    c.restore()
    sh = S.FX['shake']
    if sh > 0:
        # 重画一遍带抖动（简单可靠）
        rnd = random.Random(int(tt * 60))
        dx, dy = rnd.uniform(-1, 1) * 28 * sh, rnd.uniform(-1, 1) * 22 * sh
        c.save(); c.translate(dx, dy); c.translate(fx, fy); c.scale(z * (1 + 0.02 * sh), z * (1 + 0.02 * sh)); c.translate(-fx, -fy)
        getattr(S, 'S_' + key)(c, lt, d, p)
        c.restore()
    if S.FX['flash'] > 0: redflash(c, S.FX['flash'])
    vignette(c, 0.7)
    ta = ease(lt / 0.4) * (1 - ease((lt - d + 0.25) / 0.25)) if yr else 0
    tag(c, yr, small, ta)
    if key != 'title' and sub:
        subs(c, sub, tt - starts[i], dur[i], y=120)
    n, last = count_at(tt)
    if n is not None and last > 0 and key not in NOCNT:
        S.draw_cnt(c, n, cl(1 - (tt - last) / 0.6) if tt - last < 0.6 else 0)
    if S.FX['white'] > 0: c.set_source_rgba(1, 0.97, 0.9, S.FX['white']); c.paint()
    k = cl(lt / (0.10 if key in CLIMAX else 0.18))
    if k < 1 and i > 0: c.set_source_rgba(0, 0, 0, 1 - k); c.paint()
    if tt > TOTAL - 1.0: c.set_source_rgba(0, 0, 0, cl((tt - TOTAL + 1.0) / 1.0)); c.paint()
    return sf

if __name__ == '__main__':
    if sys.argv[1] == 'info':
        print('TOTAL', TOTAL)
        for i, x in enumerate(L): print(f"{starts[i]:7.2f} {dur[i]:5.2f} {x[0]}")
        sys.exit()
    if sys.argv[1] == 'still':
        for a in sys.argv[2:]:
            tt = float(a); frame(tt).write_to_png(f'st_{a}.png')
        sys.exit()
    if sys.argv[1] == 'mids':
        outs = []
        for i, x in enumerate(L):
            tt = starts[i] + dur[i] * 0.75; frame(tt).write_to_png(f'm_{i:02d}.png'); outs.append(f'm_{i:02d}.png')
        sys.exit()
    part, nparts = int(sys.argv[1]), int(sys.argv[2])
    N = int(TOTAL * FPS); a = N * part // nparts; b = N * (part + 1) // nparts
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', f'part{part}.mp4'], stdin=subprocess.PIPE)
    for f in range(a, b):
        sf = frame(f / FPS); p.stdin.write(bytes(sf.get_data()))
    p.stdin.close(); p.wait(); open(f'part{part}.done', 'w').write('ok')
