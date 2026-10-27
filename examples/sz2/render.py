import sys, json, subprocess, math
import scenes as S
from kit import *
from pov import eyelids
from script import L, FAST
FPS = 30; GAP = 0.25; LEAD = 0.25
dur = json.load(open('dur.json'))
starts = []; t = LEAD
for d in dur: starts.append(t); t += d + GAP
TOTAL = t + 1.2
seg = []
for i, x in enumerate(L):
    s0 = 0 if i == 0 else starts[i] - GAP * 0.5
    s1 = starts[i + 1] - GAP * 0.5 if i + 1 < len(L) else TOTAL
    seg.append((s0, s1))
CENTER = ('count', 'gold', 'end', 'zero')
BLINK = ('flag', 'huizhou', 'yang', 'lin', 'nanjing')
NOCNT = ('t1', 'o2', 'o3', 't3')
HB = {'hook2': 1.0, 'leak': 1.0, 'back': 0.8, 'caught': 1.0, 'london': 1.0, 'cell': 0.8, 'note': 0.5, 'shot': 0.6}
SHAKE = {'leak': 5, 'back': 4, 'london': 6, 'charge': 12, 'wuchang': 8, 'shot': 3, 'caught': 4}

def heartbeat(c, tt, k):
    ph = (tt * 1.15) % 1.0
    v = math.exp(-((ph - 0.0) / 0.06) ** 2) + 0.7 * math.exp(-((ph - 0.22) / 0.06) ** 2) + math.exp(-((ph - 1.0) / 0.06) ** 2)
    g = cairo.RadialGradient(W / 2, H / 2, 380, W / 2, H / 2, 1100)
    g.add_color_stop_rgba(0, 0.5, 0.0, 0.0, 0); g.add_color_stop_rgba(1, 0.55, 0.02, 0.0, 0.55 * v * k)
    c.set_source(g); c.paint()

def counter_age(c, n, flash, a=1):
    c.set_source_rgba(0, 0, 0, 0.45 * a); rr(c, 70, 952, 470, 112, 14); c.fill()
    w = text(c, "先倒下的人", 96, 1036, 44, (0.85, 0.80, 0.72), a)
    sc = 1 + 0.3 * flash
    c.save(); c.translate(96 + w + 22, 1040); c.scale(sc, sc)
    w2 = text(c, str(n), 0, 0, 84, mix((0.95, 0.30, 0.24), (1, 0.9, 0.7), flash), a)
    text(c, "人", w2 + 10, -4, 44, (0.9, 0.85, 0.78), a)
    c.restore()
    if flash > 0: glow(c, 380, 1010, 180, RED, 0.3 * flash * a)

def sub_box(c, s, center, fast=False):
    lines = s.split('|')
    n = max(len(parse(l)) for l in lines)
    size = int(max(84 if fast else 60, min(110 if fast else 96, 1150 / max(n, 1))))
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    wmax = max(sum(c.text_extents(ch)[4] for ch, _ in parse(l)) for l in lines)
    y = 120 + (size - 60) * 0.6
    return 96 + wmax, y + (len(lines) - 1) * size * 1.35

def tag2(c, yr, small, a, box):
    if not yr and not small: return
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(42)
    w = c.text_extents(yr)[4]
    c.set_font_size(30); sw = c.text_extents(small)[4] if small else 0
    y0 = 124
    if box and W - 96 - max(w + 52, sw) < box[0] + 40: y0 = box[1] + 70
    c.set_source_rgba(*RED, 0.9 * a); c.rectangle(W - 96 - w - 52, y0 - 16, 36, 3); c.fill()
    text(c, yr, W - 96, y0, 42, (0.95, 0.92, 0.85), a, 'r')
    if small:
        text(c, small, W - 96, y0 + 48, 30, (0.75, 0.70, 0.62), a * 0.9, 'r', shadow=False)

def frame(tt):
    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(sf)
    i = max(k for k in range(len(L)) if seg[k][0] <= tt)
    key, yr, small, cnt, sub = L[i]
    s0, s1 = seg[i]; d = s1 - s0; lt = tt - s0; p = cl(lt / d)
    z0, z1, fx, fy = S.CAM.get(key, (1.0, 1.06, 960, 540))
    z = lerp(z0, z1, ease(p)) * 1.025
    # 呼吸式轻晃（POV）
    sh = SHAKE.get(key, 0)
    bx = 5 * math.sin(tt * 0.9) + 2 * math.sin(tt * 2.3) + sh * (math.sin(tt * 13.1) + 0.6 * math.sin(tt * 23.7))
    by = 4 * math.sin(tt * 1.25 + 1) + sh * (math.sin(tt * 11.3 + 2) + 0.6 * math.sin(tt * 19.1))
    c.save(); c.translate(fx + bx, fy + by); c.scale(z, z); c.translate(-fx, -fy)
    getattr(S, 'S_' + key)(c, lt, d, p)
    c.restore()
    vignette(c, 0.72)
    if key in HB: heartbeat(c, tt, HB[key])
    S.post(c, key, lt, d, p)
    center = key in CENTER
    ta = ease(lt / 0.4) * (1 - ease((lt - d + 0.25) / 0.25))
    if key != 'title':
        box = sub_box(c, sub, center, key in FAST) if not center else None
        tag2(c, yr, small, ta, box)
        fast = key in FAST
        subs(c, sub, tt - starts[i], dur[i], center=center, y=(120 if not center else 300), speed=(26 if fast else 15), smin=(84 if fast else 60), smax=(110 if fast else 96))
    if cnt is not None and key not in NOCNT:
        prev = L[i - 1][3] if i > 0 else None
        prev = prev if isinstance(prev, int) else cnt
        k = S.CNT_AT.get(key, 0.2)
        if prev != cnt:
            q = cl((lt - k) / (1.6 if cnt - prev > 5 else 0.01))
            shown = int(round(lerp(prev, cnt, ease(q)))) if lt > k else prev
            fl = cl(1 - (lt - k - (1.6 if cnt - prev > 5 else 0)) / 0.6) if lt > k else 0
        else: shown, fl = cnt, 0
        counter_age(c, shown, fl)
    # 转场：眨眼或淡入
    if i > 0:
        if key in BLINK:
            eyelids(c, cl((lt - 0.05) / 0.4))
        else:
            k = cl(lt / 0.18)
            if k < 1: c.set_source_rgba(0, 0, 0, 1 - k); c.paint()
    if i + 1 < len(L) and L[i + 1][0] in BLINK:
        rem = d - lt
        if rem < 0.22: eyelids(c, rem / 0.22)
    if tt > TOTAL - 0.8: c.set_source_rgba(0, 0, 0, cl((tt - TOTAL + 0.8) / 0.8)); c.paint()
    return sf

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for a in sys.argv[2:]:
            tt = float(a); frame(tt).write_to_png(f'st_{a}.png')
        sys.exit()
    if sys.argv[1] == 'info':
        print(TOTAL); [print(i, L[i][0], round(starts[i], 2), dur[i]) for i in range(len(L))]; sys.exit()
    part, nparts = int(sys.argv[1]), int(sys.argv[2])
    N = int(TOTAL * FPS); a = N * part // nparts; b = N * (part + 1) // nparts
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', f'part{part}.mp4'], stdin=subprocess.PIPE)
    for f in range(a, b):
        sf = frame(f / FPS); p.stdin.write(bytes(sf.get_data()))
    p.stdin.close(); p.wait(); open(f'part{part}.done', 'w').write('ok')
