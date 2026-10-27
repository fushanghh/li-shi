import math, random
from core import *
from sets import vgrad
from winter import flames, smoke

BARK = (0.46, 0.32, 0.22)
PEEL = (0.96, 0.92, 0.80)


def nightvalley(c, T, hor=760, moon=True):
    vgrad(c, 0, H, (0.04, 0.05, 0.12), (0.14, 0.15, 0.26))
    rnd = random.Random(7)
    for i in range(60):
        rgba(c, (1, 1, 0.9), 0.3 + 0.3 * math.sin(T * 2 + i)); c.arc(rnd.random() * W, rnd.random() * 420, rnd.uniform(1, 2.2), 0, TAU); c.fill()
    if moon:
        c.arc(1700, 160, 44, 0, TAU); rgba(c, (0.98, 0.94, 0.80), 0.9); c.fill()


def slopes(c, a=1.0, gap=520, col=(0.18, 0.15, 0.16)):
    """two steep ridges framing a narrow road in the middle (front view)"""
    cx = W / 2
    for side in (-1, 1):
        c.move_to(cx + side * gap / 2, H)
        c.curve_to(cx + side * (gap / 2 + 80), 760, cx + side * (gap / 2 + 160), 420, cx + side * (gap / 2 + 420), 300)
        c.line_to(cx + side * 1200, 260); c.line_to(cx + side * 1200, H); c.close_path()
        rgba(c, col, a); c.fill()
        c.move_to(cx + side * gap / 2, H)
        c.curve_to(cx + side * (gap / 2 + 80), 760, cx + side * (gap / 2 + 160), 420, cx + side * (gap / 2 + 420), 300)
        rgba(c, (0.55, 0.45, 0.35), a); c.set_line_width(4); c.stroke()
    # road
    c.move_to(cx - gap / 2, H); c.line_to(cx - 40, 640); c.line_to(cx + 40, 640); c.line_to(cx + gap / 2, H); c.close_path()
    rgba(c, (0.36, 0.28, 0.20), a); c.fill()


def tree(c, x, yb, s=1.0, a=1.0, peel=1.0, writing=1.0, lit=0.0):
    c.save(); c.translate(x, yb); c.scale(s, s)
    c.move_to(-60, 0); c.curve_to(-40, -200, -50, -420, -30, -560); c.line_to(30, -560); c.curve_to(50, -420, 40, -200, 70, 0); c.close_path()
    fill2(c, BARK, a, 3, 0.72)
    for (bx, by, ex, ey) in ((0, -440, -330, -580), (0, -500, 330, -620), (0, -330, 300, -440), (0, -360, -280, -460)):
        c.move_to(bx, by); c.curve_to((bx + ex) / 2, by - 30, ex * 0.8, ey + 30, ex, ey)
        rgba(c, BARK, a); c.set_line_width(22); c.stroke()
    for (cx, cy, r) in ((-300, -660, 150), (0, -740, 200), (300, -680, 160), (-150, -580, 130), (170, -580, 140)):
        c.arc(cx, cy, r, 0, TAU); fill2(c, (0.20, 0.32, 0.22), a, 3, 0.75)
    if peel > 0.01:
        rr(c, -38, -420, 76, 380 * peel, 18); rgba(c, PEEL, a); c.fill()
        if writing > 0.01 and peel >= 0.99:
            vtext(c, '龐涓死于此樹之下', 0, -405, 40, (0.15, 0.10, 0.08), a * writing)
    if lit > 0.01:
        glow(c, 0, -230, 300, (1.0, 0.65, 0.30), 0.45 * lit)
    c.restore()


def torch(c, x, y, s=1.0, a=1.0, T=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, 0); c.line_to(0, 120); rgba(c, (0.45, 0.30, 0.18), a); c.set_line_width(12); c.stroke()
    c.restore()
    flames(c, x, y + 4, 50 * s, 80 * s, T, a, seed=2)


def crossbowman(c, x, yf, s=1.0, T=0.0, a=1.0, aim=1.0, side=1, shoot=0.0):
    """kneeling archer silhouette (faceless, small) for crowds"""
    c.save(); c.translate(x, yf); c.scale(s * side, s)
    c.move_to(-40, 0); c.line_to(40, 0); c.line_to(28, -80); c.line_to(-28, -80); c.close_path(); rgba(c, (0.24, 0.30, 0.48), a); c.fill()
    c.arc(0, -108, 28, 0, TAU); rgba(c, (0.85, 0.80, 0.72), a); c.fill()
    c.arc(0, -114, 29, math.pi * 1.05, math.pi * 1.95); c.close_path(); rgba(c, (0.12, 0.12, 0.16), a); c.fill()
    # crossbow
    c.move_to(10, -70); c.line_to(90, -78 - 20 * aim); rgba(c, (0.55, 0.38, 0.22), a); c.set_line_width(8); c.stroke()
    c.move_to(76, -110 - 20 * aim); c.line_to(96, -46 - 20 * aim); rgba(c, (0.40, 0.28, 0.18), a); c.set_line_width(6); c.stroke()
    c.restore()


def arrows(c, T, x0, y0, x1, y1, n=40, prog=1.0, a=1.0, seed=3):
    rnd = random.Random(seed)
    for i in range(n):
        ph = (T * 1.6 + rnd.random()) % 1.0
        if prog < 1 and rnd.random() > prog:
            continue
        sx = x0 + rnd.uniform(-160, 160); sy = y0 + rnd.uniform(-200, 200)
        ex = x1 + rnd.uniform(-220, 220); ey = y1 + rnd.uniform(-100, 100)
        px, py = lerp(sx, ex, ph), lerp(sy, ey, ph) - math.sin(ph * math.pi) * 80
        ang = math.atan2(ey - sy, ex - sx)
        c.move_to(px, py); c.line_to(px - math.cos(ang) * 60, py - math.sin(ang) * 60)
        rgba(c, (0.90, 0.86, 0.76), a); c.set_line_width(3); c.stroke()
        c.move_to(px + math.cos(ang) * 8, py + math.sin(ang) * 8)
        c.line_to(px - math.cos(ang + 0.5) * 10, py - math.sin(ang + 0.5) * 10)
        c.line_to(px - math.cos(ang - 0.5) * 10, py - math.sin(ang - 0.5) * 10); c.close_path(); rgba(c, (0.75, 0.75, 0.80), a); c.fill()


def zao(c, x, yb, s=1.0, a=1.0, T=0.0, fire=True):
    """army field stove: hole in ground with pot"""
    c.save(); c.translate(x, yb); c.scale(s, s)
    ell(c, 0, 0, 70, 22); rgba(c, (0.30, 0.22, 0.16), a); c.fill()
    ell(c, 0, -6, 46, 12); rgba(c, (0.10, 0.07, 0.05), a); c.fill()
    c.restore()
    if fire:
        flames(c, x, yb - 4 * s, 70 * s, 50 * s, T, a, seed=int(x) % 7)
    c.save(); c.translate(x, yb); c.scale(s, s)
    c.arc(0, -36, 40, 0, math.pi); c.close_path(); rgba(c, (0.32, 0.32, 0.36), a); c.fill()
    c.restore()


def cart(c, x, yb, s=1.0, a=1.0, T=0.0, roll=0.0, cover=True):
    """辎车: covered two-wheel cart"""
    c.save(); c.translate(x, yb); c.scale(s, s)
    if cover:
        c.move_to(-200, -150); c.curve_to(-180, -330, 180, -330, 200, -150); c.close_path()
        fill2(c, (0.40, 0.34, 0.28), a, 3, 0.7)
    rr(c, -220, -160, 440, 50, 10); fill2(c, (0.55, 0.36, 0.20), a, 3, 0.7)
    c.move_to(200, -130); c.line_to(420, -110); rgba(c, (0.45, 0.30, 0.18), a); c.set_line_width(12); c.stroke()
    for wx in (-120, 120):
        c.arc(wx, -70, 70, 0, TAU); rgba(c, (0.35, 0.24, 0.14), a); c.set_line_width(12); c.stroke()
        for k in range(6):
            ang = roll + k * math.pi / 3
            c.move_to(wx, -70); c.line_to(wx + math.cos(ang) * 64, -70 + math.sin(ang) * 64); c.set_line_width(5); c.stroke()
    c.restore()


def slip_scroll(c, x, y, w=420, h=300, a=1.0, title='孫臏兵法'):
    n = 14
    for i in range(n):
        rr(c, x - w / 2 + i * w / n, y - h / 2, w / n - 4, h, 3); rgba(c, (0.86, 0.72, 0.44), a); c.fill()
    vtext(c, title, x, y - h / 2 + 30, 44, (0.30, 0.18, 0.10), a)
