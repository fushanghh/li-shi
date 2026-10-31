import sys, subprocess, math, random
import numpy as np
import scenes as S
from kit import *
from script import L, BP, T0, END_BEAT, TAIL
FPS = 30
MAPNUM = ('hook', 'march', 'huayang', 'siege')   # 这些镜头左上自带大数字
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

YEAR = {}
def counter(c, n, flash):
    text(c, "史书记载 · 白起斩首", 96, 150, 28, (0.85, 0.75, 0.55), 1, shadow=False)
    sc = 1 + 0.45 * flash
    c.save(); c.translate(96, 250); c.scale(sc, sc)
    w = text(c, str(n), 0, 0, 100, mix(GOLD, (1, 0.95, 0.8), flash), 1)
    text(c, "万", (w or 120) + 10, -6, 44, (0.9, 0.85, 0.78), 1, shadow=False)
    c.restore()
    if flash > 0: glow(c, 170, 220, 240, RED, 0.45 * flash)

def progbar(c, k, a):
    x0, x1, y = 96, 420, 70
    c.set_source_rgba(0.85, 0.75, 0.55, 0.45 * a); c.set_line_width(2); c.move_to(x0, y); c.line_to(x1, y); c.stroke()
    c.set_source_rgba(*RED, a); c.set_line_width(4); c.move_to(x0, y); c.line_to(lerp(x0, x1, k), y); c.stroke()
    glow(c, lerp(x0, x1, k), y, 22, RED, 0.8 * a)
    text(c, "前294", x0, y + 32, 22, (0.75, 0.68, 0.55), a, shadow=False)
    text(c, "前257", x1, y + 32, 22, (0.75, 0.68, 0.55), a, 'r', shadow=False)

def subs(c, s, lt, center=False, src=None):
    s = s.replace('|', '，').replace('，，', '，').replace('。，', '。').replace('：，', '：')
    chars = parse(s); speed = 28.0
    size = 58 if len(chars) <= 22 else int(max(44, 1300 / len(chars)))
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    tw = sum(c.text_extents(ch)[4] for ch, _ in chars)
    yy = 960 if not center else 930
    # 底部暗带
    if not center:
        g = cairo.LinearGradient(0, 820, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.75)
        c.set_source(g); c.rectangle(0, 820, W, H - 820); c.fill()
    xx = W / 2 - tw / 2; k = 0
    for ch, m in chars:
        ap = cl((lt - k / speed) / 0.10)
        if ap > 0:
            col = (0.98, 0.94, 0.86) if m is None else ((0.98, 0.32, 0.24) if m == 'r' else GOLD)
            pop = 1 + 0.5 * (1 - eout(ap)) if m else 1 + 0.2 * (1 - eout(ap))
            cw = c.text_extents(ch)[4]
            c.save(); c.translate(xx + cw / 2, yy - size * 0.35); c.scale(pop, pop); c.translate(-(xx + cw / 2), -(yy - size * 0.35))
            c.set_source_rgba(0, 0, 0, 0.7 * ap); c.move_to(xx + 2, yy + 3); c.show_text(ch)
            c.set_source_rgba(*col, ap); c.move_to(xx, yy); c.show_text(ch)
            c.restore()
        xx += c.text_extents(ch)[4]; k += 1
    if src and not center:
        text(c, src, W / 2, yy + 52, 28, (0.70, 0.64, 0.55), cl(lt / 0.4), 'c', shadow=False)

def tagui(c, yr, small, a):
    if not yr or a <= 0: return
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(38)
    w = c.text_extents(yr)[4]
    c.set_source_rgba(*RED, 0.95 * a); c.rectangle(W - 96 - w - 26, 58, 5, 50); c.fill()
    text(c, yr, W - 96, 98, 38, (0.95, 0.90, 0.80), a, 'r')

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
    vignette(c, 0.62)
    # 字幕 / 标签
    ta = ease(lt / 0.3) * (1 - ease((lt - d + 0.2) / 0.2)) if yr else 0
    tagui(c, yr, small, ta)
    if sub:
        st = lt if key != 'bury' else lt - BP * 3
        global CENTER_Y; CENTER_Y = key
        if st >= 0: subs(c, sub, st, center=(key in ('end',)), src=small)
    if key not in ('title', 'end', 'hook', 'hook2', 'bury') or (key == 'bury' and lt > BP * 3):
        progbar(c, cl((tt - starts[3]) / (starts[-1] - starts[3])), 0.9)
    n, last = count_at(tt)
    if n > 0 and key not in ('title', 'end', 'hook', 'hook2', 'hook_') and key not in MAPNUM:
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
