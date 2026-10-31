# 白起的一生 · 战争风：暗金地图 + 线描侧面/背影英雄 + 红印章
import math, random
from kit import W, H, FONT, text, glow, GOLD, RED, ease, eout, cl, lerp, mix, vgrad, poly, rr, moon, flame
from fig import shape, line, tube, hatch, sword, soldier, LINE, INKF, ROBE, CAPE, CAPE_D, ZHAO_C, ZHAO_D, SKIN, STEEL
from side import side, back, head_side
import mapw as M

BP = 0.4285587
QIN = (0.75, 0.10, 0.07)
ZB = (0.20, 0.32, 0.50)
WARM = (1.0, 0.82, 0.45)

# ---------------- 通用场景件 ----------------
def sky(c, top, bot, y1=H):
    vgrad(c, 0, y1, [(0, top), (1, bot)])

def mts(c, base, col, seed=1, hmin=80, hmax=260, step=170, a=1, lit=None):
    """战争风三角群山：两面明暗"""
    r = random.Random(seed); x = -100
    while x < W + 200:
        s = r.uniform(hmin, hmax); w = s * r.uniform(1.0, 1.5)
        c.set_source_rgba(*col, a); c.move_to(x - w, base); c.line_to(x, base - s); c.line_to(x + w, base); c.close_path(); c.fill()
        if lit:
            c.set_source_rgba(*lit, 0.35 * a); c.move_to(x - w, base); c.line_to(x, base - s); c.line_to(x - w * 0.15, base); c.close_path(); c.fill()
        x += step * r.uniform(0.6, 1.3)
    c.set_source_rgba(*col, a); c.rectangle(0, base - 1, W, H - base + 40); c.fill()

def ground(c, y, col=(0.06, 0.045, 0.035)):
    c.set_source_rgb(*col); c.rectangle(0, y, W, H - y + 60); c.fill()
    c.set_source_rgba(0.9, 0.7, 0.4, 0.25); c.set_line_width(2); c.move_to(0, y); c.line_to(W, y); c.stroke()

def embers(c, t, n=60, seed=9, a=0.8, up=True):
    r = random.Random(seed)
    for i in range(n):
        x0 = r.uniform(0, W); sp = r.uniform(60, 200); ph = r.uniform(0, 10)
        y = (r.uniform(0, H) - (t + ph) * sp) % (H + 100) - 50
        x = x0 + math.sin(t * 2 + ph) * 30
        c.set_source_rgba(1, r.uniform(0.4, 0.8), 0.2, a * r.uniform(0.4, 1)); c.arc(x, y, r.uniform(1.5, 4), 0, 6.28); c.fill()

def smoke(c, t, y=700, col=(0.1, 0.08, 0.07), a=0.5, seed=3, n=14):
    r = random.Random(seed)
    for i in range(n):
        x = (r.uniform(-200, W + 200) + t * r.uniform(20, 60)) % (W + 400) - 200
        yy = y + r.uniform(-120, 80) - t * 15; rad = r.uniform(120, 260)
        glow(c, x, yy, rad, col, a)

def arrows(c, t, n=60, seed=5, ang=0.35, a=1, speed=1800, col=(0.95, 0.85, 0.6)):
    r = random.Random(seed)
    for i in range(n):
        ph = r.uniform(0, 1); L = r.uniform(40, 70)
        k = (t * speed / 2400 + ph) % 1
        x = lerp(-200, W + 200, k) if math.cos(ang) > 0 else lerp(W + 200, -200, k)
        y = r.uniform(80, 900) + (k - 0.5) * 600 * math.sin(abs(ang))
        dx, dy = math.cos(ang) * L, math.sin(ang) * L
        c.set_source_rgba(*col, a * 0.85); c.set_line_width(2.5); c.move_to(x, y); c.line_to(x + dx, y + dy); c.stroke()

def speedlines(c, t, cx=960, cy=540, n=70, a=0.35, seed=4):
    r = random.Random(seed + int(t * 12))
    for i in range(n):
        an = r.uniform(0, 6.283); r0 = r.uniform(420, 700); r1 = r0 + r.uniform(200, 600)
        c.set_source_rgba(1, 0.95, 0.85, a * r.uniform(0.3, 1)); c.set_line_width(r.uniform(1.5, 4))
        c.move_to(cx + math.cos(an) * r0, cy + math.sin(an) * r0); c.line_to(cx + math.cos(an) * r1, cy + math.sin(an) * r1); c.stroke()

def stamp(c, s, x, y, size, lt, hit=0.0, rot=-0.08, a=1):
    """红印章大字：落下震一下"""
    k = lt - hit
    if k < 0: return
    sc = lerp(2.4, 1.0, eout(k / 0.16)); al = cl(k / 0.08) * a
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    c.select_font_face(FONT, 0, 1); c.set_font_size(size)
    tw = c.text_extents(s)[4]; pad = size * 0.28
    c.set_source_rgba(0.80, 0.12, 0.08, al); c.set_line_width(size * 0.08)
    c.rectangle(-tw / 2 - pad, -size * 0.75, tw + pad * 2, size * 1.15); c.stroke()
    c.set_line_width(size * 0.025); c.rectangle(-tw / 2 - pad * 0.65, -size * 0.66, tw + pad * 1.3, size * 0.97); c.stroke()
    c.move_to(-tw / 2, size * 0.28); c.show_text(s)
    # 做旧：随机挖掉的斑点
    r = random.Random(len(s))
    for i in range(int(tw / 6)):
        c.set_source_rgba(0.08, 0.05, 0.04, 0.5 * al); c.arc(r.uniform(-tw / 2 - pad, tw / 2 + pad), r.uniform(-size * 0.7, size * 0.38), r.uniform(1, 4), 0, 6.28); c.fill()
    c.restore()
    if k < 0.3: glow(c, x, y, size * 2, (1, 0.2, 0.1), 0.35 * (1 - k / 0.3))

def flag(c, x, y, ch, col, t, h=300, s=1.0, a=1):
    c.set_source_rgba(0.12, 0.09, 0.07, a); c.rectangle(x - 4 * s, y - h, 8 * s, h); c.fill()
    w1 = math.sin(t * 4 + x) * 14 * s
    pts = [(x + 4 * s, y - h), (x + 120 * s + w1, y - h + 10 * s), (x + 116 * s - w1, y - h + 90 * s), (x + 4 * s, y - h + 84 * s)]
    shape(c, pts, col, 2.5 * s, LINE, a)
    text(c, ch, x + 60 * s, y - h + 62 * s, 48 * s, (1, 0.92, 0.75), a, 'c', shadow=False)

def wall(c, x0, x1, top, bot, col=(0.30, 0.28, 0.26), gate=None, gate_name=None, tower=True, a=1):
    """战争风灰砖城墙 + 城楼"""
    shape(c, [(x0, bot), (x0, top), (x1, top), (x1, bot)], col, 3, LINE, a)
    c.set_source_rgba(0, 0, 0, 0.25 * a); c.set_line_width(1.4)
    y = top + 24
    while y < bot:
        c.move_to(x0, y); c.line_to(x1, y)
        y += 24
    c.stroke()
    r = 0
    y = top
    while y < bot:
        off = 30 if r % 2 else 0; xx = x0 + off
        while xx < x1:
            c.move_to(xx, y); c.line_to(xx, y + 24); xx += 60
        y += 24; r += 1
    c.stroke()
    xx = x0
    while xx < x1:
        shape(c, [(xx, top), (xx, top - 26), (xx + 30, top - 26), (xx + 30, top)], col, 2, LINE, a); xx += 56
    if gate:
        gw = 120
        c.set_source_rgba(0.02, 0.015, 0.01, a); c.move_to(gate - gw / 2, bot); c.line_to(gate - gw / 2, bot - 130); c.arc(gate, bot - 130, gw / 2, 3.1416, 0); c.line_to(gate + gw / 2, bot); c.close_path(); c.fill()
        if tower:
            shape(c, [(gate - 170, top - 26), (gate - 150, top - 120), (gate + 150, top - 120), (gate + 170, top - 26)], (0.45, 0.08, 0.06), 2.5, LINE, a)
            shape(c, [(gate - 230, top - 110), (gate, top - 190), (gate + 230, top - 110), (gate + 190, top - 130), (gate, top - 170), (gate - 190, top - 130)], (0.10, 0.08, 0.07), 2.5, LINE, a)
            for k in range(-2, 3): shape(c, [(gate + k * 50 - 14, top - 110), (gate + k * 50 + 14, top - 110), (gate + k * 50 + 14, top - 40), (gate + k * 50 - 14, top - 40)], (0.75, 0.55, 0.25), 1.5, LINE, a)
        if gate_name:
            shape(c, [(gate - 30, top + 10), (gate + 30, top + 10), (gate + 30, top + 70), (gate - 30, top + 70)], (0.10, 0.07, 0.05), 2, GOLD, a)
            text(c, gate_name, gate, top + 52, 26, GOLD, a, 'c', shadow=False)

def palace(c, t, tone=(0.40, 0.07, 0.05), floor=860):
    sky(c, (0.10, 0.03, 0.02), mix(tone, (0, 0, 0), 0.4))
    # 格子窗
    for x in range(120, W, 300):
        shape(c, [(x, 160), (x + 220, 160), (x + 220, 640), (x, 640)], (0.22, 0.10, 0.05), 2.5, GOLD, 0.9)
        c.set_source_rgba(*GOLD, 0.45); c.set_line_width(1.5)
        for k in range(1, 8): c.move_to(x + k * 27.5, 160); c.line_to(x + k * 27.5, 640)
        for k in range(1, 16): c.move_to(x, 160 + k * 30); c.line_to(x + 220, 160 + k * 30)
        c.stroke()
        glow(c, x + 110, 400, 200, (1, 0.6, 0.25), 0.18)
    for x in (60, 400, 1520, 1860):
        shape(c, [(x - 34, floor), (x - 34, 0), (x + 34, 0), (x + 34, floor)], (0.55, 0.08, 0.06), 3, LINE)
        hatch(c, [(x, floor), (x, 0), (x + 34, 0), (x + 34, floor)], 1, alpha=0.3)
    for x in (230, 1690):
        line(c, [(x, 0), (x, 120)], 2, GOLD)
        shape(c, [(x - 40, 120), (x + 40, 120), (x + 50, 200), (x - 50, 200)], (0.75, 0.15, 0.08), 2.5, LINE)
        glow(c, x, 165, 120, (1, 0.6, 0.2), 0.4)
    ground(c, floor, (0.12, 0.05, 0.04))
    shape(c, [(560, floor + 40), (1360, floor + 40), (1460, H + 10), (460, H + 10)], (0.45, 0.06, 0.05), 2, GOLD, 0.8)

def throne(c, x, y, a=1):
    shape(c, [(x - 180, y), (x - 180, y - 60), (x + 180, y - 60), (x + 180, y)], (0.35, 0.22, 0.08), 3, GOLD, a)
    shape(c, [(x - 150, y - 60), (x - 150, y - 300), (x + 150, y - 300), (x + 150, y - 60)], (0.50, 0.32, 0.10), 3, GOLD, a)
    c.set_source_rgba(*GOLD, 0.5 * a); c.set_line_width(1.5)
    for k in range(1, 6): c.move_to(x - 150, y - 60 - k * 40); c.line_to(x + 150, y - 60 - k * 40)
    c.stroke()

def troops(c, rows, y0, n, s0, x0, x1, side_='qin', t=0, march=0.0, face=1, dy=40, kneel=False, bob=True, a=1):
    for r in range(rows - 1, -1, -1):
        s = s0 * (1 - 0.13 * r); y = y0 - r * dy
        for i in range(n):
            x = lerp(x0, x1, (i + 0.5 * (r % 2)) / max(1, n - 1)) + march * (1 - 0.1 * r)
            bb = abs(math.sin(t * 7 + i * 1.7)) * 8 * s / 0.3 if bob and march else 0
            soldier(c, x, y - bb, s, side_, t, True, a * (1 - 0.12 * r), 'kneel' if kneel else 'stand', face=face)

def scroll_sword(c, x, y, s, lit, a=1):
    """托盘里的赐剑"""
    sword(c, x - 260 * s, y, x + 200 * s, y, lit, a, 18 * s)
    shape(c, [(x - 300 * s, y - 34 * s), (x - 270 * s, y - 34 * s), (x - 270 * s, y + 34 * s), (x - 300 * s, y + 34 * s)], (0.55, 0.38, 0.14), 3, LINE, a)
    shape(c, [(x - 420 * s, y - 10 * s), (x - 300 * s, y - 10 * s), (x - 300 * s, y + 10 * s), (x - 420 * s, y + 10 * s)], (0.25, 0.12, 0.06), 3, LINE, a)

def badge(c, x, y, r, name, sub, who='baiqi', t=0, a=1, col=GOLD):
    """地图上的人物圆章：侧脸半身像"""
    c.save(); c.arc(x, y, r, 0, 6.28); c.clip()
    c.set_source_rgba(0.12, 0.08, 0.05, a); c.paint()
    glow(c, x, y + r * 0.4, r * 1.2, (1, 0.5, 0.2), 0.3 * a)
    kw = dict(baiqi=dict(hat='he', beard='none'), zhaokuo=dict(hat='helm', beard='none'), lianpo=dict(hat='helm', beard='white'),
              fanju=dict(hat='guan', beard='short'), king=dict(hat='mian', beard='long'), zking=dict(hat='mian', beard='short'),
              han=dict(hat='helm', beard='short'), wei=dict(hat='helm', beard='long'))[who]
    c.save(); s = r / 150.0; c.translate(x - 10 * s, y + 880 * s + r * 0.15); c.scale(s, s)
    head_side(c, t, kw['hat'], kw['beard'], a, hair_tail=False)
    c.restore(); c.restore()
    c.set_source_rgba(*col, a); c.set_line_width(4); c.arc(x, y, r, 0, 6.28); c.stroke()
    text(c, name, x, y + r + 40, 34, (1, 0.94, 0.8), a, 'c')
    if sub: text(c, sub, x, y + r + 74, 24, (0.85, 0.78, 0.62), a, 'c', shadow=False)

def hero_light(c, x, y, r=700, col=(1, 0.55, 0.2), a=0.3):
    glow(c, x, y, r, col, a)

# ---------------- 镜头 ----------------
def S_hook(c, lt, d, p):
    # 地图大远景：七十余座城一拍一拍点亮
    M.set_cam(111.6, 33.9, lerp(0.86, 0.95, p)); M.draw(c)
    names = ['新城', '伊阙', '光狼城', '鄢', '郢', '夷陵', '华阳', '陉城', '长平', '宛', '洛阳', '上党', '新郑', '大梁', '陈']
    n = int(lt / (BP / 2)) + 1
    for i, nm in enumerate(names[:n]):
        M.city(c, nm, 'red', lt, label=True, size=28, ring=(i == n - 1))
    M.city(c, '咸阳', 'gold', lt, size=34)
    k = min(70, int(ease(p * 1.2) * 70))
    text(c, "攻城", 120, 400, 34, (0.85, 0.75, 0.55), 1)
    text(c, f"{k}+", 120, 500, 110, GOLD, 1)
    text(c, "败绩  0", 120, 580, 44, (0.95, 0.35, 0.25), ease((p - 0.4) / 0.2))

def S_hook2(c, lt, d, p):
    sky(c, (0.02, 0.02, 0.03), (0.10, 0.04, 0.03))
    glow(c, 960, 520, 700, (0.8, 0.2, 0.1), 0.2)
    # 托盘里的剑，缓缓推近
    k = eout(p * 1.2)
    scroll_sword(c, 960 + lerp(200, 0, k), 560, 1.2, 0.9)
    # 背影：白起跪着？—— 用背影看着剑
    back(c, 1560, 1300, 0.82, lt, hat='he', lit=0.0, arms='none', rim=(0.9, 0.25, 0.1))
    stamp(c, "赐 死", 640, 300, 96, lt, hit=BP * 4)

def S_title(c, lt, d, p):
    sky(c, (0.03, 0.01, 0.01), (0.28, 0.06, 0.03))
    glow(c, 960, 620, 1000, (1, 0.35, 0.1), 0.35)
    mts(c, 760, (0.12, 0.04, 0.03), seed=4, lit=(1, 0.4, 0.15))
    troops(c, 4, 1000, 22, 0.24, -40, 1960, 'qin', lt, 0, 1, dy=34)
    ground(c, 1010)
    smoke(c, lt, 760, (0.25, 0.05, 0.03), 0.35)
    # 背影：高举发光剑，千军在前
    back(c, 1320, 1400, 1.0, lt, lit=1.0, arms='raise', wind=1.6)
    speedlines(c, lt, 960, 380, 90, 0.3 * (1 - ease(lt / 1.5)) + 0.08)
    k = eout(lt / 0.35); sc = lerp(1.8, 1.0, k)
    c.save(); c.translate(620, 480); c.scale(sc, sc)
    text(c, "白  起", 0, 0, 230, (1, 0.94, 0.80), k, 'c')
    c.restore()
    text(c, "一生攻城七十余座 · 未尝一败", 620, 580, 46, GOLD, ease((lt - 0.9) / 0.4), 'c')
    embers(c, lt, 90, a=0.9)

def S_first(c, lt, d, p):
    M.set_cam(lerp(109.6, 111.0, ease(p)), 34.5, 1.15); M.draw(c)
    M.city(c, '咸阳', 'gold', lt); M.city(c, '新城', 'red', lt, ring=1)
    M.march(c, M.path_pts(['咸阳', '函谷关', (111.6, 34.4), '新城']), ease(p * 1.3))
    badge(c, 420, 430, 130, "白起", "秦 · 左庶长", 'baiqi', lt, ease(p * 3))
    M.flagpin(c, *M.P('咸阳'), '秦')

def S_yique(c, lt, d, p):
    M.set_cam(112.3, 34.5, lerp(1.6, 1.75, p)); M.draw(c)
    M.city(c, '伊阙', 'gold', lt, ring=1); M.city(c, '洛阳', 'gold', lt, dx=-18)
    k = ease(p * 2)
    x, y = M.P('伊阙')
    M.army_block(c, x + 380, y - 120, 280 * k + 1, 110, (0.30, 0.38, 0.30), "韩", k)
    M.army_block(c, x + 380, y + 90, 300 * k + 1, 110, (0.35, 0.30, 0.45), "魏", k)
    M.army_block(c, x - 380, y, 150 * ease((p - 0.3) / 0.2) + 1, 90, QIN, "秦", ease((p - 0.3) / 0.2))
    text(c, "韩魏联军  24 万+", x + 380, y + 230, 40, (0.95, 0.88, 0.72), k, 'c')
    text(c, "秦军  不到一半", x - 380, y + 120, 36, (1, 0.6, 0.5), ease((p - 0.4) / 0.2), 'c')

def S_yique2(c, lt, d, p):
    M.set_cam(112.3, 34.5, 1.75); M.draw(c)
    x, y = M.P('伊阙')
    M.army_block(c, x + 380, y - 120, 280, 110, (0.30, 0.38, 0.30), "韩")
    M.army_block(c, x + 380, y + 90, 300, 110, (0.35, 0.30, 0.45), "魏")
    M.jag(c, x + 560, y - 70, x + 560, y + 40, lt, 0.9)
    text(c, "互相推诿", x + 620, y - 10, 30, (1, 0.5, 0.4), 1, 'l')
    M.arrow(c, x - 260, y - 40, x + 200, y - 120, ease(p * 2), (0.85, 0.75, 0.55), 16, dash=True)
    text(c, "佯攻", x - 40, y - 140, 34, (0.95, 0.88, 0.72), ease(p * 2), 'c')
    M.arrow(c, x - 260, y + 30, x + 210, y + 90, ease((p - 0.4) / 0.3), RED, 34)
    text(c, "主力直扑", x - 30, y + 170, 40, (1, 0.45, 0.35), ease((p - 0.45) / 0.2), 'c')
    badge(c, 260, 360, 110, "白起", None, 'baiqi', lt)

def S_yique3(c, lt, d, p):
    sky(c, (0.20, 0.05, 0.03), (0.55, 0.18, 0.06))
    glow(c, 1300, 600, 800, (1, 0.5, 0.15), 0.35)
    mts(c, 720, (0.22, 0.07, 0.04), seed=8, lit=(1, 0.5, 0.2))
    smoke(c, lt, 700, (0.2, 0.06, 0.03), 0.4)
    troops(c, 3, 860, 14, 0.26, 1000, 2000, 'zhao', lt, -lt * 120, -1, dy=30)   # 溃逃
    ground(c, 880)
    arrows(c, lt, 70, 5, 0.25, speed=2400)
    k = eout(lt / 0.5)
    side(c, lerp(250, 640, k), 1060, 0.86, lt, arms='slash', p=cl(lt / 0.35), stride=1.0, wind=1.8, lean=0.08)
    speedlines(c, lt, 700, 500, 60, 0.25)
    stamp(c, "斩首二十四万", 1320, 380, 92, lt, hit=BP * 2)
    embers(c, lt, 60)

def S_march(c, lt, d, p):
    M.set_cam(lerp(111.0, 112.5, ease(p)), lerp(34.6, 35.2, ease(p)), 1.0); M.draw(c)
    M.city(c, '咸阳', 'gold', lt)
    routes = [['咸阳', '函谷关', '洛阳', '大梁'], ['咸阳', '函谷关', '伊阙', '新郑'], ['咸阳', '陉城', '光狼城'], ['咸阳', '函谷关', '洛阳', '上党']]
    for i, rt in enumerate(routes):
        k = ease((p - i * 0.12) / 0.45)
        M.march(c, M.path_pts(rt), k)
        if k >= 1:
            x, y = M.P(rt[-1]); M.flagpin(c, x, y, '秦'); M.city(c, rt[-1], 'red', lt, label=True)
    n = int(ease(p) * 40)
    text(c, "十年 · 夺城", 120, 400, 34, (0.85, 0.75, 0.55), 1)
    text(c, f"{n} 座", 120, 500, 100, GOLD, 1)

def S_zhao280(c, lt, d, p):
    M.set_cam(112.6, 35.6, lerp(1.6, 2.0, ease(p))); M.draw(c)
    x, y = M.P('光狼城')
    M.city(c, '光狼城', 'red', lt, ring=1)
    M.arrow(c, x - 500, y + 160, x - 30, y + 10, ease(p * 2), RED, 30)
    badge(c, 330, 400, 110, "白起", "攻赵", 'baiqi', lt)
    stamp(c, "斩首三万", 1300, 420, 96, lt, hit=BP * 2)

def S_yan(c, lt, d, p):
    sky(c, (0.10, 0.12, 0.14), (0.35, 0.30, 0.25))
    mts(c, 600, (0.14, 0.15, 0.15), seed=12)
    wall(c, 700, 2000, 330, 900, (0.32, 0.30, 0.28), gate=1340, gate_name="鄢")
    for x in (900, 1700): flag(c, x, 304, "楚", (0.15, 0.35, 0.22), lt, 220)
    ground(c, 900)
    # 云梯被推倒
    for i, x in enumerate((780, 1050, 1580)):
        k = ((lt * 0.6 + i * 0.3) % 1)
        c.save(); c.translate(x, 900); c.rotate(-0.25 - 0.5 * ease(k))
        shape(c, [(-20, 0), (-20, -560), (20, -560), (20, 0)], None, 3, LINE)
        for j in range(10): line(c, [(-20, -j * 56), (20, -j * 56)], 3, LINE)
        c.restore()
    arrows(c, lt, 50, 6, 3.1416 - 0.45, speed=1600)
    side(c, 330, 1060, 0.8, lt, arms='rest', wind=1.2)

def S_canal(c, lt, d, p):
    M.set_cam(112.5, 32.0, lerp(2.0, 2.3, p)); M.draw(c)
    M.city(c, '鄢', 'red', lt, ring=1)
    src = (112.95, 32.55); dam = M.sp(*src)
    k = ease(p * 1.3)
    pts = M.path_pts([src, (112.75, 32.3), (112.55, 32.05), (112.4, 31.85), '鄢'])
    M.march(c, pts, k, (0.45, 0.75, 1.0), 9)
    shape(c, [(dam[0] - 40, dam[1] - 14), (dam[0] + 40, dam[1] - 14), (dam[0] + 40, dam[1] + 14), (dam[0] - 40, dam[1] + 14)], (0.4, 0.3, 0.2), 3, LINE)
    text(c, "垒石筑坝", dam[0] + 60, dam[1] + 10, 34, (0.95, 0.88, 0.72), 1)
    text(c, "白起渠 · 长百里", 1400, 820, 48, (0.55, 0.80, 1.0), ease((p - 0.4) / 0.2), 'c')
    badge(c, 300, 420, 110, "白起", None, 'baiqi', lt)

def S_flood(c, lt, d, p):
    sky(c, (0.06, 0.08, 0.10), (0.20, 0.24, 0.26))
    k = ease(p * 1.2)
    # 城墙泡塌
    c.save(); c.translate(1260, 900); c.rotate(0.12 * ease((p - 0.4) / 0.4)); c.translate(-1260, -900)
    wall(c, 600, 1920, 360, 900, (0.30, 0.30, 0.30), gate=1260, gate_name="鄢")
    c.restore()
    # 洪水：上涨的青色水面 + 浪线
    wy = lerp(1000, 640, k)
    c.set_source_rgba(0.10, 0.25, 0.32, 0.92); c.rectangle(0, wy, W, H); c.fill()
    for j in range(6):
        c.set_source_rgba(0.6, 0.85, 0.95, 0.6 - j * 0.08); c.set_line_width(3)
        y = wy + j * 50; c.move_to(0, y)
        for x in range(0, W + 40, 40): c.line_to(x, y + math.sin(x * 0.02 + lt * 6 + j) * 10)
        c.stroke()
    # 激流从左冲入
    for i in range(30):
        r = random.Random(i); x = (r.uniform(0, W) + lt * 900) % (W + 200) - 100; y = wy + r.uniform(-20, 200)
        line(c, [(x, y), (x + 90, y - 10)], 3, (0.8, 0.95, 1.0), 0.7)
    stamp(c, "死者数十万", 640, 420, 88, lt, hit=BP * 4)

def S_ying(c, lt, d, p):
    sky(c, (0.15, 0.03, 0.01), (0.60, 0.20, 0.05))
    glow(c, 1100, 700, 900, (1, 0.5, 0.1), 0.5)
    # 郢都宫阙燃烧
    for i, (x, w_, h_) in enumerate(((500, 380, 260), (1050, 520, 360), (1600, 380, 240))):
        shape(c, [(x - w_ / 2, 880), (x - w_ / 2, 880 - h_), (x + w_ / 2, 880 - h_), (x + w_ / 2, 880)], (0.25, 0.08, 0.05), 3, LINE)
        shape(c, [(x - w_ / 2 - 80, 880 - h_), (x, 880 - h_ - 140), (x + w_ / 2 + 80, 880 - h_)], (0.08, 0.05, 0.04), 3, LINE)
        for j in range(6): flame(c, x - w_ / 2 + j * w_ / 5, 880 - h_ + 20, 120 + 40 * math.sin(lt * 5 + j), lt, i * 10 + j)
    ground(c, 880, (0.08, 0.03, 0.02))
    smoke(c, lt, 400, (0.15, 0.05, 0.03), 0.5)
    embers(c, lt, 120, a=1)
    back(c, 960, 1260, 0.9, lt, lit=0.6, arms='sword', wind=1.5, rim=(1, 0.5, 0.1))
    stamp(c, "火烧夷陵", 1500, 330, 92, lt, hit=BP * 3)

def S_wuan(c, lt, d, p):
    palace(c, lt)
    throne(c, 1350, 820)
    side(c, 1350, 840, 0.62, lt, hat='mian', beard='long', armor=False, robe=(0.12, 0.08, 0.06), cape_col=None, arms='point', p=ease(p * 2), face=-1, accent=GOLD, hair_tail=False, scabbard=False, stride=0.2)
    side(c, 560, 1060, 0.78, lt, arms='bow', stride=0.35, wind=0.6, kneel=True)
    k = eout((lt - BP * 2) / 0.4)
    glow(c, 960, 330, 420, GOLD, 0.3 * k)
    c.save(); c.translate(960, 340); c.scale(lerp(2.2, 1, k), lerp(2.2, 1, k))
    text(c, "武 安 君", 0, 0, 130, GOLD, k, 'c')
    c.restore()

def S_huayang(c, lt, d, p):
    M.set_cam(lerp(111.0, 113.0, ease(p)), lerp(33.6, 34.5, ease(p)), 1.2); M.draw(c)
    M.city(c, '华阳', 'red', lt, ring=1); M.city(c, '宛', 'gold', lt)
    M.march(c, M.path_pts(['咸阳', (110.0, 34.0), '宛', (113.2, 34.2), '华阳']), ease(p * 1.2), w=7)
    dday = 1 + int(ease(p * 1.2) * 7)
    text(c, "急行军", 120, 400, 34, (0.85, 0.75, 0.55), 1)
    text(c, f"第 {dday} 天", 120, 500, 100, GOLD, 1)

def S_huayang2(c, lt, d, p):
    sky(c, (0.10, 0.07, 0.05), (0.40, 0.26, 0.14))
    # 黄河
    c.set_source_rgba(0.45, 0.32, 0.15, 1); c.rectangle(0, 760, W, 400); c.fill()
    for j in range(8):
        c.set_source_rgba(0.85, 0.65, 0.35, 0.5); c.set_line_width(3); y = 790 + j * 40; c.move_to(0, y)
        for x in range(0, W + 40, 40): c.line_to(x, y + math.sin(x * 0.015 + lt * 4 + j) * 8)
        c.stroke()
    text(c, "黄 河", 1600, 1000, 60, (0.95, 0.8, 0.5), 0.5, 'c')
    # 赵军被逼入河
    for i in range(12):
        k = ease((lt - i * 0.1) / 0.8); x = 900 + i * 80
        soldier(c, x + k * 60, lerp(760, 880, k), 0.2, 'zhao', lt, True, 1, 'lie' if k > 0.6 else 'stand', p=k)
    ground(c, 760, (0.14, 0.10, 0.07))
    troops(c, 2, 760, 8, 0.24, 120, 760, 'qin', lt, lt * 40, 1, dy=26)
    side(c, 420, 1060, 0.82, lt, arms='fwd', stride=0.9, wind=1.5, p=1)
    stamp(c, "斩首十三万", 1350, 380, 88, lt, hit=BP * 2)

def S_xing(c, lt, d, p):
    M.set_cam(111.6, 35.4, lerp(1.6, 1.9, p)); M.draw(c)
    x, y = M.P('陉城')
    M.city(c, '陉城', 'red', lt, ring=1)
    r = random.Random(4)
    for i in range(5):
        k = ease((p - 0.1 - i * 0.08) / 0.15)
        if k > 0:
            ox, oy = math.cos(i * 1.25) * 220, math.sin(i * 1.25) * 140
            M.flagpin(c, x + ox, y + oy, '秦', a=k)
    badge(c, 330, 400, 110, "白起", "攻韩", 'baiqi', lt)
    text(c, "拔城五座", x + 260, y + 220, 40, (0.95, 0.88, 0.72), ease(p * 2), 'c')
    stamp(c, "斩首五万", 1400, 330, 92, lt, hit=BP * 2)

def S_fear(c, lt, d, p):
    sky(c, (0.02, 0.01, 0.01), (0.12, 0.03, 0.02))
    glow(c, 1100, 520, 700, (0.9, 0.2, 0.08), 0.25)
    # 侧脸大特写：眼神一亮
    c.save(); s = 2.6; c.translate(820, 2850); c.scale(s, s)
    head_side(c, lt, 'he', 'none', 1, True, 1.2)
    c.restore()
    k = cl((lt - BP * 2) / 0.12) * (1 - cl((lt - BP * 2 - 0.4) / 0.4))
    glow(c, 820 + 42 * 2.6, 2850 - 887 * 2.6, 140, (1, 0.9, 0.7), 0.8 * k)
    # 六国名字在发抖
    for i, nm in enumerate("齐楚燕韩赵魏"):
        x = 1300 + (i % 3) * 200; y = 420 + (i // 3) * 220
        jx = math.sin(lt * 60 + i) * 6 * ease((lt - BP * 2) / 0.2); jy = math.cos(lt * 53 + i) * 6 * ease((lt - BP * 2) / 0.2)
        c.set_source_rgba(0.9, 0.85, 0.7, 0.5); c.set_line_width(2); c.arc(x + jx, y + jy - 30, 78, 0, 6.28); c.stroke()
        text(c, nm, x + jx, y + jy, 90, (0.9, 0.85, 0.75), 0.9, 'c')

def S_changping(c, lt, d, p):
    M.set_cam(112.9, lerp(35.6, 35.85, ease(p)), lerp(1.4, 1.8, ease(p))); M.draw(c)
    x, y = M.P('长平')
    M.city(c, '长平', 'red', lt, label=False, ring=1)
    k = ease(p * 2)
    M.army_block(c, x - 360, y + 40, 260 * k + 1, 120, QIN, "秦", k, "倾国之兵")
    M.army_block(c, x + 360, y + 40, 300 * k + 1, 120, ZB, "赵", k, "四十余万")
    M.jag(c, x - 200, y + 40, x + 180, y + 40, lt, k)
    text(c, "长  平", x, y - 120, 110, (1, 0.94, 0.8), ease(p * 3), 'c')

def S_lianpo(c, lt, d, p):
    sky(c, (0.08, 0.10, 0.13), (0.26, 0.26, 0.28))
    mts(c, 640, (0.15, 0.16, 0.18), seed=3)
    wall(c, 820, 2000, 520, 1000, (0.28, 0.28, 0.30), tower=False)
    flag(c, 1100, 494, "赵", ZB, lt, 220); flag(c, 1700, 494, "赵", ZB, lt, 220)
    # 廉颇：侧面立于垒上，白须
    side(c, 1420, 520, 0.42, lt, hat='helm', beard='white', cape_col=ZHAO_C, cape_dark=ZHAO_D, accent=ZHAO_C, arms='rest', face=-1, stride=0.3, hair_tail=False)
    text(c, "廉颇", 1420, 0 + 2 * 0, 1, (0, 0, 0), 0)
    text(c, "赵将 · 廉颇", 1420, 1050 - 1000 + 0, 1, (0, 0, 0), 0)
    text(c, "廉颇", 1520, 120 + 140, 46, (0.85, 0.9, 1.0), 1, 'l')
    ground(c, 1000)
    ph = (lt * 1.4) % 1; xoff = math.sin(ph * 3.1416) * 220
    troops(c, 2, 1040, 8, 0.24, 60 + xoff, 680 + xoff, 'qin', lt, 0, 1, dy=26)
    arrows(c, lt, 40, 8, 3.1416 - 0.25)
    stamp(c, "坚壁不出", 520, 360, 80, lt, hit=BP * 3)

def S_spy(c, lt, d, p):
    palace(c, lt, tone=(0.10, 0.12, 0.25))
    throne(c, 520, 820)
    side(c, 520, 840, 0.6, lt, hat='mian', beard='short', armor=False, robe=(0.12, 0.14, 0.22), cape_col=None, arms='hang', face=1, accent=GOLD, hair_tail=False, scabbard=False, stride=0.2)
    text(c, "赵王", 520, 280, 44, (0.85, 0.9, 1.0), 1, 'c')
    r = random.Random(1)
    for i in range(12):
        k = ((lt * 0.7 + i * 0.09) % 1)
        x = lerp(200, 1800, k) + r.uniform(-60, 60); y = 560 - math.sin(k * 3.14) * 260 + r.uniform(-80, 80)
        c.save(); c.translate(x, y); c.rotate(r.uniform(-0.6, 0.6))
        shape(c, [(-26, -38), (26, -38), (26, 38), (-26, 38)], (0.88, 0.82, 0.66), 1.5, (0.4, 0.3, 0.2), 0.9)
        for j in range(3): line(c, [(-14 + j * 12, -28), (-14 + j * 12, 28)], 2, (0.2, 0.15, 0.1), 0.8)
        c.restore()
    text(c, "“秦军只怕赵括”", 1000, 300, 52, GOLD, ease(p * 2), 'c')
    k = ease((p - 0.45) / 0.2)
    side(c, 1450, 1060, 0.74, lt, hat='helm', beard='none', cape_col=ZHAO_C, cape_dark=ZHAO_D, accent=ZHAO_C, arms='raise', p=k, face=-1, stride=0.5, a=max(0.001, k), hair_tail=True)
    text(c, "赵括", 1650, 380, 54, GOLD, k, 'l')

def S_secret(c, lt, d, p):
    sky(c, (0.01, 0.01, 0.03), (0.05, 0.05, 0.09))
    for i in range(80):
        r = random.Random(i); c.set_source_rgba(1, 1, 1, r.uniform(0.2, 0.7)); c.arc(r.uniform(0, W), r.uniform(0, 500), r.uniform(1, 2.2), 0, 6.28); c.fill()
    shape(c, [(1000, 900), (1400, 380), (1800, 900)], (0.14, 0.10, 0.07), 3, LINE)
    c.set_source_rgba(1, 0.7, 0.35, 0.6); c.move_to(1330, 900); c.line_to(1400, 560); c.line_to(1470, 900); c.close_path(); c.fill()
    glow(c, 1400, 760, 300, (1, 0.6, 0.3), 0.4)
    ground(c, 900, (0.03, 0.03, 0.04))
    # 背影：夜里走向军帐
    k = ease(p * 1.4)
    back(c, lerp(500, 1080, k), 1180, 0.62, lt, lit=0.0, arms='none', wind=0.8, rim=(1, 0.55, 0.25))
    soldier(c, 260, 900, 0.3, 'qin', lt); soldier(c, 1820, 900, 0.3, 'qin', lt, face=-1)
    stamp(c, "泄 者 斩", 600, 360, 100, lt, hit=BP * 4)

def S_trap(c, lt, d, p):
    M.set_cam(112.9, 35.8, 2.3); M.draw(c)
    k = ease(p * 1.6)
    x0, y0 = M.P('长平')
    zx = lerp(x0 + 420, x0 - 120, k)
    M.army_block(c, zx, y0, 360, 200, ZB, "赵括主力")
    M.army_block(c, x0 - 520, y0, 200, 300, (0.35, 0.30, 0.28), "秦壁")
    M.arrow(c, zx - 200, y0 + 140, zx - 200 - 240 * k, y0 + 140, k, (0.7, 0.7, 0.75), 12, dash=True)
    text(c, "佯败", x0 - 420, y0 + 220, 34, (0.9, 0.85, 0.75), k, 'c')
    k2 = ease((p - 0.4) / 0.3)
    if k2 > 0:
        M.arrow(c, x0 + 420, y0 - 420, x0 + 420, lerp(y0 - 420, y0 + 360, k2), 1, RED, 30)
        M.arrow(c, x0 - 300, y0 + 420, x0 - 300, lerp(y0 + 420, y0 - 300, k2), 1, RED, 26)
        text(c, "奇兵 2.5万 断后", x0 + 460, y0 - 330, 36, (1, 0.6, 0.5), k2, 'l')
        text(c, "骑兵 5千 截断", x0 - 260, y0 + 400, 36, (1, 0.6, 0.5), k2, 'l')

def S_siege(c, lt, d, p):
    M.set_cam(112.9, 35.8, lerp(2.0, 2.5, ease(p))); M.draw(c)
    x, y = M.P('长平')
    glow(c, x, y, 220, (1, 0.15, 0.1), 0.6)
    c.set_source_rgba(0.95, 0.2, 0.15, 1); c.arc(x, y, 14, 0, 6.28); c.fill()
    text(c, "赵军 四十万", x, y + 60, 34, (1, 0.9, 0.8), 1, 'c')
    n = 16
    for i in range(n):
        an = i / n * 6.283 + lt * 0.05; k = ease((p * 1.6 - i * 0.03))
        rr_ = lerp(520, 260, ease(p))
        M.flagpin(c, x + math.cos(an) * rr_, y + math.sin(an) * rr_ * 0.7 + 30, '秦', a=k, s=0.9)
    dd = 1 + int(ease(p) * 45)
    text(c, "断粮", 120, 400, 34, (0.85, 0.75, 0.55), 1)
    text(c, f"第 {dd} 天", 120, 500, 100, (0.95, 0.30, 0.24), 1)

def S_zhaokuo(c, lt, d, p):
    sky(c, (0.18, 0.04, 0.03), (0.50, 0.12, 0.05))
    glow(c, 900, 600, 800, (1, 0.3, 0.1), 0.3)
    mts(c, 760, (0.16, 0.05, 0.04), seed=6)
    ground(c, 900, (0.07, 0.03, 0.02))
    k = ease(p * 1.3); hitk = ease((p - 0.55) / 0.15)
    # 赵括侧面冲锋，中箭后仰
    c.save(); c.translate(lerp(300, 820, k), 1060); c.rotate(-0.35 * hitk); c.translate(-lerp(300, 820, k), -1060)
    side(c, lerp(300, 820, k), 1060, 0.82, lt, hat='helm', beard='none', cape_col=ZHAO_C, cape_dark=ZHAO_D, accent=ZHAO_C, arms='fwd', stride=1.0, wind=1.6)
    c.restore()
    arrows(c, lt, 120, 12, 3.1416 - 0.12, a=1, speed=2800)
    if hitk > 0:
        for j in range(5):
            ax = lerp(300, 820, k) + 40 + j * 20; ay = 1060 - 700 + j * 50
            line(c, [(ax, ay), (ax + 120, ay - 30)], 4, (0.95, 0.85, 0.6))
    text(c, "赵括", lerp(300, 820, k), 200, 54, (0.85, 0.9, 1.0), 1, 'c')
    stamp(c, "乱箭射死", 1450, 360, 92, lt, hit=BP * 4.5)

def S_surrender(c, lt, d, p):
    sky(c, (0.10, 0.09, 0.10), (0.30, 0.26, 0.24))
    mts(c, 640, (0.18, 0.16, 0.16), seed=9)
    ground(c, 660, (0.10, 0.09, 0.09))
    for r in range(6):
        s = 0.12 + r * 0.03; y = 700 + r * 60
        for i in range(26 - r * 2):
            soldier(c, 600 + i * (1400 / (26 - r * 2)) + (r % 2) * 20, y, s, 'zhao', lt, False, 1, 'kneel')
    r_ = random.Random(3)
    for i in range(50):
        x = 1500 + r_.uniform(-200, 200); y = 700 + r_.uniform(-10, 30); an = r_.uniform(-1, 1)
        line(c, [(x, y), (x + math.sin(an) * 200, y - math.cos(an) * 150)], 3, (0.75, 0.72, 0.65), 0.7)
    back(c, 300, 1250, 0.72, lt, lit=0.5, arms='sword', wind=1.0)
    text(c, "400,000", 1150, 380, 130, (0.95, 0.92, 0.85), ease(p * 2), 'c')

def S_bury(c, lt, d, p):
    if lt < BP * 3:
        sky(c, (0.0, 0.0, 0.0), (0.02, 0.02, 0.03))
        moon(c, 960, 380, 70, 0.8)
        text(c, "那 一 夜", 960, 760, 64, (0.75, 0.72, 0.7), ease(lt / 0.4), 'c')
        return
    l2 = lt - BP * 3
    sky(c, (0.15, 0.01, 0.01), (0.45, 0.04, 0.02))
    moon(c, 1500, 260, 50, 0.6)
    ground(c, 700, (0.05, 0.02, 0.02))
    c.set_source_rgb(0, 0, 0); c.save(); c.translate(1100, 860); c.scale(1, 0.22); c.arc(0, 0, 760, 0, 6.28); c.restore(); c.fill()
    for i in range(40):
        r = random.Random(i); x = 1100 + r.uniform(-640, 640); y = 860 + r.uniform(-110, 110)
        soldier(c, x, y, 0.13, 'zhao', 0, False, 0.6, 'lie', p=1, face=1 if i % 2 else -1)
    troops(c, 2, 740, 10, 0.2, 340, 900, 'qin', l2, 0, 1, dy=20)
    troops(c, 2, 740, 10, 0.2, 1300, 1880, 'qin', l2, 0, -1, dy=20)
    # 白起背影立于坑边
    back(c, 300, 1250, 0.8, l2, lit=0.3, arms='sword', wind=1.4, rim=(1, 0.15, 0.08))
    text(c, "放回 240 人", 1100, 380, 64, (0.95, 0.92, 0.85), ease(l2 / 0.3), 'c')
    stamp(c, "坑 杀", 1100, 560, 140, l2, hit=0.05, rot=-0.05)
    embers(c, l2, 50, a=0.6)

def S_fanju(c, lt, d, p):
    palace(c, lt, tone=(0.35, 0.08, 0.05))
    throne(c, 1200, 820)
    side(c, 1200, 840, 0.6, lt, hat='mian', beard='long', armor=False, robe=(0.12, 0.08, 0.06), cape_col=None, arms='hang', face=-1, accent=GOLD, hair_tail=False, scabbard=False, stride=0.2)
    side(c, 760, 1040, 0.62, lt, hat='guan', beard='short', armor=False, robe=(0.15, 0.20, 0.25), cape_col=None, arms='bow', face=1, accent=GOLD, hair_tail=False, scabbard=False, stride=0.25)
    text(c, "范雎", 600, 330, 46, (0.9, 0.85, 0.75), 1, 'c')
    # 半透明小地图：伸向邯郸的红箭被擦掉
    k = ease(p * 1.5)
    shape(c, [(1420, 180), (1840, 180), (1840, 470), (1420, 470)], (0.15, 0.11, 0.07), 2, GOLD, 0.9)
    M.arrow(c, 1470, 420, 1740, 260, 1, RED, 14, a=1 - k)
    c.set_source_rgba(0.95, 0.85, 0.6, 1); c.arc(1760, 248, 7, 0, 6.28); c.fill()
    text(c, "邯郸", 1760, 230, 30, (0.95, 0.88, 0.72), 1, 'c')
    stamp(c, "议 和", 1630, 360, 64, lt, hit=BP * 4)

def S_handan(c, lt, d, p):
    sky(c, (0.05, 0.06, 0.09), (0.18, 0.18, 0.20))
    wall(c, 500, 2000, 360, 900, (0.25, 0.26, 0.29), gate=1300, gate_name="邯郸")
    flag(c, 800, 334, "赵", ZB, lt, 220); flag(c, 1750, 334, "赵", ZB, lt, 220)
    ground(c, 900)
    for i in range(12):
        k = ease((lt - i * 0.12) / 0.4)
        soldier(c, 700 + i * 90, 980, 0.22, 'qin', lt, True, 1, 'lie', p=k)
    arrows(c, lt, 50, 6, 3.1416 - 0.45)
    # 白起侧身背对战场（称病不去）
    side(c, 250, 1060, 0.7, lt, arms='hang', face=-1, stride=0.25, wind=0.4, lit=0)
    stamp(c, "秦军大败", 1250, 640, 80, lt, hit=BP * 4)

def S_exile(c, lt, d, p):
    sky(c, (0.12, 0.10, 0.10), (0.42, 0.30, 0.20))
    wall(c, -100, 900, 380, 880, (0.28, 0.26, 0.24), gate=420, gate_name="咸阳")
    ground(c, 880)
    # 盔甲和红披风弃在地上
    shape(c, [(860, 880), (1040, 880), (1010, 858), (880, 858)], CAPE, 3, LINE)
    shape(c, [(900, 858), (900, 830, 960, 820, 960, 858)], INKF, 3, LINE)
    x = lerp(1080, 1520, ease(p))
    side(c, x, 1060, 0.66, lt, hat='bun', beard='none', armor=False, robe=(0.25, 0.22, 0.18), cape_col=None, arms='hang', stride=0.4 + 0.3 * math.sin(lt * 5), hair_tail=False, scabbard=False, accent=(0.3, 0.25, 0.2))
    text(c, "削为士伍", 1500, 300, 56, (0.95, 0.88, 0.72), ease(p * 2), 'c')

def S_duyou(c, lt, d, p):
    sky(c, (0.08, 0.06, 0.06), (0.36, 0.20, 0.12))
    glow(c, 1500, 700, 500, (1, 0.6, 0.3), 0.35)
    ground(c, 880)
    # 驿亭
    x = 1560
    shape(c, [(x - 160, 880), (x - 160, 600), (x + 160, 600), (x + 160, 880)], (0.18, 0.10, 0.06), 3, LINE)
    shape(c, [(x - 260, 610), (x, 470), (x + 260, 610)], (0.08, 0.05, 0.04), 3, LINE)
    text(c, "杜邮", x, 560, 44, GOLD, 1, 'c')
    side(c, 520, 1060, 0.66, lt, hat='bun', beard='none', armor=False, robe=(0.25, 0.22, 0.18), cape_col=None, arms='hang', stride=0.25, hair_tail=False, scabbard=False, accent=(0.3, 0.25, 0.2))
    side(c, 1150, 1060, 0.62, lt, hat='guan', beard='short', armor=False, robe=(0.20, 0.08, 0.06), cape_col=None, arms='offer', face=-1, stride=0.3, hair_tail=False, scabbard=False, accent=GOLD)
    k = ease(p * 2)
    sword(c, 980 - 120 * k, 680, 1120 - 120 * k, 680, 0.9 * k + 0.1, 1, 9)

def S_last(c, lt, d, p):
    sky(c, (0.03, 0.03, 0.04), (0.20, 0.06, 0.04))
    glow(c, 960, 820, 800, (0.9, 0.25, 0.1), 0.25)
    for i in range(40):
        r = random.Random(i); x = r.uniform(0, W); y = r.uniform(500, 900); s = r.uniform(0.15, 0.3)
        soldier(c, x, y, s, 'zhao', lt, False, 0.12 + 0.18 * ease(p), 'stand', face=-1 if x > 960 else 1)
    ground(c, 900, (0.04, 0.03, 0.03))
    # 侧面跪地，剑横于前
    side(c, 900, 1060, 0.86, lt, hat='bun', beard='none', armor=False, robe=(0.25, 0.22, 0.18), cape_col=None, arms='down', kneel=True, hair_tail=True, scabbard=False, accent=(0.3, 0.25, 0.2), wind=0.6, lit=1.0)

def S_end(c, lt, d, p):
    sky(c, (0.0, 0.0, 0.0), (0.10, 0.03, 0.02))
    glow(c, 560, 560, 600, GOLD, 0.25); glow(c, 1360, 560, 600, RED, 0.25)
    mts(c, 900, (0.05, 0.03, 0.02), seed=21)
    back(c, 960, 1330, 0.85, lt, lit=0.8, arms='sword', wind=1.4)
    text(c, "战 神", 520, 520, 120, GOLD, ease(lt / 0.4), 'c')
    text(c, "杀 神", 1400, 520, 120, (0.95, 0.3, 0.24), ease((lt - 0.3) / 0.4), 'c')
    text(c, "评论区告诉我你的答案", 960, 1035, 36, (0.75, 0.72, 0.7), ease((lt - 0.8) / 0.5), 'c', shadow=False)

CAM = {
    'hook': (1.0, 1.04, 960, 540), 'hook2': (1.05, 1.0, 960, 500), 'title': (1.15, 1.0, 960, 540),
    'yique3': (1.0, 1.10, 700, 700), 'ying': (1.0, 1.08, 960, 700), 'fear': (1.0, 1.10, 900, 500),
    'bury': (1.0, 1.08, 960, 700), 'last': (1.0, 1.15, 900, 600), 'end': (1.0, 1.06, 960, 600),
}
