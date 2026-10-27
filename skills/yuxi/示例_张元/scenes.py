from kit import *
import math, random

CNT = [None]
def cnt(c, n, lt=99):
    CNT[0] = n
def draw_cnt(c, n):
    text(c, "宋军阵亡", 96, 950, 34, (0.78, 0.72, 0.64), 1, shadow=False)
    w = text(c, f"{n:,}", 96, 1040, 84, (0.95, 0.30, 0.24), 1)
    text(c, "人", 96 + w + 10, 1036, 38, (0.9, 0.85, 0.78), 1, shadow=False)

def night(c, lt, col=((0.02, 0.03, 0.05), (0.08, 0.07, 0.09))):
    vgrad(c, 0, H, [(0, col[0]), (1, col[1])])

def desk(c, x, y, w=420):
    c.set_source_rgb(*INK); c.rectangle(x - w / 2, y, w, 20); c.fill(); c.rectangle(x - w / 2 + 20, y + 20, 16, 840 - y); c.fill(); c.rectangle(x + w / 2 - 36, y + 20, 16, 840 - y); c.fill()

def paper(c, x, y, s=1, a=1, mark=None):
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, 0, 180, (1, 0.9, 0.7), 0.35 * a)
    c.set_source_rgba(0.92, 0.88, 0.78, a); c.rectangle(-70, -90, 140, 180); c.fill()
    c.set_source_rgba(0.3, 0.25, 0.2, 0.6 * a); c.set_line_width(3)
    for i in range(6): c.move_to(-50 + i * 20, -70); c.line_to(-50 + i * 20, 70)
    c.stroke()
    if mark == 'x':
        c.set_source_rgba(0.85, 0.12, 0.08, a); c.set_line_width(14); c.move_to(-60, -70); c.line_to(60, 70); c.move_to(60, -70); c.line_to(-60, 70); c.stroke()
    c.restore()

def S_hook(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.02, 0.02)), (1, (0.08, 0.05, 0.03))])
    glow(c, W / 2, 560, 600, (1, 0.7, 0.4), 0.25)
    paper(c, 1180, 560, 1.4, mark='x' if lt > 0.8 else None)
    sil(c, 820, 900, 1.5, hat='song', pose='stand', face=1)
    dust(c, lt, 40, a=0.4)

def S_hook2(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.05, 0.03, 0.03)), (1, (0.16, 0.10, 0.06))])
    c.set_source_rgb(*INK); c.rectangle(0, 860, W, 220); c.fill()
    k = ease((p - 0.15) / 0.6)
    banner(c, 260, 860, "宋", (0.55, 0.12, 0.10), lt, h=420)
    banner(c, 1660, 860, "夏", (0.15, 0.30, 0.38), lt, h=420, a=k)
    x = lerp(520, 1360, k)
    sil(c, x, 860, 1.3, hat='song' if k < 0.5 else 'xia', pose='stand', face=1)

def S_hook3(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.10, 0.03, 0.02)), (1, (0.30, 0.08, 0.03))])
    mountains(c, lt, cols=[(0.18, 0.06, 0.04), (0.12, 0.04, 0.03), (0.06, 0.02, 0.02)])
    rnd = random.Random(4)
    for i in range(26):
        x = 80 + i * 70 + rnd.uniform(-20, 20); k = ease((lt - 0.4 - i * 0.05) / 0.4)
        glow(c, x, 960, 90, (1, 0.5, 0.2), 0.25)
        sil(c, x, 1010, 0.55, hat='helm', pose='lie' if k > 0 else 'stand', p=k, face=1 if i % 2 else -1)
    redflash(c, 0.2)

def S_title(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.02, 0.02)), (1, (0.08, 0.05, 0.03))])
    glow(c, W / 2, 820, 700, (0.9, 0.6, 0.3), 0.18)
    sil(c, W / 2, 1000, 1.3, hat='song', pose='stand', a=0.95)
    a = ease(lt / 0.4)
    text(c, "假 如 你 是 张 元", W / 2, 300, 34, GOLD, a, 'c')
    text(c, "一个落榜书生，", W / 2, 410, 80, (1, 0.96, 0.9), a, 'c')
    text(c, "凭什么改了大宋的考试规矩？", W / 2, 520, 80, (0.95, 0.30, 0.24), ease((lt - 0.5) / 0.4), 'c')

def S_chenqiao(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.03, 0.03, 0.05)), (1, (0.12, 0.08, 0.06))])
    stars(c, lt)
    c.set_source_rgb(*INK); c.rectangle(0, 880, W, 200); c.fill()
    for x in (300, 1620): campfire = glow(c, x, 860, 160, (1, 0.5, 0.2), 0.4)
    k = ease((p - 0.3) / 0.3)
    glow(c, W / 2, 640, 260, GOLD, 0.6 * k)
    sil(c, W / 2, 880, 1.4, hat='helm', pose='stand', robe=mix((0.02, 0.02, 0.02), (0.85, 0.65, 0.20), k))
    for i, x in enumerate((420, 560, 700, 1220, 1360, 1500)):
        sil(c, x, 880, 1.0, hat='helm', pose='kneel' if k > 0.5 else 'stand', face=1 if x < 960 else -1)

def S_beijiu(c, lt, d, p):
    palace(c, lt, tone=(0.12, 0.06, 0.04))
    c.set_source_rgb(*INK); c.rectangle(1360, 720, 420, 120); c.fill()
    sil(c, 1560, 720, 1.1, hat='song', pose='offer', p=1, face=-1, robe=(0.06, 0.04, 0.02))
    k = ease((p - 0.35) / 0.3)
    for i, x in enumerate((520, 760, 1000)):
        sil(c, x, 840, 1.05, hat='helm', pose='bow' if k > 0.5 else 'stand', p=k)
        c.save(); c.translate(x - 60, lerp(600, 830, k)); c.rotate(lerp(-0.2, 1.4, k))
        c.set_source_rgba(0.6, 0.6, 0.65, 0.9); c.rectangle(-5, -110, 10, 220); c.fill(); c.restore()
    glow(c, 1300, 600, 90, GOLD, 0.4)

def S_fear(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.06, 0.04, 0.03)), (1, (0.16, 0.10, 0.06))])
    glow(c, 700, 560, 380, (1, 0.8, 0.5), 0.35)
    sil(c, 700, 900, 1.4, hat='song', pose='stand')
    paper(c, 880, 620, 0.6)
    c.set_source_rgba(0.04, 0.03, 0.03, 1); c.rectangle(1150, 380, 520, 520); c.fill()
    c.set_source_rgba(0.55, 0.45, 0.35, 1); c.set_line_width(8)
    for i in range(6): c.move_to(1170 + i * 95, 380); c.line_to(1170 + i * 95, 900)
    c.stroke()
    sil(c, 1410, 880, 1.1, hat='helm', pose='stand', a=0.9)

def S_chen(c, lt, d, p):
    palace(c, lt, tone=(0.14, 0.06, 0.04))
    c.set_source_rgb(*INK); c.rectangle(1360, 760, 420, 80); c.fill()
    sil(c, 1560, 760, 1.15, hat='song', pose='sit', face=-1, robe=(0.06, 0.04, 0.03))
    sil(c, 800, 840, 1.25, hat='song', pose='bow', p=1)
    k = ease((p - 0.4) / 0.3)
    # 节钺
    c.save(); c.translate(1100, 600); c.set_source_rgba(*GOLD, k); c.set_line_width(8); c.move_to(0, 240); c.line_to(0, -60); c.stroke()
    poly(c, [(-30, -60), (30, -60), (0, -130)], GOLD, k); c.restore()
    glow(c, 1100, 520, 160, GOLD, 0.3 * k)

def S_mom(c, lt, d, p):
    palace(c, lt, tone=(0.10, 0.06, 0.04), pillars=(200, 1720), candles=((960, 760),))
    sil(c, 760, 840, 1.25, hat='song', pose='cry', p=1, face=1)
    k = 0.5 + 0.5 * math.sin(lt * 9)
    sil(c, 1150, 840, 1.25, hat='lady', pose='raise', p=1, face=-1)
    c.save(); c.translate(1150 - 55, 840 - 330); c.rotate(-0.9 + k * 1.2)
    c.set_source_rgb(*INK); c.rectangle(-8, -220, 16, 240); c.fill(); c.restore()
    if k > 0.95: redflash(c, 0.3)

def S_rule(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.06, 0.04, 0.03)), (1, (0.16, 0.10, 0.06))])
    glow(c, W / 2, 500, 500, (1, 0.8, 0.5), 0.3)
    # 天平式两条路：左书卷亮，右刀暗
    paper(c, 640, 560, 1.3)
    c.save(); c.translate(1280, 560); c.set_source_rgba(0.5, 0.5, 0.55, 0.35); c.rotate(0.6); c.rectangle(-8, -200, 16, 400); c.fill(); c.restore()
    c.set_source_rgba(0.85, 0.12, 0.08, 0.8); c.set_line_width(10); c.move_to(1180, 460); c.line_to(1380, 660); c.stroke()
    crowd(c, 1000, 9, 0.6, 300, 1000, 'bow', 'song')

def S_you(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.03, 0.03, 0.05)), (1, (0.10, 0.08, 0.08))])
    stars(c, lt); moon(c, 1550, 220, 50)
    roofhall(c, 600, 860, 900, 360, (0.05, 0.04, 0.05))
    c.set_source_rgb(0.05, 0.04, 0.04); c.rectangle(0, 860, W, 220); c.fill()
    candle(c, 1250, 840, lt, h=60)
    desk(c, 1100, 760, 360)
    sil(c, 960, 860, 1.3, hat='song', pose='sit', face=1)
    paper(c, 1120, 720, 0.4)
    yrs = int(lerp(1, 6, ease(p)))
    text(c, "第 %d 次赶考" % yrs, 1560, 600, 52, (0.9, 0.85, 0.78), 0.85, 'r')

def S_pass(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.10, 0.06, 0.04)), (1, (0.30, 0.16, 0.08))])
    c.set_source_rgb(*INK); citywall(c, 840, (0.07, 0.04, 0.03), 260)
    # 榜
    c.set_source_rgba(0.85, 0.70, 0.45, 1); c.rectangle(560, 260, 800, 420); c.fill()
    c.set_source_rgba(0.2, 0.12, 0.06, 0.7)
    for i in range(12):
        for j in range(8): c.rectangle(600 + i * 62, 300 + j * 46, 40, 26); c.fill()
    k = ease((p - 0.3) / 0.2)
    c.set_source_rgba(0.85, 0.12, 0.08, k); c.set_line_width(6); c.arc(600 + 7 * 62 + 20, 300 + 3 * 46 + 13, 40, 0, 6.28); c.stroke()
    crowd(c, 1040, 10, 0.7, 300, 1600, 'stand', 'song')

def S_fail(c, lt, d, p):
    palace(c, lt, tone=(0.16, 0.05, 0.03))
    c.set_source_rgb(*INK); c.rectangle(1360, 720, 420, 120); c.fill()
    sil(c, 1560, 720, 1.1, hat='song', pose='sit', face=-1, robe=(0.06, 0.03, 0.02))
    for i, x in enumerate((520, 700, 880, 1060)):
        out = (i == 3) and p > 0.55
        sil(c, x, 840, 1.0, hat='song', pose='kneel', a=0.35 if out else 1)
    if p > 0.55:
        k = ease((p - 0.55) / 0.15)
        paper(c, 1060, 520, 0.9 * k, a=k, mark='x')
    if 0.55 < p < 0.63: redflash(c, 0.5)

def S_home(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.30, 0.22, 0.16)), (0.7, (0.55, 0.40, 0.26)), (1, (0.25, 0.18, 0.12))])
    c.set_source_rgb(*INK); c.rectangle(0, 880, W, 200); c.fill()
    roofhall(c, 1500, 880, 600, 300, INK)
    sil(c, 900, 880, 1.25, hat='song', pose='cry', p=0.6)
    for i, x in enumerate((420, 560, 1260, 1380)):
        sil(c, x, 880, 1.05, hat='bun', pose='point', face=1 if x < 900 else -1)
    for i in range(5):
        x = 960 + math.sin(lt * 2 + i) * 400; y = 560 + i * 30
        text(c, "哈", x, y, 40 + i * 4, (0.25, 0.12, 0.08), 0.8 * ease((lt - i * 0.3) / 0.3), 'c', shadow=False)

def S_border(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.12, 0.10, 0.10)), (0.7, (0.40, 0.30, 0.22)), (1, (0.10, 0.08, 0.06))])
    mountains(c, lt, cols=[(0.22, 0.17, 0.13), (0.15, 0.11, 0.09), (0.08, 0.06, 0.05)])
    citywall(c, 900, (0.06, 0.05, 0.04), 160)
    banner(c, 1500, 740, "宋", (0.55, 0.12, 0.10), lt, h=300)
    k = ease((p - 0.5) / 0.3)
    c.set_source_rgb(0.25, 0.12, 0.05); c.rectangle(1000, 760 - 0, 160 * (1 - k) + 6, 140); c.fill()  # 城门渐关
    sil(c, 760, 1040, 1.2, hat='song', pose='offer', p=1)

def S_tavern(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.10, 0.06, 0.03)), (1, (0.25, 0.14, 0.06))])
    glow(c, 600, 600, 500, (1, 0.6, 0.3), 0.3)
    c.set_source_rgba(0.55, 0.45, 0.32, 1); c.rectangle(1000, 300, 700, 560); c.fill()
    s = "张元吴昊来此饮"; n = int(len(s) * ease((p - 0.15) / 0.5) + 0.999)
    for i, ch in enumerate(s[:n]):
        text(c, ch, 1100 + (i // 4) * 220 + 100 - (i // 4) * 0, 340 + (i % 4) * 120 if i < 4 else 340 + (i - 4) * 120, 96, (0.08, 0.05, 0.03), 1, 'c', shadow=False) if False else None
    for i, ch in enumerate(s[:n]):
        col_ = 1 - (i // 4); row = i % 4
        text(c, ch, 1220 + col_ * 260, 440 + row * 120, 100, (0.08, 0.05, 0.03), 1, 'c', shadow=False)
    sil(c, 900, 900, 1.3, hat='song', pose='raise', p=0.7)
    c.set_source_rgb(*INK); c.rectangle(0, 900, W, 200); c.fill()
    for x in (300, 460): sil(c, x, 900, 1.0, hat='bun', pose='sit', face=1)

def S_caught(c, lt, d, p):
    palace(c, lt, tone=(0.10, 0.08, 0.06))
    banner(c, 1700, 840, "夏", (0.15, 0.30, 0.38), lt, h=480)
    c.set_source_rgb(*INK); c.rectangle(1300, 720, 380, 120); c.fill()
    sil(c, 1480, 720, 1.15, hat='xia', pose='sit', face=-1)
    k = ease(p / 0.6)
    x = lerp(300, 820, k)
    sil(c, x, 840, 1.15, hat='song', pose='kneel' if k >= 1 else 'stand')
    for dx in (-160, 160): sil(c, x + dx, 840, 1.1, hat='xia', pose='stand', face=1)

def S_answer(c, lt, d, p):
    palace(c, lt, tone=(0.10, 0.08, 0.06))
    banner(c, 1700, 840, "夏", (0.15, 0.30, 0.38), lt, h=480)
    c.set_source_rgb(*INK); c.rectangle(1300, 720, 380, 120); c.fill()
    sil(c, 1480, 720, 1.15, hat='xia', pose='sit', face=-1)
    sil(c, 820, 840, 1.25, hat='song', pose='point', face=1)
    a = ease((p - 0.4) / 0.2)
    for i, (ch, col) in enumerate((("李", (0.9, 0.8, 0.6)), ("赵", (0.9, 0.8, 0.6)))):
        text(c, ch, 1150 + i * 140, 520, 90, col, a * 0.85, 'c')
    if a > 0:
        c.set_source_rgba(0.95, 0.3, 0.24, a); c.set_line_width(5); c.move_to(1100, 480); c.line_to(1340, 480); c.stroke()

def S_hired(c, lt, d, p):
    palace(c, lt, tone=(0.12, 0.08, 0.05))
    banner(c, 200, 840, "夏", (0.15, 0.30, 0.38), lt, h=480); banner(c, 1700, 840, "夏", (0.15, 0.30, 0.38), lt, h=480)
    sil(c, 1250, 840, 1.15, hat='xia', pose='offer', p=1, face=-1)
    k = ease((p - 0.3) / 0.3)
    sil(c, 800, 840, 1.25, hat='song' if k < 0.5 else 'xia', pose='bow', p=0.6)
    glow(c, 1000, 600, 220, GOLD, 0.5 * k)
    c.set_source_rgba(*GOLD, k); rr(c, 960, 560, 90, 60, 8); c.fill()

def S_map(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.12, 0.10, 0.08)), (1, (0.22, 0.17, 0.12))])
    # 示意地图：宋夏交界
    c.set_source_rgba(0.30, 0.24, 0.17, 1); c.rectangle(260, 300, 1400, 700); c.fill()
    c.set_source_rgba(0.75, 0.62, 0.40, 0.6); c.set_line_width(4); c.set_dash([14, 10])
    c.move_to(260, 580); c.curve_to(700, 480, 1100, 720, 1660, 600); c.stroke(); c.set_dash([])
    text(c, "西 夏", 760, 420, 64, (0.6, 0.8, 0.85), 0.9, 'c'); text(c, "宋", 1200, 860, 72, (0.9, 0.5, 0.4), 0.9, 'c')
    for i, (x, y, nm) in enumerate(((500, 660, "延州"), (900, 720, "镇戎军"), (1300, 740, "渭州"))):
        c.set_source_rgba(0.95, 0.9, 0.8, 1); c.rectangle(x - 14, y - 14, 28, 28); c.fill(); text(c, nm, x, y + 64, 42, (0.95, 0.9, 0.8), 1, 'c')
        k = ease((p - 0.2 - i * 0.2) / 0.2)
        if k > 0:
            c.set_source_rgba(0.95, 0.3, 0.24, k); c.set_line_width(8); c.move_to(x, 420); c.line_to(x, lerp(420, y - 30, k)); c.stroke()
            poly(c, [(x - 18, lerp(420, y - 30, k) - 10), (x + 18, lerp(420, y - 30, k) - 10), (x, lerp(420, y - 30, k) + 16)], (0.95, 0.3, 0.24), k)
    text(c, "画面为示意", 1660, 1010, 22, (0.7, 0.65, 0.58), 0.8, 'r', shadow=False)

def S_split(c, lt, d, p):
    palace(c, lt, tone=(0.12, 0.06, 0.04), pillars=(960,), lattice=False)
    sil(c, 640, 840, 1.25, hat='song', pose='point', face=1)
    sil(c, 1280, 840, 1.25, hat='song', pose='stand', face=-1)
    text(c, "韩琦", 640, 930, 44, (0.9, 0.85, 0.78), 1, 'c'); text(c, "范仲淹", 1280, 930, 44, (0.9, 0.85, 0.78), 1, 'c')
    text(c, "攻", 640, 420, 110, (0.95, 0.30, 0.24), ease(p / 0.3), 'c'); text(c, "守", 1280, 420, 110, GOLD, ease((p - 0.3) / 0.3), 'c')

def S_order(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.15, 0.12, 0.10)), (0.7, (0.50, 0.38, 0.25)), (1, (0.12, 0.09, 0.07))])
    mountains(c, lt, cols=[(0.25, 0.19, 0.14), (0.16, 0.12, 0.09), (0.08, 0.06, 0.05)])
    for i in range(6):
        x = lerp(-300, 1900, ((p * 0.6) + i / 6) % 1)
        horse(c, x, 1000, 0.65, lt, rider='helm')
    banner(c, lerp(200, 900, p), 1000, "任", (0.55, 0.12, 0.10), lt, h=420)

def S_lure(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.15, 0.12, 0.10)), (0.7, (0.45, 0.33, 0.22)), (1, (0.12, 0.09, 0.07))])
    # 峡谷两侧山壁
    poly(c, [(0, 200), (520, 380), (720, 1080), (0, 1080)], (0.08, 0.06, 0.05)); poly(c, [(W, 200), (1400, 380), (1200, 1080), (W, 1080)], (0.08, 0.06, 0.05))
    c.set_source_rgba(0.75, 0.6, 0.38, 0.25); c.set_line_width(3); c.move_to(520, 380); c.line_to(720, 1080); c.move_to(1400, 380); c.line_to(1200, 1080); c.stroke()
    for i in range(4):
        x = 960 + math.sin(i) * 60; y = lerp(1100, 500, ((p * 0.8) + i / 4) % 1); sc = lerp(0.6, 0.25, (y - 500) / -600 + 1)
        horse(c, x, y, 0.3 + 0.4 * (y - 500) / 600, lt, rider='helm')
    for i in range(3):
        c.set_source_rgba(0.35, 0.25, 0.15, 1); c.rectangle(820 + i * 120, 600 + i * 50, 40, 26); c.fill()

def S_boxes(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.15, 0.12, 0.10)), (0.7, (0.45, 0.33, 0.22)), (1, (0.12, 0.09, 0.07))])
    c.set_source_rgb(0.10, 0.08, 0.06); c.rectangle(0, 860, W, 220); c.fill()
    for i, x in enumerate((760, 960, 1160)):
        c.set_source_rgba(0.62, 0.55, 0.45, 1); rr(c, x - 60, 780, 120, 80, 10); c.fill()
    sil(c, 600, 860, 1.15, hat='helm', pose='offer', p=1)
    sil(c, 1360, 860, 1.15, hat='helm', pose='point', face=-1)
    k = ease((p - 0.55) / 0.4)
    rnd = random.Random(8)
    for i in range(100):
        if k <= 0: break
        sx = rnd.choice((760, 960, 1160)); ang = rnd.uniform(-2.6, -0.5); r = k * rnd.uniform(150, 520)
        x = sx + math.cos(ang) * r; y = 800 + math.sin(ang) * r
        f = math.sin(lt * 20 + i) * 10
        c.set_source_rgba(0.92, 0.92, 0.9, 1); c.save(); c.translate(x, y); c.scale(1, 0.6); c.arc(0, 0, 12, 0, 6.28); c.restore(); c.fill()
        c.set_line_width(4); c.move_to(x - 22, y - f); c.line_to(x, y); c.line_to(x + 22, y - f); c.stroke()

def S_ambush(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.12, 0.03, 0.02)), (1, (0.35, 0.10, 0.04))])
    mountains(c, lt, cols=[(0.20, 0.07, 0.04), (0.13, 0.05, 0.03), (0.07, 0.03, 0.02)])
    k = ease(p / 0.4)
    for i in range(12):
        side = -1 if i % 2 else 1
        x = (W / 2 + side * lerp(1000, 300 + (i // 2) * 60, k)); y = 520 + (i // 2) * 80
        horse(c, x, y + 300, 0.45, lt, rider='xia')
    for i in range(10):
        kk = ease((p - 0.35 - i * 0.03) / 0.15)
        sil(c, 700 + i * 55, 1020, 0.6, hat='helm', pose='lie' if kk > 0 else 'stand', p=kk)
    if 0.35 < p < 0.45: redflash(c, 0.5)
    n = int(10300 * ease((p - 0.4) / 0.45))
    if p > 0.4: cnt(c, n)

def S_poem(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.08, 0.06, 0.05)), (1, (0.18, 0.13, 0.09))])
    c.set_source_rgba(0.62, 0.55, 0.45, 1); c.rectangle(600, 330, 1060, 640); c.fill()
    lines = ["夏竦何曾耸", "韩琦未足奇", "满川龙虎辇", "犹自说兵机"]
    for i, ln in enumerate(lines):
        for j, ch in enumerate(ln):
            a = ease((p * 1.4 - (i * 5 + j) * 0.03) / 0.05)
            text(c, ch, 1520 - i * 140, 440 + j * 106, 84, (0.10, 0.06, 0.04), a, 'c', shadow=False)
    sil(c, 360, 940, 1.3, hat='xia', pose='raise', p=0.6)
    cnt(c, 10300)

def S_poem2(c, lt, d, p):
    S_poem(c, lt, d, 1.0)
    a = ease(p / 0.3)
    s = "太师尚书令兼中书令张元随大驾至此"
    for i, ch in enumerate(s):
        aa = ease((p - 0.2 - i * 0.02) / 0.05)
        text(c, ch, 840, 390 + i * 33, 30, (0.55, 0.08, 0.05), aa, 'c', shadow=False)

def S_court(c, lt, d, p):
    palace(c, lt, tone=(0.12, 0.06, 0.04))
    c.set_source_rgb(*INK); c.rectangle(1360, 720, 420, 120); c.fill()
    sil(c, 1560, 720, 1.1, hat='song', pose='point', face=-1, robe=(0.06, 0.03, 0.02))
    for i, (x, nm) in enumerate(((560, "夏竦"), (800, "韩琦"), (1040, "范仲淹"))):
        k = ease((p - 0.3 - i * 0.15) / 0.15)
        sil(c, x, 840, 1.05, hat='song', pose='bow' if k > 0 else 'kneel', p=k)
        text(c, nm, x, 930, 42, (0.9, 0.85, 0.78), 1, 'c')
    cnt(c, 10300)

def S_top(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.04, 0.05, 0.08)), (1, (0.12, 0.12, 0.16))])
    for i in range(5):
        c.set_source_rgba(0.10, 0.10, 0.14, 1); c.rectangle(560 + i * 70, 980 - i * 90, 800 - i * 140, 90); c.fill()
    k = ease(p / 0.6)
    y = lerp(980, 980 - 4 * 90, k)
    glow(c, W / 2, y - 200, 300, GOLD, 0.4 * k)
    sil(c, W / 2, y, 1.2, hat='xia', pose='stand')
    banner(c, 400, 1000, "夏", (0.15, 0.30, 0.38), lt, h=480); banner(c, 1520, 1000, "夏", (0.15, 0.30, 0.38), lt, h=480)

def S_rule2(c, lt, d, p):
    palace(c, lt, tone=(0.16, 0.06, 0.03))
    c.set_source_rgb(*INK); c.rectangle(1360, 720, 420, 120); c.fill()
    sil(c, 1560, 720, 1.1, hat='song', pose='sit', face=-1, robe=(0.06, 0.03, 0.02))
    for i, x in enumerate((420, 600, 780, 960, 1140)):
        k = ease((p - 0.3 - i * 0.06) / 0.15)
        sil(c, x, 840, 1.0, hat='song', pose='kneel')
        glow(c, x, 560, 90, GOLD, 0.5 * k)

def S_why(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.06, 0.04, 0.03)), (1, (0.16, 0.10, 0.06))])
    glow(c, W / 2, 600, 500, (1, 0.8, 0.5), 0.25)
    c.set_source_rgba(0.80, 0.70, 0.52, 1); c.rectangle(560, 330, 800, 580); c.fill()
    s = ["自张元以积忿", "降元昊", "归咎于殿试黜落"]
    for i, ln in enumerate(s):
        for j, ch in enumerate(ln):
            a = ease((p * 1.6 - (i * 7 + j) * 0.04) / 0.06)
            text(c, ch, 1240 - i * 150, 410 + j * 66, 58, (0.15, 0.08, 0.05), a, 'c', shadow=False)
    text(c, "白话：自从张元憋着一口气投了元昊，大家就怪殿试刷人", W / 2, 990, 42, GOLD, ease((p - 0.5) / 0.2), 'c')

def S_legacy(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.04, 0.03, 0.03)), (1, (0.12, 0.08, 0.05))])
    yrs = int(lerp(1057, 1905, ease(p / 0.8)))
    text(c, str(yrs), W / 2, 640, 220, (1, 0.95, 0.88), 0.9, 'c')
    for i in range(14):
        sil(c, 150 + i * 125, 1000, 0.55, hat='song', pose='stand', a=0.5 + 0.5 * ease((p - i * 0.04) / 0.2))

def S_end(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.02, 0.02)), (1, (0.08, 0.05, 0.03))])
    glow(c, W / 2, 820, 600, (0.9, 0.6, 0.3), 0.2)
    k = ease(p)
    sil(c, W / 2, 1000, 1.4, hat='song', pose='stand', a=1 - k * 0.5)
    sil(c, W / 2, 1000, 1.4, hat='xia', pose='stand', a=k * 0.5)

def S_end2(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.10, 0.07, 0.05)), (1, (0.30, 0.18, 0.10))])
    c.set_source_rgb(*INK); c.rectangle(0, 900, W, 200); c.fill()
    banner(c, 260, 900, "宋", (0.55, 0.12, 0.10), lt, h=420); banner(c, 1660, 900, "夏", (0.15, 0.30, 0.38), lt, h=420)
    sil(c, W / 2, 900, 1.3, hat='song', pose='stand')
    a = ease((p - 0.4) / 0.3)
    text(c, "假如你是张元", W / 2, 560, 64, GOLD, a, 'c')

CAM = {'hook': (1.15, 1.0, 1000, 600), 'chen': (1.0, 1.15, 1000, 640), 'mom': (1.0, 1.2, 960, 640), 'you': (1.0, 1.25, 1040, 760),
       'fail': (1.0, 1.15, 900, 640), 'tavern': (1.0, 1.12, 1100, 600), 'answer': (1.0, 1.15, 1000, 600), 'boxes': (1.0, 1.1, 960, 760),
       'poem': (1.0, 1.08, 1100, 520), 'poem2': (1.08, 1.12, 1100, 520), 'top': (1.0, 1.2, 960, 600), 'end': (1.2, 1.0, 960, 800), 'why': (1.0, 1.06, 960, 560)}
