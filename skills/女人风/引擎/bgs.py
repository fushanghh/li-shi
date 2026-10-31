# 场景背景：静态层缓存 + 动态层
from base import *

def sky(c, cols, y1=700):
    g = cairo.LinearGradient(0, 0, 0, y1)
    for i, col in enumerate(cols): g.add_color_stop_rgb(i / (len(cols) - 1), *hx(col))
    c.set_source(g); c.rectangle(0, 0, SW, y1); c.fill()

def speckle(c, box, n, col, seed=5, r=(2, 6)):
    rr = random.Random(seed)
    for k in range(n): ell(c, rr.uniform(box[0], box[2]), rr.uniform(box[1], box[3]), rr.uniform(*r), rr.uniform(1.5, 3), col, 0)

def ground(c, y, c1, c2, seed=6, y1=SH):
    g = cairo.LinearGradient(0, y, 0, y1); g.add_color_stop_rgb(0, *hx(c1)); g.add_color_stop_rgb(1, *hx(c2)); c.set_source(g); c.rectangle(0, y, SW, y1 - y); c.fill()
    ink(c, [(0, y), (SW, y)], 2.6, LINE, 2, 2); speckle(c, (0, y + 10, SW, y1), 80, hx(c2), seed)

def tile_roof(c, x0, x1, y, h, col='4a4a52', up=30):
    """中式坡屋顶：檐口起翘"""
    shape(c, [(x0 - 40, y + h), (x0 + 60, y + 6), (x1 - 60, y + 6), (x1 + 40, y + h), (x1 + 60, y + h - up), (x1 + 20, y + h + 8), (x0 - 20, y + h + 8), (x0 - 60, y + h - up)], hx(col), 2.6)
    for k in range(int((x1 - x0) / 26)):
        xx = x0 + 10 + k * 26; ink(c, [(xx, y + 10), (xx + (xx - (x0 + x1) / 2) * 0.06, y + h)], 2, hx('2c2c34'), 1.4, 2)
    ink(c, [(x0 + 40, y + 4), (x1 - 40, y + 4)], 10, hx('2c2c34'), 8, 2)

def column(c, x, y0, y1, col='8a3a2a', w=22):
    rect(c, x - w, y0, x + w, y1, hx(col)); ink(c, [(x - w + 8, y0 + 10), (x - w + 8, y1 - 10)], 4, hx('b25a44'), 3, 2)
    rect(c, x - w - 8, y1 - 6, x + w + 8, y1 + 16, hx('b8ad98'))

# ====================== 现代婚宴大厅 ======================
def bg_hall(c):
    c.set_source_rgb(*hx('efd9bf')); c.paint()
    for j, y in enumerate(range(40, 720, 70)):   # 墙纸纹
        for x in range(40 + (j % 2) * 60, SW, 120):
            c.set_source_rgba(*hx('e2c6a2'), 1); c.new_path(); c.arc(x, y, 14, 0, TAU); c.fill(); ink(c, [(x - 22, y), (x, y - 20), (x + 22, y)], 2, hx('d6b48c'), 1, 4)
    for x in (120, 1800): rect(c, x - 30, 0, x + 30, 720, hx('e6cfae'))
    # 舞台红幕与囍
    rect(c, 560, 90, 1360, 640, hx('b5302a')); 
    for k in range(12): ink(c, [(580 + k * 66, 100), (586 + k * 66, 630)], 6, hx('9a2620'), 4, 2)
    rect(c, 540, 70, 1380, 100, hx('c9a24a'))
    ell(c, 960, 340, 170, 170, hx('c9a24a'), 3); ell(c, 960, 340, 150, 150, hx('b5302a'), 2)
    font(c, SERIF, 220, True); tw = c.text_extents('囍')[4]; c.set_source_rgb(*hx('f2c14e')); c.move_to(960 - tw / 2, 420); c.show_text('囍')
    for sd in (-1, 1):   # 花柱
        x = 960 + sd * 470
        ink(c, [(x, 640), (x, 260)], 10, hx('c9a24a'), 8, 2)
        for k in range(7): ell(c, x + math.sin(k) * 24, 280 + k * 50, 30, 26, hx('f0c0c0') if k % 2 else hx('f7f2e6'), 2)
    # 远处圆桌
    for (x, y, s) in ((200, 760, 1.0), (520, 740, 0.9), (1420, 740, 0.9), (1740, 760, 1.0)):
        for k in range(3): ell(c, x - 90 * s + k * 90 * s, y - 70 * s, 26 * s, 34 * s, hx('c9a06a'), 2)  # 椅背
        ell(c, x, y - 20 * s, 150 * s, 36 * s, hx('f6f1e6'), 2.4); rect(c, x - 150 * s, y - 20 * s, x + 150 * s, y + 60 * s, hx('f6f1e6'))
        ell(c, x, y - 26 * s, 50 * s, 12 * s, hx('e0b040'), 1.6)
    ground(c, 800, 'b98d64', '9a6e48')
    for k in range(9): ink(c, [(k * 240, 800), (k * 240 - 300, SH)], 2, hx('a07850'), 1, 2)

def dyn_hall(c, t):
    for (x, y) in ((360, 40), (960, 30), (1560, 40)):   # 吊灯
        ink(c, [(x, 0), (x, y)], 3, hx('c9a24a'), 2, 2)
        for k in range(5): glow(c, x - 80 + k * 40, y + 30 + math.sin(t * 3 + k) * 2, 40, a=0.5)
        ell(c, x, y + 30, 100, 16, hx('e6c66a'), 2)
    dust(c, t, 24, box=(0, 0, SW, 700), col=hx('fff3c8'), a=0.4)

def gift_table(c, t, book=True):
    """礼金台（前景右）"""
    rect(c, 1080, 760, 1760, 790, hx('c8322a')); shape(c, [(1080, 790), (1760, 790), (1780, 1000), (1060, 1000)], hx('b5302a'), 2.6, n=1)
    for k in range(10): ink(c, [(1100 + k * 68, 800), (1090 + k * 70, 990)], 4, hx('9a2620'), 3, 2)
    font(c, 'LXGW WenKai', 64, True); c.set_source_rgb(*hx('f2c14e')); c.move_to(1330, 920); c.show_text('礼金台')
    # 红包箱
    rect(c, 1430, 640, 1600, 762, hx('c8322a')); rect(c, 1470, 636, 1560, 648, hx('3a1a14'))
    font(c, SERIF, 70, True); tw = c.text_extents('囍')[4]; c.set_source_rgb(*hx('f2c14e')); c.move_to(1515 - tw / 2, 735); c.show_text('囍')
    if book:   # 礼簿
        shape(c, [(1150, 760), (1250, 744), (1350, 760), (1350, 768), (1150, 768)], hx('f6eedb'), 2.2, n=1); ink(c, [(1250, 744), (1250, 766)], 2, LINE, 1, 2)
        rect(c, 1146, 766, 1354, 776, hx('c8322a'), 1.6)
    # 收款码牌
    rect(c, 1640, 600, 1730, 760, hx('f6f1e6')); rect(c, 1652, 616, 1718, 682, hx('2c2c34'), 1.4)
    rr = random.Random(9)
    for i in range(8):
        for j in range(8):
            if rr.random() < 0.5: c.set_source_rgb(*hx('f6f1e6')); c.rectangle(1655 + i * 8, 619 + j * 8, 7, 7); c.fill()
    label(c, '扫码随礼', 1685, 716, 20, hx('8e2c26'), bold=True)

# ====================== 周代丧礼 ======================
def bg_zhou(c):
    sky(c, ['c9cdc6', 'dcd8c8', 'e8dfc8'])
    for (y0, col, ph, a) in ((440, 'a8ad9e', 0.5, 50), (500, '949a8a', 2.0, 40)):
        pts = [(x, y0 + math.sin(x * 0.005 + ph) * a) for x in range(0, 1960, 40)]; shape(c, pts + [(1960, 760), (0, 760)], hx(col), 2.2, n=2)
    # 院墙
    rect(c, 0, 520, SW, 760, hx('c4b08c'))
    for k in range(1, 9): ink(c, [(0, 520 + k * 28), (SW, 520 + k * 28)], 2, hx('a8946e'), 1, 2)
    # 堂：台基 + 柱 + 屋顶
    shape(c, [(820, 760), (820, 690), (1860, 690), (1860, 760)], hx('b8ad98'), 2.6, n=1)
    for k in range(4): rect(c, 760 - k * 24, 760 + k * 0, 820, 760, hx('a89d88'), 1.6)
    for k in range(5): rect(c, 700 + k * 24, 690 + k * 14, 830, 704 + k * 14, hx('b8ad98'), 1.6)
    rect(c, 860, 330, 1820, 690, hx('3a2e26'))   # 堂内暗
    # 棺
    shape(c, [(1180, 690), (1180, 600), (1560, 586), (1580, 690)], hx('2c1814'), 2.6, n=1); ink(c, [(1190, 610), (1560, 598)], 8, hx('8a2a1a'), 6, 2)
    for x in (900, 1120, 1340, 1560, 1780): column(c, x, 330, 690, '7a4a32')
    tile_roof(c, 800, 1880, 200, 140, '4a4a46')
    # 白帷幔（挂在柱间）
    for k in range(4):
        x0 = 900 + k * 220; x1 = x0 + 220
        shape(c, [(x0 + 20, 340), (x1 - 20, 340), (x1 - 30, 420), ((x0 + x1) / 2, 450), (x0 + 30, 420)], hx('f3eee2'), 2.2)
    # 树（枯枝）
    ink(c, [(300, 760), (310, 600), (290, 480), (320, 360)], 30, hx('5a4a3a'), 12, 6)
    for (a, b) in (((300, 520), (200, 420)), ((310, 460), (420, 360)), ((300, 420), (240, 300)), ((320, 380), (380, 280))): ink(c, [a, b], 10, hx('5a4a3a'), 3, 2)
    ground(c, 760, 'b8ad98', '9e937e')
    for k in range(12): ink(c, [(0, 800 + k * 26), (SW, 800 + k * 26)], 1.4, hx('a89d88'), 1, 2)

def dyn_zhou(c, t):
    clouds(c, t, 110, 4, hx('ecebe4'), 10, 3)
    birds(c, t, 160, 3, 5)
    for k in range(4):   # 帷幔飘带
        x = 920 + k * 220 + 200
        sw = math.sin(t * 2 + k) * 14
        ink(c, [(x - 10, 340), (x - 6 + sw * 0.5, 450), (x + sw, 560)], 10, hx('f3eee2'), 3, 6)
    # 香烟
    for k in range(3):
        y = 560 - ((t * 40 + k * 60) % 180); a = 0.5 * (1 - ((t * 40 + k * 60) % 180) / 180)
        c.set_source_rgba(0.95, 0.95, 0.92, a); c.arc(1130 + math.sin(t + k) * 14, y, 12 + k * 4, 0, TAU); c.fill()
    rect(c, 1100, 620, 1160, 690, hx('6b5a3a')); ink(c, [(1130, 620), (1130, 580)], 3, hx('8a2a1a'), 2, 2)

def bamboo_card(c, k, cols, hl=None):
    """竹简展开：cols 每根一列字；k 展开进度"""
    n = len(cols); w = 120; x0 = 960 + n * w / 2
    shown = int(n * ease(k) + 0.999)
    for i in range(shown):
        x = x0 - (i + 1) * w
        rect(c, x + 6, 110, x + w - 6, 800, hx('d9bf86'), 2.2)
        ink(c, [(x + 6, 180), (x + w - 6, 180)], 3, hx('6b4528'), 2, 2); ink(c, [(x + 6, 760), (x + w - 6, 760)], 3, hx('6b4528'), 2, 2)
        font(c, SERIF, 84, True)
        for j, ch in enumerate(cols[i]):
            c.set_source_rgb(*(RED if hl and ch in hl else INK)); tw = c.text_extents(ch)[4]; c.move_to(x + w / 2 - tw / 2, 300 + j * 120); c.show_text(ch)

# ====================== 秦末沛县·吕公宅 ======================
def bg_han(c):
    sky(c, ['9cc0c8', 'd8e0cc', 'efe2c2'])
    for (y0, col, ph, a) in ((420, '9aae8c', 1.0, 50), (470, '86a07a', 2.6, 40)):
        pts = [(x, y0 + math.sin(x * 0.006 + ph) * a) for x in range(0, 1960, 40)]; shape(c, pts + [(1960, 760), (0, 760)], hx(col), 2.2, n=2)
    for k in range(6):   # 柳
        x = 80 + k * 120
        ink(c, [(x, 600), (x + 6, 460)], 14, hx('6b4528'), 6, 2)
        for j in range(7): ink(c, [(x + 6, 470), (x - 50 + j * 18, 500), (x - 56 + j * 20, 600)], 3, hx('6f9a58'), 1, 4)
        ell(c, x + 6, 450, 60, 34, hx('86ad6a'), 2)
    rect(c, 0, 560, 760, 760, hx('d1b88e'))   # 院墙
    for k in range(1, 7): ink(c, [(0, 560 + k * 28), (760, 560 + k * 28)], 2, hx('b39a6e'), 1, 2)
    tile_roof(c, -20, 760, 520, 46, '5a5a5a', 10)
    # 堂（高台）
    shape(c, [(760, 760), (760, 640), (1900, 640), (1900, 760)], hx('c9b68e'), 2.6, n=1)
    for k in range(6): rect(c, 960 + k * 0, 640 + k * 20, 1180, 660 + k * 20, hx('d8c69c'), 1.6)
    rect(c, 820, 300, 1880, 640, hx('5a3a28'))
    for x in (840, 1060, 1300, 1560, 1860): column(c, x, 300, 640, '8a3a2a', 20)
    for x in range(860, 1860, 60): ink(c, [(x, 300), (x + 30, 280)], 6, hx('6b4528'), 4, 2)  # 斗拱示意
    tile_roof(c, 780, 1920, 150, 140, '4a4a52')
    # 堂上席位、帷帐
    for k in range(5):
        x0 = 900 + k * 200; rect(c, x0, 600, x0 + 140, 616, hx('c9a06a'))
    for k in range(5): shape(c, [(840 + k * 220, 306), (1060 + k * 220, 306), (1040 + k * 220, 360), (860 + k * 220, 360)], hx('c86a4a'), 2, n=4)
    ground(c, 760, 'd6c09a', 'bba27a')
    for k in range(10): ink(c, [(k * 220, 760), (k * 220 - 160, SH)], 1.4, hx('c2aa80'), 1, 2)

def dyn_han(c, t):
    clouds(c, t, 100, 4, hx('f6f2e6'), 12, 7); birds(c, t, 150, 4, 8)
    for k in range(4):   # 灯笼摇
        x = 940 + k * 260; a = math.sin(t * 2 + k) * 0.06
        c.save(); c.translate(x, 360); c.rotate(a); ink(c, [(0, 0), (0, 30)], 2, LINE, 1, 2); ell(c, 0, 60, 24, 32, hx('d24a32'), 2); glow(c, 0, 60, 50, (1, .7, .4), 0.35); c.restore()

def lowseat_crowd(c, t, seed=11, y=700, x0=900, x1=1800, n=6, s=300):
    rr = random.Random(seed)
    cols = [hx(x) for x in ('7a3a2a', '3f6a8a', '6a7a4a', '8a6a3a', '5a4a6a')]
    for i in range(n):
        x = x0 + (x1 - x0) * i / max(1, n - 1)
        fig(c, x, y, s, dict(nsh=0.7 + 0.2 * math.sin(t * 3 + i), nel=1.2, head=0.05 * math.sin(t * 2 + i * 1.3)), t, outline=False, male=True, hair='guan', body='robe', sit='kneel',
            top=hx('e9dcc0'), bot=cols[i % 5], beard=rr.random() < 0.5, flip=rr.random() < 0.5, mouth='open' if math.sin(t * 5 + i) > 0.6 else 'closed')

# ====================== 敦煌 ======================
def bg_mogao(c):
    sky(c, ['7fb5c8', 'bfdcd8', 'f0dcae'], 760)
    for (y0, col, ph, a) in ((380, 'efc690', 0.5, 90), (450, 'e3b07a', 2.2, 60)):
        pts = [(x, y0 + math.sin(x * 0.004 + ph) * a) for x in range(0, 1960, 40)]; shape(c, pts + [(1960, 800), (0, 800)], hx(col), 2.4, n=2)
        ink(c, [(p[0], p[1] + 3) for p in pts[4:22]], 3, hx('f8e6b8'), 1, 4)
    # 崖面
    shape(c, [(0, 470), (300, 440), (900, 450), (1500, 430), (1920, 460), (1920, 760), (0, 760)], hx('c99a62'), 2.6, n=2)
    for k in range(1, 6): ink(c, [(0, 470 + k * 50), (SW, 460 + k * 50)], 2, hx('b4844e'), 1, 4)
    rr = random.Random(4)
    for row in range(3):
        for k in range(16):
            x = 60 + k * 118 + rr.uniform(-20, 20); y = 500 + row * 80 + rr.uniform(-8, 8)
            if 820 < x < 1100: continue
            c.new_path(); c.move_to(x, y + 40); c.line_to(x, y + 14); c.arc(x + 15, y + 14, 15, math.pi, TAU); c.line_to(x + 30, y + 40); c.close_path()
            c.set_source_rgb(*hx('5a3622')); c.fill_preserve(); c.set_source_rgb(*LINE); c.set_line_width(2); c.stroke()
    # 九层楼
    for k in range(9):
        y = 740 - k * 52; w = 230 - k * 14
        rect(c, 960 - w / 2 + 16, y - 40, 960 + w / 2 - 16, y, hx('e8d6b0'), 2)
        for j in range(3): rect(c, 960 - 30 + (j - 1) * 50, y - 32, 960 - 10 + (j - 1) * 50, y - 6, hx('8a3a2a'), 1.4)
        shape(c, [(960 - w / 2 - 20, y - 36), (960 - w / 2 + 20, y - 58), (960 + w / 2 - 20, y - 58), (960 + w / 2 + 20, y - 36), (960 + w / 2 + 30, y - 46), (960 - w / 2 - 30, y - 46)], hx('7a3a2a'), 2.2)
    ell(c, 960, 260, 8, 8, hx('c9a24a'), 2)
    # 白杨 + 前景沙地
    for k in range(10):
        x = 40 + k * 70 if k < 5 else 1450 + (k - 5) * 90
        ink(c, [(x, 800), (x, 700)], 6, hx('6b4a2a'), 3, 2); ell(c, x, 660, 22, 70, hx('6f8a4e'), 2)
    ground(c, 800, 'e0bf88', 'c99e66')

def dyn_mogao(c, t):
    clouds(c, t, 120, 3, hx('f8f2e6'), 10, 4); birds(c, t, 200, 3, 9)
    # 驼队
    for i in range(4):
        x = (t * 40 + i * 150) % 2300 - 300; y = 900 + i * 0; b = math.sin(t * 6 + i) * 4
        shape(c, [(x, y - 80 + b), (x + 40, y - 120 + b), (x + 70, y - 90 + b), (x + 100, y - 120 + b), (x + 130, y - 90 + b), (x + 160, y - 110 + b), (x + 190, y - 140 + b), (x + 205, y - 130 + b), (x + 180, y - 90 + b), (x + 150, y - 60 + b), (x + 10, y - 60 + b)], hx('b07a44'), 2.4)
        for j in range(4):
            sw = math.sin(t * 6 + i + j * 1.6) * 12
            ink(c, [(x + 20 + j * 40, y - 64 + b), (x + 20 + j * 40 + sw, y)], 8, hx('9a6a3a'), 6, 2)
    dust(c, t, 20, box=(0, 600, SW, 400), col=hx('f8e2b0'), a=0.5)

def bg_yard(c):
    random.seed(3)
    sky(c, ['9cc7c4', 'f0dcae'], 600)
    for (y0, col, ph, a) in ((360, 'e8c08a', 0.5, 70), (420, 'dba872', 2.2, 50)):
        pts = [(x, y0 + math.sin(x * 0.006 + ph) * a) for x in range(0, 1960, 40)]; shape(c, pts + [(1960, 700), (0, 700)], hx(col), 2.4, n=2)
    WT, WB = 330, 720
    rect(c, 0, WT, 1960, WB, hx('caa16e'))
    for k in range(1, 14): ink(c, [(0, WT + k * 28), (1960, WT + k * 28)], 2, hx('a87e50'), 1, 2)
    speckle(c, (0, WT + 10, 1920, WB - 10), 60, hx('b38a5a'))
    rect(c, -10, WT - 16, 1960, WT + 4, hx('b08254'))
    ink(c, [(820, 400), (810, 300), (790, 200)], 30, hx('6b4528'), 14, 6); ink(c, [(806, 300), (870, 230), (930, 190)], 12, hx('6b4528'), 6, 6)
    for (fx, fy, r) in ((760, 170, 80), (850, 130, 90), (940, 170, 70), (700, 230, 55), (900, 230, 60)): ell(c, fx, fy, r, r * 0.75, hx('7e9a52'), 2.4)
    rect(c, 60, 230, 400, 300, hx('8a5a34')); rect(c, 40, 212, 420, 234, hx('6b4528'))
    for k in range(2): ell(c, 180 + k * 100, 266, 14, 14, hx('c99a45'), 2)
    rect(c, 70, 300, 390, 720, hx('8a5a34')); rect(c, 100, 300, 360, 720, hx('3a2a20'))
    shape(c, [(100, 300), (170, 318), (170, 712), (100, 720)], hx('9a6a3e'), 2.4, n=1)
    for k in range(5): ell(c, 136, 360 + k * 70, 5, 5, hx('c99a45'), 1)
    HB = 760
    rect(c, 1200, 70, 1920, HB, hx('d8b585'))
    for k in range(48):
        bx = 1210 + (k % 6) * 118 + (60 if (k // 6) % 2 else 0); by = 120 + (k // 6) * 80
        if bx < 1880: ink(c, [(bx, by), (bx + 90, by)], 2, hx('b8946a'), 1, 2)
    rect(c, 1180, 40, 1940, 76, hx('8a5a34'))
    for k in range(20): ell(c, 1200 + k * 38, 84, 10, 10, hx('6b4528'), 2)
    rect(c, 1600, 250, 1820, HB, hx('2e221a')); rect(c, 1600, 250, 1710, HB, hx('8a5a34')); rect(c, 1580, 228, 1840, 252, hx('6b4528')); rect(c, 1580, HB - 16, 1840, HB, hx('6b4528'))
    for k in range(5): ink(c, [(1612, 300 + k * 90), (1700, 300 + k * 90)], 3, hx('6b4528'), 2, 2)
    rect(c, 1290, 300, 1490, 450, hx('3a2a20'))
    for k in range(10): rect(c, 1300 + k * 19, 300, 1308 + k * 19, 450, hx('a8794a'), 1.2)
    rect(c, 1280, 288, 1500, 302, hx('6b4528')); rect(c, 1280, 448, 1500, 462, hx('6b4528'))
    g = cairo.LinearGradient(0, 720, 0, SH); g.add_color_stop_rgb(0, *hx('d9b886')); g.add_color_stop_rgb(1, *hx('c79c66')); c.set_source(g)
    c.move_to(0, 720); c.line_to(1200, 720); c.line_to(1200, HB); c.line_to(1960, HB); c.line_to(1960, SH); c.line_to(0, SH); c.close_path(); c.fill()
    ink(c, [(0, 720), (1200, 720)], 2.6, LINE, 2, 2); ink(c, [(1200, HB), (1920, HB)], 2.6, LINE, 2, 2)
    speckle(c, (0, 735, 1920, SH), 70, hx('b88a58'))
    for (bx, by) in ((1800, 820), (1870, 826), (1835, 776)):
        shape(c, [(bx - 34, by + 34), (bx - 38, by - 16), (bx - 14, by - 40), (bx + 14, by - 40), (bx + 38, by - 16), (bx + 34, by + 34)], hx('e8dcc0'), 2.4)
        ink(c, [(bx - 12, by - 34), (bx + 12, by - 34)], 5, hx('8a5a30'), 2, 3)

def dyn_yard(c, t):
    clouds(c, t, 60, 3, hx('f8f2e6'), 10, 6); birds(c, t, 120, 2, 3)
    for k in range(18):   # 树叶摇
        rr = random.Random(k); x = rr.uniform(680, 1000) + math.sin(t * 2 + k) * 5; y = rr.uniform(90, 260)
        ell(c, x, y, 7, 4, hx('a3bd6c'), 0, math.sin(t + k))

def table_dh(c):
    shape(c, [(1240, 700), (1560, 700), (1560, 718), (1240, 718)], hx('8a5a34'), 2.4, n=1); rect(c, 1250, 718, 1550, 740, hx('6b4528'))
    for lx in (1262, 1538): rect(c, lx - 9, 740, lx + 9, 880, hx('6b4528'))
    shape(c, [(1270, 686), (1350, 678), (1360, 700), (1278, 702)], hx('f3e6c4'), 2, n=1)
    for k in range(4): ink(c, [(1286 + k * 16, 684), (1288 + k * 16, 698)], 1.6, LINE, 0.6, 2)
    ell(c, 1400, 694, 22, 8, hx('3a3a3a'), 2)
    shape(c, [(1460, 702), (1454, 664), (1520, 664), (1514, 702)], hx('b07a44'), 2.4, n=1)
    for k in range(10): ell(c, 1466 + k * 5, 660 - (k % 3) * 3, 4, 4, hx('e0b040'), 0.8)

def oil_jar(c, x=1138, y=880, s=1.0, lvl=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, [(-38, 0), (-72, -60), (-64, -120), (-32, -144), (32, -144), (64, -120), (72, -60), (38, 0)], hx('7a4a2e'), 2.6)
    ell(c, 0, -142, 36, 10, hx('3a2418'), 2.4); label(c, '油', 0, -68, 26, hx('e9d6a8'), bold=True); c.restore()

def bg_feast(c):
    """敦煌社邑宴席：土坯屋内"""
    c.set_source_rgb(*hx('d2ac78')); c.paint()
    for k in range(40):
        bx = (k % 8) * 250 + (125 if (k // 8) % 2 else 0); by = 60 + (k // 8) * 120
        ink(c, [(bx, by), (bx + 200, by)], 2, hx('b8925e'), 1, 2)
    rect(c, 0, 0, SW, 50, hx('6b4528'))
    for k in range(14): ell(c, 70 + k * 140, 60, 16, 16, hx('5a3a22'), 2)
    # 后墙窗、佛龛壁画
    rect(c, 200, 160, 480, 400, hx('3a2a20'))
    for k in range(12): rect(c, 212 + k * 22, 160, 220 + k * 22, 400, hx('a8794a'), 1.2)
    rect(c, 760, 120, 1160, 470, hx('e4cfa2'), 3)
    ell(c, 960, 260, 70, 70, hx('6fb0a0'), 2); ell(c, 960, 260, 50, 50, hx('f0d8a8'), 2)
    shape(c, [(900, 460), (920, 330), (960, 300), (1000, 330), (1020, 460)], hx('b5503a'), 2.2)
    ell(c, 960, 270, 26, 30, hx('e9c49a'), 2)
    for k in range(6): ell(c, 800 + k * 64, 440, 20, 12, hx('6fb0a0') if k % 2 else hx('d98c6a'), 1.6)
    rect(c, 1500, 160, 1780, 400, hx('3a2a20'))
    for k in range(12): rect(c, 1512 + k * 22, 160, 1520 + k * 22, 400, hx('a8794a'), 1.2)
    # 地面 + 席子
    ground(c, 640, 'a8794a', '8a5e38')
    for row in range(3):
        y = 680 + row * 120; shape(c, [(120, y), (1800, y), (1840, y + 80), (80, y + 80)], hx('d8c08a'), 2, n=1)
        for k in range(0, 1760, 26): ink(c, [(100 + k, y + 2), (110 + k, y + 78)], 1.4, hx('b89c62'), 1, 2)

def dyn_feast(c, t):
    for (x, y, ph) in ((600, 560, 0), (1320, 560, 2)):   # 油灯
        rect(c, x - 6, y, x + 6, y + 80, hx('6b4528')); ell(c, x, y, 26, 8, hx('b07a44'), 2); flame(c, x, y - 6, t, 1.0, ph)
    dust(c, t, 16, box=(0, 100, SW, 600), col=hx('ffe8b0'), a=0.35)

def low_table(c, x, y, w=300):
    shape(c, [(x - w / 2, y - 18), (x + w / 2, y - 18), (x + w / 2 + 10, y), (x - w / 2 - 10, y)], hx('8a5a34'), 2.4, n=1)
    for lx in (x - w / 2 + 10, x + w / 2 - 10): rect(c, lx - 7, y, lx + 7, y + 50, hx('6b4528'))
    for k in range(3):
        bx = x - w / 3 + k * w / 3; shape(c, [(bx - 24, y - 34), (bx + 24, y - 34), (bx + 16, y - 18), (bx - 16, y - 18)], hx('c9a06a'), 2, n=2); ell(c, bx, y - 34, 24, 5, hx('8a3a2a'), 1.4)
    shape(c, [(x - 10, y - 20), (x - 22, y - 60), (x, y - 76), (x + 22, y - 60), (x + 10, y - 20)], hx('7a4a2e'), 2.2)

# ====================== 明代厅堂 ======================
def bg_ming(c):
    c.set_source_rgb(*hx('e8dcc0')); c.paint()
    rect(c, 0, 0, SW, 60, hx('5a3a28'))
    for x in (160, 760, 1160, 1760): column(c, x, 40, 760, '6b3a2a', 24)
    # 中堂画 + 对联
    rect(c, 820, 110, 1100, 560, hx('f3ead6'), 2.6); rect(c, 840, 130, 1080, 540, hx('e8dcc0'), 1.6)
    for (a, b) in (((860, 480), (940, 300)), ((940, 300), (1000, 420)), ((1000, 420), (1060, 260))): ink(c, [a, b], 8, hx('6a7a6a'), 3, 2)
    ell(c, 980, 200, 30, 30, hx('c9503a'), 1.6)
    for x in (760 - 30 - 60, 1160 + 30):
        rect(c, x, 120, x + 60, 560, hx('b5302a'))
        font(c, 'LXGW WenKai', 40, True)
        for j, ch in enumerate('礼尚往来' if x < 960 else '人情世故'):
            c.set_source_rgb(*hx('f2c14e')); tw = c.text_extents(ch)[4]; c.move_to(x + 30 - tw / 2, 190 + j * 100); c.show_text(ch)
    # 八仙桌 + 太师椅
    rect(c, 760, 600, 1160, 624, hx('5a2e1e')); rect(c, 770, 624, 1150, 650, hx('6b3a2a'))
    for lx in (780, 1140): rect(c, lx - 10, 650, lx + 10, 860, hx('5a2e1e'))
    # 窗棂（两侧）
    for x0 in (250, 1250 + 220):
        rect(c, x0, 160, x0 + 220, 520, hx('caa678'))
        for i in range(6):
            for j in range(9): rect(c, x0 + 8 + i * 35, 168 + j * 38, x0 + 36 + i * 35, 196 + j * 38, hx('f3ead6'), 1.2)
    ground(c, 860, 'b08a62', '8e6a46')
    for k in range(12): ink(c, [(k * 180, 860), (k * 180 - 200, SH)], 1.6, hx('9a7650'), 1, 2)

def dyn_ming(c, t):
    dust(c, t, 22, box=(0, 100, SW, 700), col=hx('fff3d0'), a=0.35)
    for x in (300, 1620):   # 灯笼
        a = math.sin(t * 1.6 + x) * 0.05; c.save(); c.translate(x, 60); c.rotate(a); ink(c, [(0, 0), (0, 40)], 2, LINE, 1, 2)
        ell(c, 0, 90, 40, 52, hx('d24a32'), 2.4); glow(c, 0, 90, 90, (1, .7, .4), 0.35); rect(c, -20, 34, 20, 42, hx('c9a24a'), 1.4); c.restore()

def fenzi_list(c, x, y, k, rows, title_='份 子 单', rot=0):
    c.save(); c.translate(x, y); c.rotate(rot)
    h = 60 + 54 * len(rows)
    rect(c, -170, -20, 170, -20 + h * ease(k), hx('d8443a'), 2.4)
    c.save(); c.rectangle(-170, -20, 340, h * ease(k)); c.clip()
    title(c, title_, 0, 14, 40, fill=hx('f2c14e'), stroke=hx('6b1a14'), sw=4, track=6)
    font(c, 'LXGW WenKai', 36, True)
    for i, (n, v) in enumerate(rows):
        c.set_source_rgb(*hx('1e140c')); c.move_to(-140, 86 + i * 54); c.show_text(n)
        tw = c.text_extents(v)[4]; c.move_to(140 - tw, 86 + i * 54); c.show_text(v)
    c.restore(); c.restore()

# ====================== 贾府·荣庆堂 ======================
def bg_jia(c):
    c.set_source_rgb(*hx('ecdcbc')); c.paint()
    rect(c, 0, 0, SW, 70, hx('6b2a20'))
    for x in range(0, SW, 80): ink(c, [(x, 20), (x + 40, 50), (x + 80, 20)], 4, hx('c9a24a'), 3, 4)
    for x in (120, 1800): column(c, x, 60, 780, '8a2a1a', 28)
    # 大屏风
    for k in range(6):
        x0 = 520 + k * 150; rect(c, x0, 140, x0 + 146, 640, hx('3a2a26'), 2.6); rect(c, x0 + 12, 152, x0 + 134, 628, hx('e9d8b0'), 1.6)
        for j in range(3): ell(c, x0 + 73 + math.sin(j + k) * 30, 250 + j * 130, 26, 20, hx('d98c8c') if (j + k) % 2 else hx('f2f0e4'), 1.6)
        ink(c, [(x0 + 30, 600), (x0 + 60, 400), (x0 + 100, 220)], 3, hx('6a5a4a'), 1, 4)
    # 匾
    rect(c, 760, 80, 1160, 132, hx('2c1814')); title(c, '荣 庆 堂', 960, 106, 40, fill=hx('e6c66a'), stroke=hx('2c1814'), sw=2, track=8)
    # 罗汉榻
    rect(c, 760, 560, 1160, 600, hx('6b2a20')); rect(c, 740, 600, 1180, 640, hx('5a2218'))
    for lx in (760, 1160): rect(c, lx - 12, 640, lx + 12, 760, hx('4a1a14'))
    rect(c, 790, 480, 1130, 560, hx('c84a3a')); ell(c, 820, 540, 30, 22, hx('e0b040'), 2); ell(c, 1100, 540, 30, 22, hx('e0b040'), 2)
    # 两侧花几 + 瓶
    for x in (380, 1540):
        rect(c, x - 40, 600, x + 40, 620, hx('5a2218')); rect(c, x - 30, 620, x - 20, 780, hx('4a1a14')); rect(c, x + 20, 620, x + 30, 780, hx('4a1a14'))
        shape(c, [(x - 20, 600), (x - 36, 540), (x - 14, 480), (x + 14, 480), (x + 36, 540), (x + 20, 600)], hx('3f6a9a'), 2.4)
        for j in range(4): ell(c, x - 30 + j * 20, 450 - (j % 2) * 30, 18, 14, hx('d24a5a'), 1.6)
    # 地毯
    ground(c, 780, 'b5302a', '8a2420')
    shape(c, [(300, 800), (1620, 800), (1720, 1060), (200, 1060)], hx('c8423a'), 2.4, n=1)
    for k in range(8): ell(c, 400 + k * 160, 900 + (k % 2) * 60, 40, 20, hx('e0b040'), 1.6)

def dyn_jia(c, t):
    for x in (300, 1620):
        a = math.sin(t * 1.4 + x) * 0.04; c.save(); c.translate(x, 70); c.rotate(a); ink(c, [(0, 0), (0, 50)], 2, LINE, 1, 2)
        shape(c, [(-30, 50), (30, 50), (44, 110), (30, 170), (-30, 170), (-44, 110)], hx('f2e2b0'), 2.4); glow(c, 0, 110, 110, (1, .85, .5), 0.35)
        for j in range(5): ink(c, [(-10 + j * 5, 172), (-10 + j * 5, 200 + math.sin(t * 3 + j) * 4)], 2, hx('c8322a'), 1, 2)
        c.restore()
    dust(c, t, 18, box=(200, 100, 1500, 700), col=hx('fff3d0'), a=0.35)

def silver_pile(c, x, y, n, t=0):
    for i in range(n):
        row = 0; k = i; w = 6
        while k >= w and w > 0: k -= w; w -= 1; row += 1
        bx = x + (k - (w - 1) / 2) * 62; by = y - row * 34
        c.save(); c.translate(bx, by)
        shape(c, [(-30, 0), (-24, -18), (-12, -8), (12, -8), (24, -18), (30, 0), (22, 14), (-22, 14)], hx('e2e2dc'), 2.2); ell(c, 0, -10, 8, 6, hx('c8c8c0'), 1.2)
        c.restore()

# ====================== 民国婚礼堂屋 ======================
def bg_minguo(c):
    c.set_source_rgb(*hx('e6d2ae')); c.paint()
    rect(c, 0, 0, SW, 50, hx('4a2e20'))
    for x in (100, 1820): column(c, x, 40, 760, '5a3426', 24)
    rect(c, 640, 100, 1280, 600, hx('b5302a'))
    font(c, SERIF, 300, True); tw = c.text_extents('囍')[4]; c.set_source_rgb(*hx('f2c14e')); c.move_to(960 - tw / 2, 470); c.show_text('囍')
    for x in (560, 1360):
        rect(c, x - 34, 120, x + 34, 600, hx('c8322a'))
        font(c, 'LXGW WenKai', 40, True)
        for j, ch in enumerate('百年好合' if x < 960 else '永结同心'):
            c.set_source_rgb(*hx('1e140c')); tw = c.text_extents(ch)[4]; c.move_to(x - tw / 2, 200 + j * 110); c.show_text(ch)
    # 条案 + 烛台
    rect(c, 700, 600, 1220, 622, hx('4a2218')); rect(c, 720, 622, 1200, 640, hx('5a2a1e'))
    for lx in (730, 1190): rect(c, lx - 10, 640, lx + 10, 780, hx('4a2218'))
    for x in (800, 1120): rect(c, x - 10, 520, x + 10, 600, hx('c9a24a')); rect(c, x - 14, 470, x + 14, 520, hx('d8302a'))
    # 窗与门帘
    for x0 in (220, 1480):
        rect(c, x0, 160, x0 + 220, 480, hx('9a6a3e'))
        for i in range(5):
            for j in range(8): rect(c, x0 + 10 + i * 41, 170 + j * 38, x0 + 46 + i * 41, 202 + j * 38, hx('f3ead6'), 1.2)
        c.set_source_rgba(*hx('d8302a'), 1); font(c, SERIF, 70, True); c.move_to(x0 + 75, 360); c.show_text('囍')
    ground(c, 780, 'a8865e', '8a6a46')
    for k in range(14): ink(c, [(k * 150, 780), (k * 150, SH)], 1.4, hx('94744e'), 1, 2)

def dyn_minguo(c, t):
    for (x, ph) in ((800, 0), (1120, 1.3)): flame(c, x, 466, t, 1.2, ph)
    dust(c, t, 18, box=(200, 100, 1500, 600), col=hx('ffe0a0'), a=0.35)

def zhang_table(c, x=1250, y=760):
    rect(c, x - 260, y - 20, x + 260, y, hx('5a2a1e')); shape(c, [(x - 260, y), (x + 260, y), (x + 270, y + 200), (x - 270, y + 200)], hx('c8322a'), 2.4, n=1)
    title(c, '礼  账', x, y + 100, 64, fill=hx('f2c14e'), stroke=hx('6b1a14'), sw=4, track=10)
    rect(c, x - 200, y - 38, x - 20, y - 20, hx('f3e6c4'), 2); rect(c, x - 200, y - 42, x - 20, y - 36, hx('c8322a'), 1.4)
    ell(c, x + 60, y - 28, 28, 10, hx('2a2a2a'), 2); ink(c, [(x + 120, y - 30), (x + 200, y - 50)], 5, hx('6b4528'), 3, 2)
    for k in range(4): ell(c, x + 210 + (k % 2) * 6, y - 26 - k * 6, 18, 6, hx('dcdcd8'), 1.6)

def ledger_card(c, k, rows, head='礼簿', vertical=True):
    """古式礼簿翻开（竖排，右起）"""
    w = 1300; h = 700; x0 = 960 - w / 2; y0 = 90
    kk = ease(k)
    c.save(); c.translate(960, y0 + h / 2); c.scale(kk, 1); c.translate(-960, -(y0 + h / 2))
    rect(c, x0, y0, x0 + w, y0 + h, hx('f3e6c4'), 3); ink(c, [(960, y0), (960, y0 + h)], 3, hx('c9a24a'), 2, 2)
    for i in range(1, 9): ink(c, [(x0 + i * w / 9, y0 + 20), (x0 + i * w / 12, y0 + h - 20)], 1.4, hx('d8443a'), 1, 2)
    font(c, 'LXGW WenKai', 58, True)
    for i, (n, v) in enumerate(rows):
        cx = x0 + w - (i + 0.5) * w / 9
        for j, ch in enumerate(n): c.set_source_rgb(*INK); tw = c.text_extents(ch)[4]; c.move_to(cx - tw / 2, y0 + 90 + j * 64); c.show_text(ch)
        for j, ch in enumerate(v): c.set_source_rgb(*RED); tw = c.text_extents(ch)[4]; c.move_to(cx - tw / 2, y0 + 360 + j * 64); c.show_text(ch)
    c.restore()

def paper_bg(c, col='efe2c4'):
    c.set_source_rgb(*hx(col)); c.paint()
    rr = random.Random(2)
    for i in range(200): c.set_source_rgba(*hx('c9a878'), 0.15); c.arc(rr.uniform(0, SW), rr.uniform(0, SH), rr.uniform(4, 30), 0, TAU); c.fill()
    for j, y in enumerate(range(60, SH, 90)):
        for x in range(60 + (j % 2) * 60, SW, 120):
            c.set_source_rgba(*hx('c9a24a'), 0.25); c.set_line_width(2); c.new_path(); c.arc(x, y, 16, 0, TAU); c.stroke()
