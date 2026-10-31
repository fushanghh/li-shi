# 线描威武人物库：general(c, x, y, s, ...)  y=脚底，正面，身高约 1150 单位
import math, random
import cairocffi as cairo

GOLD = (0.88, 0.72, 0.42)
LINE = (0.96, 0.86, 0.62)
INKF = (0.10, 0.08, 0.07)
ROBE = (0.20, 0.10, 0.08)
CAPE = (0.70, 0.08, 0.06)
CAPE_D = (0.42, 0.04, 0.03)
ZHAO_C = (0.16, 0.26, 0.40)     # 赵国青蓝
ZHAO_D = (0.08, 0.13, 0.22)
SKIN = (0.55, 0.40, 0.30)
STEEL = (0.92, 0.95, 1.0)
DARKL = (0.05, 0.03, 0.02)

def P(c, pts, close=True):
    c.move_to(*pts[0])
    for q in pts[1:]:
        if len(q) == 6: c.curve_to(*q)
        else: c.line_to(*q)
    if close: c.close_path()

def shape(c, pts, fill, lw=4.5, col=LINE, a=1, close=True):
    P(c, pts, close)
    if fill is not None:
        c.set_source_rgba(*fill, a); c.fill_preserve()
    c.set_source_rgba(*col, a); c.set_line_width(lw); c.stroke()

def line(c, pts, lw=2.5, col=LINE, a=1):
    P(c, pts, False); c.set_source_rgba(*col, a); c.set_line_width(lw); c.stroke()

def tube(c, pts, w, fill, a=1, lw=4.5, col=LINE):
    """描边粗管：袖子、腿、矛杆"""
    c.set_line_cap(1); c.set_line_join(1)
    P(c, pts, False); c.set_source_rgba(*col, a); c.set_line_width(w + lw * 2); c.stroke()
    P(c, pts, False); c.set_source_rgba(*fill, a); c.set_line_width(w); c.stroke()

def glow(c, x, y, r, col, a):
    if a <= 0: return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
    c.set_source(g); c.arc(x, y, r, 0, 6.2832); c.fill()

def hatch(c, pts, a=1, gap=11, col=(0, 0, 0), alpha=0.35, ang=0.9):
    c.save(); P(c, pts); c.clip()
    xs = [q[-2] for q in pts]; ys = [q[-1] for q in pts]
    x0, x1, y0, y1 = min(xs) - 500, max(xs) + 400, min(ys), max(ys)
    c.set_source_rgba(*col, alpha * a); c.set_line_width(2.2)
    x = x0
    while x < x1:
        c.move_to(x, y1); c.line_to(x + (y1 - y0) * ang, y0); x += gap
    c.stroke(); c.restore()

def lamellar(c, x0, y0, x1, y1, rows, cols, a=1, lw=1.6):
    c.set_source_rgba(*GOLD, 0.75 * a); c.set_line_width(lw)
    h = (y1 - y0) / rows; w = (x1 - x0) / cols
    for r in range(rows + 1):
        c.move_to(x0, y0 + r * h); c.line_to(x1, y0 + r * h)
    c.stroke()
    for r in range(rows):
        off = (w / 2) if r % 2 else 0
        for k in range(cols + 1):
            x = x0 + k * w + off
            if x0 < x < x1: c.move_to(x, y0 + r * h); c.line_to(x, y0 + (r + 1) * h)
        c.stroke()
        for k in range(cols):
            x = x0 + (k + 0.5) * w + off
            if x0 < x < x1: c.arc(x, y0 + r * h + h * 0.3, 2.2, 0, 6.28); c.fill()

# ---------------- 部件 ----------------
def cape(c, t, col, dark, wind=1.0, a=1):
    w = math.sin(t * 2.6) * 30 * wind; w2 = math.sin(t * 2.6 + 1.2) * 40 * wind
    pts = [(-150, -775), (-260, -640, -420 - w, -380, -560 - w2, -90), (-430 - w2 * 0.6, -60),
           (-330 - w * 0.5, -40), (-240, -30, -170, -200, -100, -300), (150, -775)]
    shape(c, pts, col, 5, LINE, a)
    hatch(c, pts[:3] + [(-430 - w2 * 0.6, -60), (-300, -500)], a, gap=10, col=(0.2, 0, 0), alpha=0.45)
    for x0, x1 in [(-150, -470), (-130, -380), (-110, -300)]:
        line(c, [(x0, -720), (x0 - 60, -520, x1 - w * 0.6, -300, x1 - w2 * 0.8, -100)], 2.4, (1, 0.62, 0.5), 0.6 * a)
    shape(c, [(150, -775), (200, -600, 260 + w * 0.3, -420, 300 + w * 0.5, -300), (230, -320), (150, -560)], dark, 4, LINE, a)

def hat_draw(c, hat, t, a):
    sw = math.sin(t * 3) * 4
    if hat == 'he':      # 秦将鹖冠
        for sx in (-1, 1):
            shape(c, [(sx * 18, -1000), (sx * 50, -1040, sx * (95 + sw), -1060, sx * (118 + sw), -1035),
                      (sx * (100 + sw), -1048, sx * 70, -1030, sx * 46, -990)], (0.20, 0.14, 0.10), 3.5, LINE, a)
            line(c, [(sx * 40, -1010), (sx * (98 + sw), -1044)], 1.6, GOLD, 0.8 * a)
        shape(c, [(-62, -925), (-66, -975), (-40, -1006), (40, -1006), (66, -975), (62, -925)], INKF, 4.5, LINE, a)
        line(c, [(-64, -955), (64, -955)], 2.4, GOLD, a)
        for k in range(-2, 3): c.set_source_rgba(*GOLD, a); c.arc(k * 22, -940, 3, 0, 6.28); c.fill()
    elif hat == 'helm':  # 赵将：圆兜鍪 + 长缨
        shape(c, [(-66, -900), (-70, -960, -40, -1010, 0, -1012), (40, -1010, 70, -960, 66, -900), (40, -915), (-40, -915)], (0.14, 0.16, 0.20), 4.5, LINE, a)
        for k in range(-2, 3): line(c, [(k * 26, -1008), (k * 34, -915)], 1.6, GOLD, 0.7 * a)
        shape(c, [(0, -1010), (-6, -1060), (6, -1060)], GOLD, 2, LINE, a)
        shape(c, [(-4, -1060), (-40 + sw * 2, -1100, -90 + sw * 3, -1110, -120 + sw * 4, -1090), (-70, -1080, -30, -1060, 4, -1056)], CAPE, 2.5, LINE, a)
        shape(c, [(-70, -905), (-80, -850), (-56, -830), (-56, -900)], (0.14, 0.16, 0.20), 3, LINE, a)
        shape(c, [(70, -905), (80, -850), (56, -830), (56, -900)], (0.14, 0.16, 0.20), 3, LINE, a)
    elif hat == 'mian':  # 王：冕冠 + 旒
        shape(c, [(-50, -930), (-54, -985), (54, -985), (50, -930)], (0.12, 0.08, 0.06), 4, LINE, a)
        shape(c, [(-120, -1000), (120, -1000), (120, -985), (-120, -985)], INKF, 3.5, LINE, a)
        for k in range(-5, 6):
            x = k * 21
            line(c, [(x, -985), (x, -900 - abs(k) * 2)], 1.2, GOLD, 0.8 * a)
            for j in range(4): c.set_source_rgba(0.9, 0.3, 0.2, a); c.arc(x, -970 + j * 18, 3, 0, 6.28); c.fill()
    elif hat == 'guan':  # 文官高冠
        shape(c, [(-46, -925), (-46, -985), (-26, -1030), (26, -1030), (46, -985), (46, -925)], (0.08, 0.06, 0.05), 4, LINE, a)
        line(c, [(0, -1030), (0, -930)], 2, GOLD, 0.8 * a)
        shape(c, [(-58, -930), (58, -930), (58, -918), (-58, -918)], INKF, 3, LINE, a)
    elif hat == 'bun':   # 布衣发髻
        shape(c, [(-56, -925), (-58, -970, -30, -995, 0, -995), (30, -995, 58, -970, 56, -925)], DARKL, 4, LINE, a)
        shape(c, [(-18, -990), (-20, -1030), (20, -1030), (18, -990)], DARKL, 3.5, LINE, a)
        line(c, [(-22, -1010), (22, -1010)], 2.4, GOLD, a)

def head(c, t, hat='he', beard='full', age=0, a=1):
    # 鬓发
    hc = (0.75, 0.72, 0.68) if beard == 'white' else (0.06, 0.05, 0.04)
    shape(c, [(-62, -925), (-66, -880), (-58, -850), (-52, -905)], hc, 2.5, LINE, a)
    shape(c, [(62, -925), (66, -880), (58, -850), (52, -905)], hc, 2.5, LINE, a)
    if beard == 'none':   # 年轻：窄下巴
        face = [(-54, -925), (-56, -870, -52, -830, -36, -805), (-14, -792), (14, -792), (36, -805, 52, -830, 56, -870), (54, -925)]
    else:
        face = [(-56, -925), (-60, -870, -58, -835, -44, -808), (-20, -786), (20, -786), (44, -808, 58, -835, 60, -870), (56, -925)]
    shape(c, face, SKIN, 4.5, LINE, a)
    hatch(c, [(18, -925), (56, -925), (60, -870), (44, -808), (20, -786), (24, -840)], a, gap=8, alpha=0.3)
    if age:  # 皱纹
        for k in range(2): line(c, [(-30, -915 + k * 7), (30, -915 + k * 7)], 1.4, (0.3, 0.15, 0.08), a)
        line(c, [(-48, -860), (-40, -830)], 1.6, (0.3, 0.15, 0.08), a); line(c, [(48, -860), (40, -830)], 1.6, (0.3, 0.15, 0.08), a)
    else:
        line(c, [(-46, -858), (-36, -842)], 1.8, (0.25, 0.12, 0.07), a); line(c, [(46, -858), (36, -842)], 1.8, (0.25, 0.12, 0.07), a)
    bc = (0.85, 0.82, 0.78) if beard == 'white' else (0.05, 0.04, 0.03)
    for sx in (-1, 1):
        shape(c, [(sx * 50, -902), (sx * 30, -900), (sx * 8, -886), (sx * 12, -880), (sx * 32, -890), (sx * 50, -893)], bc, 1.5, LINE, a)
        shape(c, [(sx * 40, -872), (sx * 26, -880), (sx * 12, -872), (sx * 26, -868)], (0.95, 0.88, 0.75), 1.6, DARKL, a)
        c.set_source_rgba(*DARKL, a); c.arc(sx * 24, -873, 4, 0, 6.28); c.fill()
        c.set_source_rgba(1, 1, 1, a); c.arc(sx * 23, -875, 1.3, 0, 6.28); c.fill()
    line(c, [(-4, -892), (-2, -878)], 1.6, (0.25, 0.12, 0.07), a); line(c, [(4, -892), (2, -878)], 1.6, (0.25, 0.12, 0.07), a)
    line(c, [(-2, -870), (-8, -840), (0, -834), (8, -838)], 2.4, (0.18, 0.09, 0.05), a)
    if beard in ('full', 'white'):
        shape(c, [(-58, -850), (-56, -820, -40, -790, -20, -778), (0, -770), (20, -778), (40, -790, 56, -820, 58, -850),
                  (46, -830), (20, -812), (0, -816), (-20, -812), (-46, -830)], bc, 2.4, LINE, a)
        ln = 120 if beard == 'white' else 90
        shape(c, [(-22, -790), (-18, -750, -10, -725, 0, -790 + ln), (10, -725, 18, -750, 22, -790)], bc, 2.4, LINE, a)
        for k in range(-2, 3): line(c, [(k * 7, -785), (k * 5, -800 + ln)], 1.2, GOLD if beard == 'full' else (0.5, 0.5, 0.5), 0.6 * a)
    if beard in ('full', 'white', 'short', 'long'):
        shape(c, [(-2, -830), (-24, -828, -44, -822, -54, -800), (-30, -816, -14, -820, 0, -822),
                  (14, -820, 30, -816, 54, -800), (44, -822, 24, -828, 2, -830)], bc, 2, LINE, a)
    if beard == 'short':
        shape(c, [(-12, -800), (0, -770), (12, -800)], bc, 2, LINE, a)
    if beard == 'long':
        shape(c, [(-26, -800), (-20, -740, -8, -700, 0, -680), (8, -700, 20, -740, 26, -800)], bc, 2.4, LINE, a)
    line(c, [(-14, -812), (14, -812)], 2.2, (0.35, 0.1, 0.06), a)
    hat_draw(c, hat, t, a)

def sword(c, x0, y0, x1, y1, lit=1.0, a=1, w=14):
    if lit > 0:
        glow(c, (x0 + x1) / 2, (y0 + y1) / 2, 0.6 * math.hypot(x1 - x0, y1 - y0), (0.7, 0.82, 1.0), 0.35 * lit)
    c.set_line_cap(1)
    c.set_source_rgba(*STEEL, (0.6 + 0.4 * lit) * a); c.set_line_width(w); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    c.set_source_rgba(1, 1, 1, lit * a); c.set_line_width(w * 0.3); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()

def legs(c, a, armor):
    lc = (0.13, 0.10, 0.09)
    shape(c, [(-95, -330), (-115, -170), (-140, -50), (-190, -12), (-190, 0), (-70, 0), (-66, -50), (-45, -170), (-22, -330)], lc, 4.5, LINE, a)
    shape(c, [(95, -330), (115, -170), (140, -50), (190, -12), (190, 0), (70, 0), (66, -50), (45, -170), (22, -330)], lc, 4.5, LINE, a)
    for sx in (-1, 1):
        line(c, [(sx * 64, -70), (sx * 142, -70)], 2.5, GOLD, a)
        if armor:
            for yy in (-130, -180, -230): line(c, [(sx * (50 + (yy + 330) * 0.05), yy), (sx * (118 - (yy + 170) * 0.1), yy - 8)], 1.6, GOLD, 0.6 * a)
    hatch(c, [(95, -330), (115, -170), (140, -50), (190, -12), (110, -12), (66, -50), (60, -170), (50, -330)], a)

def torso(c, a, armor, robe, accent):
    c.save(); c.scale(1.18, 1)
    shape(c, [(-115, -560), (-150, -400), (-165, -290), (-80, -270), (0, -282), (80, -270), (165, -290), (150, -400), (115, -560)], robe, 4.5, LINE, a)
    line(c, [(-60, -540), (-80, -400, -92, -330, -100, -280)], 2, GOLD, 0.6 * a)
    line(c, [(60, -540), (80, -400, 92, -330, 100, -280)], 2, GOLD, 0.6 * a)
    hatch(c, [(40, -560), (115, -560), (150, -400), (165, -290), (60, -275)], a)
    if armor:
        shape(c, [(-112, -575), (-130, -420), (0, -400), (130, -420), (112, -575)], INKF, 4.5, LINE, a)
        lamellar(c, -122, -570, 122, -412, 4, 9, a)
        pts = [(-110, -755), (-125, -640), (-112, -560), (0, -520), (112, -560), (125, -640), (110, -755)]
        shape(c, pts + [(40, -770), (-40, -770)], INKF, 5, LINE, a)
        c.save(); P(c, pts); c.clip(); lamellar(c, -125, -700, 125, -520, 6, 10, a); c.restore()
        hatch(c, [(40, -770), (110, -755), (125, -640), (112, -560), (40, -530)], a)
        for sx in (-1, 1):
            shape(c, [(sx * 62, -735), (sx * 86, -722), (sx * 72, -700), (sx * 50, -712)], accent, 2.5, LINE, a)
        line(c, [(-110, -700), (110, -700)], 3, LINE, a)
    else:   # 长袍：交领右衽
        pts = [(-110, -760), (-130, -640), (-118, -560), (118, -560), (130, -640), (110, -760)]
        shape(c, pts, robe, 4.5, LINE, a)
        line(c, [(-40, -775), (30, -640), (60, -565)], 3, GOLD, a)
        line(c, [(40, -775), (-10, -700)], 3, GOLD, a)
        hatch(c, [(40, -770), (110, -760), (130, -640), (118, -560), (40, -560)], a)
    shape(c, [(-30, -770), (0, -740), (30, -770), (0, -790)], accent, 3, LINE, a)
    shape(c, [(-120, -600), (120, -600), (118, -575), (-118, -575)], (0.30, 0.18, 0.08), 3, LINE, a)
    shape(c, [(-14, -598), (14, -598), (10, -578), (-10, -578)], GOLD, 2, LINE, a)
    if armor:
        for sx in (-1, 1):
            for k in range(4):
                y = -772 + k * 38; x0 = sx * (96 + k * 4); x1 = sx * (190 + k * 12)
                shape(c, [(x0, y), (x1, y + 6), (x1 + sx * 8, y + 46), (x0, y + 38)], INKF, 3.5, LINE, a)
                c.set_source_rgba(*GOLD, 0.8 * a); c.arc((x0 + x1) / 2, y + 20, 2.4, 0, 6.28); c.fill()
    c.restore()

def hand(c, x, y, r=24, a=1):
    shape(c, [(x - r, y - r * 0.6), (x + r * 0.8, y - r), (x + r, y + r * 0.6), (x - r * 0.7, y + r)], SKIN, 3.5, LINE, a)

def arms(c, kind, t, a, robe, sword_lit, p):
    """肩点 (±205, -720)（已含 1.18 横向放大）"""
    q = p
    if kind == 'rest':
        for sx in (-1, 1):
            tube(c, [(sx * 200, -700), (sx * 190, -600), (sx * 60, -520)], 62, robe, a)
        sword(c, 0, -470, 0, -10, sword_lit, a)
        shape(c, [(-48, -480), (48, -480), (40, -462), (-40, -462)], (0.45, 0.32, 0.12), 3, LINE, a)
        shape(c, [(-10, -530), (10, -530), (10, -480), (-10, -480)], (0.2, 0.12, 0.06), 2.5, LINE, a)
        hand(c, -24, -526, 26, a); hand(c, 24, -530, 26, a)
        c.set_source_rgba(*GOLD, a); c.arc(0, -552, 13, 0, 6.28); c.fill()
    elif kind == 'raise':   # 右手举剑向天（q: 0 下垂 → 1 高举）
        tube(c, [(-200, -700), (-215, -600), (-120, -560)], 62, robe, a); hand(c, -110, -560, 26, a)
        ex, ey = 270, -760 - 160 * q; hx, hy = 230 + 20 * q, -760 - 360 * q
        tube(c, [(200, -700), (ex, ey), (hx, hy)], 62, robe, a); hand(c, hx, hy, 28, a)
        ang = -1.9 - 0.3 * q
        sword(c, hx, hy, hx + math.cos(ang) * 620 * (0.4 + 0.6 * q), hy + math.sin(ang) * 620 * (0.4 + 0.6 * q), sword_lit, a, 16)
    elif kind == 'point':   # 右手前指
        tube(c, [(-200, -700), (-215, -600), (-120, -560)], 62, robe, a); hand(c, -110, -560, 26, a)
        hx = 200 + 300 * q
        tube(c, [(200, -700), (hx * 0.7 + 60, -740), (hx + 40, -760)], 58, robe, a); hand(c, hx + 60, -760, 26, a)
        line(c, [(hx + 80, -768), (hx + 120, -770)], 6, SKIN, a)
    elif kind == 'down':
        for sx in (-1, 1):
            tube(c, [(sx * 200, -700), (sx * 225, -560), (sx * 215, -440)], 62, robe, a); hand(c, sx * 215, -420, 26, a)
    elif kind == 'offer':   # 双手前捧托盘
        for sx in (-1, 1):
            tube(c, [(sx * 200, -700), (sx * 190, -590), (sx * 80, -580)], 62, robe, a)
        shape(c, [(-170, -600), (170, -600), (150, -575), (-150, -575)], (0.35, 0.20, 0.08), 3, LINE, a)
        hand(c, -80, -582, 24, a); hand(c, 80, -582, 24, a)
    elif kind == 'fist':    # 握拳于腰，怒立
        for sx in (-1, 1):
            tube(c, [(sx * 200, -700), (sx * 245, -610), (sx * 150, -580)], 62, robe, a); hand(c, sx * 140, -580, 28, a)

def general(c, x, y, s=1.0, t=0.0, hat='he', beard='full', cape_col=CAPE, cape_dark=CAPE_D, armor=True,
            arms_kind='rest', robe=ROBE, accent=CAPE, sword_lit=1.0, wind=1.0, p=1.0, a=1, age=0, rim=(1, 0.55, 0.2), face=1):
    c.save(); c.translate(x, y); c.scale(s * face, s)
    if rim: glow(c, 0, -620, 560, rim, 0.18 * a)
    if cape_col: cape(c, t, cape_col, cape_dark, wind, a)
    legs(c, a, armor)
    torso(c, a, armor, robe, accent)
    shape(c, [(-22, -800), (22, -800), (26, -770), (-26, -770)], SKIN, 3, LINE, a)
    arms(c, arms_kind, t, a, robe, sword_lit, p)
    head(c, t, hat, beard, age, a)
    c.restore()

def baiqi(c, x, y, s=1.0, t=0.0, arms_kind='rest', **k):
    general(c, x, y, s, t, 'he', 'full', arms_kind=arms_kind, **k)

def soldier(c, x, y, s=0.3, side='qin', t=0.0, spear=True, a=1, pose='stand', p=1.0, face=1):
    """小兵：线描，秦=灰甲红缨，赵=青甲"""
    body = (0.30, 0.28, 0.26) if side == 'qin' else ZHAO_C
    tas = CAPE if side == 'qin' else (0.85, 0.80, 0.70)
    c.save(); c.translate(x, y); c.scale(s * face, s)
    lw = 4.5
    if pose == 'kneel':
        c.translate(0, 120)
        shape(c, [(-60, -120), (60, -120), (70, -250), (-50, -250)], body, lw, LINE, a)
        tube(c, [(40, -230), (100, -170)], 40, body, a)
        shape(c, [(-36, -250), (40, -250), (36, -330), (-30, -330)], SKIN, lw, LINE, a)
        c.restore(); return
    if pose == 'lie':
        c.rotate(-1.45 * p)
    for sx in (-1, 1): tube(c, [(sx * 25, -260), (sx * 40, -10)], 40, (0.14, 0.11, 0.10), a)
    shape(c, [(-62, -480), (62, -480), (72, -260), (-72, -260)], body, lw, LINE, a)
    lamellar(c, -60, -460, 60, -280, 4, 4, a, 1.2)
    tube(c, [(-70, -460), (-90, -330)], 40, body, a)
    tube(c, [(70, -460), (110, -360), (120, -330)], 40, body, a)
    shape(c, [(-32, -490), (32, -490), (36, -560), (-36, -560)], SKIN, lw, LINE, a)
    shape(c, [(-42, -545), (-40, -600, 40, -600, 42, -545)], (0.15, 0.13, 0.12), lw, LINE, a)
    shape(c, [(0, -598), (-14, -640), (14, -640)], tas, 2.5, LINE, a)
    if spear:
        c.set_line_cap(1); c.set_source_rgba(*LINE, a); c.set_line_width(10); c.move_to(120, 20); c.line_to(120, -780); c.stroke()
        c.set_source_rgba(0.35, 0.22, 0.12, a); c.set_line_width(5); c.move_to(120, 20); c.line_to(120, -780); c.stroke()
        shape(c, [(120, -860), (104, -780), (136, -780)], STEEL, 3, LINE, a)
        shape(c, [(108, -770), (132, -770), (128, -740), (112, -740)], tas, 2, LINE, a)
    c.restore()
