from kit import *
import math

# 每个场景: f(c, lt, d, p) ; p=lt/d 进度
def S_hook(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.03, 0.03)), (1, (0.05, 0.04, 0.03))])
    dust(c, lt, 50, JADE, a=0.35)
    seal(c, W / 2 + 120, 560 + 10 * math.sin(lt * 2), 1.5, t=lt)
    for i, (x, y, an) in enumerate(((-200, 1200, -0.75), (300, 1250, -1.1), (2100, 1150, -2.4), (1700, 1300, -2.0), (-250, 700, -0.15), (2150, 650, -3.0))):
        k = eout((lt - 0.12 * i) / 1.6)
        hand(c, x, y, an, L=380 + 230 * k, a=0.97, open_=0.3 + 0.5 * math.sin(lt * 3 + i) ** 2)

def S_hook2(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.03, 0.03, 0.03)), (1, (0.08, 0.06, 0.04))])
    c.set_source_rgba(0.2, 0.15, 0.1, 1); c.rectangle(0, 820, W, 260); c.fill()
    k = ease((p - 0.25) / 0.45)
    stone(c, lerp(W / 2, 640, k), 760, 1.8, a=1 - k * 0.0, lit=0.2)
    if k > 0:
        c.set_source_rgba(*GOLD, k); c.set_line_width(5); c.set_dash([18, 14])
        c.move_to(820, 680); c.line_to(lerp(820, 1150, k), 680); c.stroke(); c.set_dash([])
        poly(c, [(1150, 660), (1180, 680), (1150, 700)], GOLD, k)
        seal(c, 1420, 700, 1.4 * k, a=k, t=lt)

def S_hook3(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.06, 0.02, 0.02)), (0.7, (0.25, 0.06, 0.03)), (1, (0.05, 0.02, 0.02))])
    seal(c, W / 2, 560, 1.0, t=lt)
    for i in range(7):
        x = 260 + i * 233 if i < 3 else 260 + (i + 1) * 233 - 233 + 233
        x = [240, 460, 680, 1240, 1460, 1680, 1880][i]
        k = ease((lt - 0.8 - i * 0.45) / 0.5)
        if k > 0: redflash(c, 0)
        sil(c, x, 930, 1.05, hat='mian', pose='lie' if k > 0 else 'stand', p=k, face=1 if x < W / 2 else -1)
    vgrad(c, 980, H, [(0, (0.03, 0.01, 0.01)), (1, (0, 0, 0))])

def S_title(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.02, 0.02)), (1, (0.07, 0.05, 0.03))])
    glow(c, W / 2, 760, 700, (0.9, 0.6, 0.3), 0.18)
    c.set_source_rgb(*INK); c.rectangle(560, 800, 800, 26); c.fill(); c.rectangle(600, 826, 24, 200); c.fill(); c.rectangle(1296, 826, 24, 200); c.fill()
    stone(c, W / 2, 770, 1.4, lit=0.6 + 0.3 * math.sin(lt * 3))
    sil(c, 330, 1000, 1.25, hat='bun', pose='kneel', a=0.95)
    sil(c, 1620, 1000, 1.3, hat='mian', pose='stand', face=-1)
    a = ease(lt / 0.4)
    text(c, "假 如 你 是 和 氏 璧", W / 2, 300, 34, GOLD, a, 'c')
    text(c, "从石头到传国玉玺", W / 2, 410, 80, (1, 0.96, 0.9), a, 'c')
    c.save(); w = 0
    text(c, "你害死了多少个皇帝？", W / 2, 520, 92, (0.95, 0.30, 0.24), ease((lt - 0.5) / 0.4), 'c')
    c.restore()

def S_mount(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.03, 0.05)), (1, (0.08, 0.08, 0.10))])
    stars(c, lt, 90); moon(c, 1500, 230, 55)
    mountains(c, lt)
    k = ease((p - 0.2) / 0.5)
    sil(c, 900, 950, 1.3, hat='bun', pose='bow', p=k)
    stone(c, 1060, 945, 0.55, lit=0.5 + 0.5 * k)

def _court(c, lt, d, p, n):
    palace(c, lt)
    # 王座
    c.set_source_rgb(*INK); c.rectangle(1360, 760, 420, 80); c.fill(); c.rectangle(1400, 700, 340, 60); c.fill()
    sil(c, 1560, 700, 1.15, hat='mian', pose='sit', face=-1)
    k = ease((p - 0.15) / 0.3)
    sil(c, 960, 840, 1.15, hat='guan', pose='offer', p=k, face=-1)
    stone(c, lerp(560, 860, k), lerp(780, 650, k), 0.45, lit=0.3)
    hit = (p - 0.62)
    if hit < 0: sil(c, 520, 840, 1.1, hat='bun', pose='kneel')
    else: sil(c, 520, 840, 1.1, hat='bun', pose='cry', p=ease(hit / 0.2))
    if 0 < hit < 0.25: redflash(c, 1 - hit / 0.25)
    if n == 2 and p > 0.0:
        pass

def S_court1(c, lt, d, p): _court(c, lt, d, p, 1)
def S_court2(c, lt, d, p): _court(c, lt, d, p, 2)

def S_cry(c, lt, d, p):
    # 三天三夜：日月轮转
    cyc = p * 3.0; ph = cyc % 1
    day = math.sin(ph * math.pi)
    sky = mix((0.02, 0.03, 0.05), (0.30, 0.18, 0.12), day * 0.8)
    vgrad(c, 0, H, [(0, sky), (1, mix(sky, (0.1, 0.06, 0.04), 0.5))])
    stars(c, lt, 80, a=1 - day)
    ang = math.pi * (1 - ph); cx, cy = W / 2 + math.cos(ang) * 800, 800 - math.sin(ang) * 600
    if day > 0.02 and int(cyc) == int(cyc): glow(c, cx, cy, 200, (1, 0.7, 0.4), 0.5 * day)
    moon(c, W / 2 - math.cos(ang) * 800, 800 - math.sin(ang) * 600, 45, a=1 - day)
    mountains(c, lt)
    sil(c, W / 2 - 40, 960, 1.4, hat='bun', pose='cry', p=1)
    stone(c, W / 2 + 60, 900, 0.5, lit=0.4)
    tear = (1, 1, 1) if p < 0.7 else (0.85, 0.12, 0.1)
    for i in range(4):
        y = 760 + ((lt * 160 + i * 50) % 160)
        c.set_source_rgba(*tear, 0.9); c.arc(W / 2 + 10, y, 6, 0, 6.28); c.fill()

def S_reveal(c, lt, d, p):
    palace(c, lt, candles=((620, 760), (1300, 760)))
    c.set_source_rgb(*INK); c.rectangle(700, 790, 520, 22); c.fill(); c.rectangle(730, 812, 20, 40); c.fill(); c.rectangle(1170, 812, 20, 40); c.fill()
    k = ease((p - 0.1) / 0.4); k2 = ease((p - 0.5) / 0.3)
    if k2 < 1: stone(c, W / 2, 760, 1.3, a=1 - k2, crack=k, lit=0.4 + k)
    if k2 > 0:
        bi(c, W / 2, lerp(740, 600, k2), lerp(0.4, 1.3, k2), a=k2, rot=lt * 0.2)
    sil(c, 520, 840, 1.15, hat='bun', pose='kneel')
    sil(c, 1450, 840, 1.15, hat='mian', pose='stand', face=-1)

def S_qin15(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.10, 0.06, 0.08)), (0.6, (0.45, 0.25, 0.16)), (1, (0.12, 0.07, 0.05))])
    glow(c, W / 2, 620, 300, (1, 0.8, 0.5), 0.5)
    c.set_source_rgb(*INK); c.rectangle(0, 820, W, 300); c.fill()
    banner(c, 220, 820, "秦", (0.15, 0.15, 0.18), lt); banner(c, 1640, 820, "赵", (0.55, 0.12, 0.10), lt)
    sil(c, 420, 820, 1.2, hat='mian', pose='point')
    bi(c, 1450, 640, 0.75)
    for i in range(15):
        k = ease((p - 0.15 - i * 0.03) / 0.25)
        row, col = divmod(i, 5)
        x = lerp(560, 760 + col * 120, k); y = 560 + row * 90
        if k > 0:
            c.save(); c.translate(x, y); c.set_source_rgba(*GOLD, k)
            c.rectangle(-36, -10, 72, 34); c.fill(); poly(c, [(-44, -10), (44, -10), (30, -32), (-30, -32)], GOLD, k)
            c.set_source_rgba(*INK, k); c.rectangle(-9, 4, 18, 20); c.fill(); c.restore()

def S_pillar(c, lt, d, p):
    palace(c, lt, pillars=(1500,), lattice=True, candles=((700, 760),))
    sil(c, 360, 840, 1.15, hat='mian', pose='point', face=1)
    k = ease((p - 0.25) / 0.3)
    sil(c, 1200, 840, 1.25, hat='guan', pose='raise', p=k, face=1)
    bi(c, lerp(1260, 1290, k), lerp(640, 470, k), 0.42, lit=0.8)
    if k > 0.9: redflash(c, 0.25 * (0.5 + 0.5 * math.sin(lt * 8)))

def S_return(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.03, 0.05)), (1, (0.06, 0.06, 0.08))])
    stars(c, lt); moon(c, 300, 220, 50); mountains(c, lt, base=880)
    c.set_source_rgba(*GOLD, 0.8); c.set_line_width(4); c.set_dash([16, 14])
    x1 = lerp(300, 1500, ease(p))
    c.move_to(200, 900); c.curve_to(600, 820, 1000, 960, x1, 880); c.stroke(); c.set_dash([])
    horse(c, x1, 940, 0.8, lt, rider='bun')
    glow(c, x1 - 10, 760, 60, JADE, 0.9)
    banner(c, 1750, 960, "赵", (0.55, 0.12, 0.10), lt, a=ease((p - 0.6) / 0.3))

def S_handan(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.08, 0.02, 0.02)), (1, (0.35, 0.08, 0.03))])
    citywall(c, 760, (0.12, 0.04, 0.03), 140)
    fires(c, lt, [200, 520, 900, 1300, 1700], 620, 160)
    for i in range(9):
        x = lerp(-200, 2100, ((lt * 0.06) + i / 9) % 1)
        sil(c, x, 1040, 0.8, hat='helm', pose='stand'); c.set_source_rgb(*INK); c.set_line_width(5); c.move_to(x + 20, 1040 - 40); c.line_to(x + 30, 1040 - 300); c.stroke()
    banner(c, 960, 1040, "秦", (0.15, 0.15, 0.18), lt, h=420)
    dust(c, lt, 60, (1, 0.6, 0.3), a=0.7, up=True)

def S_seal(c, lt, d, p):
    palace(c, lt, tone=(0.12, 0.04, 0.03))
    k = ease((p - 0.05) / 0.3)
    if k < 1: bi(c, W / 2, 560, 1.2, a=1 - k)
    if k > 0: seal(c, W / 2, 600, 1.5 * k, a=k, t=lt)
    chars = "受命于天既寿永昌"
    for i, ch in enumerate(chars):
        a = ease((p - 0.45 - i * 0.04) / 0.08)
        x = 560 if i < 4 else 1360; y = 420 + (i % 4) * 110
        text(c, ch, x, y, 88, GOLD, a, 'c')
    sil(c, 260, 1000, 1.3, hat='guan', pose='bow', p=1)

def S_sealq(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.06, 0.03, 0.02)), (1, (0.20, 0.08, 0.04))])
    for i in range(9):
        an = -1.5708 + (i - 4) * 0.18
        c.move_to(W / 2, 560); c.line_to(W / 2 + math.cos(an - 0.04) * 1400, 560 + math.sin(an - 0.04) * 1400); c.line_to(W / 2 + math.cos(an + 0.04) * 1400, 560 + math.sin(an + 0.04) * 1400)
        c.close_path(); c.set_source_rgba(1, 0.85, 0.55, 0.06); c.fill()
    c.set_source_rgb(0.45, 0.06, 0.05); rr(c, W / 2 - 170, 650, 340, 60, 26); c.fill()
    seal(c, W / 2, 600, 1.1, t=lt)
    k = ease(p / 0.6)
    crowd(c, 1000, 8, 0.85, 160, 760, 'bow', 'guan')
    crowd(c, 1000, 8, 0.85, 1160, 1760, 'bow', 'guan')

def S_ziying(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.55, 0.56, 0.58)), (0.75, (0.78, 0.78, 0.76)), (1, (0.62, 0.62, 0.60))])
    c.set_source_rgba(0.85, 0.85, 0.83, 1); c.rectangle(0, 840, W, 240); c.fill()
    for i, x in enumerate((1300, 1460, 1620, 1780)): banner(c, x, 860, "汉", (0.65, 0.10, 0.08), lt, h=360)
    crowd(c, 860, 6, 0.6, 1250, 1850, 'stand', 'helm')
    sil(c, 900, 860, 1.25, hat='bun', pose='kneel', col=(0.95, 0.95, 0.93), face=1)
    c.set_source_rgba(0.1, 0.1, 0.1, 0.9); c.set_line_width(4); c.move_to(905, 640); c.curve_to(870, 700, 860, 760, 870, 860); c.stroke()
    seal(c, 1010, 690, 0.4, t=lt)
    k = ease((p - 0.75) / 0.15)
    if k > 0:
        banner(c, 260, 860, "楚", (0.10, 0.10, 0.10), lt, h=420, a=k)
        redflash(c, k * (1 - ease((p - 0.9) / 0.1)))

def S_wangzh(c, lt, d, p):
    palace(c, lt)
    k = ease((p - 0.45) / 0.15)
    sil(c, 760, 840, 1.25, hat='lady', pose='throw' if k > 0 else 'raise', p=k if k > 0 else 1, face=1)
    if k <= 0: seal(c, 820, 440, 0.38, t=lt)
    else:
        f = ease((p - 0.45) / 0.2); x = lerp(880, 1180, f); y = lerp(480, 820, f ** 1.6)
        seal(c, x, y, 0.38, chip=ease((p - 0.66) / 0.1), t=lt)
        if 0.64 < p < 0.75: redflash(c, 0.6)
    sil(c, 1450, 840, 1.15, hat='guan', pose='kneel', face=-1)

def S_wangd(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.05, 0.01, 0.01)), (1, (0.30, 0.07, 0.03))])
    roofhall(c, W / 2, 820, 1100, 520, (0.05, 0.02, 0.02))
    fires(c, lt, [380, 700, 1220, 1540], 820, 230)
    for j, (x, k0) in enumerate(((760, 0.2), (1160, 0.62))):
        k = ease((p - k0) / 0.15)
        sil(c, x, 1000, 1.3, hat='mian', pose='lie' if k > 0 else 'stand', p=k, face=1 if j == 0 else -1)
        if 0 < p - k0 < 0.08: redflash(c, 0.6)
    c.set_source_rgb(*INK); c.rectangle(0, 1050, W, 40); c.fill()
    dust(c, lt, 50, (1, 0.6, 0.3), a=0.7, up=True)

def _well(c, x, y, s, glowk=0, t=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if glowk > 0:
        cols = [(1, 0.3, 0.3), (1, 0.7, 0.2), (1, 1, 0.4), (0.3, 1, 0.5), (0.4, 0.6, 1)]
        for i, col in enumerate(cols):
            c.move_to(-90 + i * 36, -60); c.line_to(-260 + i * 120 + math.sin(t + i) * 20, -1100); c.line_to(-200 + i * 120 + math.sin(t + i) * 20, -1100); c.line_to(-60 + i * 36, -60); c.close_path()
            c.set_source_rgba(*col, 0.25 * glowk); c.fill()
        glow(c, 0, -60, 260, (1, 0.95, 0.8), 0.6 * glowk)
    c.set_source_rgb(*INK); c.rectangle(-120, -80, 240, 80); c.fill()
    c.set_source_rgba(0.5, 0.4, 0.3, 0.4); c.set_line_width(3); c.rectangle(-120, -80, 240, 80); c.stroke()
    c.set_source_rgb(*INK); c.rectangle(-110, -260, 14, 180); c.fill(); c.rectangle(96, -260, 14, 180); c.fill(); c.rectangle(-130, -270, 260, 18); c.fill()
    c.restore()

def S_well(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.02, 0.04)), (1, (0.06, 0.05, 0.07))])
    stars(c, lt); moon(c, 1600, 200, 45)
    roofhall(c, 400, 860, 700, 380, (0.05, 0.04, 0.05))
    c.set_source_rgb(0.05, 0.04, 0.04); c.rectangle(0, 860, W, 220); c.fill()
    glow(c, 1150, 760, 650, (0.6, 0.65, 0.9), 0.22)
    _well(c, 1100, 900, 1.1)
    k = ease((p - 0.15) / 0.25)
    sil(c, 900, 900, 1.15, hat='guan', pose='throw', p=k)
    if k < 1: seal(c, lerp(960, 1100, k), lerp(680, 760, k) + 200 * max(0, k - 0.7) ** 2, 0.3, t=lt)
    k2 = ease((p - 0.55) / 0.15)
    sil(c, 1550, 900, 1.0, hat='bun', pose='stand', face=-1, a=1 - k2)
    sil(c, 1550, 900, 1.0, hat='bun', pose='lie', face=-1, a=k2, p=1)
    if 0 < p - 0.55 < 0.1: redflash(c, 0.5)

def S_light(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.25, 0.25, 0.27)), (1, (0.40, 0.40, 0.40))])
    citywall(c, 820, (0.12, 0.12, 0.13), 200)
    c.set_source_rgb(0.18, 0.18, 0.19); c.rectangle(0, 900, W, 200); c.fill()
    _well(c, W / 2, 960, 1.2, glowk=ease(p / 0.3), t=lt)
    for x in (400, 560, 1360, 1520): sil(c, x, 960, 0.95, hat='helm', pose='stand', face=1 if x < W / 2 else -1)
    banner(c, 230, 960, "孙", (0.65, 0.10, 0.08), lt, h=380)
    k = ease((p - 0.5) / 0.3)
    if k > 0: seal(c, W / 2, lerp(900, 560, k), 0.75, chip=1, t=lt, a=k)

def S_yuan(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.55, 0.42, 0.28)), (0.8, (0.85, 0.70, 0.48)), (1, (0.60, 0.46, 0.30))])
    c.set_source_rgba(0.45, 0.33, 0.22, 1); c.rectangle(0, 860, W, 220); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(14)
    c.move_to(520, 860); c.line_to(520, 520); c.move_to(1400, 860); c.line_to(1400, 520); c.stroke()
    poly(c, [(420, 540), (1500, 540), (1420, 470), (500, 470)], INK)
    c.set_line_width(10); c.move_to(220, 860); c.line_to(240, 560); c.move_to(235, 650); c.line_to(150, 560); c.move_to(238, 610); c.line_to(320, 520); c.stroke()
    banner(c, 1680, 860, "仲", (0.80, 0.62, 0.15), lt, h=420)
    c.set_source_rgb(*INK); c.rectangle(700, 760, 380, 18); c.fill(); c.rectangle(720, 778, 14, 82); c.fill(); c.rectangle(1050, 778, 14, 82); c.fill()
    k = ease((p - 0.7) / 0.15)
    sil(c, 840, 860, 1.15, hat='mian', pose='sit' if k == 0 else 'lie', p=k * 0.3 if k > 0 else 1)
    seal(c, 1000, 735, 0.25, t=lt)
    sil(c, 1240, 860, 1.15, hat='bun', pose='offer', face=-1, p=0.5)
    c.set_source_rgb(0.25, 0.18, 0.12); c.arc(1150, 700, 26, 0, 6.28); c.fill()
    if 0 < p - 0.7 < 0.1: redflash(c, 0.5)

def S_cere(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.20, 0.12, 0.20)), (0.6, (0.75, 0.48, 0.35)), (1, (0.25, 0.14, 0.12))])
    glow(c, W / 2, 470, 260, (1, 0.9, 0.7), 0.7); c.set_source_rgba(1, 0.93, 0.8, 0.9); c.arc(W / 2, 470, 150, 0, 6.28); c.fill()
    st = 0 if p < 0.5 else 1
    ch, col = [("魏", (0.25, 0.35, 0.60)), ("晋", (0.50, 0.15, 0.45))][st]
    for i in range(3):
        c.set_source_rgba(0.12, 0.08, 0.08, 1); c.rectangle(560 - i * 120, 700 + i * 50, 800 + i * 240, 50); c.fill()
    for x in (160, 380, 1540, 1760): banner(c, x, 900, ch, col, lt, h=420)
    sil(c, 860, 700, 1.0, hat='mian', pose='offer', p=1)
    sil(c, 1060, 700, 1.0, hat='mian', pose='stand', face=-1)
    seal(c, 975, 545, 0.22, chip=1, t=lt)
    crowd(c, 1050, 10, 0.6, 150, 750, 'bow', 'guan'); crowd(c, 1050, 10, 0.6, 1170, 1770, 'bow', 'guan')
    yr = "220" if st == 0 else "265"
    text(c, yr, W - 110, 300, 110, (1, 0.95, 0.88), 0.9, 'r')

def S_huai(c, lt, d, p):
    palace(c, lt, tone=(0.10, 0.06, 0.06))
    c.set_source_rgb(*INK); c.rectangle(1300, 740, 450, 100); c.fill()
    sil(c, 1500, 740, 1.1, hat='helm', pose='sit', face=-1)
    seal(c, 1680, 720, 0.22, chip=1, t=lt)
    crowd(c, 840, 5, 0.75, 180, 700, 'kneel', 'guan')
    k = ease((p - 0.25) / 0.2)
    x = lerp(850, 1150, k)
    sil(c, x, 840, 1.15, hat='guan', pose='offer', p=1, robe=(0.20, 0.40, 0.65), face=1)
    c.set_source_rgba(*GOLD, 1); c.rectangle(x + 105, 668, 30, 22); c.fill()
    if p > 0.85: redflash(c, 1 - (p - 0.85) / 0.15)

def S_liuyao(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.03, 0.03, 0.05)), (1, (0.12, 0.08, 0.06))])
    stars(c, lt); moon(c, 300, 200, 40)
    glow(c, 900, 760, 800, (0.6, 0.6, 0.85), 0.22)
    c.set_source_rgb(*INK); c.rectangle(0, 900, W, 200); c.fill()
    banner(c, 1650, 900, "后赵", (0.30, 0.30, 0.32), lt, h=420)
    k = ease((p - 0.55) / 0.2)
    horse(c, lerp(500, 800, ease(p / 0.55)), 900, 0.9, lt, rider='mian' if k == 0 else None, gallop=k == 0)
    if k > 0:
        sil(c, 1000, 900, 1.1, hat='mian', pose='lie', p=k, face=-1)
        if k < 0.6: redflash(c, 0.5)
    crowd(c, 900, 4, 0.9, 1250, 1560, 'stand', 'helm')

def S_ranmin(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.02, 0.04)), (1, (0.07, 0.05, 0.06))])
    stars(c, lt)
    citywall(c, 820, (0.05, 0.04, 0.05), 220)
    for x in (300, 1620): c.set_source_rgba(1, 0.6, 0.3, 0.9); c.arc(x, 560, 8, 0, 6.28); c.fill(); glow(c, x, 560, 80, (1, 0.6, 0.3), 0.6)
    banner(c, 1500, 1000, "燕", (0.15, 0.30, 0.25), lt, h=440)
    k = ease((p - 0.3) / 0.15)
    sil(c, 900, 1000, 1.2, hat='mian', pose='kneel' if k == 0 else 'lie', p=k)
    sil(c, 1150, 1000, 1.2, hat='helm', pose='sword', p=k, face=-1)
    if 0 < p - 0.3 < 0.08: redflash(c, 0.7)
    k2 = ease((p - 0.55) / 0.35)
    seal(c, lerp(700, 1700, k2), lerp(900, 420, k2), 0.35, chip=1, t=lt)

def S_liangw(c, lt, d, p):
    palace(c, lt, tone=(0.06, 0.06, 0.10), pillars=(200,), curtain=False, candles=((400, 760),))
    g = cairo.LinearGradient(1400, 0, 1700, 0); g.add_color_stop_rgb(0, 0.85, 0.45, 0.15); g.add_color_stop_rgb(1, 0.95, 0.6, 0.25)
    c.set_source(g); c.rectangle(1400, 320, 300, 520); c.fill()
    for x in (1460, 1550, 1640): sil(c, x, 840, 1.0, hat='helm', pose='stand', face=-1); c.set_source_rgb(*INK); c.set_line_width(6); c.move_to(x + 25, 800); c.line_to(x + 30, 380); c.stroke()
    c.set_source_rgb(*INK); c.rectangle(500, 760, 600, 30); c.fill(); c.rectangle(520, 790, 16, 50); c.fill(); c.rectangle(1070, 790, 16, 50); c.fill()
    sil(c, 640, 760, 1.05, hat='mian', pose='lie', p=1, face=1)
    c.set_source_rgba(0.6, 0.6, 0.65, 1); c.save(); c.translate(1200, 820); c.scale(1, 0.4); c.arc(0, 0, 40, 0, 3.14); c.restore(); c.fill()
    seal(c, 1250, 760, 0.25, chip=1, t=lt)
    if p > 0.85: redflash(c, 0.4 * (1 - (p - 0.85) / 0.15))

def S_suiy(c, lt, d, p):
    palace(c, lt, tone=(0.10, 0.05, 0.08))
    k = ease((p - 0.2) / 0.4)
    c.set_source_rgba(0.95, 0.95, 0.92, 0.95); c.set_line_width(16)
    c.move_to(1200, 0)
    for i in range(1, 21):
        yy = i * lerp(10, 34, k); c.line_to(1200 + math.sin(lt * 3 + i * 0.6) * 40, yy)
    c.stroke()
    sil(c, 960, 840, 1.25, hat='mian', pose='stand' if p < 0.7 else 'kneel', face=1)
    sil(c, 1420, 840, 1.15, hat='helm', pose='point', face=-1)
    sil(c, 1560, 840, 1.15, hat='helm', pose='stand', face=-1)
    if 0.7 < p < 0.82: redflash(c, 0.6)

def S_tang(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.02, 0.06)), (1, (0.08, 0.05, 0.08))])
    stars(c, lt); moon(c, 1550, 200, 48)
    roofhall(c, W / 2, 760, 900, 420, (0.04, 0.03, 0.04), lit=True, t=lt)
    rnd = random.Random(9)
    for i in range(160):
        x, y = rnd.uniform(0, W), rnd.uniform(800, 1060)
        a = 0.5 + 0.5 * math.sin(lt * 2 + i)
        c.set_source_rgba(1, 0.7, 0.3, 0.5 + 0.4 * a); c.arc(x, y, 3 + 2 * (y - 800) / 260, 0, 6.28); c.fill()
    yrs = int(lerp(621, 907, ease(p / 0.5)))
    text(c, str(yrs), W - 110, 300, 110, (1, 0.95, 0.88), 0.9, 'r')
    k = ease((p - 0.6) / 0.1)
    if k > 0:
        c.set_source_rgba(0, 0, 0, 0.55 * k); c.paint(); glow(c, 900, 820, 420, (1, 0.6, 0.3), 0.35 * k)
        sil(c, 900, 980, 1.3, hat='mian', pose='drink' if p < 0.8 else 'lie', p=ease((p - 0.8) / 0.12) if p >= 0.8 else ease((p - 0.6) / 0.15), a=1)
        if 0.8 < p < 0.9: redflash(c, 0.6)

def S_liang(c, lt, d, p):
    palace(c, lt, tone=(0.07, 0.04, 0.04), lattice=True, candles=((1500, 780),))
    k = ease((p - 0.55) / 0.12)
    sil(c, 840, 840, 1.25, hat='mian', pose='kneel')
    sil(c, 1120, 840, 1.25, hat='guan', pose='sword', p=k, face=-1)
    seal(c, 600, 780, 0.25, chip=1, t=lt)
    if 0.66 < p < 0.76: redflash(c, 0.7)

def S_tower(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.05, 0.01, 0.01)), (1, lerp(0.2, 0.5, p) * 1 and (lerp(0.2, 0.55, p), 0.10, 0.03))])
    dust(c, lt, 80, (1, 0.6, 0.3), a=0.8, up=True)
    x = W / 2 + 200
    for i in range(4):
        w = 520 - i * 90; y = 1000 - i * 190
        c.set_source_rgb(*INK); c.rectangle(x - w / 2 + 40, y - 150, w - 80, 150); c.fill()
        poly(c, [(x - w / 2 - 30, y - 140), (x + w / 2 + 30, y - 140), (x + w / 2 - 40, y - 190), (x - w / 2 + 40, y - 190)], INK)
        lit = ease((p - 0.3 - i * 0.08) / 0.2)
        for j in range(4):
            c.set_source_rgba(1, 0.75, 0.3, 0.4 + 0.6 * lit); c.rectangle(x - w / 2 + 70 + j * (w - 140) / 4, y - 120, (w - 140) / 4 - 16, 70); c.fill()
    sil(c, x, 240, 0.7, hat='mian', pose='raise', p=1)
    seal(c, x + 40, 15, 0.18, chip=1, t=lt, tassel=False)
    k = ease((p - 0.35) / 0.5)
    fires(c, lt, [x - 330, x - 180, x, x + 180, x + 330, 300, 1700], 1060, lerp(60, 420, k), a=k)
    c.set_source_rgb(*INK); c.rectangle(0, 1040, W, 40); c.fill()

def S_gone(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.03, 0.025, 0.02)), (1, (0.06, 0.045, 0.035))])
    dust(c, lt, 70, (0.7, 0.65, 0.6), a=0.4)
    a = 1 - ease(p / 0.8)
    glow(c, W / 2, 700, 140, JADE, 0.7 * a)
    c.set_source_rgba(0.12, 0.10, 0.08, 1); c.rectangle(0, 800, W, 280); c.fill()

NAMES = ["子婴", "王莽", "刘玄", "刘辩", "袁术", "晋怀帝", "刘曜", "冉闵", "梁武帝", "隋炀帝", "唐哀帝", "朱友贞", "李从珂"]
def S_count(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.02, 0.02)), (1, (0.08, 0.04, 0.03))])
    for i, nm in enumerate(NAMES):
        k = ease((lt - i * 0.18) / 0.3)
        x = 150 + i * 135; y = 900
        glow(c, x, y - 100, 90, (1, 0.5, 0.2), 0.25 * k)
        sil(c, x, y, 0.62, hat='mian', pose='stand', a=k, face=1)
        c.save(); c.translate(x, y + 50)
        text(c, nm, 0, 0, 26, (0.85, 0.80, 0.72), k, 'c', shadow=False); c.restore()
    k = ease((lt - 2.6) / 0.3)
    text(c, "13", W / 2, 600, 220 * (1 + 0.2 * (1 - k)), (0.95, 0.30, 0.24), k, 'c')

def S_stone(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.03, 0.05)), (1, (0.08, 0.08, 0.10))])
    stars(c, lt); moon(c, 1450, 220, 55)
    mountains(c, lt)
    stone(c, W / 2, 900, 1.0, lit=0.3)
    sil(c, W / 2 - 220, 960, 1.3, hat='bun', pose='cry', p=1, a=0.35 * ease((p - 0.4) / 0.3), col=(0.5, 0.5, 0.55))

def S_heart(c, lt, d, p):
    vgrad(c, 0, H, [(0, (0.02, 0.02, 0.02)), (1, (0.06, 0.02, 0.02))])
    k = ease((p - 0.3) / 0.4)
    if k < 1: seal(c, W / 2, 560, 1.3, a=1 - k, t=lt)
    if k > 0: stone(c, W / 2, 600, 1.4, a=k, lit=0.1)
    for i, (x, y, an) in enumerate(((-200, 1200, -0.75), (300, 1250, -1.1), (2100, 1150, -2.4), (1700, 1300, -2.0), (-250, 700, -0.15), (2150, 650, -3.0))):
        hand(c, x, y, an, L=560, a=0.97, col=mix(INK, (0.55, 0.06, 0.04), 0.5 + 0.5 * math.sin(lt * 2 + i)), open_=0.6)
    glow(c, W / 2, 1080, 600, (0.8, 0.1, 0.05), 0.25)

def S_end(c, lt, d, p):
    sky = mix((0.02, 0.03, 0.05), (0.30, 0.20, 0.18), ease(p))
    vgrad(c, 0, H, [(0, sky), (1, (0.10, 0.08, 0.08))])
    glow(c, W / 2, 820, 500, (1, 0.7, 0.4), 0.35 * ease(p))
    mountains(c, lt)
    stone(c, W / 2, 900, 0.9, lit=0.6)
    a = ease((p - 0.4) / 0.3)
    text(c, "假如你是和氏璧", W / 2, 560, 64, GOLD, a, 'c')
    text(c, "— 剧终 —", W / 2, 630, 28, (0.8, 0.75, 0.68), a, 'c', shadow=False)

# 镜头：(起始缩放, 终止缩放, 焦点x, 焦点y)
CAM = {'hook': (1.15, 1.0, 1080, 560), 'title': (1.0, 1.06, 960, 540), 'mount': (1.0, 1.25, 960, 860), 'court1': (1.0, 1.15, 760, 700),
       'court2': (1.15, 1.0, 760, 700), 'cry': (1.0, 1.2, 960, 860), 'reveal': (1.0, 1.3, 960, 640), 'pillar': (1.0, 1.2, 1200, 600),
       'seal': (1.0, 1.1, 960, 560), 'ziying': (1.0, 1.2, 1000, 700), 'wangzh': (1.0, 1.2, 960, 700), 'well': (1.0, 1.15, 1050, 800),
       'light': (1.0, 1.25, 960, 700), 'yuan': (1.0, 1.25, 900, 760), 'huai': (1.0, 1.2, 1100, 700), 'liangw': (1.0, 1.2, 900, 760),
       'tower': (1.0, 1.25, 1160, 500), 'count': (1.0, 1.0, 960, 540), 'heart': (1.0, 1.15, 960, 600), 'end': (1.2, 1.0, 960, 800)}
