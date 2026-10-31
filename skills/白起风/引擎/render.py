import sys, subprocess, math, random
import numpy as np
import scenes as S
from kit import *
from script import L, BP, T0, END_BEAT, TAIL
FPS = 30
QUIET = [(0, 16), (79, 96), (216, 219), (249, 251), (262, 300)]
def Tb(k): return 0.0 if k == 0 else T0 + k * BP
starts = [Tb(x[0]) for x in L]
TOTAL = Tb(END_BEAT) + TAIL
seg = [(starts[i], starts[i + 1] if i + 1 < len(L) else TOTAL) for i in range(len(L))]

def is_quiet(k): return any(a <= k < b for a, b in QUIET)

def count_at(tt):
    n = 0; last = -99
    for i, x in enumerate(L):
        if x[4] is not None:
            hit = Tb(x[0] + (3 if x[1] == 'bury' else 2))
            if tt >= hit: n = x[4]; last = hit
    return n, last

def counter(c, n, flash):
    text(c, "史书记载 · 白起斩首", 96, 950, 28, (0.80, 0.74, 0.66), 1, shadow=False)
    sc = 1 + 0.45 * flash
    c.save(); c.translate(96, 1040); c.scale(sc, sc)
    w = text(c, str(n), 0, 0, 84, mix((0.95, 0.30, 0.24), (1, 0.95, 0.8), flash), 1)
    text(c, "万", w + 10, -4, 40, (0.9, 0.85, 0.78), 1, shadow=False)
    c.restore()
    if flash > 0: glow(c, 150, 1010, 220, RED, 0.45 * flash)

CENTER_Y = ''
def subs(c, s, lt, center=False):
    lines = s.split('|'); speed = 28.0
    n = max(len(parse(l)) for l in lines)
    size = int(max(62, min(100, 1150 / max(n, 1))))
    y = (130 if not center else (330 if CENTER_Y == 'end' else 470)) + (size - 60) * 0.6
    k = 0
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    for li, line in enumerate(lines):
        chars = parse(line)
        tw = sum(c.text_extents(ch)[4] for ch, _ in chars)
        xx = W / 2 - tw / 2 if center else 96
        yy = y + li * size * 1.32
        for ch, m in chars:
            ap = cl((lt - k / speed) / 0.10)
            if ap > 0:
                col = (1, 0.97, 0.92) if m is None else ((0.98, 0.28, 0.22) if m == 'r' else GOLD)
                pop = 1 + 0.5 * (1 - eout(ap)) if m else 1 + 0.25 * (1 - eout(ap))
                cw = c.text_extents(ch)[4]
                c.save(); c.translate(xx + cw / 2, yy - size * 0.35); c.scale(pop, pop); c.translate(-(xx + cw / 2), -(yy - size * 0.35))
                if m == 'r':
                    c.set_source_rgba(0.9, 0.1, 0.05, 0.35 * ap); c.move_to(xx - 2, yy + 2); c.show_text(ch); c.move_to(xx + 4, yy - 1); c.show_text(ch)
                c.set_source_rgba(0, 0, 0, 0.55 * ap); c.move_to(xx + 2, yy + 3); c.show_text(ch)
                c.set_source_rgba(*col, ap); c.move_to(xx, yy); c.show_text(ch)
                c.restore()
            xx += c.text_extents(ch)[4]; k += 1

def tagui(c, yr, small, a):
    if not yr or a <= 0: return
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(42)
    w = c.text_extents(yr)[4]
    c.set_source_rgba(*RED, 0.9 * a); c.rectangle(W - 96 - w - 52, 108, 36, 3); c.fill()
    text(c, yr, W - 96, 124, 42, (0.95, 0.92, 0.85), a, 'r')
    if small: text(c, small, W - 96, 172, 30, (0.75, 0.70, 0.62), a * 0.9, 'r', shadow=False)

def glitch(sf, amt, seed):
    if amt <= 0: return
    sf.flush()
    a = np.ndarray((H, W, 4), np.uint8, sf.get_data())
    d = int(18 * amt) + 2
    r = a[..., 2].copy(); b = a[..., 0].copy()
    a[..., 2] = np.roll(r, d, axis=1); a[..., 0] = np.roll(b, -d, axis=1)
    rnd = random.Random(seed)
    for _ in range(int(6 * amt) + 1):
        y0 = rnd.randint(0, H - 60); h = rnd.randint(8, 60); sh = rnd.randint(-80, 80)
        a[y0:y0 + h] = np.roll(a[y0:y0 + h], int(sh * amt), axis=1)
    sf.mark_dirty()

def frame(tt):
    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(sf)
    i = max(k for k in range(len(L)) if seg[k][0] <= tt)
    b0, key, yr, small, cnt, sub, fx = L[i]
    s0, s1 = seg[i]; d = s1 - s0; lt = tt - s0; p = cl(lt / d)
    kb = (tt - T0) / BP; kbi = math.floor(kb); dtb = (kb - kbi) * BP
    quiet = is_quiet(kbi) or tt < T0
    # 节拍推镜
    pulse = 0
    if not quiet:
        pulse = (0.035 if kbi % 4 == 0 else 0.012) * math.exp(-dtb * 14)
    z0, z1, fxp, fyp = S.CAM.get(key, (1.0, 1.07, 960, 540))
    z = lerp(z0, z1, ease(p)) + pulse
    if fx in ('slam', 'drop', 'kill'): z += 0.18 * (1 - eout(lt / 0.28))
    # 震屏
    sh = 0
    if fx in ('kill', 'drop'): sh = 22 * math.exp(-lt * 7)
    if key == 'bury' and lt > BP * 3: sh = 30 * math.exp(-(lt - BP * 3) * 6)
    if not quiet and kbi % 8 == 0: sh = max(sh, 6 * math.exp(-dtb * 18))
    ox = math.sin(tt * 91) * sh; oy = math.cos(tt * 77) * sh
    c.save(); c.translate(fxp + ox, fyp + oy); c.scale(z, z); c.translate(-fxp, -fyp)
    getattr(S, 'S_' + key)(c, lt, d, p)
    c.restore()
    vignette(c, 0.72)
    # 字幕 / 标签
    ta = ease(lt / 0.3) * (1 - ease((lt - d + 0.2) / 0.2)) if yr else 0
    tagui(c, yr, small, ta)
    if sub:
        st = lt if key != 'bury' else lt - BP * 3
        global CENTER_Y; CENTER_Y = key
        if st >= 0: subs(c, sub, st, center=(key in ('end', 'fear')))
    n, last = count_at(tt)
    if n > 0 and key not in ('title', 'end', 'hook', 'hook2'):
        counter(c, n, cl(1 - (tt - last) / 0.5) if tt - last < 0.5 else 0)
    # 闪白/红闪
    fl = 0
    if fx == 'drop': c.set_source_rgba(1, 1, 1, 0.85 * math.exp(-lt * 8)); c.paint()
    if fx == 'slam': c.set_source_rgba(1, 0.95, 0.9, 0.35 * math.exp(-lt * 14)); c.paint()
    if fx == 'kill': redflash(c, math.exp(-lt * 4) * 1.6)
    if n and 0 <= tt - last < 0.5: redflash(c, (1 - (tt - last) / 0.5) * 1.2)
    if key == 'bury' and lt > BP * 3: redflash(c, math.exp(-(lt - BP * 3) * 3) * 1.8)
    # 切镜淡入（很短）
    k = cl(lt / 0.06)
    if k < 1 and i > 0: c.set_source_rgba(0, 0, 0, 1 - k); c.paint()
    if tt > TOTAL - 1.0: c.set_source_rgba(0, 0, 0, cl((tt - TOTAL + 1.0) / 1.0)); c.paint()
    # 故障效果：glitch 镜头开头 + 每 16 拍乐句头
    g = 0
    if fx in ('glitch', 'drop'): g = max(g, 1 - lt / 0.22)
    if not quiet and kbi % 16 == 0 and dtb < 0.12: g = max(g, 0.8)
    if fx == 'kill': g = max(g, 0.6 * (1 - lt / 0.15))
    if g > 0: glitch(sf, cl(g), int(tt * 30))
    return sf

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for a in sys.argv[2:]:
            frame(float(a)).write_to_png(f'st_{a}.png')
        sys.exit()
    if sys.argv[1] == 'sheet':
        from PIL import Image
        ims = []
        for i in range(len(L)):
            tt = seg[i][0] + (seg[i][1] - seg[i][0]) * 0.7
            sf = frame(tt); sf.write_to_png('/tmp/_s.png'); ims.append(Image.open('/tmp/_s.png').convert('RGB').resize((480, 270)))
        cols = 6; rows = (len(ims) + cols - 1) // cols
        o = Image.new('RGB', (480 * cols, 270 * rows))
        for j, im in enumerate(ims): o.paste(im, ((j % cols) * 480, (j // cols) * 270))
        o.save('sheet.jpg', quality=85); sys.exit()
    part, nparts = int(sys.argv[1]), int(sys.argv[2])
    N = int(TOTAL * FPS); a = N * part // nparts; b = N * (part + 1) // nparts
    pr = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', f'part{part}.mp4'], stdin=subprocess.PIPE)
    for f in range(a, b):
        sf = frame(f / FPS); pr.stdin.write(bytes(sf.get_data()))
    pr.stdin.close(); pr.wait(); open(f'part{part}.done', 'w').write('ok')
