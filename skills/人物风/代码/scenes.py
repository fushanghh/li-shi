from kit import *
from modern import *
import math, random

CNT = [None]
FX = {'shake': 0.0, 'flash': 0.0, 'white': 0.0}

def draw_cnt(c, n, flash=0):
    text(c, "杨振宁", 96, 950, 32, (0.78, 0.72, 0.64), 1, shadow=False)
    sc = 1 + 0.3 * flash
    c.save(); c.translate(96, 1040); c.scale(sc, sc)
    w = text(c, f"{n}", 0, 0, 84, mix(GOLD, (1, 1, 0.9), flash), 1)
    text(c, "岁", w + 10, -4, 38, (0.9, 0.85, 0.78), 1, shadow=False)
    c.restore()
    if flash > 0: glow(c, 140, 1010, 170, GOLD, 0.35 * flash)

def bg(c, top, bot): vgrad(c, 0, H, [(0, top), (1, bot)])

# 推镜：(起始缩放, 终止缩放, 焦点x, 焦点y)
CAM = {
 'open': (1.0, 1.10, 960, 560), 'open2': (1.04, 1.14, 900, 600), 'open3': (1.0, 1.08, 960, 600),
 'title': (1.0, 1.05, 960, 540), 'born': (1.0, 1.12, 1100, 640), 'tsinghua': (1.0, 1.08, 1100, 600),
 'war': (1.08, 1.0, 960, 600), 'flee': (1.0, 1.06, 700, 700), 'lianda': (1.0, 1.10, 1000, 650),
 'alarm': (1.0, 1.08, 1100, 600), 'alarm2': (1.05, 1.16, 1000, 640), 'ship': (1.0, 1.10, 1100, 650),
 'chicago': (1.0, 1.08, 1100, 620), 'deng49': (1.0, 1.10, 1000, 650), 'deng50': (1.1, 1.0, 1000, 600),
 'princeton': (1.0, 1.08, 1000, 600), 'ym': (1.0, 1.12, 1000, 560), 'mirror': (1.0, 1.12, 1200, 560),
 'ask': (1.0, 1.10, 1100, 600), 'test': (1.0, 1.10, 1200, 600),
 'crack': (1.15, 1.30, 1200, 560), 'shatter': (1.0, 1.12, 1200, 560), 'shock': (1.0, 1.08, 960, 600),
 'prize': (1.0, 1.15, 960, 520), 'ages': (1.08, 1.0, 960, 600), 'king': (1.0, 1.14, 1000, 620), 'first': (1.0, 1.18, 960, 520),
 'bomb': (1.0, 1.08, 1100, 600), 'return': (1.0, 1.08, 1100, 650), 'reunion': (1.0, 1.10, 1000, 650),
 'airport': (1.0, 1.08, 1100, 650), 'letter': (1.0, 1.10, 1150, 600), 'letter2': (1.0, 1.15, 1150, 560),
 'tears': (1.06, 1.16, 1150, 600), 'hospital': (1.0, 1.08, 1100, 650), 'flowers': (1.0, 1.12, 1250, 600),
 'home': (1.0, 1.08, 1000, 650), 'citizen': (1.0, 1.10, 1100, 640), 'hundred': (1.0, 1.10, 1100, 640),
 'gone': (1.0, 1.06, 960, 640), 'end': (1.0, 1.10, 960, 600), 'end2': (1.0, 1.16, 1200, 560),
}

# ------------------------------------------------------------------ 开场
def stage(c, lt, warm=1.0):
    bg(c, (0.03, 0.02, 0.02), (0.14, 0.08, 0.04))
    for x in (380, 960, 1540): chandelier(c, x, 400, 1.0, 0.9, lt)
    c.set_source_rgb(*INK); c.rectangle(0, 860, W, 240); c.fill()
    c.set_source_rgba(0.75, 0.55, 0.3, 0.25); c.rectangle(0, 860, W, 3); c.fill()
    for s in (-1, 1):
        x = 0 if s < 0 else W
        c.move_to(x, 0); c.line_to(x - s * 260, 0); c.curve_to(x - s * 200, 320, x - s * 140, 620, x - s * 180, 880); c.line_to(x, 880); c.close_path()
        c.set_source_rgba(0.28, 0.04, 0.04, 0.92); c.fill()

def S_open(c, lt, d, p):
    stage(c, lt)
    glow(c, 1100, 700, 520, (1, 0.85, 0.55), 0.35)
    for i, x in enumerate((520, 640, 1320, 1440, 1560)): man(c, x, 860, 1.0, face=1 if x < 960 else -1, a=0.92)
    man(c, 980, 860, 1.25, face=1, glasses=True); man(c, 1150, 860, 1.18, face=-1)
    mirror(c, 1080, 480, 0.35, lit=0.5 + 0.2 * math.sin(lt * 2))
    dust(c, lt, 40, (1, 0.9, 0.6), a=0.4)

def S_open2(c, lt, d, p):
    bg(c, (0.02, 0.02, 0.03), (0.10, 0.07, 0.05))
    glow(c, 900, 520, 480, (1, 0.85, 0.6), 0.3)
    man(c, 900, 1380, 3.2, glasses=True, pose='stand')   # 半身特写
    text(c, "杨振宁", 1300, 760, 64, GOLD, ease(lt / 0.6), 'l')
    text(c, "物理学家  1922—2025", 1300, 820, 32, (0.8, 0.75, 0.68), ease((lt - 0.3) / 0.6), 'l', shadow=False)
    dust(c, lt, 30, a=0.35)

def S_open3(c, lt, d, p):
    bg(c, (0.10, 0.07, 0.05), (0.28, 0.16, 0.08))
    glow(c, 960, 760, 800, (1, 0.7, 0.4), 0.3)
    rnd = random.Random(5)
    for i in range(10):
        x = 230 + i * 160; k = ease((lt - 0.5 - i * 0.12) / 0.6)
        man(c, x, 900, 0.95, pose='bow' if k < 0.5 else 'stand', p=1 - k, face=1, a=0.8)
    c.set_source_rgb(*INK); c.rectangle(0, 900, W, 200); c.fill()
    for i in range(10):
        k = ease((lt - 0.5 - i * 0.12) / 0.6); glow(c, 230 + i * 160, 700, 140, GOLD, 0.25 * k)

def S_title(c, lt, d, p):
    bg(c, (0.01, 0.01, 0.02), (0.06, 0.05, 0.05))
    k = ease(lt / 1.0)
    mirror(c, 960, 450, 0.9, a=k, lit=0.8 + 0.2 * math.sin(lt * 2.5))
    man(c, 960, 740, 0.8, glasses=True, a=k)
    text(c, "杨 振 宁", W / 2, 860, 120, (1, 0.96, 0.9), ease((lt - 0.6) / 0.5), 'c')
    text(c, "一面镜子，和一百零三年", W / 2, 950, 46, GOLD, ease((lt - 1.2) / 0.5), 'c')

# ------------------------------------------------------------------ 少年
def S_born(c, lt, d, p):
    bg(c, (0.05, 0.04, 0.07), (0.16, 0.10, 0.06))
    stars(c, lt, 80, ymax=500, a=0.6)
    for x, w in ((300, 260), (760, 300), (1500, 320)):
        poly(c, [(x - w / 2, 860), (x + w / 2, 860), (x + w / 2, 640), (x + w * 0.6, 640), (x, 540), (x - w * 0.6, 640), (x - w / 2, 640)], INK)
    c.set_source_rgba(1, 0.75, 0.4, 0.85); c.rectangle(1060, 660, 120, 120); c.fill(); glow(c, 1120, 720, 260, (1, 0.7, 0.35), 0.45)
    poly(c, [(980, 860), (1260, 860), (1260, 640), (1290, 640), (1120, 540), (950, 640), (980, 640)], INK, 0.0)
    c.set_source_rgba(*INK, 1); c.rectangle(980, 640, 40, 220); c.fill(); c.rectangle(1220, 640, 40, 220); c.fill()
    poly(c, [(940, 650), (1300, 650), (1120, 540)], INK)
    ground(c, 860)
    k = ease((lt - 0.4) / 1.0)
    glow(c, 1120, 720, 80, (1, 0.95, 0.85), 0.6 * k)

def S_tsinghua(c, lt, d, p):
    bg(c, (0.10, 0.08, 0.10), (0.35, 0.20, 0.10))
    glow(c, 1500, 500, 500, (1, 0.7, 0.35), 0.3)
    auditorium(c, 1250, 860, 1.1)
    for x in (180, 330, 1750): 
        c.set_source_rgb(*INK); c.rectangle(x - 8, 560, 16, 300); c.fill(); c.arc(x, 540, 110, 0, 6.28); c.fill()
    ground(c, 860)
    wk = lt * 0.9
    x = lerp(320, 760, ease(p))
    man(c, x, 860, 1.2, pose='walk', walk=wk, gown=True, hair='short', glasses=True)
    man(c, x + 90, 860, 0.62, pose='walk', walk=wk + 0.5, kid=True)
    nametag(c, "父亲 杨武之", x, 560, ease((lt - 0.6) / 0.5), size=40)

def S_war(c, lt, d, p):
    bg(c, (0.20, 0.04, 0.02), (0.06, 0.02, 0.02))
    citywall(c, 860, (0.03, 0.02, 0.02), 220)
    for i in range(6):
        xx = 200 + i * 300; fires(c, lt, [xx], 640, 120)
    rnd = random.Random(3)
    for i in range(5):
        t0 = 0.3 + i * 0.25; x = ((lt - t0) * 900 + rnd.uniform(-200, 200)) - 200
        if lt > t0: plane(c, x, 220 + i * 50, 0.6, 0.95)
    k = ease((lt - 0.8) / 0.3)
    FX['flash'] = max(FX['flash'], cl(1 - abs(lt - 1.3) / 0.35) * 0.6)
    dust(c, lt, 60, (1, 0.5, 0.2), a=0.6, up=True)

def S_flee(c, lt, d, p):
    bg(c, (0.08, 0.07, 0.09), (0.22, 0.15, 0.10))
    mountains(c, lt, cols=[(0.16, 0.13, 0.13), (0.10, 0.08, 0.08), (0.05, 0.04, 0.04)])
    ground(c, 900)
    for i in range(7):
        x = (lt * 70 + i * 230) % 2200 - 150
        man(c, x, 900, 0.95 if i % 3 else 0.6, pose='walk', walk=lt * 0.8 + i * 0.3, face=1, a=0.95, gown=(i % 4 == 0))
    c.set_source_rgba(0.85, 0.15, 0.1, 0.8); c.set_line_width(5); c.set_dash([18, 14])
    c.move_to(120, 300); c.curve_to(600, 260, 900, 420, lerp(120, 1700, ease(p)), lerp(300, 420, ease(p))); c.stroke(); c.set_dash([])
    text(c, "北平", 120, 280, 40, (0.9, 0.85, 0.78), 1); text(c, "昆明", 1700, 480, 40, GOLD, ease((p - 0.7) / 0.3))

def S_lianda(c, lt, d, p):
    bg(c, (0.05, 0.05, 0.06), (0.10, 0.08, 0.07))
    tinroof(c, 260, lt, rain=1.0)
    blackboard(c, 260, 360, 700, 340)
    chalk(c, "∮ E·dl = −dΦ/dt", 300, 520, 60, lt / 2.0)
    man(c, 1000, 860, 1.15, pose='write', t=lt, gown=True, face=-1)
    for i in range(6): man(c, 1250 + (i % 3) * 170, 900 + (i // 3) * 60, 0.9, pose='sit', face=-1, a=0.95)
    man(c, 1420, 860, 0.95, pose='sit', face=-1, glasses=True)
    glow(c, 1440, 640, 120, GOLD, 0.25)
    nametag(c, "杨振宁", 1430, 560, ease((lt - 1.0) / 0.5))

def S_alarm(c, lt, d, p):
    bg(c, (0.25, 0.12, 0.05), (0.10, 0.05, 0.03))
    for i in range(3):
        k = (lt * 0.5 + i * 0.3) % 1
        plane(c, lerp(-200, 2200, k), 160 + i * 70, 0.5, 0.8)
    mountains(c, lt, cols=[(0.18, 0.09, 0.05), (0.10, 0.05, 0.03), (0.04, 0.02, 0.02)], base=900)
    man(c, 980, 900, 1.15, face=1, glasses=True, pose='stand')
    man(c, 1160, 900, 1.08, face=-1, pose='point', p=ease(lt / 1.2))
    nametag(c, "杨振宁", 980, 600, ease((lt - 0.4) / 0.4)); nametag(c, "邓稼先", 1170, 600, ease((lt - 0.7) / 0.4))
    c.set_source_rgba(1, 0.4, 0.2, 0.3 + 0.3 * math.sin(lt * 12)); c.arc(1700, 300, 26, 0, 6.28); c.fill()

def S_alarm2(c, lt, d, p):
    bg(c, (0.20, 0.17, 0.12), (0.06, 0.05, 0.04))
    ground(c, 860, (0.07, 0.06, 0.05))
    for i in range(14):
        c.set_source_rgba(*INK, 0.85); c.set_line_width(4)
        x = 100 + i * 140; c.move_to(x, 860); c.line_to(x + 10, 760 - (i % 3) * 30); c.stroke()
    rnd = random.Random(7)
    for i in range(10):
        x = (rnd.uniform(0, W) + lt * rnd.uniform(80, 160)) % W; y = rnd.uniform(300, 700)
        c.set_source_rgba(*INK, 0.85); c.set_line_width(4); c.move_to(x - 18, y); c.line_to(x, y - 8 * math.sin(lt * 9 + i)); c.line_to(x + 18, y); c.stroke()
    c.set_source_rgba(0.6, 0.55, 0.45, 0.3)
    for k in range(6):
        c.move_to(0, 600 + k * 30); c.curve_to(600, 560 + k * 20 + 20 * math.sin(lt + k), 1200, 640, W, 590 + k * 25); c.set_line_width(2); c.stroke()

# ------------------------------------------------------------------ 美国
def S_ship(c, lt, d, p):
    bg(c, (0.04, 0.05, 0.09), (0.18, 0.12, 0.10))
    moon(c, 1600, 260, 55, 0.9); stars(c, lt, 60, ymax=500, a=0.7)
    water(c, lt, 780, (0.05, 0.06, 0.10))
    ship(c, lerp(700, 1150, ease(p)), 800, 0.9, t=lt)
    man(c, lerp(700, 1150, ease(p)) + 170, 800 - 150 * 0.9 + math.sin(lt * 1.4) * 4, 0.42, face=1)

def S_chicago(c, lt, d, p):
    bg(c, (0.05, 0.05, 0.08), (0.15, 0.12, 0.12))
    rnd = random.Random(11)
    for i in range(18):
        w = rnd.uniform(60, 140); h = rnd.uniform(200, 520); x = i * 110
        c.set_source_rgb(0.06, 0.06, 0.08); c.rectangle(x, 860 - h, w, h); c.fill()
        for j in range(int(h / 40)):
            if rnd.random() < 0.4: c.set_source_rgba(1, 0.8, 0.45, 0.5); c.rectangle(x + 10 + (j % 3) * 18, 860 - h + 20 + j * 40, 8, 14); c.fill()
    ground(c, 860)
    blackboard(c, 1100, 400, 460, 280, 0.95)
    chalk(c, "H ψ = E ψ", 1140, 560, 66, lt / 1.6)
    man(c, 980, 860, 1.25, face=1, pose='point', p=ease(lt / 1.0))
    man(c, 1680, 860, 1.15, face=-1, glasses=False)
    man(c, 760, 860, 1.05, face=1, glasses=True)
    nametag(c, "费米", 980, 540, ease((lt - 0.5) / 0.4)); nametag(c, "泰勒", 1680, 560, ease((lt - 0.8) / 0.4))
    nametag(c, "杨振宁", 760, 580, ease((lt - 1.1) / 0.4), col=GOLD)

def S_deng49(c, lt, d, p):
    bg(c, (0.30, 0.18, 0.08), (0.10, 0.06, 0.04))
    glow(c, 960, 760, 700, (1, 0.6, 0.25), 0.35)
    ground(c, 880)
    for x in (200, 1720): c.set_source_rgb(*INK); c.rectangle(x - 6, 600, 12, 280); c.fill(); c.arc(x, 580, 120, 0, 6.28); c.fill()
    man(c, 860, 880, 1.25, glasses=True, pose='offer', p=ease(lt / 1.0))
    man(c, 1080, 880, 1.2, face=-1, pose='offer', p=ease(lt / 1.0))
    nametag(c, "杨振宁", 860, 560, 1); nametag(c, "邓稼先", 1080, 560, 1)
    k = ease((p - 0.55) / 0.35)
    if k > 0:
        c.set_source_rgba(0, 0, 0, 0.5 * k); c.paint()
        text(c, "22 年", W / 2, 440, 130, RED, k, 'c')

def S_deng50(c, lt, d, p):
    bg(c, (0.10, 0.10, 0.14), (0.22, 0.18, 0.16))
    water(c, lt, 800, (0.06, 0.07, 0.10))
    x = lerp(900, 1700, ease(p))
    ship(c, x, 820, 0.7, t=lt)
    man(c, 420, 800, 1.0, face=1, a=0.9, glasses=True, pose='behind')
    c.set_source_rgb(*INK); c.rectangle(0, 800, 600, 300); c.fill()
    nametag(c, "邓稼先  回国", x, 560, ease((lt - 0.5) / 0.5))

def S_princeton(c, lt, d, p):
    bg(c, (0.06, 0.08, 0.10), (0.20, 0.17, 0.14))
    c.set_source_rgb(*INK)
    c.rectangle(500, 520, 900, 340); c.fill()
    poly(c, [(480, 520), (1420, 520), (1300, 440), (600, 440)], INK)
    c.rectangle(900, 260, 100, 200); c.fill(); poly(c, [(880, 260), (1020, 260), (950, 180)], INK)
    for i in range(9):
        c.set_source_rgba(1, 0.8, 0.45, 0.55); c.rectangle(540 + i * 95, 600, 40, 70); c.fill()
    for x in (180, 300, 1640, 1780): c.set_source_rgb(*INK); c.rectangle(x - 6, 560, 12, 300); c.fill(); c.arc(x, 540, 100, 0, 6.28); c.fill()
    ground(c, 860)
    glow(c, 1000, 820, 500, (1, 0.8, 0.5), 0.25)
    man(c, 1160, 1000, 1.5, face=-1, hair='none', old=0.3)
    c.set_source_rgba(0.88, 0.88, 0.88, 0.9)  # 爱因斯坦蓬发示意
    hx, hy = 1160 - 4 * 1.5, 1000 - (100 + 150 + 1.2) * 1.5
    for k in range(11):
        an = 3.0 + k * 0.33; c.arc(hx + math.cos(an) * 40, hy + math.sin(an) * 34 - 4, 11, 0, 6.28); c.fill()
    man(c, 860, 1000, 1.5, face=1, glasses=True)
    c.set_source_rgb(*INK); c.rectangle(0, 1000, W, 100); c.fill()
    nametag(c, "爱因斯坦", 1160, 560, ease((lt - 0.6) / 0.5)); nametag(c, "杨振宁", 860, 560, ease((lt - 0.3) / 0.5), col=GOLD)

def S_ym(c, lt, d, p):
    bg(c, (0.02, 0.03, 0.05), (0.06, 0.06, 0.08))
    blackboard(c, 160, 360, 1180, 440, 1)
    eq = ["F = dA − ig [A, A]", "Dμ Fμν = Jν", "SU(2) 规范场"]
    for i, s in enumerate(eq): chalk(c, s, 220, 480 + i * 120, 72, (lt - i * 0.7) / 1.0)
    man(c, 1500, 880, 1.2, pose='write', t=lt, face=-1, glasses=True)
    man(c, 1720, 880, 1.15, pose='stand', face=-1)
    nametag(c, "米尔斯", 1720, 600, ease((lt - 1.2) / 0.5))
    k = ease((p - 0.6) / 0.3)
    glow(c, 700, 540, 600, GOLD, 0.25 * k)
    ground(c, 880)

def S_mirror(c, lt, d, p):
    bg(c, (0.02, 0.02, 0.04), (0.07, 0.06, 0.08))
    mirror(c, 1200, 520, 1.0, lit=0.9)
    # 镜前与镜中的人：完全对称
    man(c, 760, 900, 1.2, face=1, pose='raise', p=ease(lt / 1.2), glasses=True)
    c.save(); c.rectangle(1080, 330, 240, 400); c.clip()
    man(c, 1200, 760, 0.7, face=-1, pose='raise', p=ease(lt / 1.2), a=0.75, col=(0.25, 0.28, 0.35))
    c.restore()
    ground(c, 900)
    text(c, "左 ⇄ 右", 1200, 900, 44, GOLD, ease((lt - 1) / 0.5), 'c')

def S_ask(c, lt, d, p):
    bg(c, (0.02, 0.03, 0.05), (0.08, 0.07, 0.07))
    mirror(c, 1500, 480, 0.6, lit=0.6 + 0.2 * math.sin(lt * 3))
    man(c, 820, 880, 1.25, face=1, glasses=True, pose='point', p=ease(lt / 0.8))
    man(c, 1060, 880, 1.15, face=1, pose='stand')
    nametag(c, "杨振宁", 820, 560, 1, col=GOLD); nametag(c, "李政道", 1060, 580, 1)
    ground(c, 880)
    k = ease((lt - 1.2) / 0.4)
    text(c, "？", 1500, 760, 160, RED, k, 'c')

def S_test(c, lt, d, p):
    bg(c, (0.01, 0.02, 0.04), (0.04, 0.06, 0.09))
    # 低温装置（示意）
    c.set_source_rgb(0.08, 0.10, 0.14); c.rectangle(1300, 380, 260, 500); c.fill()
    c.set_source_rgba(0.5, 0.75, 1.0, 0.35); c.set_line_width(3); c.rectangle(1300, 380, 260, 500); c.stroke()
    for i in range(5):
        c.set_source_rgba(0.5, 0.8, 1, 0.12 + 0.08 * math.sin(lt * 3 + i)); c.rectangle(1310, 410 + i * 90, 240, 40); c.fill()
    rnd = random.Random(1)
    for i in range(30):
        tt = (lt * 0.8 + rnd.random()) % 1
        y = 600 - tt * 400 * (1.0 if rnd.random() < 0.7 else -0.4)
        c.set_source_rgba(0.7, 0.9, 1, 1 - tt); c.arc(1430 + rnd.uniform(-40, 40), y, 4, 0, 6.28); c.fill()
    woman(c, 1080, 880, 1.25, face=1, pose='reach', p=ease(lt / 1.0))
    nametag(c, "吴健雄", 1080, 560, ease((lt - 0.4) / 0.5))
    text(c, "钴-60", 1430, 360, 40, (0.7, 0.85, 1), 1, 'c')
    mirror(c, 460, 500, 0.5, lit=0.7)
    ground(c, 880)

# ------------------------------------------------------------------ 高潮
def S_crack(c, lt, d, p):
    bg(c, (0.0, 0.0, 0.01), (0.03, 0.03, 0.05))
    k = ease(p)
    mirror(c, 1200, 520, 1.0, lit=1.0, crack=ease((lt - 0.9) / 0.6), t=lt)
    FX['shake'] = max(FX['shake'], 0.3 * cl((lt - 1.2) / 0.4))

def S_shatter(c, lt, d, p):
    bg(c, (0.0, 0.0, 0.0), (0.05, 0.04, 0.06))
    sh = eout(lt / 1.6)
    mirror(c, 1200, 520, 1.0, shards=max(0.01, sh), t=lt)
    rays(c, 1200, 520, 1 - ease(lt / 1.8), (1, 1, 1), 30, 1600, 0.35, lt * 0.2)
    FX['shake'] = max(FX['shake'], cl(1 - lt / 0.6)); FX['white'] = max(FX['white'], cl(1 - lt / 0.25))

def S_shock(c, lt, d, p):
    bg(c, (0.04, 0.02, 0.01), (0.15, 0.06, 0.02))
    rays(c, 960, 640, 1, GOLD, 28, 1600, 0.12, lt * 0.15)
    for i, x in enumerate((360, 560, 1360, 1560)):
        man(c, x, 900, 1.0, face=1 if x < 960 else -1, pose='raise', p=ease((lt - 0.2 * i) / 0.5), a=0.95)
    man(c, 860, 900, 1.35, glasses=True, pose='fist'); man(c, 1060, 900, 1.3, face=-1, pose='fist')
    ground(c, 900)
    sparks(c, lt, 960, 600, 80, GOLD, 900)
    FX['shake'] = max(FX['shake'], 0.5 * cl(1 - lt / 0.4))

def S_prize(c, lt, d, p):
    bg(c, (0.05, 0.03, 0.01), (0.20, 0.12, 0.04))
    rays(c, 960, 460, ease(lt / 0.6), GOLD, 32, 1700, 0.18, lt * 0.25)
    # 奖章
    k = eout(lt / 0.6); s = lerp(2.4, 1.0, k)
    c.save(); c.translate(960, 480); c.scale(s, s)
    glow(c, 0, 0, 360, GOLD, 0.6)
    g = cairo.RadialGradient(-40, -40, 10, 0, 0, 170); g.add_color_stop_rgb(0, 1, 0.92, 0.6); g.add_color_stop_rgb(1, 0.72, 0.50, 0.18)
    c.set_source(g); c.arc(0, 0, 160, 0, 6.28); c.fill()
    c.set_source_rgba(0.5, 0.33, 0.1, 0.8); c.set_line_width(6); c.arc(0, 0, 140, 0, 6.28); c.stroke()
    man(c, 0, 90, 0.75, col=(0.55, 0.38, 0.12), hair='short')
    c.restore()
    sparks(c, lt, 960, 480, 120, (1, 0.9, 0.55), 1100, seed=3)
    FX['shake'] = max(FX['shake'], 0.8 * cl(1 - (lt - 0.5) / 0.4) if lt > 0.5 else 0)
    FX['white'] = max(FX['white'], cl(1 - abs(lt - 0.55) / 0.12) * 0.6)

def S_ages(c, lt, d, p):
    bg(c, (0.03, 0.02, 0.02), (0.12, 0.08, 0.04))
    rays(c, 960, 700, 1, GOLD, 24, 1500, 0.10, -lt * 0.2)
    for i, (x, name, age, tt) in enumerate(((640, "杨振宁", "35", 0.0), (1280, "李政道", "31", 0.9))):
        k = eout((lt - tt) / 0.35)
        if k <= 0: continue
        glow(c, x, 640, 320, GOLD, 0.35 * k)
        man(c, x, 920, 1.55 * lerp(1.3, 1, k), glasses=(i == 0), pose='stand', face=1 if i == 0 else -1)
        text(c, age, x, 480, int(220 * lerp(1.5, 1, k)), GOLD, k, 'c')
        text(c, name, x, 560, 44, (0.95, 0.9, 0.82), k, 'c')
        if lt - tt < 0.2: FX['shake'] = max(FX['shake'], 0.7)
    ground(c, 920)

def S_king(c, lt, d, p):
    stage(c, lt)
    glow(c, 1000, 640, 600, (1, 0.85, 0.5), 0.45)
    man(c, 1180, 860, 1.35, face=-1, pose='offer', p=ease(lt / 0.8))
    c.set_source_rgb(*INK); poly(c, [(1150, 860 - 215 * 1.35), (1210, 860 - 215 * 1.35), (1200, 860 - 245 * 1.35), (1160, 860 - 245 * 1.35)], INK)  # 王冠意象省略
    man(c, 860, 860, 1.3, face=1, pose='offer', p=ease((lt - 0.4) / 0.8), glasses=True)
    k = ease((lt - 1.0) / 0.3)
    glow(c, 1020, 860 - 120 * 1.3, 120 + 60 * k, GOLD, 0.9 * k)
    c.set_source_rgba(1, 0.85, 0.45, k); c.arc(1020, 860 - 120 * 1.3, 22, 0, 6.28); c.fill()
    nametag(c, "瑞典国王", 1180, 520, 1); nametag(c, "杨振宁", 860, 540, 1, col=GOLD)
    crowd_m(c, 1080, 16, 0.85, a=1, clap=ease((lt - 1.2) / 0.3))
    sparks(c, lt, 1020, 700, 60, GOLD, 800, k=k)

def S_first(c, lt, d, p):
    bg(c, (0.06, 0.03, 0.01), (0.25, 0.10, 0.03))
    rays(c, 960, 520, 1, GOLD, 36, 1800, 0.22, lt * 0.3)
    k = eout(lt / 0.5)
    text(c, "第 一 次", W / 2, 520, int(230 * lerp(1.6, 1, k)), GOLD, k, 'c')
    man(c, 960, 1000, 1.4, glasses=True, pose='raise', p=ease((lt - 0.4) / 0.5))
    sparks(c, lt, 960, 520, 160, (1, 0.85, 0.5), 1300, seed=12)
    FX['shake'] = max(FX['shake'], cl(1 - lt / 0.5))
    FX['white'] = max(FX['white'], cl(1 - lt / 0.15) * 0.7)

# ------------------------------------------------------------------ 归来
def S_bomb(c, lt, d, p):
    bg(c, (0.30, 0.18, 0.10), (0.10, 0.06, 0.04))
    ground(c, 880, (0.06, 0.04, 0.03))
    mushroom(c, 1350, 880, ease(lt / 2.2), lt, s=0.9)
    # 报纸
    k = ease((lt - 1.4) / 0.6)
    c.save(); c.translate(560, 560); c.rotate(-0.06)
    c.set_source_rgba(0.86, 0.83, 0.76, k); c.rectangle(-260, -200, 520, 400); c.fill()
    c.set_source_rgba(0.15, 0.12, 0.1, k)
    c.rectangle(-230, -175, 460, 36); c.fill()
    for i in range(7): c.rectangle(-230, -110 + i * 36, 300 if i != 3 else 200, 10); c.fill()
    c.restore()
    text(c, "邓稼先", 560, 640, 46, RED, k, 'c')
    FX['shake'] = max(FX['shake'], 0.4 * cl(1 - abs(lt - 0.3) / 0.4))

def S_return(c, lt, d, p):
    bg(c, (0.14, 0.12, 0.14), (0.34, 0.22, 0.14))
    glow(c, 1500, 520, 500, (1, 0.75, 0.4), 0.3)
    plane(c, lerp(1900, 1250, ease(p)), lerp(220, 520, ease(p)), 1.1)
    c.set_source_rgb(*INK); c.rectangle(0, 860, W, 220); c.fill()
    for i in range(20): c.set_source_rgba(1, 0.8, 0.4, 0.6); c.rectangle(80 + i * 95, 868, 30, 5); c.fill()
    man(c, 640, 860, 1.25, glasses=True, pose='wave', t=lt, face=1)
    nametag(c, "杨振宁", 640, 560, ease((lt - 0.5) / 0.5), col=GOLD)

def S_reunion(c, lt, d, p):
    palace(c, lt, tone=(0.22, 0.06, 0.04), candles=((420, 760), (1500, 760)))
    man(c, 860, 840, 1.3, glasses=True, pose='offer', p=ease(lt / 1.0))
    man(c, 1080, 840, 1.25, face=-1, pose='offer', p=ease(lt / 1.0))
    nametag(c, "杨振宁", 860, 500, 1, col=GOLD); nametag(c, "邓稼先", 1080, 500, 1)
    for i, x in enumerate((360, 480, 1480, 1600)): man(c, x, 840, 1.0, face=1 if x < 960 else -1, a=0.85)

def S_airport(c, lt, d, p):
    bg(c, (0.20, 0.16, 0.18), (0.40, 0.25, 0.14))
    glow(c, 960, 700, 700, (1, 0.7, 0.35), 0.25)
    plane(c, 1500, 640, 1.4, 1)
    c.set_source_rgb(*INK); c.rectangle(1380, 640, 14, 240); c.fill()
    ground(c, 880)
    man(c, 840, 880, 1.3, glasses=True, pose='point', p=ease(lt / 1.0), face=1)
    man(c, 1060, 880, 1.25, face=-1, pose='stand')
    k = ease((lt - 1.3) / 0.4)
    text(c, "？", 950, 520, 120, GOLD, k, 'c')

def S_letter(c, lt, d, p):
    bg(c, (0.10, 0.05, 0.04), (0.22, 0.12, 0.07))
    c.set_source_rgb(*INK); c.rectangle(300, 760, 1320, 30); c.fill()
    for x in (360, 1560): c.rectangle(x, 790, 20, 300); c.fill()
    for i, x in enumerate((460, 640, 1280, 1460)): man(c, x, 900, 0.95, pose='sit', face=1 if x < 960 else -1, a=0.95)
    for x in (540, 1380): candle(c, x, 760, lt, 90)
    x = lerp(1900, 1180, ease(lt / 1.2))
    man(c, x, 900, 1.1, pose='hold', face=-1, a=1)
    letter(c, x - 90, 760 - 40, 0.25, lit=0.8, lines=6, k=0)
    man(c, 960, 900, 1.05, pose='sit', glasses=True, face=1)
    nametag(c, "杨振宁", 960, 610, 1, col=GOLD)

def S_letter2(c, lt, d, p):
    bg(c, (0.05, 0.03, 0.02), (0.14, 0.09, 0.05))
    letter(c, 1150, 580, 1.25, lit=1, lines=8, k=lt / 2.8, rot=-0.03)
    hand(c, 1900, 900, -2.8, 300, 1); hand(c, 300, 950, -0.5, 380, 1)
    dust(c, lt, 30, a=0.35)

def S_tears(c, lt, d, p):
    bg(c, (0.03, 0.03, 0.04), (0.10, 0.07, 0.06))
    glow(c, 1150, 520, 400, (1, 0.85, 0.6), 0.25)
    man(c, 1150, 1300, 3.4, glasses=True, pose='wipe', p=ease((lt - 0.8) / 0.8), face=1)
    k = cl((lt - 0.6) / 1.5)
    for i in range(3):
        tt = (lt * 0.7 + i * 0.33) % 1
        c.set_source_rgba(0.85, 0.9, 1, 0.8 * k * (1 - tt)); c.arc(1150 + 80, 1300 - 3.4 * 150 + 40 + tt * 160, 7, 0, 6.28); c.fill()
    kk = ease((lt - 0.8) / 0.8)
    c.save(); c.translate(1150 + 3.4 * 30, 1300 - 3.4 * 248); c.rotate(0.3); c.set_source_rgba(0.82, 0.80, 0.76, 0.85 * kk); c.rectangle(-30, -20, 60, 50); c.fill(); c.restore()
    letter(c, 600, 820, 0.45, lit=0.6, lines=6, k=1, rot=0.15)

def S_hospital(c, lt, d, p):
    bg(c, (0.07, 0.08, 0.10), (0.15, 0.15, 0.16))
    window(c, 1300, 260, 380, 420, (0.85, 0.88, 0.95))
    glow(c, 1490, 470, 500, (0.9, 0.95, 1), 0.25)
    c.set_source_rgb(*INK); c.rectangle(400, 720, 600, 60); c.fill(); c.rectangle(400, 640, 30, 240); c.fill(); c.rectangle(970, 680, 30, 200); c.fill()
    man(c, 640, 720, 1.0, pose='sit', face=1, a=1, old=0.3)
    x = lerp(1500, 1150, ease(lt / 1.4))
    man(c, x, 880, 1.25, pose='hold', face=-1, glasses=True, old=0.3)
    bouquet(c, x - 85, 880 - 80 * 1.25, 0.9, t=lt)
    ground(c, 880, (0.05, 0.05, 0.06))
    nametag(c, "邓稼先", 640, 480, 1); nametag(c, "杨振宁", x, 560, 1, col=GOLD)

def S_flowers(c, lt, d, p):
    bg(c, (0.06, 0.07, 0.09), (0.10, 0.10, 0.12))
    window(c, 900, 200, 700, 560, (0.75, 0.80, 0.90))
    k = ease(p)
    glow(c, 1250, 480, 600, (0.9, 0.95, 1), 0.3 * (1 - 0.6 * k))
    c.set_source_rgb(*INK); c.rectangle(860, 760, 780, 40); c.fill()
    bouquet(c, 1250, 770, 1.6, a=1 - 0.3 * k, t=lt)
    c.set_source_rgba(0, 0, 0, 0.45 * k); c.paint()

def S_home(c, lt, d, p):
    bg(c, (0.20, 0.10, 0.05), (0.40, 0.22, 0.10))
    glow(c, 1500, 560, 600, (1, 0.7, 0.35), 0.4)
    auditorium(c, 1500, 860, 0.6, (0.06, 0.04, 0.03))
    c.set_source_rgb(*INK); c.rectangle(380, 520, 620, 340); c.fill(); poly(c, [(340, 530), (1040, 530), (690, 400)], INK)
    c.set_source_rgba(1, 0.8, 0.45, 0.8); c.rectangle(480, 620, 110, 120); c.fill(); c.rectangle(790, 620, 110, 120); c.fill()
    c.set_source_rgba(0.85, 0.7, 0.45, 1); c.rectangle(600, 470, 180, 50); c.fill()
    text(c, "归根居", 690, 508, 36, (0.15, 0.1, 0.06), 1, 'c', shadow=False)
    ground(c, 860)
    for i in range(12):
        tt = (lt * 0.2 + i * 0.09) % 1
        c.set_source_rgba(0.85, 0.5, 0.2, 0.8 * (1 - tt)); c.save(); c.translate(200 + i * 140 + math.sin(lt + i) * 40, 200 + tt * 660); c.rotate(lt + i); c.scale(1, 0.5); c.arc(0, 0, 12, 0, 6.28); c.restore(); c.fill()
    man(c, 1160, 860, 1.2, glasses=True, old=0.8, pose='walk', walk=lt * 0.4, face=-1)

def S_citizen(c, lt, d, p):
    bg(c, (0.04, 0.03, 0.03), (0.16, 0.08, 0.05))
    glow(c, 1100, 560, 500, (1, 0.6, 0.3), 0.35)
    man(c, 1100, 1250, 3.0, glasses=True, old=0.8, pose='stand', face=-1)
    # 胸口一点金光：中华文化的血液
    k = ease((lt - 1.2) / 1.0)
    glow(c, 1080, 1250 - 3 * 100, 160 * (0.6 + 0.4 * math.sin(lt * 3)), GOLD, 0.7 * k)

def S_hundred(c, lt, d, p):
    bg(c, (0.03, 0.03, 0.05), (0.10, 0.08, 0.08))
    stars(c, lt, 100, ymax=700, a=0.8)
    man(c, 760, 900, 1.2, glasses=True, old=0.9, pose='sit', face=1)
    k = ease((lt - 0.6) / 1.0)
    man(c, 1300, 900, 1.2, face=-1, a=0.35 * k, col=(0.55, 0.55, 0.6))
    nametag(c, "邓稼先", 1300, 600, 0.6 * k, col=(0.75, 0.75, 0.8))
    c.set_source_rgba(*GOLD, 0.55 * k); c.set_line_width(3); c.set_dash([10, 12])
    c.move_to(840, 700); c.curve_to(980, 560, 1120, 560, 1260, 700); c.stroke(); c.set_dash([])
    ground(c, 900)

def S_gone(c, lt, d, p):
    bg(c, (0.06, 0.06, 0.08), (0.16, 0.13, 0.12))
    glow(c, 960, 700, 700, (1, 0.85, 0.6), 0.25)
    for i in range(14):
        x = 200 + i * 115
        man(c, x, 900, 0.9, pose='bow', p=ease((lt - 0.4 - i * 0.05) / 0.8), face=1, a=0.9)
        bouquet(c, x + 30, 900 - 80, 0.35, a=0.9)
    ground(c, 900)
    candle(c, 960, 700, lt, 140)

def S_end(c, lt, d, p):
    bg(c, (0.20, 0.10, 0.05), (0.06, 0.04, 0.03))
    glow(c, 960, 860, 700, (1, 0.6, 0.3), 0.4)
    auditorium(c, 960, 860, 0.9)
    ground(c, 860)
    # 起点与终点：一个圆
    k = ease(p)
    c.set_source_rgba(*GOLD, 0.8); c.set_line_width(4)
    c.arc(960, 500, 300, -1.5708, -1.5708 + 6.2832 * k); c.stroke()
    c.set_source_rgba(*GOLD, 1); c.arc(960, 200, 10, 0, 6.28); c.fill()

def S_end2(c, lt, d, p):
    bg(c, (0.0, 0.0, 0.01), (0.04, 0.04, 0.06))
    sh = 0.5 + 0.12 * math.sin(lt * 0.8)
    mirror(c, 1200, 520, 1.0, shards=sh * (1 - 0.3 * p), t=lt, seed=4)
    glow(c, 760, 700, 380, (1, 0.9, 0.7), 0.25 + 0.3 * ease(p))
    man(c, 760, 900, 1.3, glasses=True, face=1, pose='stand')
    ground(c, 900)
