# 线描威武武将：白起（秦将鹖冠、甲衣、红披风、拄剑）
import math, random
import cairocffi as cairo

GOLD = (0.88, 0.72, 0.42)
LINE = (0.96, 0.86, 0.62)      # 主描线：暖金白
INKF = (0.10, 0.08, 0.07)      # 甲片底色
ROBE = (0.20, 0.10, 0.08)
CAPE = (0.70, 0.08, 0.06)
CAPE_D = (0.42, 0.04, 0.03)
SKIN = (0.55, 0.40, 0.30)
STEEL = (0.92, 0.95, 1.0)

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

def glow(c, x, y, r, col, a):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
    c.set_source(g); c.arc(x, y, r, 0, 6.2832); c.fill()

def hatch(c, pts, a=1, gap=11, col=(0, 0, 0), alpha=0.35, ang=0.9):
    """暗面斜排线"""
    c.save(); P(c, pts); c.clip()
    xs = [q[-2] for q in pts]; ys = [q[-1] for q in pts]
    x0, x1, y0, y1 = min(xs) - 400, max(xs) + 400, min(ys), max(ys)
    c.set_source_rgba(*col, alpha * a); c.set_line_width(2.2)
    x = x0
    while x < x1:
        c.move_to(x, y1); c.line_to(x + (y1 - y0) * ang, y0); x += gap
    c.stroke(); c.restore()

def lamellar(c, x0, y0, x1, y1, rows, cols, a=1, lw=1.6, rivet=True):
    """甲片网格：横排错缝 + 铆钉点"""
    c.set_source_rgba(*GOLD, 0.75 * a); c.set_line_width(lw)
    h = (y1 - y0) / rows; w = (x1 - x0) / cols
    for r in range(rows + 1):
        c.move_to(x0, y0 + r * h); c.line_to(x1, y0 + r * h)
    c.stroke()
    for r in range(rows):
        off = (w / 2) if r % 2 else 0
        for k in range(cols + 1):
            x = x0 + k * w + off
            if x0 < x < x1:
                c.move_to(x, y0 + r * h); c.line_to(x, y0 + (r + 1) * h)
        c.stroke()
        if rivet:
            for k in range(cols):
                x = x0 + (k + 0.5) * w + off
                if x0 < x < x1:
                    c.arc(x, y0 + r * h + h * 0.3, 2.2, 0, 6.28); c.fill()

def cape(c, t, wind=1.0, a=1):
    w = math.sin(t * 2.6) * 30 * wind; w2 = math.sin(t * 2.6 + 1.2) * 40 * wind
    pts = [(-150, -775), (-260, -640, -420 - w, -380, -560 - w2, -90), (-430 - w2 * 0.6, -60),
           (-330 - w * 0.5, -40), (-240, -30, -170, -200, -100, -300), (120, -760)]
    shape(c, pts, CAPE, 5, LINE, a)
    hatch(c, pts[:3] + [(-430 - w2 * 0.6, -60), (-300, -500)], a, gap=10, col=(0.25, 0, 0), alpha=0.45)
    # 褶皱
    for k, (x0, x1) in enumerate([(-150, -470), (-130, -380), (-110, -300)]):
        line(c, [(x0, -720), (x0 - 60, -520, x1 - w * 0.6, -300, x1 - w2 * 0.8, -100)], 2.4, (1, 0.62, 0.5), 0.7 * a)
    # 披风右侧露出一角
    shape(c, [(120, -760), (200, -600, 260 + w * 0.3, -420, 300 + w * 0.5, -300), (230, -320), (150, -560)], CAPE_D, 4, LINE, a)

def head(c, t, a=1):
    sw = math.sin(t * 3) * 4
    # 鹖冠双尾：向两侧后方卷起（不是竖直的耳朵）
    for sx in (-1, 1):
        shape(c, [(sx * 18, -1000), (sx * 50, -1040, sx * (95 + sw), -1060, sx * (118 + sw), -1035),
                  (sx * (100 + sw), -1048, sx * 70, -1030, sx * 46, -990)], (0.20, 0.14, 0.10), 3.5, LINE, a)
        line(c, [(sx * 40, -1010), (sx * (98 + sw), -1044)], 1.6, GOLD, 0.8 * a)
    # 冠体
    shape(c, [(-62, -925), (-66, -975), (-40, -1006), (40, -1006), (66, -975), (62, -925)], INKF, 4.5, LINE, a)
    line(c, [(-64, -955), (64, -955)], 2.4, GOLD, a)
    for k in range(-2, 3): c.set_source_rgba(*GOLD, a); c.arc(k * 22, -940, 3, 0, 6.28); c.fill()
    # 鬓发
    shape(c, [(-62, -925), (-66, -880), (-58, -850), (-52, -905)], (0.06, 0.05, 0.04), 2.5, LINE, a)
    shape(c, [(62, -925), (66, -880), (58, -850), (52, -905)], (0.06, 0.05, 0.04), 2.5, LINE, a)
    # 方脸，宽下颌
    face = [(-56, -925), (-60, -870, -58, -835, -44, -808), (-20, -786), (20, -786), (44, -808, 58, -835, 60, -870), (56, -925)]
    shape(c, face, SKIN, 4.5, LINE, a)
    hatch(c, [(18, -925), (56, -925), (60, -870), (44, -808), (20, -786), (24, -840)], a, gap=8, alpha=0.3)
    line(c, [(-46, -858), (-36, -842)], 1.8, (0.25, 0.12, 0.07), a)   # 颧骨
    line(c, [(46, -858), (36, -842)], 1.8, (0.25, 0.12, 0.07), a)
    # 浓剑眉，压低成倒八字
    shape(c, [(-50, -902), (-30, -900), (-8, -886), (-12, -880), (-32, -890), (-50, -893)], (0.05, 0.04, 0.03), 1.5, LINE, a)
    shape(c, [(50, -902), (30, -900), (8, -886), (12, -880), (32, -890), (50, -893)], (0.05, 0.04, 0.03), 1.5, LINE, a)
    line(c, [(-4, -892), (-2, -878)], 1.6, (0.25, 0.12, 0.07), a); line(c, [(4, -892), (2, -878)], 1.6, (0.25, 0.12, 0.07), a)  # 川字纹
    # 眼：锐利
    for sx in (-1, 1):
        shape(c, [(sx * 40, -872), (sx * 26, -880), (sx * 12, -872), (sx * 26, -868)], (0.95, 0.88, 0.75), 1.6, (0.05, 0.03, 0.02), a)
        c.set_source_rgba(0.05, 0.03, 0.02, a); c.arc(sx * 24, -873, 4, 0, 6.28); c.fill()
        c.set_source_rgba(1, 1, 1, a); c.arc(sx * 23, -875, 1.3, 0, 6.28); c.fill()
    # 鼻
    line(c, [(-2, -870), (-8, -840), (0, -834), (8, -838)], 2.4, (0.18, 0.09, 0.05), a)
    # 浓髯：八字胡 + 满腮短须 + 下巴长须
    shape(c, [(-58, -850), (-56, -820, -40, -790, -20, -778), (0, -770), (20, -778), (40, -790, 56, -820, 58, -850),
              (46, -830), (20, -812), (0, -816), (-20, -812), (-46, -830)], (0.07, 0.05, 0.04), 2.4, LINE, a)
    shape(c, [(-22, -790), (-18, -750, -10, -725, 0, -700), (10, -725, 18, -750, 22, -790)], (0.07, 0.05, 0.04), 2.4, LINE, a)
    for k in range(-2, 3): line(c, [(k * 7, -785), (k * 5, -722)], 1.2, GOLD, 0.6 * a)
    shape(c, [(-2, -830), (-24, -828, -44, -822, -54, -800), (-30, -816, -14, -820, 0, -822),
              (14, -820, 30, -816, 54, -800), (44, -822, 24, -828, 2, -830)], (0.05, 0.04, 0.03), 2, LINE, a)
    line(c, [(-14, -812), (14, -812)], 2.2, (0.35, 0.1, 0.06), a)    # 抿嘴
    # 冠缨
    line(c, [(-58, -925), (-64, -860, -54, -800, -40, -790)], 2, GOLD, 0.8 * a)
    line(c, [(58, -925), (64, -860, 54, -800, 40, -790)], 2, GOLD, 0.8 * a)

def body(c, t, a=1, sword_lit=1.0):
    c.save()
    # 腿与靴（开立，粗壮）
    shape(c, [(-95, -330), (-115, -170), (-140, -50), (-190, -12), (-190, 0), (-70, 0), (-66, -50), (-45, -170), (-22, -330)], (0.13, 0.10, 0.09), 4.5, LINE, a)
    shape(c, [(95, -330), (115, -170), (140, -50), (190, -12), (190, 0), (70, 0), (66, -50), (45, -170), (22, -330)], (0.13, 0.10, 0.09), 4.5, LINE, a)
    for sx in (-1, 1):
        line(c, [(sx * 64, -70), (sx * 142, -70)], 2.5, GOLD, a)
        for yy in (-130, -180, -230): line(c, [(sx * (50 + (yy + 330) * 0.05), yy), (sx * (118 - (yy + 170) * 0.1), yy - 8)], 1.6, GOLD, 0.6 * a)
        # 暗面排线
    hatch(c, [(95, -330), (115, -170), (140, -50), (190, -12), (110, -12), (66, -50), (60, -170), (50, -330)], a)
    c.save(); c.scale(1.18, 1)
    # 下摆长袍（双层）
    shape(c, [(-115, -560), (-150, -400), (-165, -290), (-80, -270), (0, -282), (80, -270), (165, -290), (150, -400), (115, -560)], ROBE, 4.5, LINE, a)
    line(c, [(-60, -540), (-80, -400, -92, -330, -100, -280)], 2, GOLD, 0.6 * a)
    line(c, [(60, -540), (80, -400, 92, -330, 100, -280)], 2, GOLD, 0.6 * a)
    hatch(c, [(40, -560), (115, -560), (150, -400), (165, -290), (60, -275)], a)
    # 甲裙（下缘甲片）
    shape(c, [(-112, -575), (-130, -420), (0, -400), (130, -420), (112, -575)], INKF, 4.5, LINE, a)
    lamellar(c, -122, -570, 122, -412, 4, 9, a)
    # 胸甲：前胸尖角下摆（秦将军俑式）
    shape(c, [(-110, -755), (-125, -640), (-112, -560), (0, -520), (112, -560), (125, -640), (110, -755), (40, -770), (-40, -770)], INKF, 5, LINE, a)
    c.save(); P(c, [(-110, -755), (-125, -640), (-112, -560), (0, -520), (112, -560), (125, -640), (110, -755)]); c.clip()
    lamellar(c, -125, -700, 125, -520, 6, 10, a)
    c.restore()
    hatch(c, [(40, -770), (110, -755), (125, -640), (112, -560), (40, -530)], a)
    # 胸前护心彩结（将军俑胸前花结）
    for sx in (-1, 1):
        shape(c, [(sx * 62, -735), (sx * 86, -722), (sx * 72, -700), (sx * 50, -712)], CAPE, 2.5, LINE, a)
    shape(c, [(-30, -770), (0, -740), (30, -770), (0, -790)], (0.5, 0.06, 0.04), 3, LINE, a)   # 领巾
    line(c, [(-110, -700), (110, -700)], 3, LINE, a)
    # 腰带 + 带钩
    shape(c, [(-120, -600), (120, -600), (118, -575), (-118, -575)], (0.30, 0.18, 0.08), 3, LINE, a)
    shape(c, [(-14, -598), (14, -598), (10, -578), (-10, -578)], GOLD, 2, LINE, a)
    # 披膊（肩甲，层叠）
    for sx in (-1, 1):
        for k in range(4):
            y = -772 + k * 38; x0 = sx * (96 + k * 4); x1 = sx * (190 + k * 12)
            shape(c, [(x0, y), (x1, y + 6), (x1 + sx * 8, y + 46), (x0, y + 38)], INKF, 3.5, LINE, a)
            c.set_source_rgba(*GOLD, 0.8 * a); c.arc((x0 + x1) / 2, y + 20, 2.4, 0, 6.28); c.fill()
    # 手臂（袖）向中间收，双手叠在剑首
    for sx in (-1, 1):
        shape(c, [(sx * 120, -640), (sx * 180, -640), (sx * 170, -560), (sx * 90, -500), (sx * 40, -500), (sx * 50, -540), (sx * 120, -580)], ROBE, 4.5, LINE, a)
        line(c, [(sx * 160, -620), (sx * 110, -545)], 1.8, GOLD, 0.6 * a)
    c.restore()
    # 剑：剑首在双手下，剑身插地，发光
    gx = 0
    if sword_lit > 0:
        glow(c, gx, -260, 300, (0.7, 0.82, 1.0), 0.35 * sword_lit)
    c.set_source_rgba(*STEEL, 0.6 + 0.4 * sword_lit); c.set_line_width(14); c.move_to(gx, -470); c.line_to(gx, -10); c.stroke()
    c.set_source_rgba(1, 1, 1, sword_lit); c.set_line_width(4); c.move_to(gx, -460); c.line_to(gx, -20); c.stroke()
    shape(c, [(gx - 48, -480), (gx + 48, -480), (gx + 40, -462), (gx - 40, -462)], (0.45, 0.32, 0.12), 3, LINE, a)   # 剑格
    shape(c, [(gx - 10, -530), (gx + 10, -530), (gx + 10, -480), (gx - 10, -480)], (0.2, 0.12, 0.06), 2.5, LINE, a)   # 剑柄
    # 双手（交叠握剑首）
    shape(c, [(-46, -540), (-6, -548), (8, -520), (-40, -500)], SKIN, 3.5, LINE, a)
    shape(c, [(46, -545), (6, -552), (-8, -522), (40, -505)], SKIN, 3.5, LINE, a)
    for k in range(3):
        line(c, [(-30 + k * 9, -540), (-26 + k * 9, -510)], 1.4, (0.2, 0.1, 0.05), a)
    c.set_source_rgba(*GOLD, a); c.arc(gx, -548, 13, 0, 6.28); c.fill()
    c.restore()
    # 脖子
    shape(c, [(-20, -800), (20, -800), (24, -770), (-24, -770)], SKIN, 3, LINE, a)

def baiqi_line(c, x, y, s=1.0, t=0.0, a=1, sword_lit=1.0, wind=1.0, rim=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    if rim: glow(c, 0, -620, 520, (1, 0.55, 0.2), 0.18 * a)
    cape(c, t, wind, a)
    body(c, t, a, sword_lit)
    head(c, t, a)
    c.restore()

if __name__ == '__main__':
    import sys
    W, H = 1920, 1080
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.06, 0.04, 0.03); g.add_color_stop_rgb(1, 0.24, 0.10, 0.05)
    c.set_source(g); c.paint()
    glow(c, 960, 640, 900, (0.95, 0.35, 0.1), 0.25)
    rnd = random.Random(2)
    # 远山 + 战旗
    c.set_source_rgb(0.12, 0.06, 0.04); c.move_to(0, 900)
    for i in range(13): c.line_to(i * 160 + 80, 760 - rnd.uniform(0, 150)); c.line_to(i * 160 + 160, 880)
    c.line_to(W, H); c.line_to(0, H); c.fill()
    c.set_source_rgb(0.04, 0.03, 0.02); c.rectangle(0, 990, W, 90); c.fill()
    baiqi_line(c, 960, 1010, 0.86, t=0.6)
    for i in range(80):
        x = rnd.uniform(0, W); y = rnd.uniform(200, 1080); r = rnd.uniform(1.5, 4)
        c.set_source_rgba(1, rnd.uniform(0.4, 0.8), 0.2, rnd.uniform(0.3, 0.9)); c.arc(x, y, r, 0, 6.28); c.fill()
    c.select_font_face("Noto Serif CJK SC", 0, 1)
    c.set_font_size(150); c.set_source_rgb(*LINE); c.move_to(1330, 470); c.show_text("白起")
    c.set_font_size(44); c.set_source_rgb(*GOLD); c.move_to(1340, 550); c.show_text("秦 · 武安君")
    c.set_font_size(30); c.set_source_rgba(0.8, 0.75, 0.68, 1); c.move_to(1340, 610); c.show_text("鹖冠 · 甲衣 · 拄剑")
    surf.write_to_png(sys.argv[1] if len(sys.argv) > 1 else 'baiqi_hero.png')
