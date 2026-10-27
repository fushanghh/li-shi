from frame import *
from scenes1 import _CAM, NONE, NOSEAL, NS_NW, face_at

SEAL = {'seal': True}
BLADE = {'wpn': 'blade', 'seal': False, 'one_hand': True}

def ctr(p, g, t, label, marks):
    cur = None
    for mb, v in marks:
        if t >= mb * B: cur = (v, mb * B)
    if cur: counter(p, g, label, cur[0], t, cur[1])

def pieces(p, x, y, t, t0, n=6, col='WOOD', seed=0, size=1.0, w=10):
    if t < t0: return
    k = t - t0; rnd = random.Random(seed)
    for i in range(n):
        vx = rnd.uniform(-600, 600) * size; vy = rnd.uniform(-900, -200) * size; L = rnd.uniform(30, 70) * size
        px = x + vx * k; py = min(GY + 10, y + vy * k + 2400 * k * k); an = rnd.uniform(0, 6) + k * rnd.uniform(-12, 12)
        if py >= GY + 10: an = 0
        p.line([(px - math.cos(an) * L, py - math.sin(an) * L), (px + math.cos(an) * L, py + math.sin(an) * L)], 'BLK', w + 4); p.line([(px - math.cos(an) * L, py - math.sin(an) * L), (px + math.cos(an) * L, py + math.sin(an) * L)], col, w)

def cangue(p, hd, sc=1.0):
    x, y = hd
    p.poly([(x - 70 * sc, y + 40 * sc), (x + 70 * sc, y + 40 * sc), (x + 70 * sc, y + 62 * sc), (x - 70 * sc, y + 62 * sc)], 'WOOD', 'BLK', 3)
    p.ell(x - 50 * sc, y + 51 * sc, 4, 4, 'BLK'); p.ell(x + 50 * sc, y + 51 * sc, 4, 4, 'BLK')

def bound_walk(t, ph=0.0):
    q = walk(t, 0.9, ph); q.update(uaF=60, faF=100, uaB=50, faB=100); return q

# ======================= 4 白虎堂 =======================
@shot(5, trans='slide', cam=camk([(0, (500, 560, 1.0)), (5, (560, 540, 1.12))], fn=lambda x: x),
      caps=[(0, '街上偶遇一口宝刀，', '寒光逼人', (), ((3, 5),))], ev=[(1, 'shimmer'), (3, 'shimmer'), (0, 'wood')], name='street')
def street(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_street(p, g, t, cam)
    q_s = anim(t, kb([(0, 'idle'), (0.8, 'guardH'), (2.6, 'guardH'), (3, 'idle')]))
    figure(p, g, 700, GY, 0.95, -1, q_s, 'seller', t=t, extra={'wpn': 'blade' if b < 3 else None, 'one_hand': True})
    q_l = anim(t, kb([(0, 'idle'), (1.6, 'point'), (2.8, 'point'), (3.1, 'guardH')]))
    o = figure(p, g, 420, GY, 1.0, 1, q_l, 'lin', t=t, extra=dict(BLADE, wpn='blade' if b >= 3 else None))
    for tb, (x, y) in [(1, (560, 470)), (3.2, (o['tip'][0], o['tip'][1]))]:
        k = (t - tb * B) / 0.6
        if 0 <= k <= 1: star(g, x, y, 90 * math.sin(k * math.pi), 'CREAM', 1, k * 2)

@shot(5, trans='slide', cam=camk([(0, (300, 540, 1.0)), (5, (540, 540, 1.0))]),
      caps=[(0, '太尉请他进府比刀，', '一路领进了白虎节堂', (), ((5, 9),))], ev=[(i * 0.5, 'step') for i in range(6)] + [(2.5, 'title'), (2.5, 'boom')], name='hall_walk')
def hall_walk(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_hall(p, g, t, cam)
    k = clamp(b / 3)
    x = lerp(60, 480, k)
    q = walk(t, 1.0) if b < 3 else anim(t - 3 * B, kb([(0, 'idle'), (0.6, 'guardH')]))
    if b < 3: q = dict(q, uaF=60, faF=110)
    figure(p, g, x, GY, 1.0, 1, q, 'lin', t=t, extra=BLADE)
    for i, off in enumerate((180, 300)):
        cx = x + off if b < 3.4 else x + off + (b - 3.4) * 900
        figure(p, g, cx, GY, 0.95, 1, walk(t, 1.0, i), 'cop', t=t, extra=NONE)
def hall_walk_ov(p, g, t):
    pass
SHOTS[-1].ov = hall_walk_ov

def dais(p, x):
    p.poly([(x - 220, GY), (x + 300, GY), (x + 300, GY - 120), (x - 160, GY - 120)], 'BLK', 'LN', 3)
    for k in range(3): p.line([(x - 200 + k * 20, GY - 30 - k * 30), (x + 300, GY - 30 - k * 30)], 'LN2', 2)

@shot(2, cam=camk([(0, (800, 520, 1.0)), (1.2, (900, 450, 1.5)), (2, (900, 450, 1.55))]), ev=[(0.4, 'boom'), (0.4, 'title')],
      caps=[(0, '高太尉一声断喝：', '持刀擅闯节堂，拿下！', (), ((7, 10),))], name='gq')
def gqs(p, g, t):
    cam = _CAM['cur']
    bg_hall(p, g, t, cam, plaque_on=True)
    dais(p, 900)
    figure(p, g, 920, GY - 120, 1.0, -1, anim(t, kb([(0, 'idle'), (0.4, 'point', 'snap')])), 'gq', t=t)
    figure(p, g, 420, GY, 1.0, 1, 'guardH', 'lin', t=t, extra=BLADE)
def gqs_ov(p, g, t):
    onomato(p, '拿下！', 700, 330, t, 0.4 * B, 130, 'RED', 1.2)
    nametag(p, 'GAO QIU', '殿帅府太尉 · 高俅', 300, 200, t, 0.2, 2 * B)
SHOTS[-1].ov = gqs_ov

# 围攻军汉
def guard_ring(p, g, t, b, cx, n, radius, y0, sc, seed, poseB='guard', enter=None):
    """一圈军汉（前后两层，画在指定层）"""
    out = []
    for i in range(n):
        side = -1 if i % 2 == 0 else 1
        d = radius + (i // 2) * 90
        x = cx + side * d
        if enter is not None:
            k = eo(clamp((b - enter[0]) / enter[1] - i * 0.03))
            x = lerp(cx + side * (d + 900), x, k)
        figure(p, g, x, y0, sc, -side, poseB, 'guard', t=t + i)
        out.append(x)
    return out

@shot(3, cam=camk([(0, (540, 560, 1.1)), (3, (540, 560, 0.95))]), ev=[(0, 'whoosh'), (0.5, 'step'), (1, 'step'), (1.5, 'step'), (2, 'boom')],
      caps=[(0, '堂上军汉，', '从两边一拥而上', ((0, 4),), ())], name='surround')
def surround(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_hall(p, g, t, cam, plaque_on=False)
    guard_ring(p, g, t, b, 540, 10, 260, GY - 50, 0.72, 1, 'guard', (0, 1.6))
    haze(p, '#7a321a', 0.35)
    figure(p, g, 540, GY, 1.05, 1, anim(t, kb([(0, 'guardH'), (2, 'coil')])), 'lin', t=t, extra=BLADE)
    guard_ring(p, g, t, b, 540, 6, 220, GY + 50, 1.05, 2, 'guard', (0.3, 1.6))

# 大战：每个军汉一条记录：(x, y, sc, face, hit_beat, vx, vy, spin)
HF = []
for i, (d, sd) in enumerate([(200, -1), (200, 1), (290, -1), (290, 1), (380, -1), (380, 1)]):
    HF.append((540 + sd * d, GY, 1.0, -sd, 1.0 + i * 0.04, sd * (700 + i * 40), -650 - i * 30, 500))
for i in range(3): HF.append((800 + i * 60, GY, 1.0, -1, 3.5, 300 + i * 120, -900 + i * 60, 600))
for i, x in enumerate((690, 590, 490, 390)): HF.append((x, GY, 1.0, 1, 4.6 + i, -500 - i * 60, -700, 500 if i % 2 else 0))
for i in range(5): HF.append((150 + i * 70, GY, 1.0, 1, 9.0 + i * 0.03, -800 - i * 60, -500 - i * 40, 500))
HALL_KEYS = kb([(0, 'coil'), (0.2, 'spinA'), (1.0, 'spinA'), (1.4, 'guard'), (2.2, 'coil'), (2.5, 'jump', 'out'), (3.4, 'jump'), (3.5, 'smash', 'snap'), (4.2, 'guard'),
                (4.6, 'swingR', 'snap'), (5.2, 'guard'), (5.6, 'smash', 'snap'), (6.2, 'guard'), (6.6, 'swingR', 'snap'), (7.2, 'guard'), (7.6, 'thrust', 'snap'), (8.2, 'guard'),
                (8.7, 'coil'), (9, 'sweepL', 'snap'), (9.8, 'guard'), (12, 'guard')])
HALL_X = kb([(0, 540), (2.4, 540), (3.5, 820, 'io'), (4.3, 820), (4.6, 720), (5.3, 720), (5.6, 620), (6.3, 620), (6.6, 520), (7.3, 520), (7.6, 420), (8.4, 420), (12, 420)])
def hall_face(tt):
    b = tt / B
    if b < 1.0: return 1 if int(b * 8) % 2 == 0 else -1
    if b < 4.2: return 1
    if b < 8.4: return -1
    return -1
def hall_lin(q, tt, gg=None):
    b = tt / B
    jy = -math.sin(clamp((b - 2.5) / 1.0) * math.pi) * 330 if 2.5 <= b < 3.5 else 0
    return figure(q, gg, track(tt, HALL_X), GY + jy, 1.05, hall_face(tt), anim(tt, HALL_KEYS), 'lin', t=tt, wind=0.6, extra=BLADE)

@shot(12, cam=lambda t: (lerp(track(t, HALL_X), 540, 0.4), 560 - (30 if 2.5 * B < t < 3.6 * B else 0), 1.0 - 0.06 * (1 if t > 8.5 * B else 0)),
      caps=[(0, '一刀转一圈，', '倒下一片', (), ((0, 4),)), (4, '刀光过处，', '一排接一排地倒', (), ()), (8.5, '人越打越多，', '刀却越来越快', (), ((5, 8),))],
      ev=[(0.2, 'whoosh'), (0.6, 'swish'), (1, 'hit'), (1.05, 'hit'), (2.5, 'whoosh'), (3.5, 'land'), (3.5, 'clang'), (4.6, 'hit'), (5.6, 'hit'), (6.6, 'hit'), (7.6, 'hit'), (8.6, 'step'), (9, 'hit'), (9, 'boom'), (10.5, 'tension')], name='hall_fight')
def hall_fight(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_hall(p, g, t, cam, plaque_on=False)
    # 后排一直有人
    for i in range(14):
        x = -300 + i * 120 + (30 if i % 2 else 0)
        adv = 60 * eo(clamp((b - 10) / 1.5))
        figure(p, None, x + (adv if x < 420 else -adv), GY - 70, 0.55, 1 if x < track(t, HALL_X) else -1, 'guard' if b < 10 else 'thrust', 'guard', t=t + i)
    haze(p, '#7a321a', 0.45)
    # 第二波：从左冲来
    for rec in HF:
        x, y, sc, f, hb, vx, vy, spin = rec
        if hb >= 9:
            xx = lerp(x - 700, x, eo(clamp((b - 7.6) / 1.2)))
            if b < hb: figure(p, g, xx, GY, sc, f, walk(t, 2.2) if b < 8.8 else 'guard', 'guard', t=t)
            else: ragdoll(p, g, 'guard', f, sc, x, t, hb * B, vx, vy, spin, slide=100)
        else:
            ragdoll(p, g, 'guard', f, sc, x, t, hb * B, vx, vy, spin, slide=100)
    o = hall_lin(p, t, g)
    draw_trail(g, hall_lin, t, 8, 1 / 60, 'CREAM', 26, 500)
    if b < 1.1:
        k = clamp(b / 1.0)
        g.c.save(); g.c.translate(540, GY - 170); g.c.scale(1, 0.32)
        g.arc(0, 0, 240, -math.pi / 2, -math.pi / 2 + k * 2 * math.pi, 'CREAM', 18, 0.8); g.c.restore()
    for hb, x, y, sz in [(1, 330, 640, 1.0), (1.05, 760, 640, 1.0), (3.5, 860, 760, 1.2), (4.6, 660, 640, 0.8), (5.6, 560, 660, 0.8), (6.6, 460, 640, 0.8), (7.6, 340, 640, 0.8), (9, 240, 680, 1.2)]:
        impact(p, g, x, y, t, hb * B, sz, seed=int(hb * 10))
    pieces(p, 860, 760, t, 3.5 * B, 8, 'WOOD', 3)
    dust(p, 820, GY, t, 3.5 * B, 1.2); shockring(p, g, 820, GY, t, 3.5 * B, 1.0)
    shockring(p, g, 420, GY, t, 9 * B, 1.3)
    # 前排压阵
    if b > 10:
        for i, x in enumerate((140, 250, 600, 710)):
            figure(p, g, x, GY + 50, 1.05, 1 if x < 420 else -1, 'thrust', 'guard', t=t)
def hall_fight_ov(p, g, t):
    ctr(p, g, t, '放倒军汉', [(1, '×6'), (3.5, '×9'), (4.6, '×10'), (5.6, '×11'), (6.6, '×12'), (7.6, '×13'), (9, '×18')])
    onomato(p, '唰——', 760, 300, t, 0.3 * B, 90, 'CREAM', 0.8)
    onomato(p, '咔嚓！', 820, 360, t, 3.5 * B, 100, 'GOLD', 0.7)
SHOTS[-1].ov = hall_fight_ov

@shot(4, cam=camk([(0, (520, 520, 1.25)), (4, (520, 540, 1.4))], fn=lambda x: x),
      caps=[(0, '几十杆枪顶在喉咙前，', '刀，他自己放下了', (), ((0, 4),))], ev=[(0, 'swish'), (1, 'tension'), (2, 'clang'), (2.5, 'thud'), (3, 'wood')], name='drop')
def drop(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_hall(p, g, t, cam, plaque_on=False)
    q = anim(t, kb([(0, 'guard'), (1.6, 'guard'), (2.0, 'fistLow'), (2.6, 'kneel')]))
    o = figure(p, g, 420, GY, 1.05, -1, q, 'lin', t=t, extra=dict(BLADE, wpn='blade' if b < 2 else None))
    hd = o['head']; tx, ty = hd[0], hd[1] + 50 + (60 if b > 2.4 else 0)
    k = eo(clamp(b / 1.0))
    rnd = random.Random(2)
    for i in range(12):
        an = math.pi * (0.1 + 0.8 * i / 11) * (1 if i % 2 else -1) + (0 if i % 2 else math.pi)
        r0, r1 = 900, lerp(700, 60, k) + rnd.uniform(0, 20)
        x0, y0 = tx + math.cos(an) * r0, ty + math.sin(an) * r0 * 0.35 - 30
        x1, y1 = tx + math.cos(an) * r1, ty + math.sin(an) * r1 * 0.35
        p.line([(x0, y0), (x1, y1)], 'BLK', 9); p.poly([(x1, y1 - 7), (x1, y1 + 7), (x1 - math.cos(an) * 40, y1 - math.sin(an) * 14)], 'CREAM')
    if b >= 2:
        kk = clamp((b - 2) / 0.5)
        bx, by = lerp(o['hand'][0], 300, kk), lerp(o['hand'][1], GY - 8, ei(kk))
        p.c.save(); p.c.translate(bx, by); p.c.rotate(lerp(-1.2, 0, kk)); p.poly([(0, -6), (150, -4), (170, 0), (150, 8), (0, 8)], 'CREAM', 'BLK', 2); p.rect(-24, -8, 24, 16, 'GOLD'); p.c.restore()
        clash(p, g, 380, GY - 10, t, 2.5 * B, 0.6)
def drop_ov(p, g, t):
    if t >= 2.5 * B: counter(p, g, '退', '×2', t, 2.5 * B)
    onomato(p, '哐当', 300, 760, t, 2.5 * B, 70, 'CREAM', 1.0)
SHOTS[-1].ov = drop_ov

@shot(3, cam=camk([(0, (540, 560, 1.0)), (3, (540, 560, 1.06))]), caps=[(0, '刺配沧州，', '脸上烙了金印', ((0, 4),), ((4, 6),))],
      ev=[(0.5, 'stamp'), (0.5, 'flash'), (0.6, 'gong')], name='seal')
def sealsh(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_hall(p, g, t, cam, plaque_on=True)
    dais(p, 900); figure(p, g, 920, GY - 120, 1.0, -1, 'point', 'gq', t=t)
    guard_ring(p, g, t, b, 540, 8, 300, GY - 40, 0.72, 4, 'guard')
    haze(p, '#7a321a', 0.35)
    o = figure(p, g, 540, GY, 1.05, 1, 'kneel', 'lin', t=t, extra={'seal': b >= 0.5, 'wpn': None})
    impact(p, g, o['head'][0] - 15, o['head'][1] + 15, t, 0.5 * B, 0.6)
def seal_ov(p, g, t):
    seal_stamp(p, g, '刺配沧州', 540, 380, t, 0.5 * B)
SHOTS[-1].ov = seal_ov

# ======================= 5 野猪林 =======================
@shot(4, trans='slide', cam=camk([(0, (420, 560, 1.0)), (4, (620, 560, 1.0))], fn=lambda x: x),
      caps=[(0, '发配路上，', '两个公差一路棍棒伺候', (), ((2, 4),))], ev=[(1, 'whip'), (2, 'whip'), (3, 'whip')] + [(i * 0.5, 'step') for i in range(8)], name='road')
def road(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_road(p, g, t, cam)
    crows(p, t, -200 + b * 40, 200, 5, 2)
    x = 300 + b * 70
    figure(p, g, x + 260, GY, 0.95, 1, walk(t, 0.9, 1), 'cop', t=t)
    o = figure(p, g, x, GY, 1.0, 1, bound_walk(t), 'lin', t=t, extra=NONE)
    cangue(p, o['head'])
    q = anim(t, kb([(0, 'walkA'), (0.7, 'raiseO'), (1, 'smash', 'snap'), (1.7, 'raiseO'), (2, 'smash', 'snap'), (2.7, 'raiseO'), (3, 'smash', 'snap'), (3.6, 'walkB')]))
    figure(p, g, x - 230, GY, 0.95, 1, q, 'cop', t=t)
def road_ov(p, g, t):
    nametag(p, 'DONG CHAO', '公差 · 董超', 160, 300, t, 0.2, 3 * B, 'l')
    nametag(p, 'XUE BA', '公差 · 薛霸', 760, 300, t, 0.5 * B, 3 * B)
    for b0, x in ((1, 360), (2, 420), (3, 480)): onomato(p, '啪！', x, 470, t, b0 * B, 66, 'CREAM', 0.4)
SHOTS[-1].ov = road_ov

def big_tree(p, x, rot=0.0):
    p.c.save(); p.c.translate(x, GY - 300); p.c.rotate(rot); p.c.translate(-x, -(GY - 300))
    gnarled(p, x, GY, 760, 1.25, 'BLK', seed=77); p.c.restore()

@shot(4, trans='slide', cam=camk([(0, (560, 560, 1.0)), (4, (560, 470, 1.45))], fn=lambda x: x),
      caps=[(0, '野猪林里，绑上大树，', '他闭上眼，又退了一步', ((0, 3),), ((8, 11),))], ev=[(0, 'wind'), (2, 'wood'), (3, 'tension')], name='bound')
def boundsh(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_forest(p, g, t, cam)
    big_tree(p, 560)
    o = figure(p, g, 560, GY, 1.0, 1, 'bound', 'lin', t=t, extra=NONE); cangue(p, o['head'])
    for k in range(3): p.line([(480, GY - 230 + k * 50), (640, GY - 220 + k * 50)], 'CREAM', 5)
    q = anim(t, kb([(0, 'idle'), (2, 'raiseO')]))
    figure(p, g, 340, GY, 1.0, 1, q, 'cop', t=t); figure(p, g, 790, GY, 1.0, -1, q, 'cop', t=t)
def bound_ov(p, g, t):
    if t >= 2 * B: counter(p, g, '退', '×3', t, 2 * B)
SHOTS[-1].ov = bound_ov

def chan_fly(p, g, t, t0, t1, x0, y0, x1, y1):
    if t < t0 or t > t1: return
    k = (t - t0) / (t1 - t0); x, y = lerp(x0, x1, k), lerp(y0, y1, k); an = t * 22
    for i in range(10):
        kk = max(0, k - i * 0.03); g.ell(lerp(x0, x1, kk), lerp(y0, y1, kk), 40 * (1 - i / 10), 40 * (1 - i / 10), 'GOLD', a=0.4 * (1 - i / 10))
    p.c.save(); p.c.translate(x, y); p.c.rotate(an)
    p.line([(-170, 0), (170, 0)], 'BLK', 16); p.ell(170, 0, 34, 34, 'CREAM', 'BLK', 4); p.ell(170, 0, 13, 13, 'BLK'); p.poly([(-170, -14), (-170, 14), (-210, 0)], 'CREAM')
    p.c.restore()
    g.c.save(); g.c.translate(x, y); g.c.rotate(an); g.arc(0, 0, 175, 0, 2.5, 'CREAM', 10, 0.7); g.c.restore()

@shot(3, cam=camk([(0, (560, 520, 1.2)), (3, (560, 520, 1.0))]), caps=[(0, '水火棍刚要落下——', '', (), ())],
      ev=[(0.6, 'whoosh'), (1.0, 'whoosh'), (2, 'clang'), (2, 'flash'), (2, 'hit')], name='staff_down')
def staff_down(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_forest(p, g, t, cam); big_tree(p, 560)
    o = figure(p, g, 560, GY, 1.0, 1, 'bound', 'lin', t=t, extra=NONE); cangue(p, o['head'])
    for k in range(3): p.line([(480, GY - 230 + k * 50), (640, GY - 220 + k * 50)], 'CREAM', 5)
    q = anim(t, kb([(0, 'raiseO'), (2, 'smash', 'in')])) if b < 2 else 'cower'
    broken = b >= 2
    figure(p, g, 340, GY, 1.0, 1, q, 'cop', t=t, extra={'wpn': None} if broken else None)
    figure(p, g, 790, GY, 1.0, -1, q, 'cop', t=t, extra={'wpn': None} if broken else None)
    chan_fly(p, g, t, 0.6 * B, 2 * B, -250, -200, 560, 560)
    clash(p, g, 560, 560, t, 2 * B, 1.4); impact(p, g, 560, 560, t, 2 * B, 1.2)
    pieces(p, 470, 560, t, 2 * B, 4, 'WOOD', 5); pieces(p, 650, 560, t, 2 * B, 4, 'WOOD', 6)
def staff_ov(p, g, t):
    onomato(p, '呼——！', 260, 240, t, 0.7 * B, 110, 'CREAM', 1.2)
    onomato(p, '铛！', 760, 420, t, 2 * B, 130, 'GOLD', 0.9)
SHOTS[-1].ov = staff_ov

@shot(3, cam=camk([(0, (640, 470, 1.05)), (3, (640, 520, 1.0))]), caps=[(0, '禅杖天降，', '花和尚到了！', ((0, 4),), ((0, 3),))],
      ev=[(0, 'whoosh'), (0.6, 'land'), (0.6, 'crash'), (1, 'title')], name='lu_land')
def lu_land(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_forest(p, g, t, cam); big_tree(p, 400)
    o = figure(p, g, 400, GY, 1.0, 1, 'bound', 'lin', t=t, extra=NONE); cangue(p, o['head'])
    k = clamp(b / 0.6)
    ly = lerp(-700, GY, ei(k))
    q = 'jump' if b < 0.6 else anim(t - 0.6 * B, kb([(0, 'land'), (1.2, 'smash')]))
    figure(p, g, 760, ly, 1.3, -1, q, 'lu', t=t, wind=0.5)
    if b < 0.6: speedlines_screen(p, t, 0, 0.6 * B, math.pi / 2, 18, 'CREAM', 5)
    if b >= 0.6:
        rnd = random.Random(1)
        for i in range(9):
            an = rnd.uniform(-0.3, math.pi + 0.3); L = rnd.uniform(120, 340) * eo((b - 0.6) / 0.4)
            p.line([(760, GY + 6), (760 + math.cos(an) * L, GY + 6 + abs(math.sin(an)) * 40)], 'GOLD', 3)
    dust(p, 760, GY, t, 0.6 * B, 1.6, n=12); shockring(p, g, 760, GY, t, 0.6 * B, 1.6)
    for x, f in ((180, 1), (1000, -1)):
        figure(p, g, x, GY, 0.95, f, 'cower' if b < 0.8 else 'hurt', 'cop', t=t, extra=NONE)
def lu_ov(p, g, t):
    big_title(p, g, '禅杖天降', 540, 230, t, 1 * B, size=130)
    nametag(p, 'LU ZHI SHEN', '花和尚 · 鲁智深', 800, 330, t, 1.2 * B, 2 * B)
SHOTS[-1].ov = lu_ov

LU_KEYS = kb([(0, 'guard'), (0.6, 'swingL'), (1, 'swingR', 'snap'), (1.7, 'guard'), (2.6, 'guard'), (3, 'kick', 'snap'), (3.6, 'guard'), (4.2, 'raiseO'), (5, 'smash', 'snap'), (6, 'smash'), (7, 'idle')])
def lu_face(tt):
    b = tt / B
    return -1 if b < 1.8 else (1 if b < 3.8 else 1)
@shot(8, cam=camk([(0, (560, 540, 1.0)), (4, (620, 540, 1.0)), (5, (760, 520, 1.1)), (8, (640, 540, 0.95))]),
      caps=[(0, '一杖一个，', '公差满地找牙', (), ()), (4, '再一禅杖，', '碗口粗的松树拦腰断', (), ((6, 9),))],
      ev=[(0.6, 'whoosh'), (1, 'hit'), (3, 'hit'), (4.2, 'whoosh'), (5, 'hit'), (5, 'crack'), (6.6, 'crash'), (7, 'thud')], name='lu_fight')
def lu_fight(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_forest(p, g, t, cam)
    o_l = figure(p, g, 280, GY, 0.95, 1, 'bound', 'lin', t=t, extra=NONE); cangue(p, o_l['head'])
    # 松树：第5拍被砍断后倒下
    if b < 5: big_tree(p, 1010)
    else:
        kk = ei(clamp((b - 5) / 1.6))
        p.c.save(); gnarled(p, 1010, GY, 180, 1.25, 'BLK', seed=78) if False else p.poly([(1010 - 32, GY), (1010 + 32, GY), (1010 + 26, GY - 200), (1010 - 26, GY - 190)], 'BLK'); p.c.restore()
        p.c.save(); p.c.translate(1010, GY - 200); p.c.rotate(-kk * 1.45); p.c.translate(-1010, -(GY - 200))
        p.c.rectangle(-2000, -2000, 5000, 2000 + GY - 200); p.c.clip(); big_tree(p, 1010); p.c.restore()
    # 公差1 从左冲 → 被扫飞
    if b < 1:
        figure(p, g, lerp(420, 560, eo(b)), GY, 0.95, 1, walk(t, 2), 'cop', t=t, extra=NONE)
    else: ragdoll(p, g, 'cop', 1, 0.95, 560, t, 1 * B, vx=-900, vy=-800, spin=900, slide=80, extra=NONE)
    # 公差2 从右冲 → 被踢飞
    if b < 3:
        figure(p, g, lerp(1200, 860, eo(clamp((b - 1.5) / 1.3))), GY, 0.95, -1, walk(t, 2) if b < 2.8 else 'guard', 'cop', t=t, extra=NONE)
    else: ragdoll(p, g, 'cop', -1, 0.95, 860, t, 3 * B, vx=500, vy=-500, spin=0, slide=40, extra=NONE)
    lx = track(t, kb([(0, 700), (2.4, 700), (3, 740), (4, 780)]))
    o = figure(p, g, lx, GY, 1.3, lu_face(t), anim(t, LU_KEYS), 'lu', t=t, wind=0.4)
    fn = lambda q, tt: figure(q, None, track(tt, kb([(0, 700), (2.4, 700), (3, 740), (4, 780)])), GY, 1.3, lu_face(tt), anim(tt, LU_KEYS), 'lu', t=tt)
    draw_trail(g, fn, t, 8, 1 / 60, 'GOLD2', 34, 500)
    impact(p, g, 560, 600, t, 1 * B, 1.1); impact(p, g, 860, 640, t, 3 * B, 1.0); impact(p, g, 1000, 640, t, 5 * B, 1.4)
    pieces(p, 1000, 680, t, 5 * B, 6, 'WOOD', 9, 1.2)
    dust(p, 1250, GY, t, 6.6 * B, 1.8, n=12)
def lu_fight_ov(p, g, t):
    ctr(p, g, t, '打飞公差', [(1, '×1'), (3, '×2')])
    onomato(p, '咚！', 400, 360, t, 1 * B, 110, 'GOLD', 0.6); onomato(p, '砰！', 900, 380, t, 3 * B, 100, 'GOLD', 0.6)
    onomato(p, '咔——嚓！', 860, 300, t, 5 * B, 110, 'GOLD', 1.0); onomato(p, '轰！', 900, 460, t, 6.6 * B, 120, 'CREAM', 0.8)
SHOTS[-1].ov = lu_fight_ov

@shot(2, cam=camk([(0, (420, 560, 1.15)), (2, (420, 560, 1.2))]), ev=[(1, 'crack'), (1, 'hit')], name='free')
def freesh(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_forest(p, g, t, cam)
    o = figure(p, g, 360, GY, 1.0, 1, 'bound' if b < 1 else 'heroic', 'lin', t=t, extra=NONE)
    if b < 1: cangue(p, o['head'])
    figure(p, g, 560, GY, 1.3, -1, anim(t, kb([(0, 'grab'), (1, 'throw', 'snap')])), 'lu', t=t, extra={'wpn': None})
    pieces(p, o['head'][0], o['head'][1] + 50, t, 1 * B, 6, 'WOOD', 11, 1.0, 14)
    impact(p, g, o['head'][0], o['head'][1] + 50, t, 1 * B, 0.7)

@shot(5, trans='slide', cam=camk([(0, (420, 560, 1.0)), (5, (700, 560, 1.0))], fn=lambda x: x),
      caps=[(0, '一路护送，', '直到沧州', (), ((2, 4),))], ev=[(i * 0.5, 'step') for i in range(10)], name='to_cz')
def to_cz(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_road(p, g, t, cam)
    # 沧州城门
    p.rect(1100, GY - 300, 400, 300, '#5a2a16'); roof(p, 1300, GY - 300, 420, 90, 'BLK'); p.rect(1240, GY - 200, 120, 200, 'BLK')
    p.rect(1240, GY - 290, 120, 50, 'GOLD'); p.text('沧州', 1300, GY - 254, 32, 'BLK')
    x = 260 + b * 80
    figure(p, g, x, GY, 1.0, 1, walk(t, 0.9), 'lin', t=t, extra=NONE)
    figure(p, g, x + 170, GY, 1.25, 1, walk(t, 0.9, 1.6), 'lu', t=t)
def to_cz_ov(p, g, t):
    nametag(p, 'CANG ZHOU', '沧州', 860, 160, t, 1.5 * B, 3.5 * B)
SHOTS[-1].ov = to_cz_ov

# ======================= 6 柴进庄 · 棒打洪教头 =======================
def watchers(p, g, t, cheer=0.0):
    for i in range(16):
        side = -1 if i < 8 else 1; j = i % 8
        x = (40 + j * 40) if side < 0 else (1040 - j * 40)
        y = GY - 110 - (j % 2) * 16
        pose = 'laugh' if cheer and (i + int(t * 4)) % 2 else ('raiseO' if cheer else 'idle')
        figure(p, None, x, y + (math.sin(t * 9 + i) * 6 if cheer else 0), 0.48, -side, pose, 'thug', t=t + i, extra={'kind': {'hat': 'tall' if j % 3 == 0 else 'band'}})
    haze(p, 'BG', 0.3)

@shot(4, trans='slide', cam=camk([(0, (540, 540, 1.0)), (4, (560, 540, 1.04))], fn=lambda x: x),
      caps=[(0, '沧州柴进庄上，', '洪教头偏要比棒', ((2, 5),), ((0, 3),))], ev=[(0, 'wood'), (2, 'swish'), (2.5, 'swish'), (3, 'boom')], name='manor')
def manor(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_manor(p, g, t, cam); watchers(p, g, t)
    figure(p, g, 560, GY, 0.95, 1, anim(t, kb([(0, 'idle'), (0.6, 'pray'), (2, 'point')])), 'chai', t=t)
    figure(p, g, 340, GY, 1.0, 1, 'idle', 'lin', t=t, extra={'wpn': 'staff'})
    q = anim(t, kb([(0, 'idle'), (2, 'raiseO'), (3, 'guard')]))
    if 2 * B <= t < 3 * B: q = dict(q, wp=(t - 2 * B) / B * 720)
    figure(p, g, lerp(1200, 800, eo(clamp(b / 2))), GY, 1.0, -1, q if b > 2 else walk(t, 1.1), 'hong', t=t)
def manor_ov(p, g, t):
    nametag(p, 'CHAI JIN', '小旋风 · 柴进', 560, 330, t, 0.3 * B, 2.5 * B)
    nametag(p, 'HONG', '洪教头', 820, 330, t, 2 * B, 2 * B)
    onomato(p, '来来来！', 820, 260, t, 3 * B, 90, 'CREAM', 1.0)
SHOTS[-1].ov = manor_ov

HONG_K = kb([(0, 'guard'), (0.5, 'raiseO'), (0.9, 'smash', 'snap'), (1.6, 'guard'), (2.1, 'coil'), (2.4, 'thrust', 'snap'), (3.2, 'guard'), (3.8, 'coil'), (4.2, 'sweepL', 'snap'), (5, 'guard'),
             (6, 'thrust', 'snap'), (6.5, 'smash', 'snap'), (7, 'thrustHi', 'snap'), (7.8, 'guard'), (8.3, 'raiseO')])
LIN_K = kb([(0, 'guard'), (0.9, 'blockH', 'snap'), (1.6, 'guard'), (2.4, 'parry', 'snap'), (3.2, 'guard'), (4.0, 'jump', 'out'), (4.7, 'land', 'in'), (5.2, 'guard'),
            (6, 'parry', 'snap'), (6.5, 'blockH', 'snap'), (7, 'parry', 'snap'), (7.8, 'guard'), (8.6, 'coil'), (9, 'sweepL', 'snap'), (10, 'sweepL'), (11, 'guard')])
def lin_duel(q, tt, gg=None):
    b = tt / B
    jy = -math.sin(clamp((b - 4.0) / 0.7) * math.pi) * 240 if 4.0 <= b < 4.7 else 0
    return figure(q, gg, 440, GY + jy, 1.0, 1, anim(tt, LIN_K), 'lin', t=tt, wind=0.4, extra={'wpn': 'staff'})
def hong_duel(q, tt, gg=None):
    return figure(q, gg, 680, GY, 1.0, -1, anim(tt, HONG_K), 'hong', t=tt)

@shot(12, cam=camk([(0, (560, 540, 1.0)), (5.6, (560, 540, 1.0)), (6, (560, 600, 1.32)), (7.6, (560, 600, 1.32)), (8.2, (580, 540, 1.0)), (12, (600, 540, 0.96))]),
      caps=[(0, '洪教头步步紧逼，', '林冲只守不攻', (), ((4, 6),)), (8.4, '第七个回合，', '一棒扫过去', (), ())],
      ev=[(0.5, 'whoosh'), (0.9, 'clang'), (2.4, 'clang'), (3.9, 'whoosh'), (4.2, 'swish'), (4.7, 'land'), (6, 'clang'), (6.5, 'clang'), (7, 'clang'), (8.6, 'tension'), (9, 'hit'), (9, 'whoosh'), (10.4, 'thud'), (10.4, 'title')], name='duel')
def duel(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_manor(p, g, t, cam); watchers(p, g, t)
    figure(p, g, 1000, GY + 20, 0.9, -1, 'idle', 'chai', t=t)
    if b < 9: hong_duel(p, t, g)
    else:
        k = clamp((b - 9) / 1.4)
        if k < 1:
            figure(p, g, lerp(680, 760, k), GY - math.sin(k * math.pi) * 240 + 118 * k * k, 1.0, -1, 'hurt', 'hong', rot=-k * 270, t=t)
        else:
            figure(p, g, 760, GY + 118, 1.0, -1, 'lie', 'hong', rot=-90, t=t)
    lin_duel(p, t, g)
    draw_trail(g, lin_duel, t, 8, 1 / 60, 'CREAM', 22, 600)
    draw_trail(g, hong_duel, t, 8, 1 / 60, 'GOLD', 18, 600) if b < 9 else None
    for hb in (0.9, 2.4, 6, 6.5, 7): clash(p, g, 560, 580 if hb != 2.4 else 700, t, hb * B, 0.8)
    impact(p, g, 700, GY - 40, t, 9 * B, 1.2); dust(p, 760, GY, t, 10.4 * B, 1.3)
def duel_ov(p, g, t):
    ctr(p, g, t, '回合', [(0.9, '×1'), (2.4, '×2'), (4.2, '×3'), (6, '×4'), (6.5, '×5'), (7, '×6'), (9, '×7')])
    for hb in (0.9, 2.4, 6, 6.5, 7): onomato(p, '铛', 560 + (hb * 37 % 200) - 100, 330, t, hb * B, 70, 'CREAM', 0.35)
    big_title(p, g, '一棒', 540, 250, t, 10.4 * B, size=170)
SHOTS[-1].ov = duel_ov

@shot(4, cam=camk([(0, (560, 540, 0.96)), (4, (560, 540, 0.92))]), ev=[(0, 'cheer'), (1, 'cheer'), (2, 'cheer')], name='cheer')
def cheer(p, g, t):
    cam = _CAM['cur']
    bg_manor(p, g, t, cam); watchers(p, g, t, 1.0)
    figure(p, g, 760 + t * 40, GY + 118, 1.0, -1, 'lie', 'hong', rot=-90, t=t)
    figure(p, g, 440, GY, 1.0, 1, 'heroic', 'lin', t=t, extra={'wpn': 'staff'})
    figure(p, g, 1000, GY + 20, 0.9, -1, 'laugh', 'chai', t=t)
def cheer_ov(p, g, t):
    onomato(p, '好！', 300, 330, t, 0.1, 110, 'GOLD', 1.2); onomato(p, '好！', 820, 300, t, 1 * B, 110, 'GOLD', 1.2)
SHOTS[-1].ov = cheer_ov
