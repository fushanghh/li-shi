# 剪影叙事风工具库（暗色电影感 · 黑剪影人物 · 发光玉器 · 打字机字幕 · 年份标签 · 计数器）
import cairocffi as cairo, math, random
W, H = 1920, 1080
FONT = "Noto Serif CJK SC"
INK = (0.035, 0.028, 0.026)
JADE = (0.72, 0.90, 0.80)
GOLD = (0.93, 0.76, 0.42)
RED = (0.86, 0.20, 0.16)

def cl(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = cl(x); return x * x * (3 - 2 * x)
def eout(x): x = cl(x); return 1 - (1 - x) ** 3
def lerp(a, b, t): return a + (b - a) * t
def mix(c1, c2, t): return tuple(lerp(a, b, t) for a, b in zip(c1, c2))

def vgrad(c, y0, y1, stops, x0=0, x1=W):
    g = cairo.LinearGradient(0, y0, 0, y1)
    for p, col in stops: g.add_color_stop_rgb(p, *col)
    c.set_source(g); c.rectangle(x0, y0, x1 - x0, y1 - y0); c.fill()

def glow(c, x, y, r, col, a=1.0):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(0.35, *col, a * 0.35); g.add_color_stop_rgba(1, *col, 0)
    c.set_source(g); c.arc(x, y, r, 0, 6.2832); c.fill()

def poly(c, pts, col, a=1):
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path(); c.set_source_rgba(*col, a); c.fill()

def rr(c, x, y, w, h, r):
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -1.5708, 0); c.arc(x + w - r, y + h - r, r, 0, 1.5708)
    c.arc(x + r, y + h - r, r, 1.5708, 3.1416); c.arc(x + r, y + r, r, 3.1416, 4.7124); c.close_path()

def text(c, s, x, y, size, col=(1, 1, 1), a=1, align='l', weight=cairo.FONT_WEIGHT_BOLD, shadow=True):
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, weight); c.set_font_size(size)
    e = c.text_extents(s); w = e[4]
    xx = x if align == 'l' else (x - w / 2 if align == 'c' else x - w)
    if shadow:
        c.set_source_rgba(0, 0, 0, 0.6 * a); c.move_to(xx + 2, y + 3); c.show_text(s)
    c.set_source_rgba(*col, a); c.move_to(xx, y); c.show_text(s)
    return w

# ---------------- 环境 ----------------
def stars(c, t, n=120, seed=3, ymax=700, a=1):
    rnd = random.Random(seed)
    for i in range(n):
        x, y = rnd.uniform(0, W), rnd.uniform(0, ymax); r = rnd.uniform(0.8, 2.2)
        tw = 0.5 + 0.5 * math.sin(t * rnd.uniform(1, 3) + i)
        c.set_source_rgba(1, 0.97, 0.9, (0.25 + 0.6 * tw) * a); c.arc(x, y, r, 0, 6.28); c.fill()

def moon(c, x, y, r=60, a=1):
    glow(c, x, y, r * 4, (0.9, 0.9, 1.0), 0.22 * a)
    c.set_source_rgba(0.93, 0.93, 0.9, a); c.arc(x, y, r, 0, 6.28); c.fill()
    c.set_source_rgba(0.8, 0.8, 0.78, 0.5 * a)
    for dx, dy, rr_ in ((-18, -10, 12), (15, 18, 9), (20, -22, 6)):
        c.arc(x + dx * r / 60, y + dy * r / 60, rr_ * r / 60, 0, 6.28); c.fill()

def dust(c, t, n=40, col=(1, 0.85, 0.6), seed=7, a=0.5, up=False):
    rnd = random.Random(seed)
    for i in range(n):
        x = (rnd.uniform(0, W) + t * rnd.uniform(-15, 15)) % W
        sp = rnd.uniform(10, 40)
        y = (rnd.uniform(0, H) + (-1 if up else 0.3) * t * sp * (3 if up else 1)) % H
        c.set_source_rgba(*col, a * rnd.uniform(0.3, 1)); c.arc(x, y, rnd.uniform(1, 3), 0, 6.28); c.fill()

def mountains(c, t, cols=None, base=820, seed=11):
    cols = cols or [(0.10, 0.11, 0.15), (0.07, 0.075, 0.10), (0.04, 0.045, 0.06)]
    rnd = random.Random(seed)
    for k, col in enumerate(cols):
        y0 = base - 260 + k * 110; pts = [(0, H)]
        ph = rnd.uniform(0, 9)
        for i in range(0, 41):
            x = i * W / 40
            y = y0 - 120 * abs(math.sin(i * 0.37 + ph)) * (1 - k * 0.2) - 40 * math.sin(i * 1.3 + ph)
            pts.append((x, y))
        pts.append((W, H)); poly(c, pts, col)
        c.set_source_rgba(0.75, 0.6, 0.38, 0.12)
        c.move_to(*pts[1]); [c.line_to(*p) for p in pts[2:-1]]; c.set_line_width(2); c.stroke()

def water(c, t, y=760, col=(0.05, 0.06, 0.09)):
    vgrad(c, y, H, [(0, col), (1, (0.01, 0.01, 0.02))])
    rnd = random.Random(5)
    for i in range(70):
        x = (rnd.uniform(0, W) + t * 20) % W; yy = rnd.uniform(y + 10, H)
        c.set_source_rgba(0.8, 0.85, 1, 0.12 * (yy - y) / (H - y) + 0.04)
        c.rectangle(x, yy, rnd.uniform(20, 70), 2); c.fill()

def reeds(c, t, y=900, n=90, seed=2):
    rnd = random.Random(seed)
    c.set_line_width(3); c.set_source_rgb(*INK)
    for i in range(n):
        x = rnd.uniform(-20, W + 20); h = rnd.uniform(80, 220); sw = math.sin(t * 1.2 + x * 0.01) * 12
        c.move_to(x, y + 60); c.curve_to(x, y - h * 0.5, x + sw, y - h * 0.8, x + sw * 1.4, y - h); c.stroke()

def palace(c, t, tone=(0.20, 0.05, 0.04), floor=840, pillars=(260, 1660), lattice=True, curtain=True, candles=((540, 760), (1380, 760))):
    vgrad(c, 0, floor, [(0, (0.05, 0.02, 0.02)), (0.6, mix(tone, (0, 0, 0), 0.3)), (1, tone)])
    if lattice:
        for x0 in (560, 1010):
            c.set_source_rgba(0.12, 0.04, 0.03, 1); c.rectangle(x0, 300, 350, 330); c.fill()
            c.set_source_rgba(0.55, 0.30, 0.18, 0.18); c.set_line_width(2)
            for i in range(1, 8): c.move_to(x0 + i * 350 / 8, 300); c.line_to(x0 + i * 350 / 8, 630)
            for j in range(1, 7): c.move_to(x0, 300 + j * 330 / 7); c.line_to(x0 + 350, 300 + j * 330 / 7)
            c.stroke()
            c.set_source_rgba(0.6, 0.35, 0.2, 0.35); c.rectangle(x0, 300, 350, 330); c.stroke()
    for px in pillars:
        g = cairo.LinearGradient(px - 45, 0, px + 45, 0)
        g.add_color_stop_rgb(0, 0.18, 0.03, 0.02); g.add_color_stop_rgb(0.45, 0.42, 0.08, 0.05); g.add_color_stop_rgb(1, 0.12, 0.02, 0.02)
        c.set_source(g); c.rectangle(px - 45, 0, 90, floor); c.fill()
    vgrad(c, floor, H, [(0, (0.10, 0.04, 0.03)), (1, (0.02, 0.01, 0.01))])
    c.set_source_rgba(0.7, 0.4, 0.2, 0.25); c.rectangle(0, floor, W, 3); c.fill()
    if curtain:
        for s in (-1, 1):
            x = 0 if s < 0 else W
            c.move_to(x, 0); c.line_to(x - s * -260, 0)
            c.curve_to(x + s * -200, 300, x + s * -120, 600, x + s * -150, 900); c.line_to(x, 900); c.close_path()
            c.set_source_rgba(0.25, 0.03, 0.03, 0.9); c.fill()
    glow(c, 960, 720, 760, (1, 0.55, 0.3), 0.16)
    for (cx, cy) in candles: candle(c, cx, cy, t)

def candle(c, x, y, t, h=120):
    c.set_source_rgb(*INK); c.rectangle(x - 3, y - h, 6, h); c.fill(); c.rectangle(x - 22, y - 4, 44, 6); c.fill()
    f = 1 + 0.15 * math.sin(t * 13 + x) + 0.08 * math.sin(t * 29)
    glow(c, x, y - h - 12, 120 * f, (1, 0.6, 0.25), 0.45)
    c.set_source_rgb(1, 0.85, 0.5); c.save(); c.translate(x, y - h - 12); c.scale(1, 1.8 * f)
    c.arc(0, 0, 6, 0, 6.28); c.restore(); c.fill()

def flame(c, x, y, h, t, seed=0, a=1):
    for k, (col, sc) in enumerate((((0.85, 0.22, 0.05), 1.0), ((1, 0.55, 0.1), 0.72), ((1, 0.88, 0.45), 0.42))):
        hh = h * sc * (1 + 0.12 * math.sin(t * 9 + seed * 1.7 + k)); ww = h * 0.36 * sc
        sw = math.sin(t * 6 + seed) * ww * 0.3
        c.move_to(x - ww, y); c.curve_to(x - ww, y - hh * 0.5, x + sw - ww * 0.2, y - hh * 0.7, x + sw, y - hh)
        c.curve_to(x + sw + ww * 0.2, y - hh * 0.7, x + ww, y - hh * 0.5, x + ww, y); c.close_path()
        c.set_source_rgba(*col, a); c.fill()

def fires(c, t, xs, y, h, a=1):
    for i, x in enumerate(xs):
        glow(c, x, y - h * 0.4, h * 1.6, (1, 0.4, 0.1), 0.35 * a)
    for i, x in enumerate(xs): flame(c, x, y, h * (0.8 + 0.4 * ((i * 37) % 10) / 10), t, i, a)

def roofhall(c, x, y, w, h, col=INK, lit=False, t=0):
    # 殿宇剪影：台基 + 屋身 + 庑殿顶
    poly(c, [(x - w * 0.55, y), (x + w * 0.55, y), (x + w * 0.5, y - h * 0.12), (x - w * 0.5, y - h * 0.12)], col)
    c.set_source_rgb(*col); c.rectangle(x - w * 0.4, y - h * 0.62, w * 0.8, h * 0.5); c.fill()
    poly(c, [(x - w * 0.62, y - h * 0.58), (x + w * 0.62, y - h * 0.58), (x + w * 0.42, y - h * 0.86), (x + w * 0.3, y - h), (x - w * 0.3, y - h), (x - w * 0.42, y - h * 0.86)], col)
    if lit:
        for i in range(6):
            fx = x - w * 0.32 + i * w * 0.128
            k = 0.7 + 0.3 * math.sin(t * 5 + i)
            c.set_source_rgba(1, 0.75, 0.35, k); c.rectangle(fx, y - h * 0.5, w * 0.06, h * 0.22); c.fill()

def citywall(c, y, col=INK, h=120):
    c.set_source_rgb(*col); c.rectangle(0, y - h, W, h + 400); c.fill()
    for i in range(0, W, 46): c.rectangle(i, y - h - 22, 26, 22); c.fill()

def banner(c, x, y, ch, col, t, h=260, a=1, s=1):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(*INK, a); c.rectangle(-4, -h, 8, h); c.fill()
    wv = math.sin(t * 2 + x) * 6
    c.move_to(4, -h + 10); c.line_to(90, -h + 10 + wv * 0.3); c.line_to(90 + wv, -h + 170); c.line_to(4, -h + 160); c.close_path()
    c.set_source_rgba(*col, a); c.fill()
    text(c, ch, 47 + wv * 0.5, -h + 112, 62, (1, 0.95, 0.85), a * 0.95, 'c', shadow=False)
    c.restore()

def crowd(c, y, n=14, s=0.7, x0=150, x1=1770, pose='kneel', hat='guan', a=1):
    for i in range(n):
        x = lerp(x0, x1, i / max(1, n - 1)); sil(c, x, y, s, hat=hat, pose=pose, face=1 if x < W / 2 else -1, a=a)

# ---------------- 剪影人物 ----------------
def sil(c, x, y, s=1.0, hat='guan', pose='stand', face=1, a=1.0, col=INK, p=1.0, robe=None, t=0):
    """y=脚底。pose: stand offer raise kneel bow lie cry sit throw drink fall"""
    c.save(); c.translate(x, y); c.scale(s * face, s)
    rc = robe if robe else col
    c.set_source_rgba(*col, a)
    if pose == 'lie':
        c.save(); c.rotate(-1.5708 * ease(p)); 
    if pose in ('kneel', 'cry', 'bow'):
        bend = {'kneel': 0.15, 'cry': 0.55, 'bow': 0.9}[pose] * (ease(p) if pose != 'kneel' else 1)
        # 跪姿：袍身低矮
        c.set_source_rgba(*rc, a)
        c.move_to(-55, 0); c.line_to(60, 0); c.curve_to(60, -60, 40, -110, 15, -130); c.line_to(-30, -130); c.curve_to(-50, -90, -60, -40, -55, 0); c.fill()
        c.save(); c.translate(0, -125); c.rotate(bend)
        c.set_source_rgba(*rc, a); poly(c, [(-28, 0), (32, 0), (26, -95), (-22, -95)], rc, a)
        _head(c, 4, -130, hat, a, col)
        # 手臂
        c.set_source_rgba(*rc, a); c.set_line_width(26); c.set_line_cap(1)
        if pose == 'kneel': c.move_to(10, -70); c.line_to(60, -40); c.line_to(85, -60)
        else: c.move_to(10, -70); c.line_to(55, -10)
        c.stroke(); c.restore()
    elif pose == 'sit':
        c.set_source_rgba(*rc, a); poly(c, [(-45, 0), (70, 0), (70, -30), (30, -40), (26, -150), (-30, -150), (-45, -60)], rc, a)
        _head(c, 0, -155, hat, a, col)
        c.set_line_width(26); c.set_line_cap(1); c.move_to(10, -120); c.line_to(55, -80); c.line_to(80, -90); c.stroke()
    else:
        c.set_source_rgba(*rc, a)
        # 长袍
        c.move_to(-42, 0); c.line_to(48, 0); c.curve_to(42, -80, 36, -170, 30, -215); c.line_to(-28, -215); c.curve_to(-36, -160, -44, -80, -42, 0); c.fill()
        _head(c, 2, -222, hat, a, col)
        c.set_source_rgba(*rc, a); c.set_line_width(30); c.set_line_cap(1); c.set_line_join(1)
        q = ease(p)
        if pose == 'stand': c.move_to(14, -195); c.line_to(30, -120); c.line_to(22, -80)
        elif pose == 'offer': c.move_to(14, -195); c.line_to(lerp(30, 70, q), lerp(-120, -150, q)); c.line_to(lerp(22, 110, q), lerp(-80, -155, q))
        elif pose == 'raise': c.move_to(14, -195); c.line_to(lerp(30, 40, q), lerp(-120, -260, q)); c.line_to(lerp(22, 60, q), lerp(-80, -320, q))
        elif pose == 'throw': c.move_to(14, -195); c.line_to(lerp(40, 80, q), lerp(-260, -200, q)); c.line_to(lerp(60, 130, q), lerp(-320, -140, q))
        elif pose == 'drink': c.move_to(14, -195); c.line_to(50, -170); c.line_to(lerp(80, 40, q), lerp(-170, -235, q))
        elif pose == 'point': c.move_to(14, -195); c.line_to(80, -190); c.line_to(140, -200)
        elif pose == 'sword': c.move_to(14, -195); c.line_to(40, -250); c.line_to(55, -300)
        c.stroke()
        # 大袖
        poly(c, [(-10, -200), (-48, -110), (-30, -70), (0, -150)], rc, a)
        if pose == 'sword':
            c.set_source_rgba(0.8, 0.8, 0.85, a); c.set_line_width(6); c.move_to(55, -300); c.line_to(lerp(55, 150, q), lerp(-480, -330, q)); c.stroke()
    if pose == 'lie': c.restore()
    c.restore()

def _head(c, hx, hy, hat, a, col):
    c.set_source_rgba(*col, a); c.arc(hx, hy - 30, 30, 0, 6.28); c.fill()
    c.rectangle(hx - 10, hy - 6, 20, 14); c.fill()
    edge = (0.55, 0.42, 0.30)
    if hat == 'mian':   # 冕旒
        c.rectangle(hx - 8, hy - 78, 16, 22); c.fill()
        c.save(); c.translate(hx, hy - 80); c.rotate(-0.08)
        c.rectangle(-58, -8, 116, 12); c.fill()
        c.set_source_rgba(*edge, 0.5 * a); c.set_line_width(2); c.rectangle(-58, -8, 116, 12); c.stroke()
        c.set_source_rgba(*col, a); c.set_line_width(2)
        for k in range(5):
            xx = 40 + k * 4; c.move_to(xx, 4); c.line_to(xx, 34); c.stroke(); c.arc(xx, 36, 3, 0, 6.28); c.fill()
            xx = -40 - k * 4; c.move_to(xx, 4); c.line_to(xx, 34); c.stroke(); c.arc(xx, 36, 3, 0, 6.28); c.fill()
        c.restore()
    elif hat == 'guan':  # 进贤冠
        poly(c, [(hx - 22, hy - 50), (hx + 20, hy - 54), (hx + 30, hy - 92), (hx - 6, hy - 84)], col, a)
        c.set_source_rgba(*edge, 0.45 * a); c.set_line_width(2); c.move_to(hx - 22, hy - 50); c.line_to(hx + 30, hy - 92); c.stroke()
    elif hat == 'helm':
        c.arc(hx, hy - 36, 34, 3.3, 6.1); c.fill(); c.set_line_width(3); c.move_to(hx, hy - 70); c.line_to(hx - 6, hy - 105); c.stroke()
        c.set_source_rgba(0.75, 0.15, 0.1, a); c.arc(hx - 6, hy - 108, 7, 0, 6.28); c.fill()
    elif hat == 'bun':
        c.arc(hx - 4, hy - 64, 13, 0, 6.28); c.fill()
    elif hat == 'lady':
        c.arc(hx - 8, hy - 66, 18, 0, 6.28); c.fill(); c.arc(hx + 12, hy - 72, 14, 0, 6.28); c.fill()
        c.set_source_rgba(*GOLD, 0.7 * a); c.set_line_width(3); c.move_to(hx - 30, hy - 70); c.line_to(hx + 28, hy - 82); c.stroke()
    elif hat == 'song':  # 宋 直脚幞头
        c.arc(hx, hy - 42, 31, 3.14, 6.28); c.fill(); c.rectangle(hx - 31, hy - 48, 62, 14); c.fill()
        c.set_line_width(5); c.move_to(hx - 30, hy - 44); c.line_to(hx - 105, hy - 44); c.move_to(hx + 30, hy - 44); c.line_to(hx + 105, hy - 44); c.stroke()
        c.set_source_rgba(*edge, 0.5 * a); c.set_line_width(2); c.arc(hx, hy - 42, 31, 3.3, 6.1); c.stroke()
    elif hat == 'xia':   # 西夏 高毡冠
        poly(c, [(hx - 28, hy - 50), (hx + 28, hy - 50), (hx + 18, hy - 110), (hx - 18, hy - 110)], col, a)
        c.set_source_rgba(*GOLD, 0.7 * a); c.set_line_width(3); c.move_to(hx - 27, hy - 58); c.line_to(hx + 27, hy - 58); c.stroke()
    elif hat == 'futou':
        c.arc(hx, hy - 40, 30, 3.2, 6.2); c.fill(); c.set_line_width(5); c.move_to(hx - 26, hy - 44); c.curve_to(hx - 50, hy - 40, hx - 56, hy - 20, hx - 52, hy); c.stroke()

def horse(c, x, y, s, t, a=1, rider='helm', gallop=True):
    c.save(); c.translate(x, y); c.scale(s, s); c.set_source_rgba(*INK, a)
    ph = t * 10 if gallop else 0
    c.save(); c.scale(1, 0.62); c.arc(0, -230, 95, 0, 6.28); c.restore(); c.fill()
    poly(c, [(60, -170), (90, -250), (135, -265), (150, -240), (110, -215), (95, -150)], INK, a)
    c.set_line_width(16); c.set_line_cap(1)
    for i, (lx, o) in enumerate(((-70, 0), (-45, 1.5), (55, 3), (80, 4.5))):
        sw = math.sin(ph + o) * 22
        c.move_to(lx, -130); c.line_to(lx + sw, -60); c.line_to(lx + sw * 1.3, 0); c.stroke()
    c.set_line_width(10); c.move_to(-90, -150); c.curve_to(-130, -140, -140, -100, -150 + math.sin(ph) * 8, -70); c.stroke()
    c.restore()
    if rider: sil(c, x - 5 * s, y - 175 * s, s * 0.75, hat=rider, pose='stand', a=a)

# ---------------- 玉器 ----------------
def stone(c, x, y, s=1, a=1, crack=0, lit=0.3):
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, -10, 170, JADE, 0.25 * lit * a)
    pts = [(-90, 30), (-100, -20), (-60, -70), (0, -85), (55, -65), (95, -25), (85, 30), (20, 50), (-40, 48)]
    poly(c, pts, (0.30, 0.32, 0.30), a)
    poly(c, [(-60, -70), (0, -85), (55, -65), (10, -30), (-40, -35)], (0.42, 0.45, 0.42), a)
    poly(c, [(55, -65), (95, -25), (85, 30), (40, 0)], (0.22, 0.23, 0.22), a)
    if crack > 0:
        c.set_source_rgba(*JADE, a); c.set_line_width(4)
        segs = [(0, -85), (-8, -40), (12, -10), (-5, 25), (8, 50)]
        n = crack * (len(segs) - 1); c.move_to(*segs[0])
        for i in range(1, len(segs)):
            if i <= n: c.line_to(*segs[i])
            else:
                f = n - (i - 1)
                if f > 0: c.line_to(lerp(segs[i - 1][0], segs[i][0], f), lerp(segs[i - 1][1], segs[i][1], f))
                break
        c.stroke(); glow(c, 0, -10, 140, JADE, 0.5 * crack * a)
    c.restore()

def bi(c, x, y, s=1, a=1, lit=1, rot=0):
    """和氏璧：玉璧，带谷纹"""
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, 0, 260, JADE, 0.45 * lit * a)
    g = cairo.RadialGradient(-30, -30, 10, 0, 0, 110)
    g.add_color_stop_rgba(0, 0.90, 0.98, 0.92, a); g.add_color_stop_rgba(1, 0.48, 0.72, 0.60, a)
    c.set_source(g); c.arc(0, 0, 100, 0, 6.28); c.arc_negative(0, 0, 32, 6.28, 0); c.fill()
    c.set_source_rgba(0.35, 0.55, 0.45, 0.6 * a)
    for i in range(18):
        an = i * 6.28 / 18 + rot
        for r in (52, 78):
            c.arc(math.cos(an + r * 0.01) * r, math.sin(an + r * 0.01) * r, 4.5, 0, 6.28); c.fill()
    c.set_line_width(2); c.set_source_rgba(1, 1, 1, 0.5 * a); c.arc(0, 0, 98, 3.6, 5.0); c.stroke()
    c.restore()

def seal(c, x, y, s=1, a=1, lit=1, chip=0, tassel=True, t=0):
    """传国玺：方形玺身 + 盘龙钮（原创造型），chip=缺角并金补"""
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, -40, 300, JADE, 0.5 * lit * a)
    # 玺身（正面+顶面+侧面，轴测）
    poly(c, [(-80, -10), (60, -10), (60, 90), (-80, 90)], (0.70, 0.88, 0.78), a)
    poly(c, [(60, -10), (100, -40), (100, 60), (60, 90)], (0.50, 0.70, 0.60), a)
    poly(c, [(-80, -10), (-40, -40), (100, -40), (60, -10)], (0.84, 0.96, 0.88), a)
    c.set_source_rgba(0.40, 0.62, 0.52, 0.8 * a); c.set_line_width(3); c.rectangle(-66, 4, 112, 72); c.stroke()
    # 盘龙钮
    c.set_source_rgba(0.78, 0.93, 0.84, a)
    c.move_to(-50, -30); c.curve_to(-60, -90, -10, -120, 10, -95); c.curve_to(30, -130, 80, -100, 70, -40)
    c.curve_to(60, -60, 40, -70, 25, -60); c.curve_to(10, -80, -20, -70, -20, -40); c.close_path(); c.fill()
    for (hx, hy) in ((-38, -88), (8, -112), (55, -98)):
        poly(c, [(hx - 8, hy + 8), (hx, hy - 16), (hx + 8, hy + 8)], (0.78, 0.93, 0.84), a)
    c.set_source_rgba(0.2, 0.35, 0.3, a); c.arc(-2, -78, 4, 0, 6.28); c.fill(); c.arc(40, -82, 4, 0, 6.28); c.fill()
    if chip > 0:
        poly(c, [(-80, -10), (-40, -40), (-28, -40), (-80, 8)], (0.95, 0.75, 0.30), a * chip)
        glow(c, -60, -18, 50, GOLD, 0.6 * chip * a)
    if tassel:
        sw = math.sin(t * 2) * 6
        c.set_source_rgba(0.75, 0.10, 0.08, a); c.set_line_width(6)
        c.move_to(70, -60); c.curve_to(110, -40, 120 + sw, 40, 112 + sw, 140); c.stroke()
        poly(c, [(104 + sw, 140), (122 + sw, 140), (128 + sw, 200), (98 + sw, 200)], (0.75, 0.10, 0.08), a)
    c.restore()

def hand(c, x, y, ang, L=520, a=1, col=INK, open_=0.5):
    """从画外伸进来的手臂"""
    c.save(); c.translate(x, y); c.rotate(ang); c.set_source_rgba(*col, a)
    c.move_to(0, -34); c.line_to(L, -20); c.line_to(L, 20); c.line_to(0, 40); c.close_path(); c.fill()
    c.arc(L + 25, 0, 32, 0, 6.28); c.fill()
    c.set_line_width(13); c.set_line_cap(1)
    for k in range(4):
        an = (k - 1.5) * 0.35 * (0.5 + open_)
        c.move_to(L + 40, 0); c.line_to(L + 40 + math.cos(an) * 55, math.sin(an) * 55); c.stroke()
    c.restore()

# ---------------- UI ----------------
import re
def parse(s):
    out = []; mode = None
    for ch in s:
        if ch == '【': mode = 'r'
        elif ch == '〖': mode = 'g'
        elif ch in '】〗': mode = None
        else: out.append((ch, mode))
    return out

def subs(c, s, lt, dur, x=96, y=128, size=None, center=False, gap=1.35):
    lines = s.split('|'); speed = 15.0
    if size is None:
        n = max(len(parse(l)) for l in lines)
        size = int(max(60, min(96, 1150 / max(n, 1))))
    y = y + (size - 60) * 0.6
    k = 0
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    for li, line in enumerate(lines):
        chars = parse(line)
        if center:
            tw = sum(c.text_extents(ch)[4] for ch, _ in chars); xx = W / 2 - tw / 2
        else: xx = x
        yy = y + li * size * gap
        for ch, m in chars:
            ap = cl((lt - k / speed) / 0.22)
            if ap > 0:
                col = (1, 0.97, 0.92) if m is None else (RED if m == 'r' else GOLD)
                if m == 'r': col = (0.95, 0.30, 0.24)
                c.set_source_rgba(0, 0, 0, 0.45 * ap); c.move_to(xx + 1, yy + 2); c.show_text(ch)
                c.set_source_rgba(*col, ap); c.move_to(xx, yy); c.show_text(ch)
            xx += c.text_extents(ch)[4]; k += 1

def tag(c, yr, small, a=1):
    if not yr: return
    c.set_source_rgba(*RED, a); c.rectangle(W - 96 - 0, 0, 0, 0)
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(42)
    w = c.text_extents(yr)[4]
    c.set_source_rgba(*RED, 0.9 * a); c.rectangle(W - 96 - w - 52, 108, 36, 3); c.fill()
    text(c, yr, W - 96, 124, 42, (0.95, 0.92, 0.85), a, 'r')
    if small: text(c, small, W - 96, 172, 30, (0.75, 0.70, 0.62), a * 0.9, 'r', shadow=False)

def counter(c, n, flash, a=1):
    text(c, "死于非命的皇帝", 96, 960, 24, (0.78, 0.72, 0.64), a, shadow=False)
    sc = 1 + 0.35 * flash
    c.save(); c.translate(96, 1040); c.scale(sc, sc)
    w = text(c, str(n), 0, 0, 74, mix((0.95, 0.30, 0.24), (1, 0.9, 0.7), flash), a)
    text(c, "位", w + 10, -4, 30, (0.9, 0.85, 0.78), a, shadow=False)
    c.restore()
    if flash > 0: glow(c, 130, 1010, 160, RED, 0.35 * flash * a)

def vignette(c, s=0.75):
    g = cairo.RadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1150)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, s)
    c.set_source(g); c.paint()

def redflash(c, k):
    if k > 0: c.set_source_rgba(0.7, 0.05, 0.03, 0.45 * k); c.paint()
