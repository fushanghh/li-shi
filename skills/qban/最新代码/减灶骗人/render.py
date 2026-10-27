import sys, os, subprocess, time
from scenes import *
import core

STARTS = []; acc = 0.0
for s in SCENES:
    STARTS.append(acc); acc += s['D']
TOTAL = acc; NF = int(round(TOTAL * FPS))
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); C = cairo.Context(surf)


def render(T):
    i = 0
    while i + 1 < len(SCENES) and T >= STARTS[i + 1]: i += 1
    t = T - STARTS[i]; sc = SCENES[i]
    C.identity_matrix(); C.set_source_rgb(0, 0, 0); C.paint()
    C.save(); sc['fn'](C, t); C.restore(); C.identity_matrix()
    footer(C, sc['src'], fin(t, 0.4))
    if i > 0 and t < 0.15:
        C.set_source_rgba(0, 0, 0, 0.55 * (1 - t / 0.15)); C.paint()
    if T > TOTAL - 0.8:
        C.set_source_rgba(0, 0, 0, clamp((T - (TOTAL - 0.8)) / 0.8)); C.paint()
    surf.flush()
    return i, t


def still(ts, d='stills'):
    os.makedirs(d, exist_ok=True)
    for T in ts:
        i, t = render(T); surf.write_to_png('%s/s%02d_%05.1f.png' % (d, i + 1, T))


def segment(f0, f1, out):
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-threads', '1', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); t0 = time.time()
    for f in range(f0, f1):
        render(f / FPS); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close(); p.wait(); print('DONE', out, '%.0fs' % (time.time() - t0), flush=True)


def events():
    core.REC[0] = True
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 64, 36); cc = cairo.Context(sf)
    out = []
    for i, (sc, st) in enumerate(zip(SCENES, STARTS)):
        core.EVENTS.clear()
        sc['fn'](cc, sc['D'] - 0.01)
        seen = set()
        out.append((st, 'cut'))
        for t0, k in core.EVENTS:
            if 0 <= t0 < sc['D'] and (round(t0, 2), k) not in seen:
                seen.add((round(t0, 2), k)); out.append((st + t0, k))
    core.REC[0] = False
    return sorted(out)


if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'info':
        print('TOTAL', TOTAL, 'NF', NF, 'shots', len(SCENES))
    elif m == 'still':
        still([float(x) for x in sys.argv[2:]])
    elif m == 'mid':
        idx = [int(x) for x in sys.argv[2:]] or range(len(SCENES))
        still([STARTS[k] + SCENES[k]['D'] * 0.85 for k in idx])
    elif m == 'seg':
        segment(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    elif m == 'ev':
        for e in events(): print('%.2f %s' % e)
