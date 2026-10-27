import math, random
from core import *
from sets import vgrad, lantern, roofline
from winter import flames, smoke, FIRE, FIREL, EMBER

BRICK = (0.62, 0.36, 0.26)
WOODC = (0.58, 0.38, 0.22)
HEMP = (0.86, 0.74, 0.50)
MUD = (0.45, 0.33, 0.22)
WATER = (0.45, 0.72, 0.95)
NIGHT_TOP = (0.05, 0.07, 0.17)
NIGHT_BOT = (0.13, 0.17, 0.33)


def nightsky(c, T, hor=760, glowx=None):
    vgrad(c, 0, hor, NIGHT_TOP, NIGHT_BOT)
    rnd = random.Random(5)
    for i in range(70):
        rgba(c, (1, 1, 0.9), 0.35 + 0.35 * math.sin(T * 2 + i)); c.arc(rnd.random() * W, rnd.random() * hor * 0.6, rnd.uniform(1, 2.2), 0, TAU); c.fill()
    c.arc(1650, 170, 46, 0, TAU); rgba(c, (0.98, 0.94, 0.80), 0.9); c.fill()
    if glowx is not None:
        glow(c, glowx, hor - 100, 700, FIRE, 0.25)


def house(c, x, yb, w=260, h=210, a=1.0, wall=(0.93, 0.87, 0.73), roof=(0.25, 0.26, 0.32), door=(0.40, 0.28, 0.20), lit=False, burnt=0.0, two=False):
    """Song-style row house; burnt 0..1 blackens"""
    if a <= 0.01:
        return
    wallc = lerpc(wall, (0.16, 0.12, 0.10), burnt); roofc = lerpc(roof, (0.08, 0.07, 0.07), burnt)
    top = yb - h
    if two:
        c.rectangle(x + 16, top - 110, w - 32, 110); rgba(c, dk(wallc, 0.92), a); c.fill()
        c.rectangle(x + 40, top - 86, 60, 46); rgba(c, (1.0, 0.82, 0.45) if lit else dk(door, 1.1), a); c.fill()
        c.rectangle(x + w - 100, top - 86, 60, 46); c.fill()
        roofline(c, x + 10, x + w - 10, top - 110, roofc, 50)
    c.rectangle(x, top, w, h); rgba(c, wallc, a); c.fill()
    rgba(c, dk(wallc, 0.8), a); c.set_line_width(3); c.rectangle(x, top, w, h); c.stroke()
    roofline(c, x - 8, x + w + 8, top, roofc, 46)
    c.rectangle(x + w * 0.35, yb - h * 0.62, w * 0.3, h * 0.62); rgba(c, door, a); c.fill()
    c.rectangle(x + 18, top + 30, w * 0.22, h * 0.28); rgba(c, (1.0, 0.82, 0.45) if lit else dk(door, 1.2), a); c.fill()


def rowhouses(c, T, yb, x0=-40, n=9, w=250, gap=6, seed=2, burnt_idx=(), fire_idx=(), fire_h=0.0, night=False, lit=True, ba=0.0):
    rnd = random.Random(seed)
    wall = (0.80, 0.62, 0.38) if night else (0.93, 0.87, 0.73)
    roof = (0.10, 0.12, 0.22) if night else (0.25, 0.26, 0.32)
    door = (0.26, 0.16, 0.12) if night else (0.40, 0.28, 0.20)
    pos = []
    for i in range(n):
        h = rnd.choice((190, 220, 250)); two = rnd.random() < 0.55
        x = x0 + i * (w + gap)
        house(c, x, yb, w, h, 1.0, wall, roof, door, lit=night and lit and rnd.random() < 0.6, burnt=(ba if i in burnt_idx else 0), two=two)
        pos.append((x + w / 2, yb - h - (110 if two else 0)))
    for i in fire_idx:
        if i < len(pos):
            px, py = pos[i]
            flames(c, px, py + 60, w * 0.9, 260 * fire_h, T, 1.0, seed=i)
            smoke(c, px, py - 140 * fire_h, T, 0.5 * fire_h, 6, (0.35, 0.32, 0.34), 60, 220)
    return pos


def watchtower(c, x, yb, s=1.0, a=1.0, T=0.0, rise=1.0, flags=0, flagcol=(0.92, 0.22, 0.16), lamps=0, watcher=True, label=None):
    """brick 望火楼: tapered brick tower + lookout pavilion"""
    if a <= 0.01 or rise <= 0.01:
        return
    c.save(); c.translate(x, yb); c.scale(s, s)
    hh = 520 * rise
    c.move_to(-130, 0); c.line_to(130, 0); c.line_to(95, -hh); c.line_to(-95, -hh); c.close_path()
    rgba(c, BRICK, a); c.fill_preserve(); rgba(c, dk(BRICK, 0.7), a); c.set_line_width(4); c.stroke()
    c.save(); c.move_to(-130, 0); c.line_to(130, 0); c.line_to(95, -hh); c.line_to(-95, -hh); c.close_path(); c.clip()
    rgba(c, dk(BRICK, 0.82), a); c.set_line_width(2)
    for k in range(int(hh // 34)):
        y = -k * 34
        c.move_to(-140, y); c.line_to(140, y); c.stroke()
        off = 30 if k % 2 else 0
        for j in range(-5, 6):
            c.move_to(j * 60 + off, y); c.line_to(j * 60 + off, y - 34); c.stroke()
    c.restore()
    # door
    c.move_to(-36, 0); c.line_to(-36, -90); c.arc(0, -90, 36, math.pi, TAU); c.line_to(36, 0); c.close_path(); rgba(c, (0.18, 0.11, 0.08), a); c.fill()
    if rise >= 0.98:
        top = -hh
        # pavilion
        c.rectangle(-110, top - 14, 220, 16); rgba(c, (0.45, 0.28, 0.16), a); c.fill()
        for px in (-96, 96):
            c.rectangle(px - 7, top - 130, 14, 118); rgba(c, (0.62, 0.20, 0.14), a); c.fill()
        c.rectangle(-104, top - 50, 208, 10); rgba(c, (0.62, 0.20, 0.14), a); c.fill()
        if watcher:
            bob = math.sin(T * 2.2) * 3
            c.arc(0, top - 92 + bob, 30, 0, TAU); rgba(c, (0.99, 0.96, 0.92), a); c.fill()
            c.arc(0, top - 98 + bob, 31, math.pi * 1.05, math.pi * 1.95); c.close_path(); rgba(c, (0.40, 0.40, 0.44), a); c.fill()
            c.move_to(0, top - 130 + bob); c.line_to(0, top - 150 + bob); rgba(c, (0.82, 0.16, 0.14), a); c.set_line_width(6); c.stroke()
            for ex in (-10, 10):
                c.arc(ex, top - 90 + bob, 3.5, 0, TAU); rgba(c, EYE_C, a); c.fill()
            ell(c, -18, top - 80 + bob, 6, 3.5); rgba(c, (0.97, 0.62, 0.64), a); c.fill()
            ell(c, 18, top - 80 + bob, 6, 3.5); c.fill()
        # roof
        c.move_to(-160, top - 118); c.curve_to(-90, top - 132, -40, top - 190, 0, top - 200)
        c.curve_to(40, top - 190, 90, top - 132, 160, top - 118); c.line_to(140, top - 136); c.line_to(-140, top - 136); c.close_path()
        rgba(c, (0.22, 0.22, 0.28), a); c.fill()
        c.move_to(-160, top - 118); c.line_to(160, top - 118); rgba(c, (0.10, 0.10, 0.14), a); c.set_line_width(6); c.stroke()
        # flag pole and flags
        if flags or lamps:
            c.move_to(130, top - 120); c.line_to(130, top - 380); rgba(c, (0.40, 0.28, 0.18), a); c.set_line_width(8); c.stroke()
            for k in range(flags):
                fy = top - 370 + k * 72
                wv = math.sin(T * 6 + k) * 10
                c.move_to(134, fy); c.curve_to(180, fy - 8 + wv, 220, fy + 8 - wv, 260, fy + wv * 0.5)
                c.line_to(260, fy + 50 + wv * 0.5); c.curve_to(220, fy + 58 - wv, 180, fy + 42 + wv, 134, fy + 50); c.close_path()
                rgba(c, flagcol, a); c.fill()
            for k in range(lamps):
                ly = top - 340 + k * 80
                glow(c, 160, ly, 70, (1.0, 0.62, 0.30), 0.5 * a)
                ell(c, 160, ly, 26, 22); rgba(c, (0.95, 0.30, 0.18), a); c.fill()
                c.rectangle(150, ly - 28, 20, 6); rgba(c, (0.2, 0.12, 0.08), a); c.fill()
    if label:
        tagbox(c, label, 0, -hh * 0.45, a, GOLDL, 46)
    c.restore()


EYE_C = (0.14, 0.10, 0.09)


def tagbox(c, s_, x, y, a=1.0, col=GOLDL, size=40):
    if a <= 0.01:
        return
    w = tw(c, s_, size) + 30
    rr(c, x - w / 2, y - size * 0.95, w, size * 1.35, 8)
    c.set_source_rgba(0.12, 0.08, 0.06, 0.92 * a); c.fill_preserve(); rgba(c, col, a); c.set_line_width(3); c.stroke()
    text(c, s_, x, y + size * 0.12, size, col, a, align='c', shadow=0)


def puhut(c, x, yb, s=1.0, a=1.0, night=False, label='军巡铺'):
    """small guard hut with vertical sign"""
    if a <= 0.01:
        return
    c.save(); c.translate(x, yb); c.scale(s, s)
    wall = (0.80, 0.62, 0.38) if night else (0.90, 0.80, 0.62)
    c.rectangle(-170, -230, 340, 230); rgba(c, wall, a); c.fill_preserve(); rgba(c, dk(wall, 0.75), a); c.set_line_width(4); c.stroke()
    roofline(c, -195, 195, -230, (0.22, 0.22, 0.28), 60)
    c.rectangle(-60, -170, 120, 170); rgba(c, (0.32, 0.20, 0.14), a); c.fill()
    if night:
        glow(c, 0, -90, 120, (1.0, 0.7, 0.35), 0.35 * a)
        c.rectangle(-50, -160, 100, 80); rgba(c, (1.0, 0.82, 0.45), a); c.fill()
    # sign board
    c.rectangle(110, -215, 52, 170); rgba(c, (0.97, 0.94, 0.86), a); c.fill_preserve(); rgba(c, (0.55, 0.40, 0.30), a); c.set_line_width(3); c.stroke()
    vtext(c, label, 136, -202, 46, (0.75, 0.15, 0.12), a)
    c.restore()


def flag(c, x, y, s=1.0, col=(0.92, 0.22, 0.16), a=1.0, T=0.0, pole=180):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, 0); c.line_to(0, -pole); rgba(c, (0.40, 0.28, 0.18), a); c.set_line_width(7); c.stroke()
    wv = math.sin(T * 6 + x) * 9
    fy = -pole + 6
    c.move_to(3, fy); c.curve_to(40, fy - 8 + wv, 80, fy + 8 - wv, 112, fy + wv * 0.5)
    c.line_to(112, fy + 64 + wv * 0.5); c.curve_to(80, fy + 72 - wv, 40, fy + 56 + wv, 3, fy + 64); c.close_path()
    rgba(c, col, a); c.fill()
    c.restore()


# -------------------------------------------------------------- tools (each centred at x,y, roughly 220px tall at s=1)
def t_bucket(c, x, y, s=1.0, a=1.0, water=True, T=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-60, -60); c.line_to(60, -60); c.line_to(48, 70); c.line_to(-48, 70); c.close_path(); fill2(c, WOODC, a, 3)
    for yy in (-30, 40):
        c.move_to(-58, yy); c.line_to(58, yy); rgba(c, (0.30, 0.22, 0.16), a); c.set_line_width(6); c.stroke()
    if water:
        ell(c, 0, -60, 58, 12); rgba(c, WATER, a); c.fill()
    c.arc(0, -60, 70, math.pi * 1.1, math.pi * 1.9); rgba(c, (0.30, 0.22, 0.16), a); c.set_line_width(5); c.stroke()
    c.restore()


def t_sazi(c, x, y, s=1.0, a=1.0):  # 洒子: wicker scoop on a short pole
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-20, 90); c.line_to(20, -40); rgba(c, WOODC, a); c.set_line_width(12); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.arc(30, -70, 50, 0, math.pi); c.close_path(); fill2(c, (0.80, 0.66, 0.40), a, 3)
    rgba(c, (0.55, 0.42, 0.24), a); c.set_line_width(2)
    for k in range(-3, 4):
        c.move_to(30 + k * 12, -70); c.line_to(30 + k * 10, -70 + math.sqrt(max(0, 2500 - (k * 12) ** 2)) * 0.95); c.stroke()
    c.restore()


def t_mada(c, x, y, s=1.0, a=1.0, T=0.0, mud=1.0, rot=0.0):  # 麻搭: 8-chi pole + hemp tuft dipped in mud
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.move_to(0, 160); c.line_to(0, -110); rgba(c, WOODC, a); c.set_line_width(14); c.stroke()
    rnd = random.Random(4)
    for i in range(26):
        ang = -math.pi / 2 + rnd.uniform(-0.9, 0.9)
        L = rnd.uniform(70, 120)
        sw = math.sin(T * 5 + i) * 6
        c.move_to(0, -110)
        c.curve_to(math.cos(ang) * L * 0.4, -110 + 30, math.cos(ang) * L * 0.8 + sw, -110 + L * 0.6, math.cos(ang) * L + sw, -110 + L)
        rgba(c, lerpc(HEMP, MUD, mud * (0.5 + 0.5 * (i % 3) / 2)), a); c.set_line_width(6); c.stroke()
    c.rectangle(-12, -122, 24, 18); rgba(c, (0.30, 0.22, 0.16), a); c.fill()
    c.restore()


def t_axe(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, 100); c.line_to(0, -90); rgba(c, WOODC, a); c.set_line_width(14); c.stroke()
    c.move_to(-6, -90); c.line_to(-80, -110); c.curve_to(-100, -70, -100, -30, -80, -10); c.line_to(-6, -40); c.close_path()
    fill2(c, (0.72, 0.74, 0.78), a, 3, 0.6)
    c.restore()


def t_saw(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-110, -80, 220, 14); rgba(c, WOODC, a); c.fill()
    for xx in (-104, 104):
        c.rectangle(xx - 7, -80, 14, 150); c.fill()
    c.move_to(-104, 40); c.line_to(104, 40); rgba(c, (0.72, 0.74, 0.78), a); c.set_line_width(10); c.stroke()
    for k in range(18):
        c.move_to(-100 + k * 11.5, 45); c.line_to(-94 + k * 11.5, 58); c.line_to(-88 + k * 11.5, 45); c.close_path(); c.fill()
    c.move_to(0, -66); c.line_to(0, 34); rgba(c, (0.40, 0.30, 0.20), a); c.set_line_width(3); c.stroke()
    c.restore()


def t_ladder(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for xx in (-40, 40):
        c.move_to(xx, 120); c.line_to(xx * 0.7, -120); rgba(c, WOODC, a); c.set_line_width(12); c.stroke()
    for k in range(6):
        yy = 100 - k * 42; f = 1 - (100 - yy) / 240 * 0.3
        c.move_to(-40 * f, yy); c.line_to(40 * f, yy); c.set_line_width(8); c.stroke()
    c.restore()


def t_fork(c, x, y, s=1.0, a=1.0):  # 火叉
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, 130); c.line_to(0, -60); rgba(c, WOODC, a); c.set_line_width(12); c.stroke()
    rgba(c, (0.62, 0.64, 0.68), a); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(-34, -60); c.line_to(34, -60); c.stroke()
    for xx in (-34, 34):
        c.move_to(xx, -60); c.line_to(xx, -125); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.restore()


def t_rope(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(5):
        ell(c, 0, 0, 80 - k * 12, 50 - k * 8); rgba(c, lerpc((0.80, 0.66, 0.40), (0.62, 0.48, 0.28), k / 5), a); c.set_line_width(12); c.stroke()
    c.move_to(70, 10); c.curve_to(110, 40, 100, 90, 70, 110); c.stroke()
    c.restore()


def t_grapnel(c, x, y, s=1.0, a=1.0):  # 铁猫儿
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, -120); c.line_to(0, 50); rgba(c, (0.55, 0.56, 0.60), a); c.set_line_width(12); c.stroke()
    c.arc(0, -130, 16, 0, TAU); c.set_line_width(7); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(11)
    for sx in (-1, 0, 1):
        c.move_to(0, 50)
        if sx == 0:
            c.line_to(0, 80); c.stroke(); continue
        c.curve_to(sx * 30, 80, sx * 70, 60, sx * 66, 10); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.restore()


def t_jitong(c, x, y, s=1.0, a=1.0, push=0.0, T=0.0, spray=0.0, rot=0.0):  # 唧筒 bamboo syringe
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rr(c, -150, -26, 250, 52, 20); fill2(c, (0.62, 0.72, 0.36), a, 3, 0.7)
    for xx in (-90, -20, 50):
        c.move_to(xx, -26); c.line_to(xx, 26); rgba(c, (0.40, 0.50, 0.22), a); c.set_line_width(5); c.stroke()
    c.move_to(100, 0); c.line_to(140, 0); c.set_line_width(14); rgba(c, (0.50, 0.60, 0.28), a); c.stroke()
    px = -150 - 120 * (1 - push)
    c.move_to(px, 0); c.line_to(-110, 0); rgba(c, WOODC, a); c.set_line_width(12); c.stroke()
    c.rectangle(px - 14, -34, 14, 68); c.fill()
    if spray > 0.01:
        for i in range(16):
            ph = (T * 3 + i / 16) % 1.0
            sx = 150 + ph * 520 * spray; sy = -ph * 60 + ph * ph * 160 + math.sin(i * 7) * 12 * ph
            c.arc(sx, sy, 9 - ph * 4, 0, TAU); rgba(c, WATER, a * (1 - ph * 0.6)); c.fill()
    c.restore()


def t_waterbag(c, x, y, s=1.0, a=1.0, squeeze=0.0, T=0.0, spray=0.0):  # 牛皮水袋 + bamboo spout
    c.save(); c.translate(x, y); c.scale(s, s)
    sq = 1 - 0.25 * squeeze
    ell(c, 0, 0, 170 * (1 + 0.1 * squeeze), 90 * sq); fill2(c, (0.62, 0.42, 0.26), a, 3, 0.7)
    rgba(c, (0.45, 0.30, 0.18), a); c.set_line_width(3)
    for k in (-1, 1):
        c.move_to(-120, k * 30 * sq); c.curve_to(-40, k * 50 * sq, 40, k * 50 * sq, 120, k * 30 * sq); c.stroke()
    c.move_to(160, -10); c.line_to(360, -60); rgba(c, (0.62, 0.72, 0.36), a); c.set_line_width(22); c.stroke()
    if spray > 0.01:
        for i in range(18):
            ph = (T * 2.6 + i / 18) % 1.0
            sx = 360 + ph * 480 * spray; sy = -60 - ph * 80 + ph * ph * 200 + math.sin(i * 5) * 14 * ph
            c.arc(sx, sy, 12 - ph * 5, 0, TAU); rgba(c, WATER, a * (1 - ph * 0.6)); c.fill()
    c.restore()


def t_vest(c, x, y, s=1.0, a=1.0):  # 火背心
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-90, -100); c.line_to(-40, -110); c.line_to(0, -60); c.line_to(40, -110); c.line_to(90, -100)
    c.line_to(100, 110); c.line_to(-100, 110); c.close_path(); fill2(c, (0.82, 0.30, 0.18), a, 3, 0.7)
    for yy in (0, 60):
        c.rectangle(-98, yy, 196, 16); rgba(c, (0.98, 0.84, 0.36), a); c.fill()
    text(c, '火', 0, -10, 60, (0.98, 0.94, 0.86), a, align='c', shadow=0)
    c.restore()


TOOLS = [('大小桶', t_bucket), ('洒子', t_sazi), ('麻搭', t_mada), ('斧', t_axe), ('锯', t_saw),
         ('梯子', t_ladder), ('火叉', t_fork), ('大索', t_rope), ('铁猫儿', t_grapnel)]


def citymap(c, T, a=1.0, x0=360, y0=230, w=1200, h=760, step=0, prog=1.0, col=GOLDL, roads=8):
    """top-down street grid; step>0 draws post dots along streets"""
    rr(c, x0, y0, w, h, 18); c.set_source_rgba(0.80, 0.70, 0.52, a); c.fill_preserve()
    rgba(c, (0.50, 0.36, 0.22), a); c.set_line_width(6); c.stroke()
    rnd = random.Random(8)
    # blocks
    for i in range(roads):
        for j in range(roads - 2):
            bx = x0 + 20 + i * (w - 40) / roads; by = y0 + 20 + j * (h - 40) / (roads - 2)
            bw = (w - 40) / roads - 22; bh = (h - 40) / (roads - 2) - 22
            for k in range(4):
                rr(c, bx + (k % 2) * bw / 2 + 3, by + (k // 2) * bh / 2 + 3, bw / 2 - 6, bh / 2 - 6, 4)
                rgba(c, (0.62, 0.48, 0.34) if rnd.random() < 0.7 else (0.55, 0.40, 0.28), a); c.fill()
    pts = []
    if step:
        for i in range(1, roads):
            xx = x0 + 20 + i * (w - 40) / roads - 11
            yy = y0 + 40
            while yy < y0 + h - 30:
                pts.append((xx, yy)); yy += step
        for j in range(1, roads - 2):
            yy = y0 + 20 + j * (h - 40) / (roads - 2) - 11
            xx = x0 + 40
            while xx < x0 + w - 30:
                pts.append((xx, yy)); xx += step
        rnd2 = random.Random(3); rnd2.shuffle(pts)
        n = len(pts)
        for k, (px, py) in enumerate(pts):
            p = back(seg(prog * n - k, 0, 1))
            if p <= 0.01:
                continue
            c.arc(px, py, 13 * p, 0, TAU); rgba(c, RED, a); c.fill_preserve(); rgba(c, (1, 0.95, 0.85), a); c.set_line_width(3); c.stroke()
    return pts


def horse_rider(c, x, yf, s=1.0, a=1.0, run=0.0, flagc=(0.92, 0.22, 0.16)):
    from chibi2 import horse
    horse(c, x, yf, s, (0.62, 0.42, 0.28), a, run)
    c.save(); c.translate(x, yf); c.scale(s, s)
    bob = abs(math.sin(run * math.pi * 2)) * 8
    c.move_to(-30, -170 - bob); c.line_to(30, -170 - bob); c.line_to(20, -250 - bob); c.line_to(-20, -250 - bob); c.close_path()
    rgba(c, (0.55, 0.22, 0.18), a); c.fill()
    c.arc(0, -282 - bob, 34, 0, TAU); rgba(c, (0.99, 0.96, 0.92), a); c.fill()
    c.arc(0, -288 - bob, 35, math.pi * 1.05, math.pi * 1.95); c.close_path(); rgba(c, (0.40, 0.40, 0.44), a); c.fill()
    for ex in (4, 20):
        c.arc(ex, -280 - bob, 4, 0, TAU); rgba(c, EYE_C, a); c.fill()
    c.move_to(-14, -250 - bob); c.line_to(-60, -400 - bob); rgba(c, (0.40, 0.28, 0.18), a); c.set_line_width(6); c.stroke()
    wv = math.sin(run * 8) * 8
    c.move_to(-60, -400 - bob); c.curve_to(-100, -400 + wv - bob, -130, -390 - wv - bob, -160, -395 - bob); c.line_to(-150, -350 - bob)
    c.curve_to(-120, -350 + wv - bob, -90, -360 - wv - bob, -52, -360 - bob); c.close_path(); rgba(c, flagc, a); c.fill()
    c.restore()


def firetruck(c, x, yb, s=1.0, a=1.0):
    c.save(); c.translate(x, yb); c.scale(s, s)
    rr(c, -260, -180, 520, 150, 16); fill2(c, (0.85, 0.16, 0.14), a, 3, 0.7)
    rr(c, 140, -260, 120, 100, 12); fill2(c, (0.85, 0.16, 0.14), a, 3, 0.7)
    rr(c, 158, -244, 84, 56, 8); rgba(c, (0.70, 0.86, 0.98), a); c.fill()
    for xx in (-220, -100, 20):
        c.rectangle(xx, -220, 110, 10); rgba(c, (0.85, 0.86, 0.90), a); c.fill()
    c.move_to(-240, -215); c.line_to(120, -215); rgba(c, (0.85, 0.86, 0.90), a); c.set_line_width(6); c.stroke()
    for xx in (-170, 170):
        c.arc(xx, -30, 44, 0, TAU); rgba(c, (0.15, 0.13, 0.13), a); c.fill(); c.arc(xx, -30, 18, 0, TAU); rgba(c, (0.7, 0.7, 0.72), a); c.fill()
    text(c, '119', -70, -90, 64, WHITE, a, align='c', shadow=0)
    c.restore()


def coins(c, x, y, n, s=1.0, a=1.0):
    for i in range(n):
        cx = x + (i % 4) * 46 * s - 70 * s; cy = y - (i // 4) * 22 * s
        ell(c, cx, cy, 30 * s, 12 * s); fill2(c, (0.95, 0.76, 0.30), a, 2, 0.7)
        c.rectangle(cx - 6 * s, cy - 3 * s, 12 * s, 6 * s); rgba(c, (0.55, 0.40, 0.14), a); c.fill()
