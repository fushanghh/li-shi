"""Paternity video helpers: dark backdrops, era buildings, court, props."""
from qing import *
from chibi import chibi

INKP = (0.16, 0.10, 0.07)
PAPER = (0.93, 0.87, 0.72)
BLOOD = (0.78, 0.08, 0.08)
BLOODL = (0.95, 0.20, 0.16)
WATER = (0.45, 0.62, 0.72)
SIL1 = (0.16, 0.12, 0.085)
SIL2 = (0.25, 0.18, 0.12)
SIL3 = (0.33, 0.23, 0.14)
CREAMP = (0.79, 0.71, 0.56)

_dust2 = [(random.Random(k * 3).uniform(0, W), random.Random(k * 7 + 1).uniform(0, H),
           random.Random(k + 11).uniform(1.0, 2.8), random.Random(k + 31).uniform(0, 6.28)) for k in range(70)]

TONES = {'brown': ((0.20, 0.13, 0.08), (0.06, 0.045, 0.035)),
         'red': ((0.30, 0.09, 0.06), (0.07, 0.03, 0.025)),
         'blue': ((0.10, 0.13, 0.24), (0.03, 0.035, 0.07))}


def bgp(c, T, sx=1100, sy=620, sr=900, tone='brown', dust=True, light=1.0):
    a0, a1 = TONES[tone]
    g = cairo.RadialGradient(sx, sy, 30, sx, sy, max(sr * 1.5, 1300))
    g.add_color_stop_rgb(0, *a0); g.add_color_stop_rgb(1, *a1)
    c.set_source(g); c.paint()
    if light > 0:
        spot(c, sx, sy, sr, 0.9 * light)
    if dust:
        for (x, y, r, ph) in _dust2:
            yy = (y - T * 10 * r) % H; xx = x + 10 * math.sin(T * 0.4 + ph)
            rgba(c, GOLDL, 0.18 + 0.15 * math.sin(T * 1.2 + ph * 3)); c.arc(xx, yy, r * 0.7, 0, 6.283); c.fill()


def ground(c, y=900, col=(0.09, 0.065, 0.045)):
    rgba(c, col); c.rectangle(-200, y, W + 400, H - y + 300); c.fill()
    g = cairo.LinearGradient(0, 0, W, 0)
    for u, al in ((0, 0.0), (0.25, 0.6), (0.75, 0.6), (1, 0.0)):
        g.add_color_stop_rgba(u, GOLD[0], GOLD[1], GOLD[2], al)
    c.set_source(g); c.rectangle(-200, y, W + 400, 3); c.fill()


def hills(c, T, ybase=760, cols=(SIL1, SIL2), seed=0):
    for k, col in enumerate(cols):
        yb = ybase - 120 + k * 90
        c.move_to(-200, H)
        for x in range(-200, W + 241, 40):
            y = yb + 60 * math.sin(x * 0.003 + k * 1.7 + seed) + 30 * math.sin(x * 0.009 + k + seed * 2)
            c.line_to(x, y)
        c.line_to(W + 240, H); c.close_path(); rgba(c, col); c.fill_preserve()
        rgba(c, GOLD, 0.25); c.set_line_width(1.5); c.stroke()


# ------------------------------------------------------------- era buildings
def _roofline(c, w, y, h, era):
    """eave line at y (bottom), roof height h, width w, centred at 0"""
    up = {'qinhan': 4, 'nanbei': 6, 'song': 16, 'ming': 22, 'qing': 22}.get(era, 14)
    e = w / 2 + 26
    c.move_to(-e, y - up)
    c.curve_to(-e + 30, y + 2, -e + 60, y + 4, -w / 2 + 40, y + 4)
    c.line_to(w / 2 - 40, y + 4)
    c.curve_to(e - 60, y + 4, e - 30, y + 2, e, y - up)
    c.line_to(w / 2 - 70, y - h); c.line_to(-w / 2 + 70, y - h); c.close_path()


def bldg(c, x, yf, w=420, h=240, era='ming', a=1.0, lit=0.6, T=0, col=SIL2, roofc=SIL1, plaque=None, door=True, tiers=1):
    if a <= 0: return
    c.save(); c.translate(x, yf)
    rgba(c, tuple(v * 0.8 for v in col), a); c.rectangle(-w / 2 - 20, -22, w + 40, 22); c.fill()  # platform
    rgba(c, col, a); c.rectangle(-w / 2, -h, w, h - 22); c.fill()
    rgba(c, GOLD, 0.35 * a); c.set_line_width(1.5); c.rectangle(-w / 2, -h, w, h - 22); c.stroke()
    # pillars
    n = max(3, int(w / 110))
    for k in range(n + 1):
        xx = -w / 2 + 10 + (w - 20) * k / n
        rgba(c, (0.30, 0.10, 0.07), a); c.rectangle(xx - 6, -h, 12, h - 22); c.fill()
    # windows
    for k in range(n):
        xx = -w / 2 + 10 + (w - 20) * (k + 0.5) / n
        if door and k == n // 2:
            rgba(c, (0.05, 0.03, 0.02), a); c.rectangle(xx - 32, -h * 0.62, 64, h * 0.62 - 22); c.fill()
            if lit > 0:
                rgba(c, (1, 0.72, 0.38), 0.25 * lit * a); c.rectangle(xx - 32, -h * 0.62, 64, h * 0.62 - 22); c.fill()
            continue
        ww = min(70, (w - 20) / n - 30)
        rgba(c, (0.95, 0.66, 0.32), (0.30 + 0.45 * lit) * a); c.rectangle(xx - ww / 2, -h * 0.68, ww, h * 0.36); c.fill()
        rgba(c, (0.20, 0.10, 0.06), a); c.set_line_width(2)
        for j in range(1, 4):
            c.move_to(xx - ww / 2 + ww * j / 4, -h * 0.68); c.line_to(xx - ww / 2 + ww * j / 4, -h * 0.32)
        c.move_to(xx - ww / 2, -h * 0.5); c.line_to(xx + ww / 2, -h * 0.5); c.stroke()
    # roof(s)
    rh = 70 if era in ('qinhan', 'nanbei') else 84
    for tier in range(tiers):
        yy = -h - tier * (rh + 40); ww = w + 40 - tier * 120
        if tier > 0:
            rgba(c, col, a); c.rectangle(-ww / 2 + 50, yy, ww - 100, 40); c.fill()
            yy -= 0
        c.save(); _roofline(c, ww, yy, rh, era); c.restore()
        rgba(c, roofc, a); c.fill_preserve(); rgba(c, GOLD, 0.6 * a); c.set_line_width(2.5); c.stroke()
        # ridge
        rgba(c, roofc, a); c.rectangle(-ww / 2 + 60, yy - rh - 10, ww - 120, 12); c.fill()
        rgba(c, GOLD, 0.6 * a); c.rectangle(-ww / 2 + 60, yy - rh - 10, ww - 120, 2); c.fill()
        ex = ww / 2 - 60
        if era == 'nanbei':                     # 鸱尾
            for sg in (-1, 1):
                c.move_to(sg * ex, yy - rh - 10); c.curve_to(sg * (ex + 10), yy - rh - 50, sg * (ex - 20), yy - rh - 64, sg * (ex - 34), yy - rh - 46)
                c.curve_to(sg * (ex - 18), yy - rh - 44, sg * (ex - 14), yy - rh - 24, sg * (ex - 20), yy - rh - 10); c.close_path()
                rgba(c, roofc, a); c.fill_preserve(); rgba(c, GOLD, 0.7 * a); c.set_line_width(2); c.stroke()
        elif era in ('ming', 'qing', 'song'):
            for sg in (-1, 1):
                c.move_to(sg * ex, yy - rh - 10); c.curve_to(sg * (ex + 6), yy - rh - 30, sg * (ex + 14), yy - rh - 34, sg * (ex + 22), yy - rh - 30)
                c.line_to(sg * (ex + 10), yy - rh - 6); c.close_path(); rgba(c, roofc, a); c.fill_preserve()
                rgba(c, GOLD, 0.7 * a); c.set_line_width(2); c.stroke()
    if plaque:
        pw = len(plaque) * 40 + 30
        rgba(c, GOLDD, a); c.rectangle(-pw / 2 - 5, -h + 14, pw + 10, 58); c.fill()
        rgba(c, (0.08, 0.06, 0.10), a); c.rectangle(-pw / 2, -h + 19, pw, 48); c.fill()
        text2(c, plaque, 0, -h + 56, 34, 99, GOLDT, a, 'c', fam=FONT_X)
    c.restore()


def que(c, x, yf, s=1.0, a=1.0):
    """Han 阙 tower"""
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s, s)
    rgba(c, SIL2, a); c.rectangle(-50, -330, 100, 330); c.fill()
    rgba(c, GOLD, 0.35 * a); c.set_line_width(1.5); c.rectangle(-50, -330, 100, 330); c.stroke()
    for yy, ww in ((-330, 170), (-230, 140)):
        c.move_to(-ww / 2, yy); c.line_to(ww / 2, yy); c.line_to(ww / 2 - 30, yy - 40); c.line_to(-ww / 2 + 30, yy - 40); c.close_path()
        rgba(c, SIL1, a); c.fill_preserve(); rgba(c, GOLD, 0.6 * a); c.set_line_width(2); c.stroke()
    c.restore()


PLAQ = {'ming': '明镜高悬', 'qing': '明镜高悬', 'song': '公生明', 'nanbei': '刺史府', 'qinhan': '廷尉', 'han': '廷尉'}


def court(c, T, era='ming', plaque=None, lamp_l=True, tone='brown', sx=960, sy=560, px_=1400):
    """公堂 interior. desk front at y≈770, floor 900"""
    bgp(c, T, sx, sy, 950, tone, dust=False)
    # back wall
    rgba(c, (0.12, 0.08, 0.055)); c.rectangle(-200, 120, W + 400, 780); c.fill()
    rgba(c, (0.25, 0.08, 0.06)); c.rectangle(380, 160, 1160, 520); c.fill()       # red screen
    rgba(c, GOLD, 0.5); c.set_line_width(3); c.rectangle(380, 160, 1160, 520); c.stroke()
    # wave/sea-cliff motif on screen
    rgba(c, (0.40, 0.14, 0.10), 0.8); c.set_line_width(4)
    for k in range(6):
        c.move_to(390, 640 - k * 22)
        for x in range(390, 1531, 40):
            c.line_to(x, 640 - k * 22 + 10 * math.sin(x * 0.03 + k))
        c.stroke()
    c.arc(1180, 300, 60, 0, 6.283); rgba(c, (0.85, 0.35, 0.18), 0.55); c.fill()       # sun on screen
    # pillars
    for xx in (250, 1670):
        g = cairo.LinearGradient(xx - 40, 0, xx + 40, 0)
        g.add_color_stop_rgb(0, 0.18, 0.05, 0.04); g.add_color_stop_rgb(0.4, 0.42, 0.10, 0.07); g.add_color_stop_rgb(1, 0.14, 0.04, 0.03)
        c.set_source(g); c.rectangle(xx - 40, 60, 80, 840); c.fill()
    # beam
    rgba(c, (0.10, 0.07, 0.05)); c.rectangle(-200, 40, W + 400, 90); c.fill()
    rgba(c, GOLD, 0.6); c.rectangle(-200, 128, W + 400, 3); c.fill()
    p_ = plaque or PLAQ.get(era, '明镜高悬')
    pw = len(p_) * 64 + 60
    if px_ is not None:
        rgba(c, GOLDD); c.rectangle(px_ - pw / 2 - 8, 52, pw + 16, 96); c.fill()
        rgba(c, (0.07, 0.06, 0.12)); c.rectangle(px_ - pw / 2, 60, pw, 80); c.fill()
        text2(c, p_, px_, 122, 54, 99, GOLDT, 1, 'c', fam=FONT_X)
    ground(c, 900, (0.10, 0.07, 0.05))
    # floor tiles
    rgba(c, GOLD, 0.12); c.set_line_width(2)
    for k in range(-8, 9):
        c.move_to(960 + k * 60, 900); c.line_to(960 + k * 260, H + 60); c.stroke()
    if lamp_l:
        for lx in (150, 1770):
            lamp(c, lx, 520, T, 0.8)


def desk(c, x=960, yf=780, w=560, a=1.0, era='ming', T=0, slam=0.0):
    if a <= 0: return
    c.save(); c.translate(x, yf)
    rgba(c, (0.30, 0.14, 0.08), a); c.rectangle(-w / 2 - 20, -170, w + 40, 26); c.fill()
    rgba(c, GOLD, 0.7 * a); c.rectangle(-w / 2 - 20, -170, w + 40, 3); c.fill()
    rgba(c, (0.62, 0.12, 0.09), a); c.rectangle(-w / 2, -144, w, 144); c.fill()     # red cloth
    rgba(c, GOLD, 0.8 * a); c.set_line_width(3); c.rectangle(-w / 2 + 14, -132, w - 28, 120); c.stroke()
    rgba(c, (0.95, 0.75, 0.35), 0.8 * a); c.arc(0, -72, 30, 0, 6.283); c.set_line_width(4); c.stroke()
    # 签筒 + 惊堂木 + 笔架
    rgba(c, (0.35, 0.20, 0.12), a); c.rectangle(w / 2 - 90, -236, 46, 66); c.fill()
    for k in range(5):
        rgba(c, (0.86, 0.70, 0.40) if k % 2 else REDL, a); c.rectangle(w / 2 - 86 + k * 8, -276 + (k % 3) * 8, 5, 50); c.fill()
    lift = 40 * (1 - slam) if slam > 0 else 0
    rgba(c, (0.24, 0.12, 0.06), a); rrect(c, -w / 2 + 70, -192 - lift, 80, 22, 4); c.fill()
    if 0 < slam < 1:
        rgba(c, GOLDL, (1 - slam) * a); c.set_line_width(4)
        for k in range(5):
            ang = math.pi + k * math.pi / 4
            c.move_to(-w / 2 + 110 + 50 * math.cos(ang), -180 + 50 * math.sin(ang)); c.line_to(-w / 2 + 110 + 90 * math.cos(ang), -180 + 90 * math.sin(ang)); c.stroke()
    c.restore()


def flash(c, t, t0, col=(0.9, 0.1, 0.05), amt=0.45, d=0.5):
    u = seg(t, t0, t0 + d)
    if 0 < u < 1:
        rgba(c, col, amt * (1 - u)); c.rectangle(-500, -500, W + 1000, H + 1000); c.fill()


# ------------------------------------------------------------- figures
def holdbaby(c, x, yf, s=1.0, face=1, a=1.0, T=0, cry=0.0, col=(0.92, 0.80, 0.55), kneel=False):
    by = yf - s * (75 if not kneel else 46)
    baby(c, x + face * s * 22, by, s * 0.9, a, col, T, cry)


def mother(c, x, yf, s=1.6, era='ming', pose='hold', face=1, expr='sad', T=0, a=1.0, cry=0.0, robe=(0.62, 0.30, 0.34), p=1.0, tear=0.0):
    chibi(c, x, yf, s, era, 'lady', pose, face, expr, T=T, a=a, robe=robe, p=p, tear=tear)
    if pose in ('hold', 'kneel'):
        holdbaby(c, x, yf, s, face, a, T, cry, kneel=(pose == 'kneel'))


def bubble(c, x, y, txt, a=1.0, size=44, col=TXT, tail=(-1, 1), bg=(0.08, 0.06, 0.05)):
    if a <= 0: return
    w = tw(c, txt, size, FONT_X) + 50; h = size * 1.6
    rgba(c, bg, 0.88 * a); rrect(c, x - w / 2, y - h / 2, w, h, 20); c.fill_preserve()
    rgba(c, GOLD, 0.8 * a); c.set_line_width(3); c.stroke()
    c.move_to(x + tail[0] * 20, y + h / 2 - 2); c.line_to(x + tail[0] * 50, y + h / 2 + 34); c.line_to(x + tail[0] * 50 + tail[1] * 40, y + h / 2 - 2)
    rgba(c, bg, 0.88 * a); c.fill()
    text2(c, txt, x, y + size * 0.36, size, 99, col, a, 'c', fam=FONT_X)


def tag(c, txt, x, y, a=1.0, size=34, col=LACQ):
    if a <= 0: return
    chip(c, txt, x, y, col, a, size)


def popin(c, t, t0, x, y, d=0.4):
    """returns scale for pop animation around (x,y); use with c.save/restore"""
    p = back(seg(t, t0, t0 + d))
    c.translate(x, y); c.scale(max(p, 0.001), max(p, 0.001)); c.translate(-x, -y)
    return p


# ------------------------------------------------------------- props
def drop(c, x, y, r=14, a=1.0, col=BLOODL):
    if a <= 0: return
    c.move_to(x, y - r * 1.9)
    c.curve_to(x + r * 0.5, y - r, x + r, y - r * 0.4, x + r, y + r * 0.2)
    c.arc(x, y + r * 0.2, r, 0, math.pi)
    c.curve_to(x - r, y - r * 0.4, x - r * 0.5, y - r, x, y - r * 1.9); c.close_path()
    rgba(c, col, a); c.fill()
    rgba(c, (1, 0.8, 0.8), 0.6 * a); c.arc(x - r * 0.35, y - r * 0.1, r * 0.22, 0, 6.283); c.fill()


def wbowl(c, x, y, s=1.0, a=1.0, blobs=(), merge=0.0, spread=0.0, T=0, salt=0.0):
    """big water bowl seen 3/4; y = rim centre. blobs: list of (dx,dy,r,alpha)"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    spot(c, 0, 0, 380, 0.7 * a, (1, 0.85, 0.6))
    # body
    c.move_to(-220, 0); c.curve_to(-210, 170, 210, 170, 220, 0); c.close_path()
    g = cairo.LinearGradient(-220, 0, 220, 0)
    g.add_color_stop_rgba(0, 0.55, 0.52, 0.46, a); g.add_color_stop_rgba(0.4, 0.93, 0.90, 0.84, a); g.add_color_stop_rgba(1, 0.50, 0.47, 0.42, a)
    c.set_source(g); c.fill()
    rgba(c, (0.22, 0.32, 0.58), a); c.set_line_width(5); c.move_to(-200, 50); c.curve_to(-120, 80, 120, 80, 200, 50); c.stroke()
    rgba(c, (0.40, 0.36, 0.30), a); c.rectangle(-70, 150, 140, 22); c.fill()
    # water surface
    c.save(); c.scale(220, 52); c.arc(0, 0, 1, 0, 6.283); c.restore()
    rgba(c, (0.85, 0.83, 0.78), a); c.fill()
    c.save(); c.scale(204, 44); c.arc(0, 0, 1, 0, 6.283); c.restore()
    g = cairo.RadialGradient(-40, -10, 10, 0, 0, 220)
    g.add_color_stop_rgba(0, 0.62, 0.78, 0.85, a); g.add_color_stop_rgba(1, 0.30, 0.45, 0.55, a)
    c.set_source(g); c.fill()
    # ripples
    rgba(c, (1, 1, 1), 0.25 * a); c.set_line_width(2)
    for k in range(2):
        ph = (T * 0.6 + k * 0.5) % 1
        c.save(); c.scale(40 + ph * 150, (40 + ph * 150) * 0.22); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.stroke()
    # salt film
    if salt > 0:
        rgba(c, (1, 1, 1), 0.35 * salt * a)
        for k in range(40):
            rr = random.Random(k)
            c.arc(rr.uniform(-170, 170), rr.uniform(-34, 34), 3, 0, 6.283); c.fill()
    # blood blobs on surface
    c.save(); c.rectangle(-204, -44, 408, 88); c.clip()
    c.save(); c.scale(1, 0.24)
    for (dx, dy, r, al) in blobs:
        rr = r * (1 + spread * 3)
        g = cairo.RadialGradient(dx, dy / 0.24, 0, dx, dy / 0.24, rr)
        g.add_color_stop_rgba(0, 0.72, 0.06, 0.06, al * a * (1 - 0.5 * spread)); g.add_color_stop_rgba(0.7, 0.72, 0.06, 0.06, 0.7 * al * a * (1 - 0.6 * spread))
        g.add_color_stop_rgba(1, 0.72, 0.06, 0.06, 0)
        c.set_source(g); c.arc(dx, dy / 0.24, rr, 0, 6.283); c.fill()
    c.restore(); c.restore()
    c.restore()


def bone(c, x, y, s=1.0, ang=0.0, a=1.0, col=(0.86, 0.80, 0.66), stain=0.0, pores=False):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rgba(c, col, a)
    c.rectangle(-110, -16, 220, 32); c.fill()
    for sx in (-1, 1):
        for sy in (-1, 1):
            c.arc(sx * 112, sy * 18, 26, 0, 6.283); c.fill()
    rgba(c, (0.45, 0.38, 0.28), 0.8 * a); c.set_line_width(2.5)
    c.move_to(-90, -16); c.line_to(90, -16); c.move_to(-90, 16); c.line_to(90, 16); c.stroke()
    if pores:
        rgba(c, (0.32, 0.25, 0.18), 0.9 * a)
        for k in range(26):
            rr = random.Random(k + 7)
            c.arc(rr.uniform(-100, 100), rr.uniform(-12, 12), rr.uniform(2, 5), 0, 6.283); c.fill()
    if stain > 0:
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 90 * stain)
        g.add_color_stop_rgba(0, 0.70, 0.05, 0.05, 0.85 * a); g.add_color_stop_rgba(1, 0.70, 0.05, 0.05, 0)
        c.set_source(g); c.rectangle(-110, -16, 220, 32); c.fill()
    c.restore()


def calpage(c, x, y, w, h, top, big, a=1.0, col=LACQ, sub=None, mark=0.0):
    if a <= 0: return
    rgba(c, (0, 0, 0), 0.35 * a); c.rectangle(x - w / 2 + 8, y - h / 2 + 10, w, h); c.fill()
    rgba(c, PAPER, a); c.rectangle(x - w / 2, y - h / 2, w, h); c.fill()
    rgba(c, col, a); c.rectangle(x - w / 2, y - h / 2, w, h * 0.24); c.fill()
    text2(c, top, x, y - h / 2 + h * 0.17, h * 0.13, 99, (1, 0.95, 0.88), a, 'c', fam=FONT_X)
    bs = min(h * 0.40, w * 0.84 / max(1, len(big) * 0.62 if big.isdigit() else len(big)))
    text2(c, big, x, y + h * 0.22, bs, 99, INKP, a, 'c', fam=FONT_X)
    if sub:
        fnt(c, h * 0.08, FONT_B); rgba(c, INKP, 0.8 * a); ww = c.text_extents(sub)[4]; c.move_to(x - ww / 2, y + h * 0.42); c.show_text(sub)
    if mark > 0:
        rgba(c, REDL, a); c.set_line_width(8); c.arc(x, y + h * 0.10, h * 0.32 * mark, 0, 6.283 * mark); c.stroke()


def slips(c, x, y, n=9, w=44, h=420, a=1.0, text=None, prog=1.0):
    """bamboo slips, vertical columns; text: list of strings (one per slip, right to left)"""
    if a <= 0: return
    tot = n * w
    show = int(n * prog + 0.999)
    for k in range(show):
        xx = x + tot / 2 - (k + 1) * w
        g = cairo.LinearGradient(xx, 0, xx + w, 0)
        g.add_color_stop_rgba(0, 0.62, 0.48, 0.26, a); g.add_color_stop_rgba(0.5, 0.86, 0.72, 0.46, a); g.add_color_stop_rgba(1, 0.58, 0.44, 0.24, a)
        c.set_source(g); c.rectangle(xx + 2, y - h / 2, w - 4, h); c.fill()
        if text and k < len(text):
            for j, ch in enumerate(text[k]):
                fnt(c, w * 0.62, FONT_X); rgba(c, INKP, a)
                ew = c.text_extents(ch)[4]; c.move_to(xx + w / 2 - ew / 2, y - h / 2 + 40 + j * w * 0.72); c.show_text(ch)
    rgba(c, (0.35, 0.22, 0.10), a); c.set_line_width(3)
    for yy in (y - h / 2 + 22, y + h / 2 - 22):
        c.move_to(x + tot / 2, yy); c.line_to(x + tot / 2 - show * w, yy); c.stroke()


def ink(c, s_, x, y, size, t=99, a=1.0, stagger=0.03):
    chars = parse2(s_, INKP)
    fnt(c, size, FONT_X)
    cx = x
    for i, (ch, col, ul) in enumerate(chars):
        adv = c.text_extents(ch)[4]
        p = eout(seg(t - i * stagger, 0, 0.25))
        if p > 0.003:
            if col != INKP: col = (0.70, 0.10, 0.06)
            rgba(c, col, p * a); c.move_to(cx, y); c.show_text(ch)
        cx += adv


def paperq(c, x, y, lines, t, t0=0.0, size=46, a=1.0, title='原文', w=None, red=()):
    """cream scroll overlay with original text lines (horizontal), unrolls from t0."""
    p = ease(seg(t, t0, t0 + 0.6))
    if p <= 0 or a <= 0: return
    fnt(c, size, FONT_X)
    tws = [tw(c, s_, size, FONT_X) for s_ in lines]
    ww = w or (max(tws) + 120)
    hh = len(lines) * size * 1.45 + 70
    cw = ww * p
    c.save()
    rgba(c, (0, 0, 0), 0.4 * a); c.rectangle(x - cw / 2 + 10, y - hh / 2 + 12, cw, hh); c.fill()
    g = cairo.LinearGradient(0, y - hh / 2, 0, y + hh / 2)
    g.add_color_stop_rgba(0, 0.96, 0.91, 0.78, a); g.add_color_stop_rgba(1, 0.86, 0.78, 0.60, a)
    c.set_source(g); c.rectangle(x - cw / 2, y - hh / 2, cw, hh); c.fill()
    rgba(c, (0.55, 0.30, 0.15), 0.6 * a); c.set_line_width(2); c.rectangle(x - cw / 2 + 12, y - hh / 2 + 12, cw - 24, hh - 24); c.stroke()
    for sx in (-1, 1):
        g = cairo.LinearGradient(0, y - hh / 2 - 14, 0, y + hh / 2 + 14)
        g.add_color_stop_rgba(0, 0.30, 0.16, 0.08, a); g.add_color_stop_rgba(0.5, 0.55, 0.32, 0.16, a); g.add_color_stop_rgba(1, 0.30, 0.16, 0.08, a)
        c.set_source(g); rrect(c, x + sx * cw / 2 - 14, y - hh / 2 - 18, 28, hh + 36, 10); c.fill()
    c.rectangle(x - cw / 2, y - hh / 2, cw, hh); c.clip()
    yy = y - hh / 2 + 35 + size * 0.95
    for i, s_ in enumerate(lines):
        base = INKP
        ink(c, s_, x - (max(tws)) / 2, yy, size, (t - t0 - 0.5 - i * 0.5) * 1.6, a)
        yy += size * 1.45
    c.restore()
    if title and p > 0.6:
        seal(c, title, x - ww / 2 + 50, y - hh / 2 + 4, 0.45, a * fin(t, t0 + 0.4))


def bookq(c, x, y, title, s=1.0, a=1.0, col=(0.20, 0.26, 0.40), rot=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rgba(c, (0, 0, 0), 0.4 * a); c.rectangle(-110, -145, 230, 300); c.fill()
    rgba(c, (0.92, 0.88, 0.78), a); c.rectangle(-118, -152, 230, 300); c.fill()
    rgba(c, col, a); c.rectangle(-124, -156, 230, 300); c.fill()
    rgba(c, (0.85, 0.75, 0.50), a); c.set_line_width(3)
    for yy in (-120, -40, 40, 120):
        c.move_to(-104, yy); c.line_to(-124, yy); c.stroke()
    rgba(c, PAPER, a); c.rectangle(-10, -130, 80, 250); c.fill()
    n = len(title); sz = min(52, 220 / max(n, 1))
    for k, ch in enumerate(title):
        fnt(c, sz, FONT_X); rgba(c, INKP, a); ew = c.text_extents(ch)[4]
        c.move_to(30 - ew / 2, -120 + sz + k * sz * 1.02 + (220 - n * sz * 1.02) / 2); c.show_text(ch)
    c.restore()


def stone(c, x, yf, lines, s=1.0, a=1.0, prog=1.0):
    """stele with carved vertical text columns (right to left)"""
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s, s)
    rgba(c, (0.20, 0.19, 0.18), a); c.rectangle(-200, -40, 400, 40); c.fill()
    g = cairo.LinearGradient(-160, 0, 160, 0)
    g.add_color_stop_rgba(0, 0.30, 0.29, 0.27, a); g.add_color_stop_rgba(0.5, 0.52, 0.50, 0.46, a); g.add_color_stop_rgba(1, 0.28, 0.27, 0.25, a)
    c.set_source(g); c.move_to(-160, -40); c.line_to(-160, -560); c.curve_to(-160, -640, 160, -640, 160, -560); c.line_to(160, -40); c.close_path(); c.fill()
    rgba(c, GOLD, 0.5 * a); c.set_line_width(2); c.move_to(-160, -40); c.line_to(-160, -560); c.curve_to(-160, -640, 160, -640, 160, -560); c.line_to(160, -40); c.stroke()
    n = len(lines)
    for k, ln in enumerate(lines):
        xx = (n - 1) * 34 - k * 68
        for j, ch in enumerate(ln):
            u = clamp(prog * (sum(len(l) for l in lines)) - (sum(len(l) for l in lines[:k]) + j))
            if u <= 0: continue
            fnt(c, 56, FONT_X); ew = c.text_extents(ch)[4]
            rgba(c, (1.0, 0.86, 0.50), u * a); c.move_to(xx - ew / 2, -520 + j * 66); c.show_text(ch)
    c.restore()


def bars(c, x0, x1, y0, y1, a=1.0):
    if a <= 0: return
    rgba(c, (0.12, 0.09, 0.07), a); c.set_line_width(14)
    for x in range(int(x0), int(x1) + 1, 46):
        c.move_to(x, y0); c.line_to(x, y1); c.stroke()
    c.set_line_width(18); c.move_to(x0 - 10, y0 + 10); c.line_to(x1 + 10, y0 + 10); c.move_to(x0 - 10, y1 - 60); c.line_to(x1 + 10, y1 - 60); c.stroke()
    rgba(c, GOLD, 0.35 * a); c.set_line_width(2)
    for x in range(int(x0), int(x1) + 1, 46):
        c.move_to(x - 6, y0); c.line_to(x - 6, y1); c.stroke()


def jiagun(c, x, y, s=1.0, a=1.0, sq=0.0):
    """夹棍: three upright sticks bound with rope"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for k, dx in enumerate((-40 + 10 * sq, 0, 40 - 10 * sq)):
        g = cairo.LinearGradient(dx - 12, 0, dx + 12, 0)
        g.add_color_stop_rgba(0, 0.36, 0.22, 0.12, a); g.add_color_stop_rgba(0.5, 0.66, 0.46, 0.26, a); g.add_color_stop_rgba(1, 0.32, 0.20, 0.10, a)
        c.set_source(g); rrect(c, dx - 12, -180, 24, 300, 8); c.fill()
    rgba(c, (0.80, 0.68, 0.45), a); c.set_line_width(6)
    for yy in (-140, 80):
        c.move_to(-60, yy); c.line_to(60, yy); c.stroke()
    c.restore()


def zanzhi(c, x, y, s=1.0, a=1.0, sq=0.0):
    """拶指: row of small sticks with cords"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    n = 6; gap = 34 - 8 * sq
    for k in range(n):
        dx = (k - (n - 1) / 2) * gap
        rgba(c, (0.66, 0.46, 0.26), a); rrect(c, dx - 8, -70, 16, 140, 6); c.fill()
        rgba(c, (0.36, 0.22, 0.12), a); c.set_line_width(2); rrect(c, dx - 8, -70, 16, 140, 6); c.stroke()
    rgba(c, (0.80, 0.68, 0.45), a); c.set_line_width(5)
    for yy in (-50, 50):
        c.move_to(-(n / 2) * gap - 40, yy); c.line_to((n / 2) * gap + 40, yy); c.stroke()
    c.restore()


def card(c, x, y, num, title, a=1.0, s=1.0, rot=0.0, hi=0.0, icon=None, T=0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rgba(c, (0, 0, 0), 0.45 * a); rrect(c, -150 + 10, -200 + 12, 300, 400, 18); c.fill()
    g = cairo.LinearGradient(0, -200, 0, 200)
    g.add_color_stop_rgba(0, 0.22, 0.12, 0.08, a); g.add_color_stop_rgba(1, 0.12, 0.07, 0.05, a)
    c.set_source(g); rrect(c, -150, -200, 300, 400, 18); c.fill()
    rgba(c, lerpc(GOLD, GOLDL, hi), a); c.set_line_width(4 + 3 * hi); rrect(c, -150, -200, 300, 400, 18); c.stroke()
    roundbadge(c, 0, -140, num, a, LACQ, 38, 40)
    if icon: icon(c, 0, 20)
    text2(c, title, 0, 160, 46, 99, TXT, a, 'c', fam=FONT_X)
    c.restore()


def mound(c, x, yf, s=1.0, a=1.0, dug=0.0):
    if a <= 0: return
    c.save(); c.translate(x, yf); c.scale(s, s)
    c.move_to(-220, 0); c.curve_to(-160, -150, 160, -150, 220, 0); c.close_path()
    rgba(c, (0.24, 0.17, 0.11), a); c.fill_preserve(); rgba(c, GOLD, 0.4 * a); c.set_line_width(2); c.stroke()
    if dug > 0:
        rgba(c, (0.04, 0.03, 0.02), a); c.save(); c.translate(0, -30); c.scale(120 * dug, 34 * dug); c.arc(0, 0, 1, 0, 6.283); c.restore(); c.fill()
    c.restore()


def dna(c, x, y, h, T, a=1.0, prog=1.0):
    if a <= 0: return
    n = 26
    for k in range(int(n * prog)):
        yy = y - h / 2 + h * k / (n - 1)
        ph = T * 1.6 + k * 0.45
        x1 = x + 120 * math.sin(ph); x2 = x - 120 * math.sin(ph)
        dep = math.cos(ph)
        rgba(c, (0.45, 0.75, 1.0), 0.5 * a); c.set_line_width(4); c.move_to(x1, yy); c.line_to(x2, yy); c.stroke()
        for xx, d in ((x1, dep), (x2, -dep)):
            rgba(c, (0.60, 0.88, 1.0) if d > 0 else (0.98, 0.80, 0.42), a); c.arc(xx, yy, 11 + 4 * d, 0, 6.283); c.fill()


def magnifier(c, x, y, r=110, a=1.0):
    if a <= 0: return
    rgba(c, (0.95, 0.95, 1.0), 0.10 * a); c.arc(x, y, r, 0, 6.283); c.fill()
    rgba(c, GOLDL, a); c.set_line_width(10); c.arc(x, y, r, 0, 6.283); c.stroke()
    rgba(c, (0.40, 0.25, 0.12), a); c.set_line_width(22); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x + r * 0.72, y + r * 0.72); c.line_to(x + r * 1.5, y + r * 1.5); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)


def redx(c, x, y, s, t, t0, col=REDL):
    p = seg(t, t0, t0 + 0.35)
    if p <= 0: return
    rgba(c, col, 1); c.set_line_width(22 * s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    u1 = clamp(p * 2); u2 = clamp(p * 2 - 1)
    c.move_to(x - 120 * s, y - 120 * s); c.line_to(x - 120 * s + 240 * s * u1, y - 120 * s + 240 * s * u1); c.stroke()
    if u2 > 0:
        c.move_to(x + 120 * s, y - 120 * s); c.line_to(x + 120 * s - 240 * s * u2, y - 120 * s + 240 * s * u2); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)


def tick_mark(c, x, y, s, t, t0, col=GREENL):
    p = seg(t, t0, t0 + 0.3)
    if p <= 0: return
    rgba(c, col); c.set_line_width(20 * s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x - 60 * s, y); c.line_to(x - 60 * s + 50 * s * clamp(p * 2), y + 50 * s * clamp(p * 2)); c.stroke()
    if p > 0.5:
        u = clamp(p * 2 - 1); c.move_to(x - 10 * s, y + 50 * s); c.line_to(x - 10 * s + 100 * s * u, y + 50 * s - 120 * s * u); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)


def stickhit(c, x, y, t, rate=2.2, a=1.0, s=1.0):
    """杖 swinging down repeatedly onto (x,y)"""
    if a <= 0: return 0
    ph = (t * rate) % 1.0
    ang = -1.2 + 1.3 * (ph / 0.35 if ph < 0.35 else 1 - (ph - 0.35) / 0.65)
    c.save(); c.translate(x - 180 * s, y - 40 * s); c.rotate(ang)
    rgba(c, (0.55, 0.32, 0.16), a); rrect(c, 0, -10 * s, 230 * s, 20 * s, 8); c.fill()
    rgba(c, LACQ, a); c.rectangle(150 * s, -11 * s, 80 * s, 22 * s); c.fill()
    c.restore()
    if ph < 0.42 and ph > 0.3:
        rgba(c, GOLDL, a); c.set_line_width(4)
        for k in range(5):
            an = -math.pi + k * math.pi / 4
            c.move_to(x + 30 * math.cos(an), y + 30 * math.sin(an)); c.line_to(x + 70 * math.cos(an), y + 70 * math.sin(an)); c.stroke()
    return ph
