import sys, math
import cairocffi as cairo
import numpy as np
from frame import *
import scenes1
import scenes2, scenes3
from scenes1 import _CAM

STARTS = []; acc = 0.0
for s in SHOTS: STARTS.append(acc); acc += s.dur
TOTAL = acc
EVENTS = sorted([(st + b * B, k) for s, st in zip(SHOTS, STARTS) for b, k in s.ev])
SHAKE_K = {'stamp': 26, 'land': 30, 'boom': 10, 'crash': 24, 'title': 8, 'hit': 9, 'thunder': 6, 'bigimpact': 40}
SHAKES = [(t, SHAKE_K[k]) for t, k in EVENTS if k in SHAKE_K]
FLASHES = [t for t, k in EVENTS if k == 'flash']
CAPS = []
for s, st in zip(SHOTS, STARTS):
    for c in s.caps: CAPS.append((st + c[0] * B,) + tuple(c[1:]))
CAPS.sort(key=lambda c: c[0])
TR = 0.55  # 横移转场时长

def shot_at(tg):
    i = max(j for j, st in enumerate(STARTS) if tg >= st - 1e-9)
    return i, tg - STARTS[i]

def draw_shot(p, g, i, t, dx=0.0):
    s = SHOTS[i]
    cam = s.cam(t)
    zpunch = 0
    for c in (p.c, g.c):
        c.save(); c.rectangle(max(0, dx), STAGE_T, W - abs(dx), SH); c.clip(); c.translate(dx, 0)
    # 镜头
    tg = STARTS[i] + t
    sx = sy = 0
    for ts, amp in SHAKES:
        if 0 <= tg - ts < 0.3:
            k = 1 - (tg - ts) / 0.3; sx += math.sin(tg * 97) * amp * k; sy += math.cos(tg * 83) * amp * k
    z = cam[2]
    for c in (p.c, g.c):
        c.save(); c.translate(SCX + sx, SCY + sy); c.scale(z, z); c.translate(-cam[0], -cam[1])
    _CAM['cur'] = cam
    s.fn(p, g, t)
    for c in (p.c, g.c): c.restore()
    if getattr(s, 'ov', None): s.ov(p, g, t)
    for c in (p.c, g.c): c.restore()

def render(tg):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); gs = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(surf); gc = cairo.Context(gs)
    for cc in (c, gc): cc.set_line_cap(cairo.LINE_CAP_ROUND); cc.set_line_join(cairo.LINE_JOIN_ROUND)
    p = P(c, gc); g = p.g
    i, t = shot_at(tg)
    s = SHOTS[i]
    if i > 0 and s.trans == 'slide' and t < TR:
        k = eio(t / TR)
        draw_shot(p, g, i - 1, SHOTS[i - 1].dur + t, -W * k)
        draw_shot(p, g, i, t, W * (1 - k))
        x = W * (1 - k)
        p.rect(x - 6, STAGE_T, 12, SH, 'BLK'); p.line([(x - 9, STAGE_T), (x - 9, STAGE_B)], 'LN', 2); p.line([(x + 9, STAGE_T), (x + 9, STAGE_B)], 'LN', 2)
    elif i > 0 and s.trans == 'dissolve' and t < 0.5:
        draw_shot(p, g, i - 1, SHOTS[i - 1].dur + t)
        c.push_group(); gc.push_group()
        draw_shot(p, g, i, t)
        c.pop_group_to_source(); c.paint_with_alpha(t / 0.5); gc.pop_group_to_source(); gc.paint_with_alpha(t / 0.5)
    else:
        draw_shot(p, g, i, t)
    fl = 0.0
    for ft in FLASHES:
        if 0 <= tg - ft < 0.35: fl = max(fl, (1 - (tg - ft) / 0.35) ** 2 * 0.85)
    if s.trans == 'flash' and t < 0.3: fl = max(fl, 1 - t / 0.3)
    # 字幕
    cap = None
    for cp in CAPS:
        if tg >= cp[0]: cap = cp
    tint = getattr(s, 'tint', None)
    arr = composite(surf, gs, fl, tint)
    out = cairo.ImageSurface.create_for_data(memoryview(bytearray(arr.tobytes())), cairo.FORMAT_ARGB32, W, H)
    c2 = cairo.Context(out); p2 = P(c2)
    capd = None
    if cap: capd = (cap[0], cap[1], cap[2], cap[3], cap[4])
    chrome(p2, capd, tg)
    out.flush()
    return out

if __name__ == '__main__':
    import subprocess
    part, nparts = int(sys.argv[1]), int(sys.argv[2])
    nf = int(TOTAL * FPS); a = nf * part // nparts; b = nf * (part + 1) // nparts
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', f'part{part}.mp4'], stdin=subprocess.PIPE)
    for fi in range(a, b):
        s = render(fi / FPS); ff.stdin.write(bytes(s.get_data()))
        if fi % 150 == 0: print(part, fi, b, flush=True)
    ff.stdin.close(); ff.wait(); print('done', part)
