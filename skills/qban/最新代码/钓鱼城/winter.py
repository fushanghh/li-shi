"""winter sets & props for 紫禁城冬天怎么取暖 (cold blue snow vs warm orange fire)"""
import math, random
from core import *
from sets import vgrad, lantern, palace

SNOWW = (0.96, 0.97, 1.0)
ICE = (0.70, 0.82, 0.96)
FIRE = (1.0, 0.55, 0.18)
FIREL = (1.0, 0.80, 0.35)
EMBER = (0.95, 0.30, 0.12)
ROOFY = (0.95, 0.74, 0.22)
PILLAR = (0.74, 0.18, 0.14)
STONE = (0.78, 0.78, 0.80)
COLD_TOP = (0.30, 0.42, 0.62)
COLD_BOT = (0.62, 0.74, 0.88)
DATAB = (0.17, 0.19, 0.25)


def snow(c, T, n=90, a=0.9, seed=11, area=(0, 0, W, H), big=1.0, wind=30):
    rnd = random.Random(seed)
    x0, y0, w, h = area
    for i in range(n):
        sp = rnd.uniform(40, 110)
        r = rnd.uniform(2.0, 5.5) * big
        x = x0 + (rnd.random() * w + T * wind + math.sin(T * 1.3 + i) * 14) % w
        y = y0 + (rnd.random() * h + T * sp) % h
        c.arc(x, y, r, 0, TAU); c.set_source_rgba(1, 1, 1, a * (0.55 + 0.45 * ((i * 37) % 10) / 10)); c.fill()


def heatwaves(c, x0, x1, y, T, a=1.0, n=6, h=160, col=FIRE):
    if a <= 0.01:
        return
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        x = x0 + (x1 - x0) * (i + 0.5) / n
        ph = (T * 0.9 + i * 0.37) % 1.0
        yy = y - ph * h
        aa = a * math.sin(ph * math.pi) * 0.85
        c.move_to(x, yy + 50)
        for k in range(1, 11):
            c.line_to(x + math.sin(k * 0.9 + T * 5 + i) * 12, yy + 50 - k * 9)
        rgba(c, col, aa); c.set_line_width(6); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)


def breath(c, x, y, T, a=0.8, period=2.2, dirx=1):
    ph = (T % period) / period
    if ph > 0.6:
        return
    u = ph / 0.6
    for k in range(3):
        rr_ = 10 + u * 26 + k * 6
        c.arc(x + dirx * (u * 70 + k * 16), y - u * 20 - k * 6, rr_, 0, TAU)
        c.set_source_rgba(1, 1, 1, a * (1 - u) * 0.6); c.fill()


def flames(c, x, yb, w, h, T, a=1.0, seed=1):
    if a <= 0.01 or h <= 1:
        return
    rnd = random.Random(seed)
    glow(c, x, yb - h * 0.4, max(w, h) * 1.3, FIRE, 0.45 * a)
    n = max(3, int(w / 26))
    for layer, (col, k) in enumerate(((EMBER, 1.0), (FIRE, 0.75), (FIREL, 0.45))):
        for i in range(n):
            fx = x - w / 2 + w * (i + 0.5) / n + rnd.uniform(-6, 6)
            fh = h * k * (0.6 + 0.4 * abs(math.sin(T * (6 + i) + i * 1.7 + layer)))
            fw = w / n * (1.15 if layer == 0 else 0.9)
            c.move_to(fx - fw / 2, yb)
            c.curve_to(fx - fw / 2, yb - fh * 0.5, fx + math.sin(T * 8 + i) * fw * 0.4, yb - fh * 0.8, fx + math.sin(T * 7 + i) * fw * 0.3, yb - fh)
            c.curve_to(fx + fw * 0.2, yb - fh * 0.6, fx + fw / 2, yb - fh * 0.4, fx + fw / 2, yb)
            c.close_path(); rgba(c, col, a); c.fill()


def smoke(c, x, y, T, a=0.6, n=5, col=(0.55, 0.55, 0.60), drift=40, rise=160):
    for i in range(n):
        ph = (T * 0.45 + i / n) % 1.0
        r = 10 + ph * 38
        c.arc(x + ph * drift + math.sin(T * 2 + i) * 8, y - ph * rise, r, 0, TAU)
        rgba(c, col, a * (1 - ph)); c.fill()


def roofsnow(c, x0, x1, y, a=1.0, seed=3):
    rnd = random.Random(seed)
    c.move_to(x0, y)
    xx = x0
    while xx < x1:
        st = rnd.uniform(40, 80)
        c.curve_to(xx + st * 0.3, y - 14, xx + st * 0.7, y - 14, min(xx + st, x1), y)
        xx += st
    c.line_to(x1, y + 12); c.line_to(x0, y + 12); c.close_path()
    rgba(c, SNOWW, a); c.fill()


def hallfront(c, x, yb, s=1.0, a=1.0, warm=0.0, T=0.0, label=None, fire=0.0, snowcap=True, burnt=0.0):
    """宫殿正立面（扁平）：台基+红柱+槛窗+黄瓦，屋顶积雪；warm=窗纸透出暖光"""
    if a <= 0.01:
        return
    c.save(); c.translate(x, yb); c.scale(s, s)
    # 台基
    c.rectangle(-470, -70, 940, 70); fill2(c, STONE, a, 3, 0.72)
    rgba(c, dk(STONE, 0.85), a); c.set_line_width(2)
    for k in range(-9, 10):
        c.move_to(k * 50, -70); c.line_to(k * 50, 0); c.stroke()
    c.rectangle(-480, -78, 960, 10); fill2(c, lt(STONE, 0.3), a, 2, 0.75)
    # steps
    for k in range(4):
        c.rectangle(-80 + k * 6, -70 + k * 17, 160 - k * 12, 17); fill2(c, lt(STONE, 0.15), a, 2, 0.75)
    # wall + windows
    c.rectangle(-400, -330, 800, 252); fill2(c, (0.62, 0.17, 0.13), a, 3, 0.75)
    for k in range(-3, 4):
        wx = k * 108
        rr(c, wx - 44, -300, 88, 190, 3); rgba(c, (0.36, 0.14, 0.10), a); c.fill()
        wc = lerpc((0.80, 0.84, 0.92), (1.0, 0.78, 0.40), warm)
        c.rectangle(wx - 36, -292, 72, 174); rgba(c, wc, a); c.fill()
        rgba(c, (0.36, 0.14, 0.10), a); c.set_line_width(3)
        for j in range(1, 3):
            c.move_to(wx - 36 + j * 24, -292); c.line_to(wx - 36 + j * 24, -118); c.stroke()
        for j in range(1, 6):
            c.move_to(wx - 36, -292 + j * 29); c.line_to(wx + 36, -292 + j * 29); c.stroke()
    if warm > 0.01:
        glow(c, 0, -200, 520, FIRE, 0.22 * warm * a)
    # pillars
    for k in range(-4, 5):
        px = k * 108 - 54 if k else None
    for px in [-400 + i * 100 for i in range(9)]:
        c.rectangle(px - 13, -340, 26, 262); fill2(c, PILLAR, a, 2.5, 0.72)
    # beam
    c.rectangle(-430, -372, 860, 34); fill2(c, (0.20, 0.36, 0.40), a, 2.5, 0.7)
    rgba(c, GOLDL, a); 
    for k in range(-7, 8):
        c.arc(k * 56, -355, 7, 0, TAU); c.fill()
    # roof (庑殿/歇山 simplified)
    c.move_to(-560, -360); c.curve_to(-480, -385, -420, -430, -380, -520); c.line_to(380, -520)
    c.curve_to(420, -430, 480, -385, 560, -360); c.close_path()
    fill2(c, ROOFY if burnt < 0.5 else (0.25, 0.20, 0.18), a, 3, 0.7)
    rgba(c, dk(ROOFY, 0.78), a); c.set_line_width(2.5)
    for k in range(-14, 15):
        c.move_to(k * 26, -515); c.line_to(k * 37, -366); c.stroke()
    c.rectangle(-400, -540, 800, 24); fill2(c, dk(ROOFY, 0.85), a, 2, 0.7)
    for sx in (-1, 1):
        c.move_to(sx * 400, -540); c.curve_to(sx * 430, -560, sx * 440, -590, sx * 425, -600); c.line_to(sx * 390, -545); c.close_path()
        fill2(c, dk(ROOFY, 0.85), a, 2, 0.7)
    if snowcap:
        roofsnow(c, -540, 540, -372, a, 2)
        roofsnow(c, -392, 392, -545, a, 5)
        c.rectangle(-470, -86, 940, 10); rgba(c, SNOWW, a); c.fill()
    if fire > 0.01:
        flames(c, -180, -360, 360, 260 * fire, T, a, 3)
        flames(c, 200, -330, 300, 220 * fire, T + 1, a, 5)
        flames(c, 0, -520, 520, 200 * fire, T + 2, a, 7)
    c.restore()
    if label:
        w = tw(c, label, 46 * s) + 40
        rr(c, x - w / 2, yb - 640 * s, w, 70 * s, 6); c.set_source_rgba(0.15, 0.17, 0.32, 0.95 * a); c.fill_preserve()
        rgba(c, GOLD, a); c.set_line_width(3); c.stroke()
        text(c, label, x, yb - 640 * s + 50 * s, 46 * s, GOLDL, a, align='c', shadow=0)


def snowscape(c, T, hor=760, warm=0.0, dusk=False, night=False):
    if night:
        vgrad(c, 0, hor, (0.08, 0.10, 0.22), (0.20, 0.24, 0.42))
    elif dusk:
        vgrad(c, 0, hor, (0.26, 0.30, 0.52), (0.72, 0.58, 0.62))
    else:
        vgrad(c, 0, hor, COLD_TOP, COLD_BOT)
    # far palace roofs silhouette
    for i, (xx, ww, hh) in enumerate(((150, 360, 120), (620, 300, 90), (1320, 420, 140), (1800, 320, 100))):
        col = (0.40, 0.48, 0.64) if not night else (0.16, 0.18, 0.32)
        c.move_to(xx - ww / 2, hor - 30); c.line_to(xx - ww * 0.36, hor - 30 - hh); c.line_to(xx + ww * 0.36, hor - 30 - hh); c.line_to(xx + ww / 2, hor - 30); c.close_path()
        rgba(c, col); c.fill()
        roofsnow(c, xx - ww * 0.36, xx + ww * 0.36, hor - 30 - hh, 0.85, i)
        c.rectangle(xx - ww * 0.42, hor - 30, ww * 0.84, 30); rgba(c, (0.50, 0.30, 0.34) if not night else (0.24, 0.16, 0.22)); c.fill()
    # red wall
    c.rectangle(0, hor - 60, W, 60); rgba(c, (0.66, 0.24, 0.22) if not night else (0.36, 0.14, 0.16)); c.fill()
    roofsnow(c, 0, W, hor - 64, 0.95, 9)
    # snow ground
    vgrad(c, hor, H, (0.88, 0.92, 0.98) if not night else (0.50, 0.56, 0.72), (0.74, 0.82, 0.94) if not night else (0.36, 0.40, 0.58))
    rnd = random.Random(4)
    for i in range(16):
        ell(c, rnd.uniform(0, W), rnd.uniform(hor + 30, H), rnd.uniform(60, 160), rnd.uniform(6, 12))
        rgba(c, (0.70, 0.78, 0.92) if not night else (0.32, 0.36, 0.52), 0.6); c.fill()


def coldhall(c, T, floor_y=830, frost=1.0):
    palace(c, T, screen=True, win=True, lant=False, floor_y=floor_y,
           tone=((0.30, 0.34, 0.50), (0.22, 0.26, 0.42)))
    # bluish wash + window snow
    c.rectangle(0, 0, W, H); c.set_source_rgba(0.45, 0.60, 0.90, 0.16); c.fill()
    snow(c, T, 26, 0.9, 5, (1522, 132, 256, 376), 0.8)
    # frost corners
    if frost > 0:
        for (cx, cy) in ((0, 0), (W, 0)):
            g = cairo.RadialGradient(cx, cy, 0, cx, cy, 420)
            g.add_color_stop_rgba(0, 0.85, 0.92, 1.0, 0.45 * frost); g.add_color_stop_rgba(1, 0.85, 0.92, 1.0, 0)
            c.set_source(g); c.rectangle(0, 0, W, H); c.fill()
    snow(c, T, 30, 0.35, 21, (0, 0, W, floor_y), 0.6, 60)


def warmhall(c, T, floor_y=830, heat=1.0, lant=True):
    palace(c, T, screen=True, win=True, lant=lant, floor_y=floor_y,
           tone=((0.55, 0.22, 0.14), (0.42, 0.16, 0.10)))
    # warm floor bricks
    for k in range(0, W, 120):
        c.rectangle(k, floor_y + 6, 116, 110); rgba(c, (0.62, 0.30, 0.18), 0.55 * heat); c.fill()
    g = cairo.LinearGradient(0, floor_y, 0, H)
    g.add_color_stop_rgba(0, 1.0, 0.55, 0.20, 0.35 * heat); g.add_color_stop_rgba(1, 1.0, 0.55, 0.20, 0.0)
    c.set_source(g); c.rectangle(0, floor_y, W, H - floor_y); c.fill()
    heatwaves(c, 150, 1770, floor_y + 20, T, heat * 0.8, 9, 220)


# ---------------------------------------------------------------- 剖面图：火地
SEC = dict(gy=560, wx=760, fl=560)


def section(c, t, T, show=1.0, heat=1.0, labels=None, lab_t=None, smoke_a=1.0, person=True):
    """cross-section: left = 室外廊下(雪)，window wall at wx; right = 室内；地下：操作口→炉腔→主烟道(斜坡)→出烟口"""
    gy = 640          # ground / floor level
    wx = 640          # window wall x
    # sky / exterior
    vgrad(c, 0, gy, (0.30, 0.42, 0.62), (0.62, 0.74, 0.88), 0, wx)
    snow(c, T, 30, 0.9, 7, (0, 0, wx, gy), 0.8)
    # interior warm room
    vgrad(c, 0, gy, (0.52, 0.22, 0.14), (0.70, 0.34, 0.18), wx, W)
    # underground earth
    vgrad(c, gy, H, (0.42, 0.32, 0.24), (0.28, 0.21, 0.16))
    # exterior ground snow strip (廊下地面)
    c.rectangle(0, gy - 12, wx, 12); rgba(c, SNOWW); c.fill()
    # pit 操作口 (outside, below ground, next to wall)
    px0, px1, pdep = 360, 600, 300
    c.rectangle(px0, gy, px1 - px0, pdep); rgba(c, (0.18, 0.14, 0.12)); c.fill()
    c.rectangle(px0, gy, px1 - px0, pdep); rgba(c, (0.55, 0.45, 0.36)); c.set_line_width(5); c.stroke()
    # lifted lid (wooden board)
    c.save(); c.translate(px0, gy - 6); c.rotate(-1.15 * show)
    c.rectangle(0, -14, px1 - px0, 16); fill2(c, (0.62, 0.42, 0.24), 1, 2.5, 0.7); c.restore()
    # 炉腔 under the window, inside
    fx, fy = wx + 60, gy + 250
    c.rectangle(wx - 40, gy + 150, 200, 150); rgba(c, (0.30, 0.18, 0.12)); c.fill()
    c.rectangle(wx - 40, gy + 150, 200, 150); rgba(c, (0.62, 0.48, 0.36)); c.set_line_width(5); c.stroke()
    # opening from pit to furnace
    c.rectangle(px1 - 4, gy + 210, wx - 40 - px1 + 8, 70); rgba(c, (0.24, 0.16, 0.12)); c.fill()
    flames(c, fx, fy + 40, 150, 120 * heat, T, 1.0, 2)
    for k in range(5):
        rr(c, fx - 70 + k * 30, fy + 22, 24, 16, 4); rgba(c, (0.15, 0.12, 0.12)); c.fill()
    # main flue sloping up toward room interior
    fx1 = 1760
    c.move_to(wx + 160, gy + 150); c.line_to(fx1, gy + 60); c.line_to(fx1, gy + 120); c.line_to(wx + 160, gy + 230); c.close_path()
    rgba(c, (0.24, 0.15, 0.11)); c.fill()
    # floor bricks on piers (架空)
    for k in range(int((W - wx) / 70) + 1):
        bx = wx + k * 70
        c.rectangle(bx + 2, gy, 66, 26); fill2(c, (0.60, 0.56, 0.54), 1, 2, 0.7)
        if k % 2 == 0 and bx + 30 < fx1 and bx > wx + 180:
            yy = gy + 26
            yb_ = gy + 150 - (bx - wx - 160) / (fx1 - wx - 160) * 90
            c.rectangle(bx + 26, yy, 18, max(4, yb_ - yy)); rgba(c, (0.50, 0.42, 0.36)); c.fill()
    # heat flow particles along flue
    if heat > 0.01:
        for i in range(26):
            u = ((T * 0.35 + i / 26) % 1.0)
            xx = lerp(wx + 170, fx1 - 20, u)
            yy = lerp(gy + 190, gy + 92, u) + math.sin(T * 6 + i) * 12
            c.arc(xx, yy, 7, 0, TAU); rgba(c, lerpc(FIREL, (0.85, 0.55, 0.45), u), 0.85 * heat); c.fill()
        heatwaves(c, wx + 120, W - 60, gy - 10, T, 0.75 * heat, 8, 190)
    # exit vent at 台基 side (right, outdoor at rear)
    c.rectangle(fx1, gy - 40, W - fx1, H); rgba(c, (0.78, 0.78, 0.80)); c.fill()
    c.rectangle(fx1, gy + 60, 50, 60); rgba(c, (0.20, 0.16, 0.14)); c.fill()
    for k in range(2):
        c.arc(fx1 + 25, gy + 76 + k * 28, 11, 0, TAU); rgba(c, (0.80, 0.80, 0.82)); c.set_line_width(4); c.stroke()
    c.rectangle(fx1 + 50, gy + 60, W - fx1, 60); rgba(c, (0.24, 0.15, 0.11)); c.fill()
    if smoke_a > 0:
        smoke(c, W - 60, gy + 70, T, 0.55 * smoke_a * heat, 4, (0.85, 0.85, 0.90), 20, 120)
    # window wall
    c.rectangle(wx - 30, 330, 60, gy - 330); fill2(c, (0.62, 0.17, 0.13), 1, 3, 0.75)
    c.rectangle(wx - 22, 380, 44, 200); rgba(c, (0.98, 0.84, 0.55)); c.fill()
    rgba(c, (0.36, 0.14, 0.10)); c.set_line_width(3)
    for j in range(1, 5):
        c.move_to(wx - 22, 380 + j * 40); c.line_to(wx + 22, 380 + j * 40); c.stroke()
    c.rectangle(0, gy, W, 4); rgba(c, (0.30, 0.22, 0.16)); c.fill()


# ---------------------------------------------------------------- props
def charcoal(c, x, y, L=300, R=40, rot=0.0, a=1.0, ember=0.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    rr(c, -L / 2, -R, L, 2 * R, R * 0.45); fill2(c, (0.18, 0.16, 0.16), a, 3, 2.0)
    rgba(c, (0.36, 0.33, 0.33), a); c.set_line_width(3)
    for k in range(-3, 4):
        c.move_to(-L / 2 + 20, k * R * 0.24); c.line_to(L / 2 - 20, k * R * 0.24 + math.sin(k) * 4); c.stroke()
    ell(c, L / 2, 0, R * 0.38, R); fill2(c, (0.30, 0.27, 0.26), a, 2.5, 1.6)
    for k in range(4):
        ang = k * 1.57 + 0.3
        c.move_to(L / 2, 0); c.line_to(L / 2 + math.cos(ang) * R * 0.3, math.sin(ang) * R * 0.85)
        rgba(c, (0.50, 0.46, 0.44), a); c.set_line_width(2); c.stroke()
    if ember > 0:
        glow(c, L / 2, 0, R * 2.2, FIRE, 0.6 * ember * a)
        ell(c, L / 2, 0, R * 0.32, R * 0.85); rgba(c, EMBER, ember * a); c.fill()
    c.restore()


def tree(c, x, yb, s=1.0, a=1.0, snowy=True):
    c.save(); c.translate(x, yb); c.scale(s, s)
    c.rectangle(-14, -120, 28, 120); fill2(c, (0.45, 0.30, 0.20), a, 2.5)
    for k, (yy, w_) in enumerate(((-120, 110), (-190, 90), (-250, 64))):
        c.move_to(-w_, yy); c.line_to(0, yy - 110); c.line_to(w_, yy); c.close_path(); fill2(c, (0.26, 0.46, 0.36), a, 2.5)
        if snowy:
            c.move_to(-w_ * 0.5, yy - 55); c.line_to(0, yy - 110); c.line_to(w_ * 0.5, yy - 55); c.close_path(); rgba(c, SNOWW, a); c.fill()
    c.restore()


def xunlong(c, x, yb, s=1.0, a=1.0, ex=0.0, T=0.0, fire=1.0):
    """熏笼：炭火盆 + 铜镂空罩；ex=0..1 罩子抬起拆解"""
    c.save(); c.translate(x, yb); c.scale(s, s)
    # basin on legs
    for sx in (-1, 1):
        c.move_to(sx * 120, -90); c.line_to(sx * 150, 0); rgba(c, (0.55, 0.40, 0.18), a); c.set_line_width(16); c.stroke()
    c.move_to(-190, -170); c.line_to(190, -170); c.curve_to(170, -90, 120, -80, 0, -80); c.curve_to(-120, -80, -170, -90, -190, -170); c.close_path()
    fill2(c, (0.80, 0.58, 0.24), a, 3, 0.7)
    rgba(c, (0.20, 0.40, 0.65), a); c.rectangle(-160, -150, 320, 26); c.fill()
    for k in range(-5, 6):
        c.arc(k * 28, -137, 6, 0, TAU); rgba(c, (0.95, 0.80, 0.35), a); c.fill()
    # coals
    for k in range(-4, 5):
        ell(c, k * 34, -176, 22, 12); rgba(c, (0.20, 0.16, 0.15), a); c.fill()
    if fire > 0:
        glow(c, 0, -190, 220, FIRE, 0.45 * fire * a)
        for k in range(-3, 4, 2):
            ell(c, k * 34, -180, 12, 6); rgba(c, EMBER, fire * a * (0.7 + 0.3 * math.sin(T * 5 + k))); c.fill()
    # dome cover
    lift = ex * 230
    c.save(); c.translate(0, -lift)
    c.move_to(-180, -172); c.curve_to(-180, -330, 180, -330, 180, -172); c.close_path()
    rgba(c, (0.85, 0.62, 0.26), a * 0.92); c.fill_preserve(); rgba(c, (0.55, 0.38, 0.14), a); c.set_line_width(4); c.stroke()
    # lattice holes
    c.save(); c.move_to(-180, -172); c.curve_to(-180, -330, 180, -330, 180, -172); c.close_path(); c.clip()
    for i in range(-6, 7):
        for j in range(4):
            cx_, cy_ = i * 28 + (j % 2) * 14, -196 - j * 30
            c.arc(cx_, cy_, 8, 0, TAU); rgba(c, (0.30, 0.16, 0.08) if fire < 0.5 else (1.0, 0.55, 0.2), a * 0.85); c.fill()
    c.restore()
    c.arc(0, -300, 18, 0, TAU); fill2(c, GOLDL, a, 2, 0.7)
    c.restore()
    c.restore()


def shoulu(c, x, y, s=1.0, a=1.0, ex=0.0, T=0.0):
    """手炉拆解：镂空盖 / 铜内胆(炭) / 外壳 / 提梁 (ex 0..1 爆炸分离)"""
    c.save(); c.translate(x, y); c.scale(s, s)
    d = ex
    # 外壳 (bottom layer)
    c.save(); c.translate(0, 110 * d)
    c.move_to(-170, -40); c.curve_to(-180, 60, -130, 100, 0, 100); c.curve_to(130, 100, 180, 60, 170, -40); c.close_path()
    fill2(c, (0.22, 0.42, 0.68), a, 3, 0.7)
    for k in range(-3, 4):
        c.arc(k * 42, 30, 14, 0, TAU); rgba(c, (0.95, 0.78, 0.40), a); c.fill()
        c.arc(k * 42, 30, 7, 0, TAU); rgba(c, (0.85, 0.30, 0.30), a); c.fill()
    ell(c, 0, -40, 170, 26); fill2(c, (0.18, 0.34, 0.56), a, 3, 0.7)
    c.restore()
    # 铜内胆 with charcoal
    c.save(); c.translate(0, -30 * d)
    c.move_to(-140, -46); c.curve_to(-140, 20, -100, 40, 0, 40); c.curve_to(100, 40, 140, 20, 140, -46); c.close_path()
    fill2(c, (0.86, 0.56, 0.30), a, 3, 0.7)
    ell(c, 0, -46, 140, 20); rgba(c, (0.30, 0.20, 0.16), a); c.fill()
    for k in range(-3, 4):
        ell(c, k * 34, -50, 18, 9); rgba(c, (0.18, 0.15, 0.14), a); c.fill()
    glow(c, 0, -50, 120, FIRE, 0.45 * a)
    for k in (-2, 0, 2):
        ell(c, k * 34, -52, 8, 4); rgba(c, EMBER, a * (0.7 + 0.3 * math.sin(T * 5 + k))); c.fill()
    c.restore()
    # 镂空盖
    c.save(); c.translate(0, -60 - 150 * d)
    ell(c, 0, 0, 172, 30); fill2(c, (0.92, 0.72, 0.32), a, 3, 0.7)
    c.save(); ell(c, 0, 0, 160, 24); c.clip()
    for i in range(-9, 10):
        for j in range(-2, 3):
            c.arc(i * 18 + (j % 2) * 9, j * 9, 3.2, 0, TAU); rgba(c, (0.40, 0.25, 0.10), a); c.fill()
    c.restore()
    c.restore()
    # 提梁
    c.save(); c.translate(0, -60 - 220 * d)
    c.move_to(-150, 0); c.curve_to(-120, -130, 120, -130, 150, 0)
    rgba(c, (0.80, 0.60, 0.26), a); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.restore()
    c.restore()


def jiaolu(c, x, yb, s=1.0, a=1.0, T=0.0):
    c.save(); c.translate(x, yb); c.scale(s, s)
    glow(c, 0, -80, 200, FIRE, 0.4 * a)
    rr(c, -150, -110, 300, 110, 30); fill2(c, (0.72, 0.50, 0.24), a, 3, 0.7)
    ell(c, 0, -110, 150, 26); fill2(c, (0.88, 0.68, 0.32), a, 3, 0.7)
    c.save(); ell(c, 0, -110, 138, 20); c.clip()
    for i in range(-8, 9):
        for j in range(-2, 3):
            c.arc(i * 17 + (j % 2) * 8, -110 + j * 8, 3, 0, TAU); rgba(c, (0.95, 0.45, 0.15), a * (0.6 + 0.4 * math.sin(T * 4 + i))); c.fill()
    c.restore()
    c.restore()


def tonggang(c, x, yb, s=1.0, a=1.0, T=0.0, fire=1.0, cover=1.0):
    """铜缸 + 缸盖/缸套 + 石座下烧炭"""
    c.save(); c.translate(x, yb); c.scale(s, s)
    # stone base with fire opening
    c.rectangle(-210, -90, 420, 90); fill2(c, (0.86, 0.86, 0.88), a, 3, 0.72)
    c.move_to(-70, 0); c.line_to(-70, -50); c.arc(0, -50, 70, math.pi, TAU); c.line_to(70, 0); c.close_path(); rgba(c, (0.18, 0.12, 0.10), a); c.fill()
    if fire > 0:
        flames(c, 0, -4, 110, 90 * fire, T, a, 4)
    # vat
    c.move_to(-230, -380); c.curve_to(-280, -250, -230, -110, -150, -90); c.line_to(150, -90); c.curve_to(230, -110, 280, -250, 230, -380); c.close_path()
    fill2(c, (0.62, 0.46, 0.26), a, 3, 0.7)
    for sx in (-1, 1):
        c.arc(sx * 230, -280, 26, 0, TAU); rgba(c, (0.45, 0.32, 0.16), a); c.set_line_width(8); c.stroke()
    rgba(c, (0.78, 0.62, 0.36), a); c.set_line_width(4)
    c.move_to(-240, -330); c.curve_to(-80, -315, 80, -315, 240, -330); c.stroke()
    if cover > 0:
        # 缸套 quilted cover + 缸盖
        c.save(); c.translate(0, -(1 - cover) * 120)
        ell(c, 0, -380, 250, 36); fill2(c, (0.30, 0.40, 0.62), a * cover, 3, 0.7)
        c.move_to(-250, -380); c.line_to(-262, -300); c.curve_to(-90, -280, 90, -280, 262, -300); c.line_to(250, -380); c.close_path()
        fill2(c, (0.36, 0.48, 0.72), a * cover, 3, 0.7)
        rgba(c, (0.25, 0.34, 0.52), a * cover); c.set_line_width(3)
        for k in range(-5, 6):
            c.move_to(k * 46, -376); c.line_to(k * 49, -292); c.stroke()
        c.arc(0, -414, 16, 0, TAU); fill2(c, GOLDL, a * cover, 2, 0.7)
        roofsnow(c, -230, 230, -406, a * cover * 0.9, 6)
        c.restore()
    c.restore()


def calendar(c, x, y, top, big, sub, a=1.0, s=1.0, col=REDL):
    if a <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -180, -230, 360, 460, 14); rgba(c, (0.98, 0.96, 0.90), a); c.fill_preserve(); rgba(c, (0.70, 0.62, 0.50), a); c.set_line_width(3); c.stroke()
    rr(c, -180, -230, 360, 110, 14); rgba(c, col, a); c.fill()
    c.rectangle(-180, -150, 360, 30); rgba(c, col, a); c.fill()
    for sx in (-110, 110):
        c.arc(sx, -230, 14, 0, TAU); rgba(c, (0.35, 0.28, 0.22), a); c.fill()
    ts = min(56, 300 / max(1, len(top)))
    text(c, top, 0, -152, ts, WHITE, a, align='c', shadow=0)
    bs = min(150, 320 / max(1, len(big)) * 1.0)
    text(c, big, 0, 40 + bs * 0.25, bs, (0.25, 0.16, 0.12), a, align='c', shadow=0)
    text(c, sub, 0, 170, 44, (0.50, 0.40, 0.30), a, align='c', shadow=0)
    c.restore()


def xiaohan(c, t, x, y, cell=150, prog=0.0, a=1.0, chars='亭前垂柳珍重待春風'):
    """九九消寒图：3x3 双钩字，prog 0..9 填充进度（示意：逐字由下而上描红）"""
    if a <= 0.01:
        return
    W_ = cell * 3 + 60
    rr(c, x - W_ / 2, y - W_ / 2 - 70, W_, W_ + 90, 10); rgba(c, (0.97, 0.94, 0.86), a); c.fill_preserve()
    rgba(c, (0.62, 0.46, 0.28), a); c.set_line_width(4); c.stroke()
    text(c, '管城春满', x, y - W_ / 2 - 18, 44, (0.55, 0.20, 0.14), a, align='c', shadow=0)
    for i, ch in enumerate(chars):
        cx = x + (i % 3 - 1) * cell; cy = y + (i // 3 - 1) * cell + 10
        rr(c, cx - cell / 2 + 6, cy - cell / 2 + 6, cell - 12, cell - 12, 4); rgba(c, (0.82, 0.30, 0.22), a * 0.5); c.set_line_width(2); c.stroke()
        size = cell * 0.78
        font(c, size); w = c.text_extents(ch)[4]
        tx, ty = cx - w / 2, cy + size * 0.36
        f = clamp(prog - i)
        if f > 0:
            c.save()
            top_ = cy + cell / 2 - cell * f
            c.rectangle(cx - cell / 2, top_, cell, cell * f + 4); c.clip()
            c.move_to(tx, ty); c.text_path(ch); rgba(c, (0.85, 0.16, 0.12), a); c.fill()
            c.restore()
        c.move_to(tx, ty); c.text_path(ch); rgba(c, (0.78, 0.18, 0.14), a); c.set_line_width(2.5); c.stroke()


def bars(c, t, t0, items, x0=200, yb=900, bw=150, gap=40, hmax=560, vmax=120, a=1.0):
    """stacked bars: items = (name, red, black)"""
    for i, (nm, rd, bk) in enumerate(items):
        p = eout(seg(t, t0 + i * 0.22, t0 + i * 0.22 + 0.5))
        if p <= 0:
            continue
        rec(t0 + i * 0.22, 'tick')
        x = x0 + i * (bw + gap)
        hb = bk / vmax * hmax * p; hr = rd / vmax * hmax * p
        c.rectangle(x, yb - hb, bw, hb); fill2(c, (0.30, 0.30, 0.34), a, 3, 0.6)
        c.rectangle(x, yb - hb - hr, bw, hr); fill2(c, (0.88, 0.30, 0.20), a, 3, 0.7)
        tot = rd + bk
        otext(c, '%d' % tot, x + bw / 2, yb - hb - hr - 22, 54, GOLDL if i == 0 else WHITE, a * p, align='c')
        otext(c, nm, x + bw / 2, yb + 62, 44, WHITE, a, align='c')
