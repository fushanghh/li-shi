"""v2 引擎：画笔、纸纹、辉光合成、镜头、转场、特效、版式"""
import cairocffi as cairo, math, random, numpy as np
from PIL import Image, ImageFilter

W, H = 1080, 1440
FPS = 30
BPM = 96.0
B = 60.0 / BPM
STAGE_T, STAGE_B = 40, 1004
SW, SH = W, STAGE_B - STAGE_T
SCX, SCY = W / 2, (STAGE_T + STAGE_B) / 2
CAP_T, CAP_B = 1028, 1290

PAL = dict(BG='#b8622e', BG2='#a2522a', BGD='#7a3a1c', HILL='#8e4524', HILL2='#a5552c', BLK='#15100c', BLK2='#221813',
           LN='#e0904a', LN2='#b8703a', CREAM='#f3dfb6', GOLD='#f0b850', GOLD2='#ffd27a', RED='#b8332a', RED2='#8c2420',
           GREEN='#3f5c48', NIGHT='#1b2134', NIGHT2='#283252', NIGHT3='#36426a', SNOW='#f6eedc', FIRE='#f39a36',
           PURPLE='#5b3b60', DRED='#7c2b22', WOOD='#5a3a22', STONE='#3a2a20', TEAL='#1e3236')

def hx(h, a=1.0):
    h = PAL.get(h, h).lstrip('#')
    return (int(h[:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:], 16) / 255, a)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def ei(x): x = clamp(x); return x ** 3
def eback(x, s=1.9): x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, k): return a + (b - a) * k

def track(t, keys, fn=eio):
    """keys [(t, value)]，按缓动插值；value 可为数字或元组"""
    if t <= keys[0][0]: return keys[0][1]
    for i in range(len(keys) - 1):
        t0, v0 = keys[i][0], keys[i][1]; t1, v1 = keys[i + 1][0], keys[i + 1][1]
        f = keys[i + 1][2] if len(keys[i + 1]) > 2 else fn
        if isinstance(f, str): f = {'io': eio, 'out': eo, 'in': ei, 'lin': (lambda v: v), 'snap': (lambda v: eback(v, 1.6))}[f]
        if t0 <= t < t1:
            k = f((t - t0) / (t1 - t0)) if t1 > t0 else 1
            if isinstance(v0, tuple): return tuple(lerp(a, b, k) for a, b in zip(v0, v1))
            return lerp(v0, v1, k)
    return keys[-1][1]

def punch(t, t0, dur=0.22, amp=0.35):
    if t < t0: return 0.6
    x = (t - t0) / dur
    if x >= 1: return 1.0
    if x < 0.45: return (1 + amp) * lerp(0.6, 1.0, eo(x / 0.45))
    return 1 + amp * (1 - ease((x - 0.45) / 0.55))

class P:
    """双层画笔：c 为主画面，g 为发光层（之后模糊叠加）"""
    def __init__(s, ctx, gctx=None):
        s.c = ctx; s.gc = gctx
    @property
    def g(s):
        q = P(s.gc, None); return q
    def col(s, k, a=1.0): s.c.set_source_rgba(*hx(k, a))
    def poly(s, pts, col, stroke=None, w=2.5, a=1.0):
        c = s.c; c.move_to(*pts[0])
        for q in pts[1:]: c.line_to(*q)
        c.close_path(); s.col(col, a)
        if stroke: c.fill_preserve(); s.col(stroke, a); c.set_line_width(w); c.stroke()
        else: c.fill()
    def line(s, pts, col, w, a=1.0):
        c = s.c; c.move_to(*pts[0])
        for q in pts[1:]: c.line_to(*q)
        s.col(col, a); c.set_line_width(w); c.stroke()
    def curve(s, pts, col, w, a=1.0, close=False, fill=None):
        """Catmull-Rom 平滑曲线"""
        c = s.c
        if len(pts) < 3: return s.line(pts, col, w, a)
        c.move_to(*pts[0])
        P_ = [pts[0]] + list(pts) + [pts[-1]]
        for i in range(1, len(P_) - 2):
            p0, p1, p2, p3 = P_[i - 1], P_[i], P_[i + 1], P_[i + 2]
            c.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
        if close: c.close_path()
        if fill:
            s.col(fill, a)
            if col: c.fill_preserve()
            else: c.fill(); return
        s.col(col, a); c.set_line_width(w); c.stroke()
    def ell(s, x, y, rx, ry, col, stroke=None, w=2.5, a=1.0, rot=0):
        c = s.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(max(rx, .01), max(ry, .01)); c.arc(0, 0, 1, 0, 6.2832); c.restore()
        s.col(col, a)
        if stroke: c.fill_preserve(); s.col(stroke, a); c.set_line_width(w); c.stroke()
        else: c.fill()
    def arc(s, x, y, r, a0, a1, col, w, a=1.0):
        s.c.new_sub_path(); s.c.arc(x, y, r, a0, a1); s.col(col, a); s.c.set_line_width(w); s.c.stroke()
    def ring(s, x, y, r, col, w, a=1.0):
        s.c.new_sub_path(); s.c.arc(x, y, max(r, .1), 0, 6.2832); s.col(col, a); s.c.set_line_width(w); s.c.stroke()
    def rect(s, x, y, w_, h_, col, a=1.0): s.poly([(x, y), (x + w_, y), (x + w_, y + h_), (x, y + h_)], col, a=a)
    def text(s, t, x, y, size, col, anchor='c', bold=1, outline=None, ow=None, a=1.0, font="Noto Serif CJK SC"):
        c = s.c
        c.select_font_face(font, 0, bold); c.set_font_size(size)
        e = c.text_extents(t)
        dx = {'c': e[4] / 2, 'l': 0, 'r': e[4]}[anchor]
        c.move_to(x - dx, y)
        if outline:
            c.text_path(t); s.col(outline, a); c.set_line_width(ow or size * 0.16); c.stroke_preserve(); s.col(col, a); c.fill()
        else:
            s.col(col, a); c.show_text(t)
        return e[4]
    def radial(s, x, y, r, col, a0=0.8, a1=0.0):
        g = cairo.RadialGradient(x, y, 0, x, y, r)
        cc = hx(col); g.add_color_stop_rgba(0, cc[0], cc[1], cc[2], a0); g.add_color_stop_rgba(1, cc[0], cc[1], cc[2], a1)
        s.c.set_source(g); s.c.arc(x, y, r, 0, 6.2832); s.c.fill()
    def vgrad(s, x, y0, w_, y1, c0, c1):
        g = cairo.LinearGradient(0, y0, 0, y1)
        a = hx(c0); b = hx(c1); g.add_color_stop_rgba(0, *a); g.add_color_stop_rgba(1, *b)
        s.c.set_source(g); s.c.rectangle(x, y0, w_, y1 - y0); s.c.fill()

# ---------- 纸纹 + 暗角（预计算乘法图） ----------
def _paper():
    rng = np.random.default_rng(11)
    n = rng.normal(0, 1, (SH // 4 + 1, SW // 4 + 1)).astype(np.float32)
    im = Image.fromarray(((n * 30) + 128).clip(0, 255).astype(np.uint8)).resize((SW, SH), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3))
    low = (np.asarray(im, np.float32) - 128) / 128 * 0.05
    fine = rng.normal(0, 0.035, (SH, SW)).astype(np.float32)
    fib = np.asarray(Image.fromarray((rng.random((SH // 2, SW // 8)) * 255).astype(np.uint8)).resize((SW, SH), Image.BILINEAR), np.float32) / 255 * 0.04 - 0.02
    yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
    d = np.sqrt(((xx - SW / 2) / (SW * 0.62)) ** 2 + ((yy - SH * 0.45) / (SH * 0.62)) ** 2)
    vig = 1.06 - 0.42 * np.clip(d, 0, 1.3) ** 2.2
    return np.clip((1 + low + fine + fib) * vig, 0.45, 1.15)[..., None]
PAPER = _paper()

def composite(surf, gsurf, flash=0.0, tint=None):
    """主画面 × 纸纹 + 模糊发光层（加亮） + 发光层原样"""
    a = np.ndarray((H, W, 4), np.uint8, surf.get_data()).astype(np.float32)
    st = a[STAGE_T:STAGE_B, :, :3]
    st *= PAPER
    if gsurf is not None:
        g = np.ndarray((H, W, 4), np.uint8, gsurf.get_data())
        gs = g[STAGE_T:STAGE_B]
        small = Image.fromarray(gs[..., :3].copy()).resize((SW // 4, SH // 4), Image.BILINEAR)
        b1 = np.asarray(small.filter(ImageFilter.GaussianBlur(5)).resize((SW, SH), Image.BILINEAR), np.float32)
        b2 = np.asarray(small.filter(ImageFilter.GaussianBlur(14)).resize((SW, SH), Image.BILINEAR), np.float32)
        ga = gs[..., 3:4].astype(np.float32) / 255
        st[:] = st * (1 - ga) + gs[..., :3].astype(np.float32)  # 预乘 alpha
        st += b1 * 1.1 + b2 * 0.9
    if tint is not None:
        col, amt = tint; cc = np.array(hx(col)[:3], np.float32)[::-1] * 255
        st[:] = st * (1 - amt) + cc * amt
    if flash > 0: st[:] = st + (np.array([200, 230, 250], np.float32) - st) * flash
    a[STAGE_T:STAGE_B, :, :3] = st
    return np.clip(a, 0, 255).astype(np.uint8)

# ---------- 特效（画在发光层 g 或主层 p） ----------
def star(p, x, y, r, col='GOLD2', a=1.0, rot=0.0):
    pts = []
    for i in range(8):
        an = rot + i * math.pi / 4; rr = r if i % 2 == 0 else r * 0.18
        pts.append((x + math.cos(an) * rr, y + math.sin(an) * rr))
    p.poly(pts, col, a=a)

def impact(p, g, x, y, t, t0, size=1.0, col='GOLD2', seed=0):
    """打击：十字星闪 + 放射线 + 冲击环 + 火星"""
    k = (t - t0) / 0.5
    if k < 0 or k > 1: return
    a = 1 - k
    if k < 0.25:
        star(g, x, y, 170 * size * eo(k / 0.25), 'CREAM', 1.0, 0.3)
        star(g, x, y, 110 * size * eo(k / 0.25), col, 1.0, 0.3 + math.pi / 8)
        g.ell(x, y, 40 * size, 40 * size, 'CREAM', a=1 - k * 4)
    g.ring(x, y, 30 + 200 * size * eo(k), col, 8 * a + 1, a)
    rnd = random.Random(seed * 131 + int(t0 * 97))
    for i in range(16):
        an = rnd.uniform(0, 6.283); L = rnd.uniform(.6, 1.2)
        r1 = 60 * size + 260 * size * eo(k) * L * 0.6; r2 = r1 + 90 * size * a * L
        g.line([(x + math.cos(an) * r1, y + math.sin(an) * r1), (x + math.cos(an) * r2, y + math.sin(an) * r2)], col, 4 * a + 1, a)
    for i in range(22):
        an = rnd.uniform(0, 6.283); sp = rnd.uniform(200, 700) * size
        px = x + math.cos(an) * sp * k; py = y + math.sin(an) * sp * k + 500 * k * k
        g.ell(px, py, 5 * a + 1.5, 5 * a + 1.5, 'GOLD2', a=a)

def clash(p, g, x, y, t, t0, size=1.0):
    """兵器相交：白色火花 + 竖向闪光"""
    k = (t - t0) / 0.4
    if k < 0 or k > 1: return
    a = 1 - k
    g.poly([(x - 8 * a, y - 160 * size * a), (x + 8 * a, y - 160 * size * a), (x + 3, y + 160 * size * a), (x - 3, y + 160 * size * a)], 'CREAM', a=a)
    rnd = random.Random(int(t0 * 777))
    for i in range(26):
        an = rnd.uniform(-3.0, 0.1); sp = rnd.uniform(300, 900) * size
        px, py = x + math.cos(an) * sp * k, y + math.sin(an) * sp * k + 900 * k * k
        g.line([(px, py), (px - math.cos(an) * 24 * a, py - math.sin(an) * 24 * a)], 'GOLD2', 4, a)

def dust(p, x, y, t, t0, size=1.0, col='CREAM', n=9, dur=0.8, seed=0):
    k = (t - t0) / dur
    if k < 0 or k > 1: return
    a = (1 - k) ** 1.5
    rnd = random.Random(seed + int(t0 * 991))
    for i in range(n):
        dirx = rnd.uniform(-1, 1); d = 220 * size * eo(k) * abs(dirx) + 30
        r = (26 + 50 * k) * size * rnd.uniform(.7, 1.2)
        p.ell(x + dirx * d * 1.4, y - rnd.uniform(0, 50) * size * k - r * 0.4, r, r * 0.75, col, 'BLK', 3, a=a * 0.95)

def shockring(p, g, x, y, t, t0, size=1.0, col='CREAM'):
    k = (t - t0) / 0.6
    if k < 0 or k > 1: return
    a = 1 - k
    g.ell(x, y, 40 + 520 * size * eo(k), 10 + 90 * size * eo(k), None if False else col, a=0) if False else None
    p.c.save(); p.c.translate(x, y); p.c.scale(1, 0.18)
    g.c.save(); g.c.translate(x, y); g.c.scale(1, 0.18)
    g.ring(0, 0, 40 + 520 * size * eo(k), col, 30 * a + 2, a); g.c.restore(); p.c.restore()

def speedlines_screen(p, t, t0, dur, ang=0.0, n=24, col='CREAM', seed=1, a0=0.7):
    k = (t - t0) / dur
    if k < 0 or k > 1: return
    a = a0 * math.sin(k * math.pi)
    rnd = random.Random(seed)
    ca, sa = math.cos(ang), math.sin(ang)
    for i in range(n):
        o = rnd.uniform(-700, 700); s0 = rnd.uniform(-900, 900); L = rnd.uniform(150, 500)
        ph = (s0 + k * 3000 * rnd.uniform(.7, 1.3)) % 1800 - 900
        x0 = SCX + ca * ph - sa * o; y0 = SCY + sa * ph + ca * o
        p.line([(x0, y0), (x0 - ca * L, y0 - sa * L)], col, rnd.uniform(2, 6), a)

def trail(g, pts, col='CREAM', w=26, a=0.9):
    """动作弧光：一串点，尾细头粗"""
    n = len(pts)
    if n < 2: return
    for i in range(1, n):
        k = i / (n - 1)
        g.line([pts[i - 1], pts[i]], col, max(1, w * k), a * k)

def snowfall(p, t, n=120, seed=1, speed=1.0, wind=60, frozen=None, x0=-200, x1=W + 200, y0=-100, y1=1200, size=1.0, a=0.9):
    rnd = random.Random(seed); tt = frozen if frozen is not None else t
    for i in range(n):
        xs = rnd.uniform(x0, x1); v = rnd.uniform(50, 130) * speed; r = rnd.uniform(1.8, 5.2) * size; ph = rnd.uniform(0, 1000)
        y = y0 + ((ph + tt * v) % (y1 - y0))
        x = x0 + ((xs - x0 + tt * wind * rnd.uniform(.7, 1.3) + math.sin(tt * 1.7 + ph) * 14) % (x1 - x0))
        p.ell(x, y, r, r, 'SNOW', a=a * rnd.uniform(.6, 1))

def embers(g, t, n=50, seed=3, x0=0, x1=W, ybase=900, h=700, col='GOLD2'):
    rnd = random.Random(seed)
    for i in range(n):
        xs = rnd.uniform(x0, x1); v = rnd.uniform(60, 180); ph = rnd.uniform(0, 100)
        yy = ybase - ((ph * 13 + t * v) % h); xx = xs + math.sin(t * 2 + ph) * 30
        al = 1 - ((ph * 13 + t * v) % h) / h
        g.ell(xx, yy, 3, 3, col, a=al)

def flames(p, g, x, gy, w, h, t, seed=3, glow=1.0):
    rnd = random.Random(seed)
    n = max(1, int(w / 26))
    for layer, (colr, hk, wk) in enumerate([('RED2', 1.1, 1.3), ('FIRE', 0.9, 1.0), ('GOLD2', 0.55, 0.6)]):
        tgt = g if layer > 0 else p
        ga = 0.92 * (glow if layer > 0 else 1)
        for i in range(n):
            fx = x - w / 2 + (i + .5) * w / n + rnd.uniform(-8, 8)
            fh = h * hk * (0.55 + 0.45 * abs(math.sin(t * 6.5 + i * 1.7 + layer))) * rnd.uniform(.6, 1)
            sw = 30 * wk
            tip = fx + 14 * math.sin(t * 8 + i)
            tgt.curve([(fx - sw, gy), (fx - sw * .6, gy - fh * .4), (tip - 4, gy - fh * .8), (tip, gy - fh), (tip + 4, gy - fh * .8), (fx + sw * .6, gy - fh * .4), (fx + sw, gy)], None, 1, a=ga, close=True, fill=colr)

def lightning(g, x0, y0, x1, y1, t, seed=0, a=1.0):
    rnd = random.Random(seed + int(t * 20))
    pts = [(x0, y0)]
    for i in range(1, 9):
        k = i / 9; pts.append((lerp(x0, x1, k) + rnd.uniform(-40, 40), lerp(y0, y1, k)))
    pts.append((x1, y1))
    g.line(pts, 'CREAM', 6, a); g.line(pts, 'GOLD2', 2, a)

def cloud_icon(p, x, y, s=1.0, col='BLK', ln='LN', a=1.0):
    p.curve([(x - 70 * s, y), (x - 60 * s, y - 26 * s), (x - 30 * s, y - 34 * s), (x - 6 * s, y - 52 * s), (x + 30 * s, y - 44 * s), (x + 48 * s, y - 26 * s), (x + 74 * s, y - 14 * s), (x + 70 * s, y)], None, 1, close=True, fill=col, a=a)
    for dx in (-24, 14):
        p.arc(x + dx * s, y - 18 * s, 12 * s, math.pi * .3, math.pi * 2.1, ln, 3 * s, a)

# ---------- 版式 ----------
def meander(p, y, h, col='LN', step=40):
    for i in range(0, W + step, step):
        p.line([(i + 6, y + h - 6), (i + 6, y + 6), (i + step - 8, y + 6), (i + step - 8, y + h - 12), (i + 16, y + h - 12), (i + 16, y + 14)], col, 3)

def chrome(p, cap=None, t=0.0, wm=True):
    c = p.c
    p.rect(0, 0, W, STAGE_T, 'BLK'); meander(p, 4, STAGE_T - 8)
    p.rect(0, STAGE_B, W, H - STAGE_B, '#110c09')
    p.rect(0, STAGE_B, W, 24, '#c26c36'); meander(p, STAGE_B + 1, 22, 'BLK', 34)
    # 底部彩陶纹
    p.rect(0, CAP_B, W, H - CAP_B, '#c46e38')
    p.line([(0, CAP_B + 5), (W, CAP_B + 5)], 'BLK', 6); p.line([(0, H - 7), (W, H - 7)], 'BLK', 6)
    for i in range(0, W, 46):
        p.poly([(i, CAP_B + 12), (i + 23, CAP_B + 30), (i + 46, CAP_B + 12)], 'BLK')
        p.poly([(i, H - 14), (i + 23, H - 32), (i + 46, H - 14)], 'BLK')
    cy = (CAP_B + H) / 2
    p.curve([(x, cy + 14 * math.sin(x / 54 * math.pi)) for x in range(0, W + 20, 18)], 'BLK', 4)
    for i in range(10):
        cx = 54 + i * 108
        p.ell(cx, cy, 30, 30, '#c46e38'); [p.ring(cx, cy, r, 'BLK', 4) for r in (28, 18, 8)]
    if wm: p.text('水浒群英', 24, STAGE_T + 34, 22, 'CREAM', 'l', 0, a=0.55)
    if cap:
        t0, l1, l2, h1, h2 = cap
        for li, (line, hl, y, ton) in enumerate([(l1, h1, 1138, t0), (l2, h2, 1222, t0 + 0.55)]):
            if not line or t < ton: continue
            c.select_font_face("Noto Serif CJK SC", 0, 1); c.set_font_size(52)
            tw = c.text_extents(line)[4]; x = W / 2 - tw / 2
            for ci, ch in enumerate(line):
                a = clamp((t - ton - ci * 0.035) / 0.12)
                if a <= 0: break
                colr = 'GOLD' if any(a_ <= ci < b_ for a_, b_ in hl) else 'CREAM'
                c.move_to(x, y + (1 - a) * 8); p.col(colr, a); c.show_text(ch)
                x += c.text_extents(ch)[4]

def hl(s, *words):
    out = []
    for w_ in words:
        i = s.find(w_)
        if i >= 0: out.append((i, i + len(w_)))
    return tuple(out)

def big_title(p, g, txt, x, y, t, t0, t1=None, size=130, col='GOLD', glow=True):
    if t < t0 or (t1 is not None and t > t1): return
    s = punch(t, t0, 0.28, 0.5); a = 1.0
    if t1 is not None and t > t1 - 0.3: a = (t1 - t) / 0.3
    for q, gl in ((p, False), (g, True)):
        if gl and not glow: continue
        q.c.save(); q.c.translate(x, y); q.c.scale(s, s)
        if gl:
            if t - t0 < 0.6: q.text(txt, 0, 0, size, 'GOLD', a=a * (1 - (t - t0) / 0.6) * 0.8)
        else:
            q.text(txt, 4, 6, size, 'BLK', a=a * 0.6)
            q.text(txt, 0, 0, size, col, outline='BLK', ow=size * 0.12, a=a)
        q.c.restore()

def onomato(p, txt, x, y, t, t0, size=90, col='CREAM', dur=0.8, rot=-0.12):
    if t < t0 or t > t0 + dur: return
    s = punch(t, t0, 0.2, 0.45); a = 1 if t < t0 + dur - 0.2 else (t0 + dur - t) / 0.2
    c = p.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p.text(txt, 0, 0, size, col, outline='BLK', ow=size * 0.2, a=a)
    c.restore()

def counter(p, g, label, val, t, t_last, show=True):
    if not show: return
    x, y = W - 30, STAGE_T + 30
    s = punch(t, t_last, 0.22, 0.4) if t_last is not None else 1
    p.poly([(x - 210, y), (x, y), (x, y + 108), (x - 210, y + 108)], '#1a120c', 'LN', 3, a=0.9)
    p.line([(x - 200, y + 34), (x - 10, y + 34)], 'LN2', 1.5)
    p.text(label, x - 105, y + 26, 22, 'LN', bold=0)
    c = p.c; c.save(); c.translate(x - 105, y + 90); c.scale(s, s)
    p.text(val, 0, 0, 56, 'GOLD', outline='BLK', ow=5)
    c.restore()
    if t_last is not None and 0 <= t - t_last < 0.3:
        g.c.save(); g.c.translate(x - 105, y + 90); g.c.scale(s, s); g.text(val, 0, 0, 56, 'GOLD', a=1 - (t - t_last) / 0.3); g.c.restore()

def nametag(p, py, cn, x, y, t, t0, dur=2.0, anchor='c'):
    if t < t0 or t > t0 + dur: return
    a = min(1, (t - t0) / 0.2, (t0 + dur - t) / 0.3)
    dy = (1 - eo((t - t0) / 0.3)) * 12
    p.text(py, x, y + dy, 17, 'CREAM', anchor, 0, a=a * 0.85)
    p.line([(x - 60 if anchor == 'c' else x, y + 10 + dy), (x + 60 if anchor == 'c' else x + 120, y + 10 + dy)], 'CREAM', 1.5, a * 0.6)
    p.text(cn, x, y + 44 + dy, 32, 'CREAM', anchor, a=a, outline='BLK', ow=5)

def haze(p, col='BG', a=0.35):
    p.rect(-3000, -1500, 7000, 4000, col, a)
