import math, random
from core import *
from chibi2 import ped, chibi, horse

PAL = {
    'palace': dict(top=(0.47, 0.15, 0.12), bot=(0.36, 0.11, 0.09), floor=(0.27, 0.15, 0.10)),
    'paper': dict(top=(0.62, 0.52, 0.36), mid=(0.88, 0.80, 0.62), wall=(0.93, 0.87, 0.73), roof=(0.25, 0.26, 0.32),
                  ground=(0.80, 0.72, 0.56), door=(0.40, 0.28, 0.20)),
    'night': dict(top=(0.05, 0.07, 0.17), mid=(0.12, 0.16, 0.33), wall=(0.78, 0.56, 0.30), roof=(0.10, 0.12, 0.22),
                  ground=(0.22, 0.17, 0.15), door=(0.26, 0.16, 0.12)),
    'fest': dict(top=(0.55, 0.20, 0.14), mid=(0.85, 0.62, 0.40), wall=(0.94, 0.85, 0.66), roof=(0.55, 0.42, 0.16),
                 ground=(0.70, 0.55, 0.40), door=(0.45, 0.20, 0.14)),
}


def vgrad(c, y0, y1, c0, c1, x0=0, x1=W):
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgb(0, *c0); g.add_color_stop_rgb(1, *c1)
    c.set_source(g); c.rectangle(x0, y0, x1 - x0, y1 - y0); c.fill()


def lantern(c, x, y, T, s=1.0, a=1.0, string=True, gl=True):
    sw = math.sin(T * 1.6 + x) * 0.05
    c.save(); c.translate(x, y); c.rotate(sw); c.scale(s, s)
    if string:
        c.move_to(0, -400); c.line_to(0, -40); c.set_source_rgba(0.1, 0.07, 0.06, a); c.set_line_width(3); c.stroke()
    if gl:
        glow(c, 0, 0, 170, (1.0, 0.62, 0.30), 0.35 * a)
    ell(c, 0, 0, 44, 38); fill2(c, (0.86, 0.20, 0.15), a, 3, 0.65)
    rgba(c, (0.65, 0.12, 0.10), a); c.set_line_width(2.5)
    for k in (-0.5, 0, 0.5):
        ell(c, 0, 0, 44 * abs(k) + 0.1, 38); c.stroke()
    ell(c, -14, -10, 9, 13); rgba(c, (1, 0.62, 0.50), 0.7 * a); c.fill()
    c.rectangle(-16, -46, 32, 9); rgba(c, (0.25, 0.15, 0.10), a); c.fill()
    c.rectangle(-16, 37, 32, 9); c.fill()
    c.move_to(0, 46); c.line_to(0, 74); rgba(c, (0.95, 0.75, 0.30), a); c.set_line_width(4); c.stroke()
    c.restore()


def palace(c, T, screen=True, win=True, lant=True, floor_y=830, tone=None):
    p = PAL['palace']
    top, bot = (tone or (p['top'], p['bot']))
    vgrad(c, 0, floor_y, top, bot)
    # wall panels
    rgba(c, dk(bot, 0.85), 0.5); c.set_line_width(3)
    for x in range(240, W, 420):
        c.move_to(x, 0); c.line_to(x, floor_y); c.stroke()
    # pillars
    for x in (40, 1830):
        c.rectangle(x, 0, 70, floor_y); rgba(c, (0.70, 0.16, 0.12)); c.fill()
        c.rectangle(x + 8, 0, 14, floor_y); rgba(c, (0.82, 0.26, 0.20)); c.fill()
    if win:
        rr(c, 1500, 110, 300, 420, 6); rgba(c, (0.30, 0.18, 0.12)); c.fill()
        c.rectangle(1522, 132, 256, 376); rgba(c, (0.10, 0.13, 0.28)); c.fill()
        rgba(c, (0.30, 0.18, 0.12)); c.set_line_width(8)
        for k in range(1, 4):
            c.move_to(1522 + k * 64, 132); c.line_to(1522 + k * 64, 508); c.stroke()
        for k, (xx, yy) in enumerate(((1620, 300), (1700, 270), (1760, 330))):
            c.arc(xx, yy, 13, 0, TAU); rgba(c, (0.92, 0.38, 0.22)); c.fill()
    if screen:
        sx, sy, sw_, sh_ = 760, 340, 640, 460
        rr(c, sx - 16, sy - 16, sw_ + 32, sh_ + 16, 6); rgba(c, (0.36, 0.20, 0.10)); c.fill()
        for k in range(4):
            x = sx + k * sw_ / 4
            c.rectangle(x + 5, sy, sw_ / 4 - 10, sh_); rgba(c, (0.80, 0.62, 0.30)); c.fill()
        rgba(c, (0.62, 0.45, 0.20)); c.set_line_width(4)
        c.move_to(sx + 40, sy + 200); c.curve_to(sx + 90, sy + 140, sx + 140, sy + 150, sx + 180, sy + 200)
        c.move_to(sx + 330, sy + 180); c.curve_to(sx + 400, sy + 110, sx + 460, sy + 120, sx + 520, sy + 180)
        c.move_to(sx + 150, sy + 330); c.curve_to(sx + 210, sy + 280, sx + 260, sy + 290, sx + 300, sy + 330)
        c.stroke()
    # floor
    vgrad(c, floor_y, H, p['floor'], dk(p['floor'], 0.7))
    c.rectangle(0, floor_y, W, 6); rgba(c, (0.40, 0.24, 0.14)); c.fill()
    if lant:
        lantern(c, 1760, 330, T, 1.0)
    dust(c, T, 5, 26, (1, 0.85, 0.7), 0.25)


def roofline(c, x0, x1, y, col, h=60):
    c.move_to(x0 - 40, y + 10)
    c.curve_to(x0 + 20, y - 10, x0 + 60, y - h * 0.4, x0 + 120, y - h * 0.5)
    c.line_to(x1 - 120, y - h * 0.5)
    c.curve_to(x1 - 60, y - h * 0.4, x1 - 20, y - 10, x1 + 40, y + 10)
    c.line_to(x1 + 30, y + 22); c.curve_to(x1 - 40, y + 6, x1 - 80, y - 4, x1 - 120, y - 4)
    c.line_to(x0 + 120, y - 4); c.curve_to(x0 + 80, y - 4, x0 + 40, y + 6, x0 - 30, y + 22); c.close_path()
    fill2(c, col, 1, 3, 0.7)


def street(c, T, off=0.0, tone='paper', signs=None, lanterns=False, palace_wall=False, unit=480, ybase=880,
           stalls=False):
    p = PAL[tone]
    vgrad(c, 0, ybase, p['top'], p['mid'])
    if tone == 'night':
        rnd = random.Random(2)
        for i in range(80):
            rgba(c, (1, 1, 0.9), 0.4 + 0.4 * math.sin(T * 2 + i)); c.arc(rnd.random() * W, rnd.random() * 420, rnd.uniform(1, 2.4), 0, TAU); c.fill()
    if palace_wall:
        c.rectangle(0, 318, W, 160); rgba(c, (0.66, 0.20, 0.15)); c.fill()
        c.rectangle(0, 300, W, 24); rgba(c, (0.85, 0.66, 0.22)); c.fill()
        c.rectangle(0, 322, W, 6); rgba(c, (0.55, 0.40, 0.14)); c.fill()
    signs = signs or ['包子', '茶坊', '酒', '羹店']
    n0 = int(math.floor(-off / unit)) - 1
    for k in range(n0, n0 + W // unit + 3):
        x0 = k * unit + off
        x1 = x0 + unit - 30
        # upper floor
        c.rectangle(x0 + 20, 330, unit - 70, 140); rgba(c, dk(p['wall'], 0.93)); c.fill()
        for j in range(2):
            c.rectangle(x0 + 70 + j * 190, 360, 110, 70); rgba(c, dk(p['door'], 1.1)); c.fill()
        roofline(c, x0 + 20, x1, 330, p['roof'], 70)
        c.rectangle(x0, 490, unit - 30, ybase - 490); rgba(c, p['wall']); c.fill()
        rgba(c, dk(p['wall'], 0.8)); c.set_line_width(3); c.rectangle(x0, 490, unit - 30, ybase - 490); c.stroke()
        roofline(c, x0, x1, 490, p['roof'], 50)
        c.rectangle(x0 + 90, 600, unit - 210, ybase - 600); rgba(c, p['door']); c.fill()
        rgba(c, dk(p['door'], 1.25)); c.set_line_width(2)
        for j in range(1, 6):
            c.move_to(x0 + 100, 600 + j * 45); c.line_to(x0 + unit - 130, 600 + j * 45); c.stroke()
        sg = signs[k % len(signs)]
        if not sg:
            if lanterns:
                lantern(c, x0 + 60, 560, T, 0.75)
            continue
        sx = x0 + unit - 110
        sh_ = 70 * len(sg) + 40
        c.rectangle(sx - 34, 520, 68, sh_); rgba(c, (0.97, 0.94, 0.86)); c.fill_preserve()
        rgba(c, (0.55, 0.40, 0.30)); c.set_line_width(3); c.stroke()
        vtext(c, sg, sx, 536, 52, (0.75, 0.15, 0.12))
        if stalls:
            c.rectangle(x0 + 60, ybase - 110, unit - 150, 24); rgba(c, (0.55, 0.32, 0.18)); c.fill()
        if lanterns:
            lantern(c, x0 + 60, 560, T, 0.75)
    vgrad(c, ybase, H, p['ground'], dk(p['ground'], 0.85))
    rgba(c, dk(p['ground'], 0.8)); c.set_line_width(2)
    for k in range(-2, 22):
        xb = k * 110 + (off % 110)
        c.move_to(xb, ybase); c.line_to(xb + (xb - W / 2) * 0.5, H); c.stroke()
    c.rectangle(0, ybase, W, 5); rgba(c, dk(p['ground'], 0.7)); c.fill()
    if tone == 'paper':
        g = cairo.LinearGradient(0, 0, 0, 380)
        g.add_color_stop_rgba(0, 0.25, 0.18, 0.10, 0.55); g.add_color_stop_rgba(1, 0.25, 0.18, 0.10, 0)
        c.set_source(g); c.rectangle(0, 0, W, 380); c.fill()


def darkbg(c, T, col=(0.10, 0.08, 0.09)):
    vgrad(c, 0, H, lt(col, 0.04), dk(col, 0.7))
    dust(c, T, 9, 50, (1, 0.85, 0.5), 0.3)


def brownbg(c, T):
    vgrad(c, 0, H, (0.30, 0.21, 0.15), (0.18, 0.12, 0.09))
    c.rectangle(0, 860, W, H - 860); rgba(c, (0.15, 0.10, 0.08)); c.fill()
    dust(c, T, 4, 40, (1, 0.85, 0.6), 0.25)


def mountains(c, y, col, seed=1, amp=160, n=7, off=0):
    rnd = random.Random(seed)
    c.move_to(-50, H)
    c.line_to(-50, y)
    step = (W + 100) / n
    for i in range(n + 1):
        x = -50 + i * step + off
        c.curve_to(x + step * 0.25, y - amp * rnd.uniform(0.5, 1.0), x + step * 0.55, y - amp * rnd.uniform(0.6, 1.1), x + step, y - amp * rnd.uniform(0.0, 0.3))
    c.line_to(W + 50, H); c.close_path(); rgba(c, col); c.fill()


def passgate(c, T, close=0.0, night=False, plaque='居庸关'):
    if night:
        vgrad(c, 0, 760, (0.05, 0.07, 0.17), (0.14, 0.18, 0.34))
        rnd = random.Random(5)
        for i in range(70):
            rgba(c, (1, 1, .9), 0.4 + 0.3 * math.sin(T * 2 + i)); c.arc(rnd.random() * W, rnd.random() * 500, rnd.uniform(1, 2.2), 0, TAU); c.fill()
        c.arc(1700, 150, 60, 0, TAU); rgba(c, (0.98, 0.92, 0.75)); c.fill()
        m1, m2, wall, stone = (0.12, 0.15, 0.27), (0.17, 0.20, 0.33), (0.36, 0.36, 0.44), (0.30, 0.30, 0.38)
    else:
        vgrad(c, 0, 760, (0.55, 0.30, 0.22), (0.92, 0.66, 0.42))
        glow(c, 1500, 560, 500, (1, 0.8, 0.5), 0.4)
        m1, m2, wall, stone = (0.45, 0.30, 0.26), (0.36, 0.24, 0.22), (0.62, 0.52, 0.44), (0.52, 0.43, 0.36)
    mountains(c, 520, m1, 3, 220, 5)
    mountains(c, 640, m2, 8, 200, 6)
    # wall
    c.rectangle(0, 560, W, 330); rgba(c, wall); c.fill()
    rgba(c, dk(wall, 0.85)); c.set_line_width(2)
    for j in range(6):
        y = 590 + j * 52
        c.move_to(0, y); c.line_to(W, y); c.stroke()
        for i in range(24):
            x = (i * 120 + (60 if j % 2 else 0))
            c.move_to(x, y); c.line_to(x, y + 52); c.stroke()
    for i in range(0, W, 90):
        c.rectangle(i, 520, 55, 42); rgba(c, wall); c.fill()
    # tower
    c.rectangle(650, 360, 620, 200); rgba(c, (0.60, 0.20, 0.16)); c.fill()
    for i in range(6):
        c.rectangle(680 + i * 100, 360, 22, 200); rgba(c, (0.45, 0.14, 0.12)); c.fill()
    roofline(c, 620, 1300, 360, (0.20, 0.20, 0.25), 110)
    rr(c, 860, 400, 200, 70, 6); rgba(c, (0.15, 0.12, 0.25)); c.fill_preserve(); rgba(c, GOLD); c.set_line_width(3); c.stroke()
    text(c, plaque, 960, 452, 42, GOLDL, align='c', shadow=0)
    # arch
    ax, aw, ay = 960, 300, 620
    c.move_to(ax - aw / 2, 890); c.line_to(ax - aw / 2, ay + aw / 2); c.arc(ax, ay + aw / 2, aw / 2, math.pi, TAU); c.line_to(ax + aw / 2, 890); c.close_path()
    rgba(c, (0.07, 0.06, 0.08)); c.fill()
    # doors
    dw = aw / 2 * close
    for sx in (-1, 1):
        x = ax + sx * aw / 2
        c.rectangle(min(x, x - sx * dw), ay + 30, dw, 890 - ay - 30); rgba(c, (0.55, 0.18, 0.12)); c.fill()
        rgba(c, (0.90, 0.72, 0.30))
        for i in range(4):
            for j in range(5):
                xx = x - sx * dw * (i + 0.5) / 4
                if dw > 10:
                    c.arc(xx, ay + 80 + j * 45, 5, 0, TAU); c.fill()
    c.rectangle(0, 880, W, H - 880); rgba(c, dk(stone, 0.8)); c.fill()
    c.rectangle(0, 880, W, 6); rgba(c, dk(stone, 0.6)); c.fill()


def procession(c, T, off, y=880):
    """Qing 骑驾卤簿 marching left->right as faceless figures with props"""
    items = ['spear'] * 4 + ['bow'] * 4 + ['blade'] * 4 + ['canopy'] + ['ped'] * 3 + ['chair'] + ['ped'] * 2 + ['spear'] * 4 + ['banner']
    x = off
    for i, it in enumerate(items):
        wk = T * 1.6 + i * 0.5
        if it == 'canopy':
            c.move_to(x, y - 60); c.line_to(x, y - 430); rgba(c, (0.45, 0.30, 0.18)); c.set_line_width(8); c.stroke()
            c.move_to(x - 120, y - 400); c.curve_to(x - 60, y - 470, x + 60, y - 470, x + 120, y - 400); c.close_path(); fill2(c, (0.96, 0.78, 0.22), 1, 3)
            for k in range(7):
                c.rectangle(x - 118 + k * 34, y - 402, 28, 40); rgba(c, (0.90, 0.68, 0.16)); c.fill()
            ped(c, x, y, 1.0, (0.45, 0.30, 0.22), walk=wk)
            x += 220; continue
        if it == 'chair':
            rr(c, x - 90, y - 300, 180, 200, 14); fill2(c, (0.95, 0.75, 0.22), 1, 3)
            c.rectangle(x - 200, y - 150, 400, 14); rgba(c, (0.50, 0.30, 0.15)); c.fill()
            ped(c, x - 170, y, 0.9, (0.40, 0.30, 0.25), walk=wk); ped(c, x + 170, y, 0.9, (0.40, 0.30, 0.25), walk=wk + 1)
            x += 380; continue
        if it == 'banner':
            c.move_to(x, y - 40); c.line_to(x, y - 520); rgba(c, (0.45, 0.30, 0.18)); c.set_line_width(9); c.stroke()
            c.move_to(x, y - 510); c.line_to(x + 200, y - 470); c.line_to(x + 170, y - 420); c.line_to(x + 200, y - 370); c.line_to(x, y - 330); c.close_path()
            fill2(c, (0.96, 0.78, 0.22), 1, 3)
            c.arc(x + 80, y - 420, 30, 0, TAU); rgba(c, (0.80, 0.25, 0.15)); c.set_line_width(5); c.stroke()
            ped(c, x, y, 1.0, (0.45, 0.30, 0.22), walk=wk)
            x += 260; continue
        col = (0.36, 0.30, 0.36) if it != 'ped' else (0.42, 0.30, 0.26)
        if it == 'spear':
            c.move_to(x + 46, y - 60); c.line_to(x + 46, y - 360); rgba(c, (0.45, 0.30, 0.18)); c.set_line_width(6); c.stroke()
            c.move_to(x + 46, y - 400); c.line_to(x + 36, y - 360); c.line_to(x + 56, y - 360); c.close_path(); rgba(c, (0.85, 0.85, 0.9)); c.fill()
            ell(c, x + 46, y - 345, 14, 22); rgba(c, (0.25, 0.2, 0.18)); c.fill()
        elif it == 'bow':
            c.arc(x + 50, y - 150, 50, -1.2, 1.2); rgba(c, (0.55, 0.35, 0.18)); c.set_line_width(7); c.stroke()
        elif it == 'blade':
            c.move_to(x + 44, y - 70); c.line_to(x + 60, y - 260); rgba(c, (0.85, 0.85, 0.9)); c.set_line_width(9); c.stroke()
        ped(c, x, y, 0.9, col, walk=wk, hatk='nuanmao' if it != 'ped' else 'nuanmao')
        x += 150


def mapbg(c, T, a=1.0):
    vgrad(c, 0, H, (0.10, 0.09, 0.11), (0.06, 0.05, 0.07))
    x0, y0, x1, y1 = 640, 300, 1860, 1050
    rr(c, x0, y0, x1 - x0, y1 - y0, 18); rgba(c, (0.15, 0.13, 0.15)); c.fill_preserve()
    rgba(c, GOLDD); c.set_line_width(4); c.stroke()
    c.save(); rr(c, x0, y0, x1 - x0, y1 - y0, 18); c.clip()
    rgba(c, (0.25, 0.22, 0.25)); c.set_line_width(1.5)
    for x in range(x0, x1, 80):
        c.move_to(x, y0); c.line_to(x, y1); c.stroke()
    for y in range(y0, y1, 80):
        c.move_to(x0, y); c.line_to(x1, y); c.stroke()
    # mountains (军都山/燕山) as triangles band
    rnd = random.Random(4)
    for i in range(36):
        t_ = i / 36
        mx = 700 + t_ * 1000 + rnd.uniform(-30, 30)
        my = 520 + t_ * 120 + rnd.uniform(-90, 90) + (180 if mx > 1500 else 0)
        if mx > 1550 and my > 800:
            continue
        s = rnd.uniform(22, 38)
        c.move_to(mx - s, my + s * 0.6); c.line_to(mx, my - s * 0.8); c.line_to(mx + s, my + s * 0.6); c.close_path()
        rgba(c, (0.32, 0.28, 0.26)); c.fill()
        c.move_to(mx, my - s * 0.8); c.line_to(mx + s * 0.35, my - s * 0.25); c.line_to(mx - s * 0.1, my - s * 0.3); c.close_path()
        rgba(c, (0.55, 0.50, 0.46)); c.fill()
    # great wall zigzag
    pts = [(660, 470), (820, 430), (980, 500), (1140, 470), (1300, 560), (1402, 680), (1500, 620), (1660, 560), (1860, 520)]
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    rgba(c, (0.62, 0.42, 0.30)); c.set_line_width(7); c.set_dash([14, 6]); c.stroke(); c.set_dash([])
    text(c, '长城', 1700, 520, 26, (0.75, 0.55, 0.40), shadow=0)
    c.restore()


MAPPTS = {'北京': (1600, 985), '沙河': (1540, 860), '昌平': (1480, 780), '居庸关': (1402, 680), '宣府': (796, 437)}


def mappin(c, name, a, big=False, col=GOLDL, dx=24, dy=10):
    if a <= 0.01:
        return
    x, y = MAPPTS[name]
    glow(c, x, y, 40, col, 0.6 * a)
    c.arc(x, y, 11 if big else 8, 0, TAU); rgba(c, col, a); c.fill()
    size = 40 if big else 32
    w = tw(c, name, size)
    rr(c, x + dx - 8, y + dy - size * 0.95, w + 20, size * 1.25, 4)
    c.set_source_rgba(0.08, 0.06, 0.05, 0.85 * a); c.fill_preserve(); rgba(c, GOLD, a); c.set_line_width(2); c.stroke()
    text(c, name, x + dx + 2, y + dy, size, WHITE, a, shadow=0)


def route(c, pts, prog, col=REDL, a=1.0, w=6):
    if prog <= 0:
        return
    L = [0]
    for i in range(1, len(pts)):
        L.append(L[-1] + math.dist(pts[i - 1], pts[i]))
    tot = L[-1] * clamp(prog)
    c.move_to(*pts[0])
    end = pts[0]
    for i in range(1, len(pts)):
        if L[i] <= tot:
            c.line_to(*pts[i]); end = pts[i]
        else:
            u = (tot - L[i - 1]) / (L[i] - L[i - 1])
            end = (lerp(pts[i - 1][0], pts[i][0], u), lerp(pts[i - 1][1], pts[i][1], u)); c.line_to(*end); break
    rgba(c, col, a); c.set_line_width(w); c.set_dash([18, 10]); c.stroke(); c.set_dash([])
    c.arc(end[0], end[1], 10, 0, TAU); rgba(c, col, a); c.fill()


def book_page(c, x, y, w, h, lines, hl=None, a=1.0, size=46):
    """old vertical book page; lines right->left; hl=(col_idx, start, n) chars highlighted"""
    rr(c, x, y, w, h, 6); rgba(c, (0.93, 0.86, 0.70), a); c.fill_preserve()
    rgba(c, (0.55, 0.40, 0.25), a); c.set_line_width(4); c.stroke()
    c.rectangle(x + 24, y + 24, w - 48, h - 48); rgba(c, (0.70, 0.30, 0.22), a); c.set_line_width(2); c.stroke()
    cw = (w - 60) / max(len(lines), 1)
    for i, ln in enumerate(lines):
        cx = x + w - 30 - cw * (i + 0.5)
        if i > 0:
            c.move_to(cx + cw / 2, y + 24); c.line_to(cx + cw / 2, y + h - 24); rgba(c, (0.70, 0.30, 0.22), 0.6 * a); c.set_line_width(1.5); c.stroke()
        for j, ch in enumerate(ln):
            colr = (0.18, 0.12, 0.10)
            if hl and hl[0] == i and hl[1] <= j < hl[1] + hl[2]:
                colr = (0.72, 0.12, 0.10)
            font(c, size); wch = c.text_extents(ch)[4]
            rgba(c, colr, a); c.move_to(cx - wch / 2, y + 40 + size + j * size * 1.12); c.show_text(ch)
    c.new_path()


def dangzi(c, x, yb, w, h, flip, T, a=1.0):
    """painted scenery board; flip 0 = front painted, 1 = back (planks + straw bags). rotates around vertical axis"""
    ang = flip * math.pi
    sx = math.cos(ang)
    front = sx >= 0
    c.save(); c.translate(x, yb); c.scale(max(abs(sx), 0.02), 1)
    if front:
        c.rectangle(-w / 2, -h, w, h); rgba(c, (0.60, 0.80, 0.86), a); c.fill()
        c.move_to(-w / 2, -h * 0.3)
        c.curve_to(-w * 0.3, -h * 0.85, -w * 0.15, -h * 0.9, 0, -h * 0.55)
        c.curve_to(w * 0.15, -h * 0.95, w * 0.35, -h * 0.8, w / 2, -h * 0.35); c.line_to(w / 2, 0); c.line_to(-w / 2, 0); c.close_path()
        rgba(c, (0.42, 0.62, 0.42), a); c.fill()
        for k in range(4):
            tx = -w * 0.4 + k * w * 0.27
            c.rectangle(tx - 6, -h * 0.35, 12, h * 0.25); rgba(c, (0.45, 0.30, 0.18), a); c.fill()
            c.arc(tx, -h * 0.42, 36, 0, TAU); rgba(c, (0.25, 0.50, 0.30), a); c.fill()
        c.move_to(-w * 0.15, 0); c.line_to(-w * 0.05, -h * 0.4); c.line_to(w * 0.08, -h * 0.25); c.line_to(w * 0.12, 0); c.close_path()
        rgba(c, (0.60, 0.58, 0.55), a); c.fill()
        c.rectangle(-w / 2, -h, w, h); rgba(c, (0.85, 0.20, 0.15), a); c.set_line_width(10); c.stroke()
    else:
        c.rectangle(-w / 2, -h, w, h); rgba(c, (0.62, 0.45, 0.28), a); c.fill()
        rgba(c, (0.45, 0.30, 0.18), a); c.set_line_width(4)
        for k in range(1, 8):
            c.move_to(-w / 2 + k * w / 8, -h); c.line_to(-w / 2 + k * w / 8, 0); c.stroke()
        c.rectangle(-w / 2 + 10, -h * 0.6, w - 20, 16); rgba(c, (0.40, 0.26, 0.16), a); c.fill()
        c.rectangle(-w / 2 + 10, -h * 0.25, w - 20, 16); c.fill()
        for k in range(5):
            ell(c, -w * 0.38 + k * w * 0.19, -40, 50, 38); fill2(c, (0.80, 0.68, 0.42), a, 3)
            rgba(c, (0.60, 0.48, 0.28), a); c.set_line_width(2)
            c.move_to(-w * 0.38 + k * w * 0.19 - 30, -50); c.line_to(-w * 0.38 + k * w * 0.19 + 30, -30); c.stroke()
    c.restore()


def canal(c, T, off=0):
    vgrad(c, 0, 600, (0.62, 0.52, 0.36), (0.90, 0.82, 0.64))
    mountains(c, 520, (0.70, 0.62, 0.48), 6, 90, 6)
    c.rectangle(0, 600, W, 120); rgba(c, (0.78, 0.70, 0.52)); c.fill()
    vgrad(c, 720, 860, (0.42, 0.58, 0.66), (0.32, 0.46, 0.56))
    rgba(c, (0.75, 0.86, 0.90), 0.6); c.set_line_width(3)
    for k in range(14):
        x = (k * 170 + T * 60 + off) % (W + 200) - 100
        c.move_to(x, 760 + (k % 3) * 30); c.curve_to(x + 20, 752 + (k % 3) * 30, x + 40, 768 + (k % 3) * 30, x + 60, 760 + (k % 3) * 30); c.stroke()
    c.rectangle(0, 860, W, H - 860); rgba(c, (0.80, 0.72, 0.56)); c.fill()
    c.rectangle(0, 860, W, 6); rgba(c, (0.60, 0.50, 0.36)); c.fill()


def boat(c, x, y, s=1.0, a=1.0, T=0):
    c.save(); c.translate(x, y + math.sin(T * 2) * 4); c.scale(s, s)
    c.move_to(-260, -40); c.line_to(260, -40); c.curve_to(230, 10, 200, 20, 160, 24); c.line_to(-180, 24); c.curve_to(-220, 20, -250, 0, -260, -40); c.close_path()
    fill2(c, (0.60, 0.30, 0.16), a, 3)
    c.rectangle(-150, -170, 300, 130); fill2(c, (0.85, 0.24, 0.16), a, 3)
    for k in range(4):
        c.rectangle(-130 + k * 70, -150, 46, 70); rgba(c, (0.98, 0.85, 0.50), a); c.fill()
    roofline(c, -150, 150, -170, (0.92, 0.70, 0.20), 50)
    c.move_to(0, -220); c.line_to(0, -320); rgba(c, (0.45, 0.30, 0.18), a); c.set_line_width(6); c.stroke()
    c.move_to(0, -320); c.line_to(90, -300); c.line_to(0, -270); c.close_path(); rgba(c, (0.95, 0.78, 0.22), a); c.fill()
    c.restore()


def kiosk(c, x, yb, s=1.0, a=1.0):
    c.save(); c.translate(x, yb); c.scale(s, s)
    for sx in (-60, 60):
        c.rectangle(sx - 8, -200, 16, 200); rgba(c, (0.75, 0.18, 0.14), a); c.fill()
    c.move_to(-120, -190); c.curve_to(-60, -220, -30, -280, 0, -320); c.curve_to(30, -280, 60, -220, 120, -190); c.close_path()
    fill2(c, (0.92, 0.70, 0.20), a, 3)
    c.arc(0, -330, 12, 0, TAU); rgba(c, (0.85, 0.20, 0.15), a); c.fill()
    c.rectangle(-40, -90, 80, 90); rgba(c, (0.55, 0.30, 0.18), a); c.fill()
    c.move_to(0, -100); c.line_to(0, -150); rgba(c, (0.6, 0.6, 0.6), 0.7 * a); c.set_line_width(3); c.stroke()
    c.restore()


def icon_grid(c, x0, y0, cols, rows, n, prog, col, cell=26, r=9):
    k = int(n * clamp(prog))
    for i in range(k):
        cx = x0 + (i % cols) * cell; cy = y0 + (i // cols) * cell
        c.arc(cx, cy - r * 0.9, r * 0.55, 0, TAU); rgba(c, lt(col, 0.3)); c.fill()
        c.move_to(cx - r * 0.6, cy - r * 0.3); c.line_to(cx + r * 0.6, cy - r * 0.3); c.line_to(cx + r * 0.85, cy + r * 0.8); c.line_to(cx - r * 0.85, cy + r * 0.8); c.close_path()
        rgba(c, col); c.fill()
