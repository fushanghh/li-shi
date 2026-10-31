from kit import *
import math, random

CAPE = (0.72, 0.08, 0.06)
STEEL = (0.92, 0.95, 1.0)
ZHAO = (0.20, 0.32, 0.45)

# ---------------- 共用 ----------------
def sky(c, top, bot, y1=H):
    vgrad(c, 0, y1, [(0, top), (1, bot)])

def ground(c, y, col=INK):
    c.set_source_rgb(*col); c.rectangle(0, y, W, H - y + 50); c.fill()

def baiqi(c, x, y, s=1.0, pose='stand', face=1, t=0, p=1.0, a=1, sword_lit=0.0, cape=True):
    """白起：盔 + 全片唯一红色（披风）+ 剑是唯一发光体"""
    if cape:
        c.save(); c.translate(x, y); c.scale(s * face, s)
        wv = math.sin(t * 3.2) * 18
        c.move_to(-10, -205); c.curve_to(-70, -150, -110 + wv, -60, -140 + wv * 1.5, -8)
        c.line_to(-60 + wv * 0.5, 0); c.curve_to(-50, -80, -30, -150, 20, -200); c.close_path()
        c.set_source_rgba(*CAPE, a); c.fill()
        c.restore()
    sil(c, x, y, s, hat='helm', pose=pose, face=face, a=a, p=p)
    if pose == 'sword' and sword_lit > 0:
        q = ease(p)
        hx, hy = x + face * 55 * s, y - 300 * s
        tx, ty = x + face * lerp(55, 150, q) * s, y + lerp(-480, -330, q) * s
        glow(c, (hx + tx) / 2, (hy + ty) / 2, 220 * s, (0.75, 0.85, 1.0), 0.45 * sword_lit)
        c.set_source_rgba(*STEEL, sword_lit); c.set_line_width(9 * s); c.set_line_cap(1)
        c.move_to(hx, hy); c.line_to(tx, ty); c.stroke()

def spear_row(c, y, n, s, x0, x1, face=1, hat='helm', t=0, march=0.0, a=1, col=INK, spears=True):
    for i in range(n):
        x = lerp(x0, x1, i / max(1, n - 1)) + march
        bob = abs(math.sin(t * 7 + i)) * 6 * (1 if march else 0)
        sil(c, x, y - bob, s, hat=hat, pose='stand', face=face, a=a, col=col)
        if spears:
            c.set_source_rgba(*col, a); c.set_line_width(4 * s + 1)
            c.move_to(x + face * 30 * s, y - 60 * s - bob); c.line_to(x + face * 48 * s, y - 380 * s - bob); c.stroke()
            poly(c, [(x + face * 44 * s, y - 375 * s - bob), (x + face * 54 * s, y - 375 * s - bob), (x + face * 50 * s, y - 410 * s - bob)], col, a)

def army(c, y0, rows, n, s0, x0, x1, face=1, hat='helm', t=0, march=0.0, a=1, col=INK):
    for r in range(rows):
        k = r / max(1, rows - 1)
        spear_row(c, y0 + r * 60 * s0, n + r * 2, s0 * (0.6 + 0.5 * k), x0 - r * 40, x1 + r * 40, face, hat, t, march * (0.5 + k), a, col)

def arrows(c, t, n=60, seed=5, ang=0.35, col=(0.05, 0.04, 0.04), a=1, speed=1800):
    rnd = random.Random(seed)
    for i in range(n):
        x0 = rnd.uniform(-600, W); y0 = rnd.uniform(-400, H); ph = rnd.uniform(0, 1)
        d = ((t * speed / 1000 + ph) % 1.0) * 1600
        x = x0 + math.cos(ang) * d; y = y0 + math.sin(ang) * d - 400
        c.set_source_rgba(*col, a); c.set_line_width(3)
        c.move_to(x, y); c.line_to(x - math.cos(ang) * 70, y - math.sin(ang) * 70); c.stroke()

def embers(c, t, n=60, seed=9, a=0.8):
    rnd = random.Random(seed)
    for i in range(n):
        x = rnd.uniform(0, W); sp = rnd.uniform(60, 200); y = (rnd.uniform(0, H) - t * sp) % (H + 100)
        x += math.sin(t * 2 + i) * 20; r = rnd.uniform(1.5, 4)
        c.set_source_rgba(1, rnd.uniform(0.4, 0.7), 0.15, a * rnd.uniform(0.4, 1)); c.arc(x, y, r, 0, 6.28); c.fill()

def smoke(c, t, y=700, col=(0.1, 0.08, 0.07), a=0.5, seed=3):
    rnd = random.Random(seed)
    for i in range(14):
        x = (rnd.uniform(0, W) + t * 40) % (W + 400) - 200; r = rnd.uniform(160, 320)
        glow(c, x, y + rnd.uniform(-120, 120), r, col, a)

def speedlines(c, t, cx=960, cy=540, n=70, a=0.35, seed=4):
    rnd = random.Random(seed + int(t * 24))
    c.set_line_width(2)
    for i in range(n):
        an = rnd.uniform(0, 6.283); r0 = rnd.uniform(380, 700); r1 = r0 + rnd.uniform(200, 600)
        c.set_source_rgba(1, 0.95, 0.85, a * rnd.uniform(0.3, 1))
        c.move_to(cx + math.cos(an) * r0, cy + math.sin(an) * r0); c.line_to(cx + math.cos(an) * r1, cy + math.sin(an) * r1); c.stroke()

def flag(c, x, y, ch, col, t, h=300, s=1, a=1):
    banner(c, x, y, ch, col, t, h=h, a=a, s=s)

def wall_city(c, y, x0, x1, h=200, col=INK, gate=True):
    c.set_source_rgb(*col); c.rectangle(x0, y - h, x1 - x0, h + 400); c.fill()
    for xx in range(int(x0), int(x1), 50): c.rectangle(xx, y - h - 26, 30, 26); c.fill()
    if gate:
        mx = (x0 + x1) / 2; roofhall(c, mx, y - h, 360, 180, col)

def map_bg(c, t):
    sky(c, (0.10, 0.08, 0.06), (0.03, 0.03, 0.03))
    c.set_source_rgba(0.85, 0.65, 0.35, 0.08); c.set_line_width(1)
    for i in range(0, W, 80): c.move_to(i, 0); c.line_to(i, H)
    for j in range(0, H, 80): c.move_to(0, j); c.line_to(W, j)
    c.stroke()

# ---------------- 镜头 ----------------
def S_hook(c, lt, d, p):
    sky(c, (0.03, 0.03, 0.04), (0.14, 0.07, 0.04))
    glow(c, 960, 900, 900, (1, 0.45, 0.15), 0.25)
    mountains(c, lt, cols=[(0.12, 0.06, 0.04), (0.07, 0.04, 0.03), (0.03, 0.02, 0.02)])
    # 身后无数倒下的旗
    rnd = random.Random(3)
    for i in range(14):
        x = 120 + i * 130 + rnd.uniform(-30, 30)
        c.save(); c.translate(x, 960); c.rotate(rnd.uniform(-0.9, 0.9))
        c.set_source_rgb(*INK); c.rectangle(-3, -260, 6, 260); c.fill()
        poly(c, [(3, -250), (80, -240), (78, -170), (3, -180)], (0.20, 0.10, 0.07)); c.restore()
    ground(c, 950)
    baiqi(c, 960, 960, 1.5, 'sword', 1, lt, p=1, sword_lit=0.9)
    embers(c, lt, 50)

def S_hook2(c, lt, d, p):
    sky(c, (0.02, 0.02, 0.03), (0.06, 0.05, 0.06))
    glow(c, 960, 420, 700, (0.6, 0.65, 0.8), 0.14)
    ground(c, 900)
    # 一把剑从上方缓缓落入画面，被一只手托着
    k = eout(p * 1.3)
    y = lerp(-200, 520, k)
    glow(c, 960, y, 300, (0.75, 0.85, 1.0), 0.5)
    c.set_source_rgba(*STEEL, 1); c.set_line_width(12); c.move_to(960, y - 260); c.line_to(960, y + 120); c.stroke()
    c.set_source_rgb(*INK); c.rectangle(900, y + 120, 120, 16); c.fill(); c.rectangle(950, y + 136, 20, 90); c.fill()
    baiqi(c, 1300, 900, 1.25, 'kneel', -1, lt, cape=True)
    sil(c, 620, 900, 1.25, hat='guan', pose='offer', face=1, p=ease(p * 2))

def S_title(c, lt, d, p):
    sky(c, (0.01, 0.01, 0.01), (0.10, 0.02, 0.02))
    glow(c, 960, 640, 900, (0.9, 0.15, 0.08), 0.35)
    smoke(c, lt, 760, (0.25, 0.05, 0.03), 0.35)
    ground(c, 1000)
    baiqi(c, 960, 1010, 1.9, 'sword', 1, lt, p=1, sword_lit=1.0)
    speedlines(c, lt, 960, 520, 90, 0.25 * (1 - ease(lt / 1.5)) + 0.08)
    k = eout(lt / 0.35); sc = lerp(1.8, 1.0, k)
    c.save(); c.translate(960, 340); c.scale(sc, sc)
    text(c, "白  起", 0, 0, 210, (1, 0.96, 0.9), k, 'c')
    c.restore()
    a2 = ease((lt - 0.9) / 0.4)
    text(c, "战神 · 杀神 · 一生攻城七十余座", 960, 120, 46, GOLD, a2, 'c')
    embers(c, lt, 80, a=0.9)

def S_first(c, lt, d, p):
    sky(c, (0.18, 0.12, 0.08), (0.45, 0.28, 0.14))
    glow(c, 1500, 640, 500, (1, 0.7, 0.3), 0.45)
    mountains(c, lt, cols=[(0.30, 0.18, 0.10), (0.18, 0.11, 0.07), (0.08, 0.05, 0.04)])
    wall_city(c, 820, 1250, 1920, 170, (0.05, 0.04, 0.035))
    flag(c, 1500, 610, "韩", (0.25, 0.30, 0.20), lt, 220)
    ground(c, 880)
    army(c, 900, 2, 7, 0.55, 60, 800, 1, 'helm', lt, march=lt * 60)
    baiqi(c, 880 + lt * 50, 900, 1.05, 'point', 1, lt)
    flag(c, 300 + lt * 60, 880, "秦", (0.12, 0.10, 0.10), lt, 360)

def S_yique(c, lt, d, p):
    sky(c, (0.08, 0.07, 0.10), (0.30, 0.20, 0.16))
    # 伊阙：两山对峙如门阙
    poly(c, [(0, 900), (0, 250), (260, 300), (520, 520), (640, 900)], (0.07, 0.06, 0.06))
    poly(c, [(W, 900), (W, 220), (1660, 300), (1400, 520), (1280, 900)], (0.07, 0.06, 0.06))
    water(c, lt, 860)
    ground(c, 920)
    # 远处联军：密密麻麻，旗帜林立
    k = ease(p * 1.5)
    army(c, 820, 3, 14, 0.30, 700, 1250, -1, 'guan', lt, 0, a=0.9, col=(0.10, 0.10, 0.12))
    flag(c, 820, 780, "韩", (0.25, 0.30, 0.20), lt, 200, 0.8); flag(c, 1150, 780, "魏", (0.35, 0.25, 0.10), lt, 200, 0.8)
    # 近景：秦军人少
    spear_row(c, 1060, 4, 0.9, 120, 520, 1, 'helm', lt)
    baiqi(c, 680, 1060, 1.1, 'stand', 1, lt)

def S_yique2(c, lt, d, p):
    map_bg(c, lt)
    # 俯视战场：韩、魏两块，箭头
    c.set_source_rgba(0.25, 0.30, 0.20, 0.85); rr(c, 1080, 330, 360, 200, 20); c.fill()
    c.set_source_rgba(0.40, 0.28, 0.12, 0.85); rr(c, 1080, 700, 360, 200, 20); c.fill()
    text(c, "韩", 1260, 462, 90, (1, 0.95, 0.85), 1, 'c'); text(c, "魏", 1260, 832, 90, (1, 0.95, 0.85), 1, 'c')
    # 两军之间的空隙 / 互相推诿的虚线
    c.set_source_rgba(1, 1, 1, 0.5); c.set_dash([14, 12]); c.set_line_width(3); c.move_to(1260, 540); c.line_to(1260, 690); c.stroke(); c.set_dash([])
    k1 = ease(p * 2.2); k2 = ease((p - 0.35) * 2.2)
    def arrow(x0, y0, x1, y1, k, col, w):
        if k <= 0: return
        x = lerp(x0, x1, k); y = lerp(y0, y1, k); an = math.atan2(y1 - y0, x1 - x0)
        c.set_source_rgba(*col, 1); c.set_line_width(w); c.set_line_cap(1); c.move_to(x0, y0); c.line_to(x, y); c.stroke()
        poly(c, [(x + math.cos(an) * w * 1.6, y + math.sin(an) * w * 1.6), (x + math.cos(an + 2.4) * w * 1.6, y + math.sin(an + 2.4) * w * 1.6), (x + math.cos(an - 2.4) * w * 1.6, y + math.sin(an - 2.4) * w * 1.6)], col)
    arrow(420, 560, 1040, 430, k1, (0.7, 0.7, 0.72), 14)     # 佯攻韩
    arrow(420, 600, 1060, 800, k2, CAPE, 40)                 # 主力击魏
    text(c, "佯攻", 700, 450, 44, (0.85, 0.85, 0.85), k1, 'c')
    text(c, "主力", 720, 780, 56, (1, 0.5, 0.4), k2, 'c')
    c.set_source_rgba(*CAPE, 1); c.arc(400, 580, 28, 0, 6.28); c.fill()
    text(c, "秦", 400, 680, 50, (1, 0.9, 0.85), 1, 'c')
    if k2 > 0.9:
        glow(c, 1080, 800, 300, (1, 0.4, 0.2), 0.5 * (math.sin(lt * 20) * 0.3 + 0.7))

def S_yique3(c, lt, d, p):
    sky(c, (0.20, 0.05, 0.03), (0.50, 0.12, 0.05))
    glow(c, 960, 800, 900, (1, 0.35, 0.1), 0.35)
    smoke(c, lt, 650, (0.15, 0.04, 0.03), 0.5)
    ground(c, 930)
    rnd = random.Random(7)
    for i in range(30):
        x = 40 + i * 64 + rnd.uniform(-20, 20)
        k = ease((lt - 0.2 - i * 0.03) / 0.4)
        sil(c, x, 960, 0.5, hat='guan', pose='lie', p=k, face=1 if i % 2 else -1)
    flag(c, 1500, 940, "魏", (0.35, 0.25, 0.10), lt, 300)
    c.save(); c.translate(1500, 940); c.rotate(-1.2 * ease(lt / 1.2)); c.restore()
    baiqi(c, 700, 940, 1.35, 'sword', 1, lt, p=ease(lt / 0.4), sword_lit=0.9)
    embers(c, lt, 60)

def S_march(c, lt, d, p):
    sky(c, (0.12, 0.10, 0.12), (0.40, 0.25, 0.15))
    # 一座座城头换旗：三座城，依次插上秦旗
    for i, (x, ch, col) in enumerate(((380, "魏", (0.35, 0.25, 0.10)), (960, "韩", (0.25, 0.30, 0.20)), (1540, "赵", ZHAO))):
        wall_city(c, 760, x - 240, x + 240, 160, (0.05, 0.04, 0.04), gate=False)
        roofhall(c, x, 600, 260, 140, (0.05, 0.04, 0.04))
        k = ease((p - 0.15 - i * 0.22) / 0.12)
        flag(c, x - 60, 460, ch, col, lt, 200, a=1 - k)
        if k > 0:
            flag(c, x + 40, 460, "秦", (0.55, 0.08, 0.06), lt, int(lerp(0, 260, eout(k))) + 1)
            glow(c, x + 80, 300, 180, (1, 0.4, 0.2), 0.3 * k)
    ground(c, 900)
    army(c, 1000, 2, 18, 0.45, -100 + lt * 120, 1500 + lt * 120, 1, 'helm', lt, 0)

def S_zhao280(c, lt, d, p):
    sky(c, (0.10, 0.12, 0.16), (0.30, 0.30, 0.32))
    mountains(c, lt, cols=[(0.22, 0.24, 0.28), (0.13, 0.14, 0.17), (0.06, 0.06, 0.08)])
    wall_city(c, 820, 1100, 1920, 220, (0.04, 0.04, 0.05))
    text(c, "光狼城", 1500, 470, 48, (0.85, 0.85, 0.9), 0.8, 'c')
    fires(c, lt, (1250, 1450, 1700), 600, 90)
    ground(c, 900)
    horse(c, 300 + lt * 260, 960, 0.9, lt, rider='helm')
    horse(c, 600 + lt * 280, 980, 1.0, lt + 0.3, rider='helm')
    arrows(c, lt, 40, 2, 0.2)
    embers(c, lt, 40)

def S_yan(c, lt, d, p):
    sky(c, (0.06, 0.10, 0.10), (0.20, 0.28, 0.25))
    wall_city(c, 820, 700, 1920, 360, (0.04, 0.05, 0.05))
    text(c, "鄢", 1310, 650, 140, (0.85, 0.9, 0.85), 0.3, 'c')
    flag(c, 900, 460, "楚", (0.50, 0.20, 0.30), lt, 240)
    flag(c, 1700, 460, "楚", (0.50, 0.20, 0.30), lt, 240)
    # 城头密集守军
    spear_row(c, 465, 14, 0.35, 760, 1880, -1, 'bun', lt, 0, a=1, col=(0.08, 0.08, 0.08))
    ground(c, 940)
    arrows(c, lt, 50, 3, 3.1416 - 0.5)
    baiqi(c, 400, 990, 1.3, 'stand', 1, lt)

def S_canal(c, lt, d, p):
    sky(c, (0.03, 0.05, 0.08), (0.10, 0.16, 0.20))
    stars(c, lt, 80, a=0.6); moon(c, 1500, 400, 50, 0.8)
    mountains(c, lt, cols=[(0.08, 0.12, 0.14), (0.05, 0.08, 0.09), (0.02, 0.03, 0.04)])
    ground(c, 760)
    # 渠：从左上蜿蜒向右下，水逐渐流进来
    k = ease(p)
    pts = [(0, 560), (300, 640), (700, 700), (1100, 760), (1500, 840), (1920, 900)]
    c.set_line_cap(1)
    c.set_source_rgb(0.02, 0.02, 0.02); c.set_line_width(70)
    c.move_to(*pts[0]); [c.line_to(*q) for q in pts[1:]]; c.stroke()
    n = k * (len(pts) - 1); c.set_source_rgba(0.35, 0.55, 0.65, 0.9); c.set_line_width(46)
    c.move_to(*pts[0])
    for i in range(1, len(pts)):
        if i <= n: c.line_to(*pts[i])
        else:
            f = n - (i - 1)
            if f > 0: c.line_to(lerp(pts[i - 1][0], pts[i][0], f), lerp(pts[i - 1][1], pts[i][1], f))
            break
    c.stroke()
    # 筑坝的人
    rnd = random.Random(2)
    for i in range(10):
        x = 200 + i * 150; y = 760 + rnd.uniform(0, 40)
        sil(c, x, y + 120, 0.5, hat='helm', pose='bow' if (i + int(lt * 3)) % 2 else 'stand', p=1, face=1)
    baiqi(c, 1600, 1060, 1.2, 'point', -1, lt)

def S_flood(c, lt, d, p):
    sky(c, (0.02, 0.04, 0.06), (0.08, 0.12, 0.14))
    k = ease(p * 1.1)
    # 城墙下沉、坍塌
    off = k * 200
    c.save(); c.translate(0, off); c.rotate(0.03 * k)
    wall_city(c, 760, 300, 1700, 300, (0.05, 0.06, 0.07))
    c.restore()
    # 洪水
    lvl = lerp(980, 640, k)
    for j in range(5):
        c.set_source_rgba(0.20 + j * 0.03, 0.35 + j * 0.03, 0.42 + j * 0.03, 0.75)
        c.move_to(0, lvl + j * 50)
        for x in range(0, W + 40, 40): c.line_to(x, lvl + j * 50 + math.sin(x * 0.012 + lt * 4 + j) * 14)
        c.line_to(W, H); c.line_to(0, H); c.close_path(); c.fill()
    rnd = random.Random(5)
    for i in range(16):
        x = rnd.uniform(100, 1800); y = lvl + rnd.uniform(-20, 120)
        sil(c, x, y + 40, 0.35, hat='bun', pose='raise', face=1 if i % 2 else -1, p=1, a=0.9)

def S_ying(c, lt, d, p):
    sky(c, (0.15, 0.03, 0.02), (0.55, 0.15, 0.05))
    glow(c, 960, 700, 1000, (1, 0.4, 0.1), 0.45)
    roofhall(c, 960, 820, 900, 420, (0.05, 0.03, 0.03))
    roofhall(c, 400, 860, 500, 240, (0.05, 0.03, 0.03)); roofhall(c, 1520, 860, 500, 240, (0.05, 0.03, 0.03))
    fires(c, lt, (250, 500, 760, 960, 1160, 1420, 1680), 820, 220)
    smoke(c, lt, 400, (0.1, 0.03, 0.02), 0.5)
    ground(c, 880)
    text(c, "夷 陵", 960, 300, 64, GOLD, 0.7 * ease(p * 3), 'c')
    baiqi(c, 960, 1060, 1.4, 'stand', -1, lt)
    embers(c, lt, 120, a=1)

def S_wuan(c, lt, d, p):
    palace(c, lt, tone=(0.22, 0.05, 0.03), candles=((420, 760), (1500, 760)))
    sil(c, 960, 760, 0.8, hat='mian', pose='sit', face=1)
    poly(c, [(800, 770), (1120, 770), (1090, 800), (830, 800)], INK)
    baiqi(c, 1400, 900, 1.2, 'kneel', -1, lt)
    k = eout((lt - 0.6) / 0.5)
    glow(c, 960, 440, 420, GOLD, 0.25 * k)
    c.save(); c.translate(960, 480); c.scale(lerp(2.2, 1, k), lerp(2.2, 1, k))
    text(c, "武 安 君", 0, 0, 120, GOLD, k, 'c')
    c.restore()

def S_huayang(c, lt, d, p):
    sky(c, (0.03, 0.03, 0.06), (0.12, 0.10, 0.16))
    stars(c, lt, 100)
    mountains(c, lt, cols=[(0.08, 0.08, 0.12), (0.05, 0.05, 0.08), (0.02, 0.02, 0.03)])
    ground(c, 860)
    # 骑兵狂奔 + 计日
    for i in range(6):
        horse(c, ((lt * 700 + i * 340) % 2400) - 300, 960 + (i % 2) * 40, 0.8 + 0.1 * (i % 3), lt + i * 0.2, rider='helm')
    day = min(8, 1 + int(p * 9))
    text(c, f"第 {day} 天", 1600, 720, 84, (1, 0.95, 0.88), 1, 'c')
    speedlines(c, lt, 1700, 900, 40, 0.25)

def S_huayang2(c, lt, d, p):
    sky(c, (0.18, 0.05, 0.04), (0.35, 0.18, 0.10))
    ground(c, 760, (0.06, 0.04, 0.03))
    # 黄河：右下大面积浊水，赵军被逼入
    for j in range(5):
        c.set_source_rgba(0.40 + j * 0.03, 0.30 + j * 0.02, 0.16, 0.9)
        c.move_to(900, 820 + j * 50)
        for x in range(900, W + 40, 40): c.line_to(x, 820 + j * 50 + math.sin(x * 0.01 + lt * 3 + j) * 12)
        c.line_to(W, H); c.line_to(900, H); c.close_path(); c.fill()
    text(c, "黄 河", 1500, 1000, 52, (0.95, 0.85, 0.6), 0.6, 'c')
    rnd = random.Random(11)
    for i in range(14):
        x = 1000 + i * 65; k = ease((lt - i * 0.06) / 0.6)
        sil(c, x, lerp(800, 900, k), 0.45, hat='guan', pose='raise', p=1, face=1, a=1 - 0.5 * k, col=(0.05, 0.06, 0.08))
    army(c, 820, 2, 8, 0.6, 80, 760, 1, 'helm', lt, march=lt * 80)
    baiqi(c, 600, 900, 1.2, 'sword', 1, lt, p=1, sword_lit=0.8)

def S_xing(c, lt, d, p):
    sky(c, (0.10, 0.08, 0.06), (0.28, 0.18, 0.10))
    for i in range(5):
        x = 200 + i * 380; k = ease((p - i * 0.12) / 0.15)
        wall_city(c, 760, x - 150, x + 150, 140, (0.05, 0.04, 0.04), gate=False)
        if k > 0: fires(c, lt, (x - 60, x + 50), 620, 70 * k)
        text(c, str(i + 1), x, 560, 60, (1, 0.5, 0.35) if k > 0 else (0.5, 0.45, 0.4), 1, 'c')
    ground(c, 880)
    army(c, 980, 2, 20, 0.45, -50, 1900, 1, 'helm', lt, march=lt * 40)

def S_fear(c, lt, d, p):
    sky(c, (0.02, 0.02, 0.02), (0.07, 0.05, 0.05))
    # 六国君主，烛火摇晃，都在发抖
    names = ["韩", "赵", "魏", "楚", "燕", "齐"]
    for i, n in enumerate(names):
        x = 200 + i * 304
        sh = math.sin(lt * 40 + i) * 4
        glow(c, x, 640, 200, (1, 0.6, 0.3), 0.18)
        candle(c, x + 90, 900, lt)
        sil(c, x + sh, 900, 0.9, hat='mian', pose='sit', face=1)
        text(c, n, x, 1000, 44, (0.85, 0.8, 0.7), 0.9, 'c')
    # 白起巨大投影压在墙上
    k = ease(p * 1.5)
    c.save(); c.translate(960, 760); c.scale(4.2, 4.2)
    sil(c, 0, 0, 1, hat='helm', pose='stand', face=1, a=0.55 * k, col=(0, 0, 0)); c.restore()

def S_changping(c, lt, d, p):
    sky(c, (0.10, 0.10, 0.12), (0.30, 0.25, 0.22))
    mountains(c, lt, cols=[(0.22, 0.20, 0.20), (0.13, 0.12, 0.12), (0.06, 0.06, 0.06)], base=760)
    ground(c, 800)
    # 左秦右赵，千军对峙
    army(c, 860, 3, 12, 0.45, 40, 820, 1, 'helm', lt)
    army(c, 860, 3, 12, 0.45, 1100, 1880, -1, 'guan', lt, col=(0.04, 0.05, 0.07))
    flag(c, 420, 760, "秦", (0.55, 0.08, 0.06), lt, 320); flag(c, 1500, 760, "赵", ZHAO, lt, 320)
    k = ease(p * 2)
    c.set_source_rgba(1, 0.9, 0.7, 0.6 * k); c.rectangle(958, 520, 4, 380); c.fill()
    text(c, "长 平", 960, 480, 96, (1, 0.95, 0.88), k, 'c')

def S_lianpo(c, lt, d, p):
    sky(c, (0.08, 0.10, 0.13), (0.22, 0.24, 0.26))
    mountains(c, lt, cols=[(0.18, 0.20, 0.22), (0.10, 0.11, 0.13), (0.05, 0.05, 0.06)])
    # 赵军壁垒：长长的土墙
    c.set_source_rgb(0.05, 0.06, 0.08); c.rectangle(1000, 640, 920, 500); c.fill()
    for xx in range(1000, 1920, 50): c.rectangle(xx, 610, 30, 30); c.fill()
    flag(c, 1500, 600, "赵", ZHAO, lt, 260)
    sil(c, 1300, 640, 0.9, hat='guan', pose='stand', face=-1, col=(0.05, 0.06, 0.08))
    text(c, "廉颇", 1300, 380, 44, (0.85, 0.88, 0.95), 1, 'c')
    ground(c, 900)
    # 秦军冲上去又被挡回
    ph = (lt * 1.4) % 1
    xoff = math.sin(ph * 3.1416) * 260
    spear_row(c, 980, 8, 0.6, 100 + xoff, 800 + xoff, 1, 'helm', lt)
    arrows(c, lt, 40, 8, 3.1416 - 0.25)

def S_spy(c, lt, d, p):
    palace(c, lt, tone=(0.06, 0.08, 0.14), candles=((380, 760), (1540, 760)))
    sil(c, 640, 860, 1.0, hat='mian', pose='sit', face=1)
    text(c, "赵王", 640, 520, 40, (0.8, 0.85, 0.95), 1, 'c')
    # 两个窃窃私语的人 → 谣言字条飞散
    sil(c, 260, 860, 0.8, hat='guan', pose='bow', face=1, p=0.6, a=0.9)
    rnd = random.Random(1)
    for i in range(10):
        k = ((lt * 0.7 + i * 0.1) % 1)
        x = lerp(320, 1700, k) + rnd.uniform(-60, 60); y = 600 - math.sin(k * 3.14) * 260 + rnd.uniform(-80, 80)
        c.save(); c.translate(x, y); c.rotate(rnd.uniform(-0.6, 0.6))
        c.set_source_rgba(0.9, 0.85, 0.72, 0.85); c.rectangle(-28, -40, 56, 80); c.fill()
        c.restore()
    k = ease((p - 0.45) / 0.2)
    sil(c, 1360, 860, 1.05, hat='helm', pose='raise', face=-1, p=k, col=(0.05, 0.06, 0.09))
    text(c, "赵括", 1360, 520, 48, GOLD, k, 'c')

def S_secret(c, lt, d, p):
    sky(c, (0.01, 0.01, 0.02), (0.05, 0.04, 0.05))
    # 夜，军帐，帐内一点烛光，白起入帐
    poly(c, [(560, 900), (960, 360), (1360, 900)], (0.10, 0.07, 0.05))
    glow(c, 960, 760, 380, (1, 0.6, 0.3), 0.45)
    candle(c, 1100, 880, lt, 90)
    baiqi(c, lerp(560, 900, ease(p * 1.5)), 900, 1.1, 'stand', 1, lt)
    ground(c, 900)
    # 两名哨兵捂嘴
    sil(c, 360, 900, 1.0, hat='helm', pose='stand', face=1); sil(c, 1560, 900, 1.0, hat='helm', pose='stand', face=-1)
    c.set_source_rgba(1, 0.92, 0.85, 0.85)
    k = ease((p - 0.5) / 0.15)
    glow(c, 960, 560, 300, (1, 0.2, 0.1), 0.4 * k)
    text(c, "斩", 960, 620, 200, (0.95, 0.25, 0.2), k, 'c')

def S_trap(c, lt, d, p):
    map_bg(c, lt)
    # 俯视：赵军向左追击 → 两路奇兵切断
    k = ease(p * 1.6)
    zx = lerp(1500, 900, k)
    c.set_source_rgba(*ZHAO, 0.9); rr(c, zx - 200, 420, 400, 240, 30); c.fill()
    text(c, "赵军", zx, 570, 64, (1, 1, 1), 1, 'c')
    c.set_source_rgba(0.3, 0.3, 0.3, 1); rr(c, 300, 380, 240, 320, 20); c.fill()
    text(c, "秦壁", 420, 560, 52, (1, 0.9, 0.85), 1, 'c')
    k2 = ease((p - 0.4) / 0.3)
    if k2 > 0:
        c.set_source_rgba(*CAPE, 1); c.set_line_width(26); c.set_line_cap(1)
        c.move_to(1250, 300); c.line_to(1250, lerp(300, 1000, k2)); c.stroke()     # 二万五千断后
        c.move_to(700, 1000); c.line_to(700, lerp(1000, 300, k2)); c.stroke()      # 五千骑断壁间
        text(c, "奇兵 2.5万", 1420, 860, 44, (1, 0.6, 0.5), k2, 'c')
        text(c, "骑兵 5千", 850, 860, 44, (1, 0.6, 0.5), k2, 'c')

def S_siege(c, lt, d, p):
    sky(c, (0.08, 0.06, 0.05), (0.22, 0.15, 0.10))
    # 山谷：两侧高山，中间被围的赵军，火把一圈
    poly(c, [(0, 1080), (0, 200), (500, 420), (760, 1080)], (0.05, 0.04, 0.04))
    poly(c, [(W, 1080), (W, 180), (1420, 420), (1160, 1080)], (0.05, 0.04, 0.04))
    for i in range(18):
        an = i / 18 * 6.283
        x = 960 + math.cos(an) * 620; y = 760 + math.sin(an) * 170
        flame(c, x, y, 40, lt, i)
    for i in range(20):
        x = 700 + (i % 10) * 55; y = 790 + (i // 10) * 50
        sil(c, x, y, 0.32, hat='guan', pose='cry' if i % 3 == 0 else 'kneel', p=1, face=1 if i % 2 else -1, col=(0.04, 0.05, 0.07))
    dd = 1 + int(ease(p) * 45)
    text(c, f"断粮 第 {dd} 天", 960, 420, 72, (0.95, 0.30, 0.24), 1, 'c')

def S_zhaokuo(c, lt, d, p):
    sky(c, (0.15, 0.04, 0.03), (0.40, 0.10, 0.05))
    ground(c, 900)
    k = ease(p * 1.4)
    horse(c, lerp(300, 900, k), 960, 1.1, lt, rider=None)
    sil(c, lerp(295, 895, k), 960 - 175 * 1.1, 0.82, hat='helm', pose='sword' if k < 0.7 else 'stand', p=1, col=(0.05, 0.06, 0.09))
    arrows(c, lt, 90, 12, 3.1416 - 0.15, a=1, speed=2600)
    if k > 0.7: glow(c, 900, 700, 300, (1, 0.2, 0.1), 0.5)
    text(c, "赵括", lerp(300, 900, k), 560, 48, (0.85, 0.88, 0.95), 1, 'c')

def S_surrender(c, lt, d, p):
    sky(c, (0.10, 0.09, 0.10), (0.25, 0.22, 0.22))
    ground(c, 760, (0.06, 0.06, 0.07))
    # 一眼望不到头的降卒跪地，兵器堆成山
    for r in range(5):
        crowd(c, 790 + r * 60, 18 + r * 2, 0.32 + r * 0.06, 0 - r * 30, 1920 + r * 30, 'kneel', 'guan', a=1)
    rnd = random.Random(3)
    c.set_line_width(4)
    for i in range(60):
        x = 1500 + rnd.uniform(-180, 180); y = 760 + rnd.uniform(-20, 20); an = rnd.uniform(-1, 1)
        c.set_source_rgba(0.6, 0.6, 0.62, 0.6); c.move_to(x, y); c.line_to(x + math.sin(an) * 200, y - math.cos(an) * 160); c.stroke()
    baiqi(c, 300, 760, 1.0, 'stand', 1, lt)
    text(c, "400,000", 960, 380, 120, (0.95, 0.92, 0.85), ease(p * 2), 'c')

def S_bury(c, lt, d, p):
    beat = 0.4285587
    if lt < beat * 3:     # 静默三拍：黑场，只有月亮
        sky(c, (0.0, 0.0, 0.0), (0.02, 0.02, 0.03))
        moon(c, 960, 380, 70, 0.8)
        text(c, "那一夜", 960, 760, 64, (0.75, 0.72, 0.7), ease(lt / 0.4), 'c')
        return
    l2 = lt - beat * 3
    sky(c, (0.12, 0.01, 0.01), (0.40, 0.04, 0.02))
    moon(c, 960, 470, 45, 0.6)
    ground(c, 760, (0.04, 0.02, 0.02))
    # 巨坑
    c.set_source_rgb(0, 0, 0); c.save(); c.translate(960, 900); c.scale(1, 0.25); c.arc(0, 0, 820, 0, 6.28); c.restore(); c.fill()
    rnd = random.Random(8)
    for i in range(40):
        x = 960 + rnd.uniform(-700, 700); y = 900 + rnd.uniform(-120, 120)
        sil(c, x, y, 0.28, hat='guan', pose='lie', p=1, face=1 if i % 2 else -1, col=(0.12, 0.03, 0.03), a=0.9)
    # 两侧持戈秦兵剪影
    spear_row(c, 780, 12, 0.5, 40, 640, 1, 'helm', l2)
    spear_row(c, 780, 12, 0.5, 1280, 1880, -1, 'helm', l2)
    text(c, "240", 960, 400, 90, (0.95, 0.92, 0.85), ease(l2 / 0.3) * (1 - ease((l2 - 1.2) / 0.4)), 'c')
    embers(c, l2, 50, a=0.6)

def S_fanju(c, lt, d, p):
    palace(c, lt, tone=(0.20, 0.06, 0.04), candles=((420, 760), (1500, 760)))
    sil(c, 960, 640, 1.0, hat='mian', pose='sit', face=1)
    poly(c, [(760, 650), (1160, 650), (1120, 690), (800, 690)], INK)
    sil(c, 700, 900, 1.1, hat='guan', pose='bow', face=1, p=0.5)
    text(c, "范雎", 700, 560, 44, (0.9, 0.85, 0.75), 1, 'c')
    # 远处地图上，指向邯郸的箭头被擦掉
    k = ease(p * 1.5)
    c.set_source_rgba(*CAPE, 1 - k); c.set_line_width(22); c.set_line_cap(1); c.move_to(1250, 470); c.line_to(1700, 360); c.stroke()
    text(c, "邯郸", 1720, 330, 44, (0.9, 0.9, 0.95), 1, 'c')
    baiqi(c, 1500, 900, 1.1, 'stand', -1, lt)

def S_handan(c, lt, d, p):
    sky(c, (0.05, 0.06, 0.08), (0.15, 0.15, 0.17))
    wall_city(c, 800, 600, 1920, 330, (0.04, 0.05, 0.07))
    text(c, "邯郸", 1260, 600, 80, (0.85, 0.88, 0.95), 0.5, 'c')
    flag(c, 900, 470, "赵", ZHAO, lt, 260); flag(c, 1600, 470, "赵", ZHAO, lt, 260)
    ground(c, 900)
    # 秦军攻城倒下
    rnd = random.Random(4)
    for i in range(14):
        x = 600 + i * 90 + rnd.uniform(-20, 20); k = ease((lt - i * 0.12) / 0.4)
        sil(c, x, 980, 0.55, hat='helm', pose='lie', p=k, face=1)
    arrows(c, lt, 50, 6, 3.1416 - 0.45)
    # 白起在左侧病榻，背过身
    poly(c, [(40, 1000), (460, 1000), (460, 960), (40, 960)], INK)
    baiqi(c, 250, 960, 0.9, 'sit', -1, lt, cape=False)

def S_exile(c, lt, d, p):
    sky(c, (0.12, 0.10, 0.10), (0.40, 0.30, 0.22))
    wall_city(c, 820, 0, 900, 280, (0.05, 0.04, 0.04))
    text(c, "咸阳", 450, 420, 64, (0.9, 0.85, 0.75), 0.6, 'c')
    ground(c, 880)
    # 盔甲和红披风丢在地上，他换成布衣独行
    poly(c, [(820, 880), (980, 880), (960, 860), (840, 860)], CAPE)
    c.set_source_rgb(*INK); c.arc(900, 850, 26, 3.14, 6.28); c.fill()
    x = lerp(1050, 1500, ease(p))
    sil(c, x, 880, 1.15, hat='bun', pose='stand', face=1, t=lt)

def S_duyou(c, lt, d, p):
    sky(c, (0.08, 0.06, 0.06), (0.30, 0.18, 0.12))
    glow(c, 1500, 700, 500, (1, 0.6, 0.3), 0.35)
    ground(c, 880)
    # 驿亭
    roofhall(c, 1500, 880, 360, 300, INK)
    text(c, "杜邮", 1500, 520, 52, (0.9, 0.85, 0.75), 0.7, 'c')
    sil(c, 600, 880, 1.15, hat='bun', pose='stand', face=1)
    sil(c, 1100, 880, 1.15, hat='guan', pose='offer', face=-1, p=ease(p * 2))
    k = ease(p * 2)
    glow(c, 960, 640, 260, (0.75, 0.85, 1.0), 0.5 * k)
    c.set_source_rgba(*STEEL, k); c.set_line_width(9); c.move_to(840, 650); c.line_to(1060, 630); c.stroke()

def S_last(c, lt, d, p):
    sky(c, (0.03, 0.03, 0.04), (0.18, 0.06, 0.04))
    glow(c, 960, 820, 800, (0.9, 0.25, 0.1), 0.25)
    ground(c, 900)
    # 他跪在地上，剑在手，身后浮现无数降卒的影子
    rnd = random.Random(6)
    for i in range(40):
        x = rnd.uniform(0, W); y = rnd.uniform(500, 900); s = rnd.uniform(0.3, 0.6)
        sil(c, x, y, s, hat='guan', pose='stand', face=-1 if x > 960 else 1, a=0.12 + 0.12 * ease(p), col=(0.4, 0.4, 0.45))
    sil(c, 960, 900, 1.4, hat='bun', pose='kneel', face=1)
    glow(c, 1080, 700, 240, (0.75, 0.85, 1.0), 0.45)
    c.set_source_rgba(*STEEL, 1); c.set_line_width(10); c.set_line_cap(1); c.move_to(1050, 760); c.line_to(1180, 520); c.stroke()

def S_end(c, lt, d, p):
    sky(c, (0.0, 0.0, 0.0), (0.06, 0.02, 0.02))
    # 一半金一半红：战神 / 杀神
    glow(c, 620, 560, 520, GOLD, 0.25); glow(c, 1300, 560, 520, RED, 0.25)
    baiqi(c, 960, 960, 1.6, 'sword', 1, lt, p=1, sword_lit=0.6)
    ground(c, 960)
    text(c, "评论区告诉我你的答案", 960, 1040, 36, (0.75, 0.72, 0.7), ease((lt - 0.8) / 0.5), 'c', shadow=False)

CAM = {
    'hook': (1.0, 1.10, 960, 700), 'hook2': (1.05, 1.0, 960, 500), 'title': (1.15, 1.0, 960, 540),
    'yique3': (1.0, 1.12, 700, 800), 'ying': (1.0, 1.1, 960, 700), 'fear': (1.0, 1.06, 960, 600),
    'bury': (1.0, 1.08, 960, 700), 'last': (1.0, 1.15, 960, 750), 'end': (1.0, 1.06, 960, 700),
}
