"""南海子 props & backgrounds (flat vector, same-hue dark edges)"""
import math, random
from core import *
from sets import vgrad

MILU = (0.72, 0.46, 0.28)       # 夏毛红棕
MILUD = (0.50, 0.32, 0.20)
ANT = (0.90, 0.82, 0.64)


# ---------------------------------------------------------------- animals
def milu(c, x, yf, s=1.0, T=0.0, a=1.0, run=0.0, expr='calm', flip=False, col=MILU, antler=True, jump=0.0):
    """Q-style 麋鹿 (四不像): horse-like long face, backward-tined antlers, cow hooves, long donkey tail.
    origin = feet centre; faces right (flip -> left). s=1 ~ 330px tall incl. antlers."""
    if a <= 0.01 or s <= 0.01:
        return
    c.save()
    bob = abs(math.sin(run * math.pi)) * 14 if run else math.sin(T * 2.2) * 2
    c.translate(x, yf - bob - jump); c.scale(-s if flip else s, s)
    # shadow
    ell(c, 0, 4 + bob / s + jump / s, 130, 14); c.set_source_rgba(0, 0, 0, 0.22 * a); c.fill()
    dark = dk(col, 0.70)
    # legs
    for i, (lx, ph) in enumerate(((-78, 0), (-50, 1), (52, 1), (82, 0))):
        sw = math.sin(run * math.pi * 2 + ph * math.pi) * 22 if run else 0
        back = i in (0, 2)
        lc = dk(col, 0.82) if back else col
        c.move_to(lx, -100); c.line_to(lx + sw, -14)
        rgba(c, lc, a); c.set_line_width(32); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        ell(c, lx + sw + 4, -8, 18, 10); rgba(c, (0.20, 0.15, 0.12), a); c.fill()   # wide cow hoof
        c.move_to(lx + sw + 4, -18); c.line_to(lx + sw + 4, 0); rgba(c, (0.45, 0.36, 0.30), a); c.set_line_width(2); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    # tail (long, donkey-like, black tuft) swishes
    tw_ = math.sin(T * 3.2) * 18
    c.move_to(-122, -160); c.curve_to(-150, -150, -160 + tw_ * 0.4, -110, -158 + tw_, -68)
    rgba(c, dark, a); c.set_line_width(12); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    ell(c, -158 + tw_, -60, 12, 22); rgba(c, (0.15, 0.11, 0.10), a); c.fill()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    # body
    ell(c, 0, -140, 132, 72); fill2(c, col, a, 3, 0.72)
    ell(c, 6, -106, 96, 28); rgba(c, lt(col, 0.28), a * 0.8); c.fill()
    # neck (camel-ish long)
    c.move_to(58, -186); c.curve_to(88, -220, 100, -245, 112, -268)
    c.line_to(156, -252); c.curve_to(138, -222, 128, -190, 112, -130); c.close_path()
    fill2(c, col, a, 3, 0.72)
    # head (long horse face)
    hx, hy = 150, -282
    c.save(); c.translate(hx, hy); c.rotate(0.28 + math.sin(T * 1.7) * 0.03); c.scale(1.35, 1.35)
    # antlers (main beam up, tines pointing BACK)
    if antler:
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        for sx, off in ((1, 0), (-1, 10)):
            ac = ANT if sx == 1 else dk(ANT, 0.82)
            c.move_to(-6 + off, -34); c.curve_to(-4 + off, -80, -16 + off, -120, -6 + off, -160)
            rgba(c, ac, a); c.set_line_width(13); c.stroke()
            for (bx, by, ex, ey) in ((-5, -70, -58, -92), (-10, -108, -62, -138), (-8, -140, -46, -176)):
                c.move_to(bx + off, by); c.curve_to(bx - 18 + off, by - 6, ex + 14 + off, ey + 8, ex + off, ey)
                c.set_line_width(9); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_BUTT)
    # ear
    ell(c, -30, -30, 12, 24); fill2(c, dk(col, 0.9), a, 2.5, 0.72)
    # face
    c.move_to(-46, -18); c.curve_to(-44, -50, 10, -52, 40, -30)
    c.curve_to(78, -16, 96, 0, 92, 20); c.curve_to(86, 40, 40, 40, 10, 34)
    c.curve_to(-30, 30, -50, 14, -46, -18); c.close_path()
    fill2(c, lt(col, 0.12), a, 3, 0.72)
    ell(c, 78, 16, 16, 13); rgba(c, dk(col, 0.6), a); c.fill()       # nose
    rgba(c, (0.15, 0.10, 0.09), a)
    c.arc(84, 12, 3, 0, TAU); c.fill()
    # eye
    ex_, ey_ = -2, -10
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    blink = (T % 3.7) > 3.58 and expr == 'calm'
    if expr in ('happy',) or blink:
        c.move_to(ex_ - 10, ey_ + 2); c.curve_to(ex_ - 5, ey_ - 7, ex_ + 5, ey_ - 7, ex_ + 10, ey_ + 2)
        rgba(c, (0.12, 0.08, 0.07), a); c.set_line_width(4.5); c.stroke()
    elif expr == 'shock':
        c.arc(ex_, ey_, 14, 0, TAU); rgba(c, (1, 1, 1), a); c.fill_preserve(); rgba(c, (0.12, 0.08, 0.07), a); c.set_line_width(3); c.stroke()
        c.arc(ex_, ey_, 6, 0, TAU); rgba(c, (0.12, 0.08, 0.07), a); c.fill()
    elif expr == 'sad':
        c.arc(ex_, ey_ + 2, 7, 0, TAU); rgba(c, (0.12, 0.08, 0.07), a); c.fill()
        ell(c, ex_ + 4, ey_ + 16 + (T * 30 % 20), 4, 6); rgba(c, (0.45, 0.72, 0.98), a); c.fill()
    else:
        c.arc(ex_, ey_, 9, 0, TAU); rgba(c, (0.12, 0.08, 0.07), a); c.fill()
        c.arc(ex_ + 3, ey_ - 3, 3, 0, TAU); rgba(c, (1, 1, 1), a); c.fill()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    ell(c, 18, 12, 11, 7); rgba(c, (0.97, 0.62, 0.64), 0.8 * a); c.fill()   # blush
    if expr == 'happy':
        c.move_to(46, 26); c.curve_to(54, 34, 64, 34, 70, 26); rgba(c, (0.25, 0.12, 0.10), a); c.set_line_width(3); c.stroke()
    c.restore()
    c.restore()


def falcon(c, x, y, s=1.0, T=0.0, a=1.0, flap=True, flip=False):
    """海东青: white-grey hawk"""
    if a <= 0.01 or s <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    w = math.sin(T * 14) * 0.6 if flap else 0.25
    col = (0.92, 0.92, 0.94)
    for sx, k in ((-1, 0.85), (1, 1.0)):
        c.save(); c.rotate(-w * sx * 0.0); c.scale(1, 1)
        c.move_to(-6, -6); c.curve_to(-30, -40 - w * 60 * k, -80, -50 - w * 70 * k, -110, -30 - w * 80 * k)
        c.curve_to(-70, -10, -40, 4, -6, 6); c.close_path()
        fill2(c, dk(col, k), a, 2.5, 0.65); c.restore()
    ell(c, 0, 0, 40, 18); fill2(c, col, a, 2.5, 0.65)
    c.move_to(-36, -2); c.line_to(-64, -10); c.line_to(-62, 12); c.close_path(); fill2(c, dk(col, 0.85), a, 2, 0.65)
    c.arc(34, -10, 16, 0, TAU); fill2(c, col, a, 2.5, 0.65)
    c.move_to(46, -12); c.line_to(60, -6); c.line_to(46, -2); c.close_path(); rgba(c, (0.95, 0.75, 0.25), a); c.fill()
    c.arc(38, -14, 3.5, 0, TAU); rgba(c, (0.1, 0.08, 0.07), a); c.fill()
    for k in range(3):
        c.move_to(-14 + k * 12, -4); c.line_to(-8 + k * 12, 4); rgba(c, (0.55, 0.55, 0.60), a); c.set_line_width(2); c.stroke()
    c.restore()


def goose(c, x, y, s=1.0, T=0.0, a=1.0, fly=True, flip=False):
    """天鹅/大雁 white"""
    if a <= 0.01 or s <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    col = (0.98, 0.97, 0.94)
    w = math.sin(T * 9 + x) * 0.7 if fly else -0.6
    c.move_to(-10, -4); c.curve_to(-30, -40 - w * 50, -70, -46 - w * 60, -96, -30 - w * 70); c.curve_to(-60, -6, -30, 6, -10, 6); c.close_path()
    fill2(c, dk(col, 0.88), a, 2.5, 0.75)
    ell(c, 0, 0, 44, 18); fill2(c, col, a, 2.5, 0.75)
    c.move_to(30, -6); c.curve_to(52, -12, 58, -30, 70, -34); rgba(c, col, a); c.set_line_width(11); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.arc(72, -36, 10, 0, TAU); fill2(c, col, a, 2, 0.75)
    c.move_to(80, -38); c.line_to(96, -34); c.line_to(80, -30); c.close_path(); rgba(c, (0.95, 0.55, 0.20), a); c.fill()
    c.arc(74, -39, 2.5, 0, TAU); rgba(c, (0.1, 0.08, 0.07), a); c.fill()
    c.restore()


def plane(c, x, y, s=1.0, a=1.0, rot=0.0):
    """generic white airliner, no markings"""
    if a <= 0.01 or s <= 0.01:
        return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    col = (0.96, 0.96, 0.98)
    c.move_to(-120, -10); c.line_to(-150, -60); c.line_to(-120, -60); c.line_to(-80, -14); c.close_path(); fill2(c, dk(col, 0.86), a, 2.5, 0.7)
    rr(c, -150, -18, 300, 40, 20); fill2(c, col, a, 2.5, 0.7)
    c.move_to(150, 2); c.curve_to(180, 2, 180, -10, 150, -16); fill2(c, col, a, 2.5, 0.7)
    c.move_to(-20, 4); c.line_to(-70, 70); c.line_to(-40, 70); c.line_to(40, 8); c.close_path(); fill2(c, dk(col, 0.9), a, 2.5, 0.7)
    for k in range(7):
        c.arc(-80 + k * 30, -4, 5, 0, TAU); rgba(c, (0.45, 0.60, 0.80), a); c.fill()
    c.restore()


# ---------------------------------------------------------------- scenery
def field(c, T, sky=((0.96, 0.66, 0.36), (0.99, 0.86, 0.56)), ground=(0.78, 0.62, 0.30), hor=640, trees=True, sun=True):
    """南囿秋风: golden autumn grassland"""
    vgrad(c, 0, hor, sky[0], sky[1])
    if sun:
        glow(c, 1500, 330, 300, (1, 0.95, 0.7), 0.55)
        c.arc(1500, 330, 70, 0, TAU); rgba(c, (1, 0.95, 0.78), 0.9); c.fill()
    # far tree line
    if trees:
        rnd = random.Random(3)
        for i in range(40):
            tx = i * 52 + rnd.uniform(-10, 10); r = rnd.uniform(26, 44)
            c.arc(tx, hor - r * 0.4, r, 0, TAU); rgba(c, (0.62, 0.48, 0.26)); c.fill()
    vgrad(c, hor, H, lt(ground, 0.08), dk(ground, 0.82))
    rnd = random.Random(7)
    for i in range(70):
        gx = rnd.uniform(0, W); gy = rnd.uniform(hor + 20, H)
        sz = 6 + (gy - hor) / 30
        sw_ = math.sin(T * 1.5 + gx * 0.01) * sz * 0.4
        rgba(c, dk(ground, 0.75), 0.7); c.set_line_width(2.5)
        for k in (-1, 0, 1):
            c.move_to(gx + k * sz * 0.4, gy); c.line_to(gx + k * sz * 0.8 + sw_, gy - sz * 1.6); c.stroke()


def reeds(c, T, y0, n=26, seed=5, col=(0.62, 0.52, 0.30), hmin=90, hmax=180, x0=0, x1=W):
    rnd = random.Random(seed)
    for i in range(n):
        rx = rnd.uniform(x0, x1); h = rnd.uniform(hmin, hmax)
        sw_ = math.sin(T * 1.4 + rx * 0.02) * 12
        c.move_to(rx, y0); c.curve_to(rx, y0 - h * 0.5, rx + sw_ * 0.5, y0 - h * 0.8, rx + sw_, y0 - h)
        rgba(c, col); c.set_line_width(4); c.stroke()
        ell(c, rx + sw_, y0 - h - 16, 7, 22); rgba(c, lt(col, 0.25)); c.fill()


def marsh(c, T, sky=((0.55, 0.75, 0.88), (0.86, 0.92, 0.90)), hor=600, warm=False):
    """海子湿地: sky, water bands, reeds"""
    vgrad(c, 0, hor, sky[0], sky[1])
    c.rectangle(0, hor, W, H - hor); rgba(c, (0.55, 0.62, 0.40) if not warm else (0.70, 0.60, 0.36)); c.fill()
    # water lakes
    for (wx, wy, rx, ry) in ((520, 760, 560, 70), (1500, 700, 520, 52), (1100, 930, 700, 60)):
        ell(c, wx, wy, rx, ry); rgba(c, (0.40, 0.62, 0.78)); c.fill()
        ell(c, wx - rx * 0.2, wy - ry * 0.25, rx * 0.5, ry * 0.18); rgba(c, (0.70, 0.85, 0.94), 0.6); c.fill()
        for k in range(3):
            xx = wx - rx * 0.6 + k * rx * 0.5 + math.sin(T + k) * 10
            c.move_to(xx, wy + ry * 0.1); c.line_to(xx + 60, wy + ry * 0.1); rgba(c, (0.85, 0.94, 1.0), 0.7); c.set_line_width(3); c.stroke()
    reeds(c, T, hor + 30, 30, 2, (0.52, 0.50, 0.28), 60, 120)


def nightbg(c, T, hor=760):
    vgrad(c, 0, hor, (0.06, 0.09, 0.22), (0.16, 0.22, 0.42))
    c.arc(1580, 220, 60, 0, TAU); rgba(c, (1, 0.96, 0.84)); c.fill()
    glow(c, 1580, 220, 220, (0.9, 0.9, 1), 0.25)
    rnd = random.Random(11)
    for i in range(60):
        sx, sy = rnd.uniform(0, W), rnd.uniform(0, hor - 100)
        rgba(c, (1, 1, 1), 0.4 + 0.4 * math.sin(T * 3 + i)); c.arc(sx, sy, rnd.uniform(1, 2.6), 0, TAU); c.fill()
    vgrad(c, hor, H, (0.18, 0.20, 0.26), (0.10, 0.11, 0.16))


def parkbg(c, T, hor=640):
    """今天：城市天际线 + 绿色湿地"""
    vgrad(c, 0, hor, (0.52, 0.76, 0.95), (0.86, 0.94, 0.98))
    rnd = random.Random(21)
    x = -20
    while x < W:
        bw = rnd.uniform(60, 130); bh = rnd.uniform(120, 300)
        rr(c, x, hor - bh, bw - 10, bh, 4); rgba(c, (0.68, 0.78, 0.88)); c.fill()
        for wy in range(int(hor - bh + 20), int(hor - 10), 26):
            c.rectangle(x + 10, wy, bw - 30, 8); rgba(c, (0.80, 0.88, 0.95)); c.fill()
        x += bw
    c.rectangle(0, hor, W, H - hor); rgba(c, (0.46, 0.70, 0.40)); c.fill()
    ell(c, 980, 820, 820, 90); rgba(c, (0.42, 0.66, 0.84)); c.fill()
    ell(c, 760, 800, 300, 22); rgba(c, (0.75, 0.88, 0.96), 0.6); c.fill()
    # boardwalk
    c.move_to(0, 960); c.curve_to(500, 900, 1200, 1010, W, 930); c.line_to(W, 990); c.curve_to(1200, 1070, 500, 960, 0, 1020); c.close_path()
    fill2(c, (0.78, 0.60, 0.40), 1, 3, 0.75)
    reeds(c, T, hor + 40, 20, 8, (0.36, 0.56, 0.30), 50, 100)


def wall(c, x0, x1, yb, h=120, col=(0.72, 0.30, 0.22), a=1.0, brick=True):
    """苑墙 red wall with grey coping"""
    c.rectangle(x0, yb - h, x1 - x0, h); fill2(c, col, a, 3, 0.75)
    if brick:
        rgba(c, dk(col, 0.82), a); c.set_line_width(2)
        for k, yy in enumerate(range(int(yb - h + 22), int(yb), 22)):
            c.move_to(x0, yy); c.line_to(x1, yy); c.stroke()
    c.move_to(x0 - 14, yb - h); c.line_to(x0 + 6, yb - h - 26); c.line_to(x1 - 6, yb - h - 26); c.line_to(x1 + 14, yb - h); c.close_path()
    fill2(c, (0.30, 0.30, 0.34), a, 3, 0.7)


def gate(c, x, yb, s=1.0, a=1.0, plaque='大红门'):
    """苑门：three-arch red gate with yellow roof"""
    if a <= 0.01 or s <= 0.01:
        return
    c.save(); c.translate(x, yb); c.scale(s, s)
    c.rectangle(-230, -230, 460, 230); fill2(c, (0.74, 0.22, 0.17), a, 3, 0.72)
    for ax in (-140, 0, 140):
        w_ = 70 if ax == 0 else 56
        c.move_to(ax - w_, 0); c.line_to(ax - w_, -110); c.arc(ax, -110, w_, math.pi, TAU); c.line_to(ax + w_, 0); c.close_path()
        rgba(c, (0.22, 0.12, 0.10), a); c.fill()
    c.move_to(-280, -230); c.line_to(-220, -310); c.line_to(220, -310); c.line_to(280, -230); c.close_path()
    fill2(c, (0.95, 0.74, 0.22), a, 3, 0.7)
    rgba(c, dk((0.95, 0.74, 0.22), 0.75), a); c.set_line_width(2.5)
    for k in range(-9, 10):
        c.move_to(k * 26, -306); c.line_to(k * 29, -234); c.stroke()
    rr(c, -80, -214, 160, 54, 6); fill2(c, (0.18, 0.20, 0.36), a, 3, 0.7)
    text(c, plaque, 0, -175, 36, GOLDL, a, align='c', shadow=0)
    c.restore()


def platform(c, x, yb, s=1.0, a=1.0, label=None):
    """晾鹰台: earthen terraced mound with grass top"""
    if a <= 0.01 or s <= 0.01:
        return
    c.save(); c.translate(x, yb); c.scale(s, s)
    c.move_to(-330, 0); c.line_to(-200, -180); c.line_to(200, -180); c.line_to(330, 0); c.close_path()
    fill2(c, (0.74, 0.58, 0.36), a, 3, 0.75)
    c.move_to(-265, -90); c.line_to(265, -90); rgba(c, dk((0.74, 0.58, 0.36), 0.85), a); c.set_line_width(4); c.stroke()
    ell(c, 0, -182, 205, 18); rgba(c, (0.55, 0.62, 0.30), a); c.fill()
    # yellow tent (幄殿)
    c.move_to(-70, -184); c.line_to(0, -270); c.line_to(70, -184); c.close_path(); fill2(c, (0.96, 0.78, 0.26), a, 3, 0.7)
    c.move_to(0, -270); c.line_to(0, -300); rgba(c, (0.6, 0.2, 0.15), a); c.set_line_width(4); c.stroke()
    c.move_to(0, -300); c.line_to(40, -290); c.line_to(0, -280); c.close_path(); rgba(c, (0.85, 0.2, 0.15), a); c.fill()
    c.restore()
    if label:
        tagbox(c, label, x, yb - 330 * s, a)


def tagbox(c, s_, x, y, a=1.0, col=GOLDL, size=40):
    if a <= 0.01:
        return
    w = tw(c, s_, size) + 30
    rr(c, x - w / 2, y - size * 0.95, w, size * 1.35, 8)
    c.set_source_rgba(0.12, 0.08, 0.06, 0.92 * a); c.fill_preserve(); rgba(c, col, a); c.set_line_width(3); c.stroke()
    text(c, s_, x, y + size * 0.12, size, col, a, align='c', shadow=0)


def hall(c, x, yb, s=1.0, a=1.0, roof=(0.95, 0.74, 0.22), wallc=(0.78, 0.24, 0.18), label=None):
    """行宫 small hall"""
    if a <= 0.01 or s <= 0.01:
        return
    c.save(); c.translate(x, yb); c.scale(s, s)
    c.rectangle(-210, -30, 420, 30); fill2(c, (0.80, 0.76, 0.70), a, 3, 0.75)
    c.rectangle(-170, -190, 340, 160); fill2(c, wallc, a, 3, 0.75)
    for k in range(-2, 3):
        rr(c, k * 64 - 22, -170, 44, 130, 4); rgba(c, (0.35, 0.18, 0.12), a); c.fill()
        rgba(c, (0.95, 0.75, 0.40), a * 0.8); c.set_line_width(2)
        for j in range(4):
            c.move_to(k * 64 - 16, -160 + j * 30); c.line_to(k * 64 + 16, -160 + j * 30); c.stroke()
    c.move_to(-250, -180); c.curve_to(-200, -200, -170, -240, -150, -280); c.line_to(150, -280)
    c.curve_to(170, -240, 200, -200, 250, -180); c.close_path(); fill2(c, roof, a, 3, 0.7)
    c.rectangle(-160, -292, 320, 16); fill2(c, dk(roof, 0.85), a, 2, 0.7)
    c.restore()
    if label:
        tagbox(c, label, x, yb - 330 * s, a)


def waves(c, T, y, amp=26, col=(0.42, 0.55, 0.62), a=1.0, k=0.012, speed=3.0):
    c.move_to(-10, H + 10)
    for xx in range(-10, W + 30, 20):
        c.line_to(xx, y + math.sin(xx * k + T * speed) * amp)
    c.line_to(W + 30, H + 10); c.close_path()
    rgba(c, col, a); c.fill()
    for xx in range(0, W, 90):
        yy = y + math.sin(xx * k + T * speed) * amp
        c.arc(xx, yy, 14, math.pi, TAU); rgba(c, (0.88, 0.94, 0.96), a * 0.8); c.set_line_width(5); c.stroke()


def citytile(c, x, y, s=1.0, a=1.0, col=(0.62, 0.62, 0.66), label='北京城'):
    """凸-shaped old Beijing (inner + outer city) icon"""
    if a <= 0.01 or s <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-70, -90); c.line_to(70, -90); c.line_to(70, 10); c.line_to(90, 10); c.line_to(90, 64); c.line_to(-90, 64)
    c.line_to(-90, 10); c.line_to(-70, 10); c.close_path()
    fill2(c, col, a, 4, 0.7)
    rgba(c, dk(col, 0.7), a); c.set_line_width(3)
    rr(c, -24, -40, 48, 40, 3); c.stroke()
    c.restore()
    if label:
        otext(c, label, x, y + 110 * s, 34 * max(s, 0.6), WHITE, a, align='c')


def coin(c, x, y, s=1.0, a=1.0):
    if a <= 0.01 or s <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.arc(0, 0, 30, 0, TAU); fill2(c, (0.96, 0.80, 0.30), a, 3, 0.7)
    c.rectangle(-9, -9, 18, 18); rgba(c, (0.55, 0.40, 0.12), a); c.fill()
    c.restore()


def crate(c, x, y, s=1.0, a=1.0, label=None):
    if a <= 0.01 or s <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -70, -50, 140, 100, 8); fill2(c, (0.72, 0.54, 0.34), a, 3, 0.72)
    rgba(c, dk((0.72, 0.54, 0.34), 0.7), a); c.set_line_width(4)
    c.move_to(-70, -50); c.line_to(70, 50); c.move_to(70, -50); c.line_to(-70, 50); c.stroke()
    c.restore()
    if label:
        tagbox(c, label, x, y - 80 * s, a, size=32)


def ship(c, x, y, s=1.0, a=1.0, T=0.0):
    if a <= 0.01 or s <= 0.01:
        return
    c.save(); c.translate(x, y + math.sin(T * 2) * 6); c.rotate(math.sin(T * 1.6) * 0.03); c.scale(s, s)
    c.move_to(-200, -40); c.line_to(200, -40); c.line_to(150, 30); c.line_to(-160, 30); c.close_path()
    fill2(c, (0.36, 0.26, 0.20), a, 3, 0.7)
    c.move_to(-10, -40); c.line_to(-10, -260); rgba(c, (0.30, 0.22, 0.16), a); c.set_line_width(8); c.stroke()
    c.move_to(-4, -250); c.curve_to(90, -200, 100, -120, -4, -60); c.close_path(); fill2(c, (0.96, 0.94, 0.88), a, 3, 0.8)
    c.move_to(-16, -230); c.curve_to(-90, -190, -100, -120, -16, -70); c.close_path(); fill2(c, (0.92, 0.90, 0.84), a, 3, 0.8)
    c.restore()


def dotgrid(c, x0, y0, cols, n, prog, col, cell=46, r=15, T=0.0):
    """tiny deer-head dots that pop one by one"""
    for i in range(n):
        p = back(seg(prog * n - i, 0, 1))
        if p <= 0.01:
            continue
        cx = x0 + (i % cols) * cell; cy = y0 + (i // cols) * cell
        c.arc(cx, cy, r * p, 0, TAU); fill2(c, col, 1, 2, 0.7)
