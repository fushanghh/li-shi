import sys, subprocess, math, random, re
import numpy as np
import cairocffi as cairo
import zscenes as S
from kit import W, H, FONT, text, glow, GOLD, RED, ease, eout, cl, lerp, mix, vignette, redflash
from zscript import L, BP, T0, END_BEAT, TAIL, QUIET
FPS = 30
def Tb(k): return 0.0 if k == 0 else T0 + k * BP
starts = [Tb(x[0]) for x in L]
TOTAL = Tb(END_BEAT) + TAIL
seg = [(starts[i], starts[i + 1] if i + 1 < len(L) else TOTAL) for i in range(len(L))]
def is_quiet(k): return any(a <= k < b for a, b in QUIET)

def title_block(c, s, sub, lt, d):
    if not s and not sub: return
    a_out = 1 - ease((lt - d + 0.12) / 0.12)
    if s:
        n = len(s); size = 100 if n <= 6 else max(64, int(1300 / n))
        c.select_font_face(S.BRUSH, 0, 0); c.set_font_size(size)
        ws = [c.text_extents(ch)[4] for ch in s]; sp = size * 0.12; tw = sum(ws) + sp * (n - 1)
        g = cairo.LinearGradient(0, 0, 0, 330); g.add_color_stop_rgba(0, 0, 0, 0, 0.55); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        c.set_source(g); c.rectangle(0, 0, W, 330); c.fill()
        xx = W / 2 - tw / 2
        for i, (ch, w) in enumerate(zip(s, ws)):
            k = cl((lt - i * 0.045) / 0.16) * a_out
            if k > 0:
                dy = 30 * (1 - eout(k)); sc = 1 + 0.6 * (1 - eout(k))
                c.save(); c.translate(xx + w / 2, 170 - size * 0.35 + dy); c.scale(sc, sc); c.translate(-(xx + w / 2), -(170 - size * 0.35))
                c.set_source_rgba(0, 0, 0, 0.6 * k); c.move_to(xx + 3, 174); c.show_text(ch)
                col = (1, 0.95, 0.86)
                c.set_source_rgba(*col, k); c.move_to(xx, 170); c.show_text(ch); c.restore()
            xx += w + sp
        uk = eout((lt - 0.25) / 0.3) * a_out
        if uk > 0: c.set_source_rgba(*RED, 0.9 * uk); c.rectangle(W / 2 - tw / 2 * uk, 196, tw * uk, 5); c.fill()
    if sub:
        k = ease((lt - 0.3) / 0.25) * a_out
        size = 38 if len(sub) <= 22 else max(28, int(1500 / len(sub)))
        text(c, sub, W / 2, 262 if s else 170, size, (0.96, 0.90, 0.78), k, 'c')

def src_line(c, src, lt, d):
    if not src: return
    k = ease((lt - 0.4) / 0.3) * (1 - ease((lt - d + 0.12) / 0.12))
    text(c, src, W / 2, H - 50, 26, (0.78, 0.70, 0.58), k, 'c', shadow=False)

def tagui(c, yr, a):
    if not yr or a <= 0: return
    c.select_font_face(FONT, 0, 1); c.set_font_size(30)
    w = c.text_extents(yr)[4]
    c.set_source_rgba(*RED, 0.95 * a); c.rectangle(W - 70 - w - 22, 46, 5, 40); c.fill()
    text(c, yr, W - 70, 78, 30, (0.95, 0.90, 0.80), a, 'r')

YR0, YR1 = 1812, 1885
def year_of(yr):
    m = re.search(r'(\d{4})', yr or ''); return int(m.group(1)) if m else None
def progbar(c, f, a):
    x0, x1, y = 70, 420, 60
    c.set_source_rgba(0.85, 0.75, 0.55, 0.45 * a); c.set_line_width(2); c.move_to(x0, y); c.line_to(x1, y); c.stroke()
    c.set_source_rgba(*RED, a); c.set_line_width(4); c.move_to(x0, y); c.line_to(lerp(x0, x1, f), y); c.stroke()
    glow(c, lerp(x0, x1, f), y, 22, RED, 0.8 * a)
    text(c, str(YR0), x0, y + 30, 20, (0.75, 0.68, 0.55), a, shadow=False)
    text(c, str(YR1), x1, y + 30, 20, (0.75, 0.68, 0.55), a, 'r', shadow=False)

def glitch(sf, amt, seed):
    if amt <= 0: return
    sf.flush(); a = np.ndarray((H, W, 4), np.uint8, sf.get_data())
    d = int(18 * amt) + 2
    r = a[..., 2].copy(); b = a[..., 0].copy()
    a[..., 2] = np.roll(r, d, axis=1); a[..., 0] = np.roll(b, -d, axis=1)
    rnd = random.Random(seed)
    for _ in range(int(6 * amt) + 1):
        y0 = rnd.randint(0, H - 60); h = rnd.randint(8, 60); sh = rnd.randint(-80, 80)
        a[y0:y0 + h] = np.roll(a[y0:y0 + h], int(sh * amt), axis=1)
    sf.mark_dirty()

LASTF = [0.0]
def frame(tt):
    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(sf)
    i = max(k for k in range(len(L)) if seg[k][0] <= tt)
    b0, key, kw, ttl, sub, src, yr, fx = L[i]
    s0, s1 = seg[i]; d = s1 - s0; lt = tt - s0; p = cl(lt / d)
    kb = (tt - T0) / BP; kbi = math.floor(kb); dtb = (kb - kbi) * BP
    quiet = is_quiet(kbi) or tt < T0
    pulse = 0 if quiet else (0.04 if kbi % 4 == 0 else 0.014) * math.exp(-dtb * 14)
    drift = 0.06 * ease(p)          # 每镜缓推（样片的慢推）
    z = 1.0 + drift + pulse
    if fx in ('slam', 'drop', 'kill'): z += 0.2 * (1 - eout(lt / 0.28))
    sh = 0
    if fx in ('kill', 'drop'): sh = 24 * math.exp(-lt * 7)
    if not quiet and kbi % 2 == 0: sh = max(sh, 6 * math.exp(-dtb * 18))
    ox = math.sin(tt * 91) * sh; oy = math.cos(tt * 77) * sh
    whip = 0
    if fx == 'streak' and lt < 0.18: whip = (1 - eout(lt / 0.18)) * 500
    c.save(); c.translate(960 + ox + whip, 540 + oy); c.scale(z, z); c.translate(-960, -540)
    getattr(S, 'S_' + key)(c, lt, d, p, **kw)
    c.restore()
    vignette(c, 0.6)
    if fx == 'streak': S.streak(c, lt, 0.0, 820, 260, 0.3)
    if fx == 'ink' and lt < 0.45:
        S.inksplash(c, 960, 540, 1500, 1 - eout(lt / 0.45), seed=i, col=(0.02, 0.015, 0.01), a=1)
    title_block(c, ttl, sub, lt, d)
    src_line(c, src, lt, d)
    ta = ease(lt / 0.3) * (1 - ease((lt - d + 0.15) / 0.15))
    tagui(c, yr, ta)
    y = year_of(yr)
    if y: LASTF[0] = cl((y - YR0) / (YR1 - YR0))
    if key not in ('title', 'end', 'black', 'bigword') and tt > starts[3]: progbar(c, LASTF[0], 0.9)
    if fx == 'drop': c.set_source_rgba(1, 1, 1, 0.85 * math.exp(-lt * 8)); c.paint()
    if fx == 'slam': c.set_source_rgba(1, 0.95, 0.9, 0.35 * math.exp(-lt * 14)); c.paint()
    if fx == 'kill': redflash(c, math.exp(-lt * 4) * 1.4)
    k = cl(lt / 0.05)
    if k < 1 and i > 0 and fx not in ('ink',): c.set_source_rgba(0, 0, 0, 1 - k); c.paint()
    if tt > TOTAL - 1.4: c.set_source_rgba(0, 0, 0, cl((tt - TOTAL + 1.4) / 1.4)); c.paint()
    g = 0
    if fx in ('glitch', 'drop'): g = max(g, 1 - lt / 0.22)
    if not quiet and kbi % 16 == 0 and dtb < 0.12: g = max(g, 0.8)
    if fx == 'kill': g = max(g, 0.6 * (1 - lt / 0.15))
    if g > 0: glitch(sf, cl(g), int(tt * 30))
    return sf

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for a in sys.argv[2:]: frame(float(a)).write_to_png(f'/tmp/st_{a}.png')
        sys.exit()
    if sys.argv[1] == 'sheet':
        from PIL import Image
        fr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7
        ims = []
        for i in range(len(L)):
            tt = seg[i][0] + (seg[i][1] - seg[i][0]) * fr
            frame(tt).write_to_png('/tmp/_s.png'); ims.append(Image.open('/tmp/_s.png').convert('RGB').resize((480, 270)))
        cols = 8; rows = (len(ims) + cols - 1) // cols
        o = Image.new('RGB', (480 * cols, 270 * rows))
        for j, im in enumerate(ims): o.paste(im, ((j % cols) * 480, (j // cols) * 270))
        o.save(sys.argv[2], quality=82); sys.exit()
    part, nparts = int(sys.argv[1]), int(sys.argv[2])
    N = int(TOTAL * FPS); a = N * part // nparts; b = N * (part + 1) // nparts
    pr = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', f'part{part}.mp4'], stdin=subprocess.PIPE)
    for f in range(a, b):
        sf = frame(f / FPS); pr.stdin.write(bytes(sf.get_data()))
    pr.stdin.close(); pr.wait(); open(f'part{part}.done', 'w').write('ok')
