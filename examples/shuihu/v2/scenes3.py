from frame import *
from scenes1 import _CAM, NONE
from scenes2 import ctr, pieces

SPEAR = {}
def shoulder_walk(t, ph=0):
    q = walk(t, 0.85, ph); q.update(uaF=150, faF=200, wp=-60); return q

# ======================= 7 风雪山神庙 =======================
def hut(p, x, k):
    p.rect(x - 140, GY - 180 + k * 120, 280, 180 - k * 120, '#1e1610')
    p.c.save(); p.c.translate(x, GY - 180 + k * 150); p.c.rotate(k * 0.25)
    p.poly([(-180, 0), (180, 0), (110, -110), (-110, -110)], '#2a1e14', 'LN2', 2)
    p.poly([(-190, -40), (190, -40), (120, -150), (-120, -150)], 'SNOW', a=0.95)
    p.c.restore()

@shot(4, trans='slide', cam=camk([(0, (420, 540, 1.0)), (4, (560, 540, 1.0))], fn=lambda x: x),
      caps=[(0, '风雪夜，', '草厅被大雪压塌', ((0, 3),), ())], ev=[(0, 'wind'), (2, 'crash')] + [(i * 0.5, 'snowstep') for i in range(4)], name='snow1')
def snow1(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_snowfield(p, g, t, cam)
    haystack(p, -100, 1.0); haystack(p, 1300, 1.1)
    hut(p, 820, eo(clamp((b - 2) / 0.4)))
    dust(p, 820, GY, t, 2 * B, 1.4, 'SNOW', 12)
    x = lerp(200, 480, clamp(b / 2))
    q = shoulder_walk(t) if b < 2 else anim(t - 2 * B, kb([(0, 'guard'), (1.5, 'idle')]))
    figure(p, g, x, GY, 1.0, 1, q, 'lin', t=t, wind=0.6)
    snowfall(p, t, 180, seed=4, speed=1.4, wind=140, x0=-600, x1=1800)
def snow1_ov(p, g, t):
    onomato(p, '轰——', 820, 400, t, 2 * B, 110, 'CREAM', 1.0)
SHOTS[-1].ov = snow1_ov

@shot(4, trans='slide', cam=camk([(0, (420, 540, 1.0)), (4, (600, 560, 1.1))], fn=lambda x: x),
      caps=[(0, '他挑着酒葫芦，', '去山神庙躲一夜', (), ((1, 4),))], ev=[(i * 0.5, 'snowstep') for i in range(6)] + [(3.5, 'thud')], name='snow2')
def snow2(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_snowfield(p, g, t, cam)
    door = 1.0 if b < 3.2 else 1 - eo((b - 3.2) / 0.3)
    small_temple(p, g, 680, t, door=door)
    if b < 3:
        x = lerp(200, 680, clamp(b / 3))
        a = 1 if b < 2.6 else 1 - (b - 2.6) / 0.4
        figure(p, g, x, GY, 1.0 - 0.1 * clamp((b - 2.4) / 0.6), 1, shoulder_walk(t), 'lin', t=t, wind=0.6)
    snowfall(p, t, 180, seed=5, speed=1.4, wind=140, x0=-600, x1=1800)

@shot(4, cam=camk([(0, (560, 500, 0.9)), (4, (560, 520, 0.85))], fn=lambda x: x),
      caps=[(0, '半夜，', '草料场烧红了半边天', ((0, 2),), ((3, 9),))], ev=[(0, 'fire'), (0.3, 'whoosh'), (2, 'boom'), (2, 'crash')], name='fire')
def firesh(p, g, t):
    cam = _CAM['cur']; b = t / B
    fk = eo(clamp(b / 2.5))
    bg_snowfield(p, g, t, cam, fire_k=fk)
    for i, x in enumerate((180, 540, 900)):
        haystack(p, x, 1.2, burn=fk)
        flames(p, g, x, GY, 260 * clamp(fk * 1.5 - i * 0.15), 360 * clamp(fk * 1.4 - i * 0.15), t, i, 0.6)
    embers(g, t, 80, 7, -200, 1300, GY, 900)
    impact(p, g, 540, 640, t, 2 * B, 1.6, 'FIRE')
    snowfall(p, t, 120, seed=6, speed=1.2, wind=140, x0=-600, x1=1800, a=0.6)
SHOTS[-1].tint = None

@shot(6, cam=camk([(0, (560, 540, 1.0)), (3, (520, 540, 1.0)), (6, (250, 470, 1.55))]),
      caps=[(0, '门外三个人在笑：', '“火，是我们放的”', (), ((4, 6),))], ev=[(0.5, 'laugh'), (1.5, 'laugh'), (3, 'tension'), (5, 'heartbeat'), (5.5, 'heartbeat')], name='overhear')
def overhear(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_snowfield(p, g, t, cam, fire_k=0.8)
    flames(p, g, 900, GY - 200, 900, 150, t, 9, 0.35); haze(p, 'NIGHT', 0.3)
    # 庙内（左）
    p.rect(-400, -600, 780, 2000, '#0c0907')
    g.rect(-400, GY - 400, 780, 400, 'FIRE', a=0.05)
    p.rect(372, GY - 420, 18, 420, '#5a2a16'); p.line([(380, GY - 420), (380, GY)], 'BLK', 3)
    figure(p, g, 260, GY, 1.0, 1, anim(t, kb([(0, 'idle'), (1, 'guard'), (4, 'coil')])), 'lin', t=t)
    for i, (k_, x) in enumerate([('lq', 560), ('fuan', 720), ('cop', 880)]):
        figure(p, g, x, GY, 0.95, -1 if i == 0 else -1, 'laugh' if (int(b * 2) + i) % 2 else 'point', k_, t=t, extra=NONE)
    snowfall(p, t, 120, seed=7, speed=1.2, wind=140, x0=380, x1=1800)
def overhear_ov(p, g, t):
    nametag(p, 'LU QIAN', '陆谦', 560, 340, t, 0.8 * B, 2.5 * B)
    nametag(p, 'FU AN', '富安', 720, 340, t, 1.0 * B, 2.3 * B)
    nametag(p, 'CHA BO', '差拨', 880, 340, t, 1.2 * B, 2.1 * B)
SHOTS[-1].ov = overhear_ov

@shot(4, cam=camk([(0, (540, 520, 1.0)), (4, (540, 520, 1.12))], fn=lambda x: x),
      caps=[(0, '退了三步，', '第四步，退不下去了', (), ((4, 9),))], ev=[(0, 'wood'), (1, 'crack'), (2, 'crack'), (3, 'shatter'), (3, 'title'), (3, 'boom'), (3, 'flash')], name='no_retreat')
def noret(p, g, t):
    cam = _CAM['cur']
    bg_moon(p, g, t, cam, dark=True)
    snowfall(p, t, 140, seed=8, speed=1.8, wind=220, x0=-400, x1=1500)
def noret_ov(p, g, t):
    b = t / B
    sh = 0 if b < 1 else (5 if b < 2 else 12)
    p.c.save(); p.c.translate(540 + math.sin(t * 80) * sh, 520 + math.cos(t * 70) * sh)
    if b < 3:
        s = punch(t, 0, 0.25, 0.3) * 2.3
        p.c.scale(s, s); p.text('退×4', 0, 40, 120, 'GOLD', outline='BLK', ow=14)
        if b >= 1: p.line([(-90, -70), (-30, -10), (-60, 20), (0, 70)], 'BLK', 7)
        if b >= 2: p.line([(70, -80), (30, -20), (70, 10), (24, 80)], 'BLK', 7); p.line([(-130, 0), (-40, 14)], 'BLK', 6)
    p.c.restore()
    if b >= 3:
        k = t - 3 * B; rnd = random.Random(4)
        for j in range(22):
            an = rnd.uniform(0, 6.28); sp = rnd.uniform(400, 1300)
            x = 540 + math.cos(an) * sp * k; y = 520 + math.sin(an) * sp * k + 1500 * k * k
            p.c.save(); p.c.translate(x, y); p.c.rotate(k * 8 + j)
            p.poly([(0, 0), (50, 10), (14, 46)], 'GOLD', 'BLK', 3); p.c.restore()
        impact(p, g, 540, 520, t, 3 * B, 2.0)
        big_title(p, g, '退无可退', 540, 560, t, 3 * B, size=160, col='CREAM')
SHOTS[-1].ov = noret_ov

# ======================= 8 进一枪 =======================
@shot(2, trans='flash', cam=camk([(0, (640, 560, 1.25)), (2, (720, 560, 1.05))]), caps=[(0, '庙门炸开——', '这一回，他往前走', (), ((3, 6),))],
      ev=[(0, 'crash'), (0, 'boom'), (0.3, 'title'), (0.3, 'whoosh')], name='burst')
def burst(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_snowfield(p, g, t, cam, fire_k=0.7)
    small_temple(p, g, 640, t, door=1.0)
    x = lerp(640, 800, eo(clamp(b / 0.6)))
    figure(p, g, x, GY, 1.15, 1, anim(t, kb([(0, 'coil'), (0.3, 'thrust', 'snap')])), 'lin', t=t, wind=1.0)
    pieces(p, 640, GY - 80, t, 0, 10, 'WOOD', 21, 1.4, 14)
    speedlines_screen(p, t, 0, 1.4 * B, 0, 26, 'CREAM', 9)
    snowfall(p, t, 160, seed=9, speed=0.6, wind=600, x0=-600, x1=1800)
def burst_ov(p, g, t):
    big_title(p, g, '进一枪', 640, 250, t, 0.3 * B, size=170)
SHOTS[-1].ov = burst_ov

@shot(3, cam=camk([(0, (620, 540, 1.1)), (3, (660, 540, 1.0))]), ev=[(0.6, 'whoosh'), (1, 'stab'), (1, 'hit')], name='k_chabo')
def k1(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_snowfield(p, g, t, cam, fire_k=0.7)
    flames(p, g, 1000, GY - 200, 700, 140, t, 4, 0.35); haze(p, 'NIGHT', 0.3)
    if b < 1:
        figure(p, g, lerp(820, 860, b), GY, 0.95, 1, walk(t, 2.4), 'cop', t=t, extra=NONE)
    else: ragdoll(p, g, 'cop', 1, 0.95, 860, t, 1 * B, vx=380, vy=-350, spin=0, slide=60, extra=NONE)
    keys = kb([(0, 'guard'), (0.6, 'coil'), (1, 'thrust', 'snap'), (1.9, 'thrust'), (2.6, 'guard')])
    xk = kb([(0, 480), (0.6, 460), (1, 600, 'out')])
    o = figure(p, g, track(t, xk), GY, 1.1, 1, anim(t, keys), 'lin', t=t, wind=0.8)
    draw_trail(g, tipfn(0, GY, 1.1, 1, keys, xk=xk), t, 8, 1 / 60, 'RED', 22, 500)
    impact(p, g, 860, 640, t, 1 * B, 1.1)
    snowfall(p, t, 140, seed=10, speed=1.2, wind=180, x0=-600, x1=1800)
def k1_ov(p, g, t):
    nametag(p, 'CHA BO', '差拨', 860, 330, t, 0, 1 * B)
    if t >= B: counter(p, g, '进', '×1', t, B)
SHOTS[-1].ov = k1_ov

@shot(3, cam=camk([(0, (600, 540, 1.0)), (3, (620, 540, 1.05))]), ev=[(0.5, 'whoosh'), (0.8, 'clang'), (1.6, 'clang'), (2.2, 'hit'), (2.2, 'whoosh')], name='k_fuan')
def k2(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_snowfield(p, g, t, cam, fire_k=0.7)
    flames(p, g, 200, GY - 200, 600, 140, t, 5, 0.35); haze(p, 'NIGHT', 0.3)
    if b < 2.2:
        qf = anim(t, kb([(0, 'guard'), (0.5, 'coil'), (0.8, 'thrust', 'snap'), (1.2, 'guard'), (1.6, 'smash', 'snap')]))
        figure(p, g, lerp(900, 720, eo(clamp(b / 0.8))), GY, 0.95, -1, qf, 'fuan', t=t)
    else: ragdoll(p, g, 'fuan', -1, 0.95, 720, t, 2.2 * B, vx=250, vy=-1100, spin=800, slide=40)
    keys = kb([(0, 'guard'), (0.8, 'parry', 'snap'), (1.2, 'guard'), (1.6, 'blockH', 'snap'), (1.9, 'coil'), (2.2, 'sweepL', 'snap'), (3, 'guard')])
    o = figure(p, g, 460, GY, 1.1, 1, anim(t, keys), 'lin', t=t, wind=0.7)
    draw_trail(g, tipfn(460, GY, 1.1, 1, keys), t, 8, 1 / 60, 'RED', 22, 500)
    clash(p, g, 600, 600, t, 0.8 * B, 0.7); clash(p, g, 600, 520, t, 1.6 * B, 0.7); impact(p, g, 700, GY - 60, t, 2.2 * B, 1.0)
    snowfall(p, t, 140, seed=11, speed=1.2, wind=180, x0=-600, x1=1800)
def k2_ov(p, g, t):
    nametag(p, 'FU AN', '富安', 820, 330, t, 0, 1.2 * B)
    if t >= 2.2 * B: counter(p, g, '进', '×2', t, 2.2 * B)
SHOTS[-1].ov = k2_ov

# 群战：庄客/军汉从火场冲来
K4_KEYS = kb([(0, 'guard'), (0.7, 'coil'), (1, 'jump', 'out'), (2.0, 'jump'), (2.2, 'spinA', 'snap'), (2.8, 'spinA'), (3.0, 'thrust', 'snap'), (3.6, 'guard'), (4, 'thrust', 'snap'), (4.6, 'guard'),
              (5, 'smash', 'snap'), (5.6, 'guard'), (6, 'sweepL', 'snap'), (6.6, 'guard'), (7, 'raiseO'), (7.8, 'raiseO'), (8, 'swingR', 'snap'), (9, 'swingR'), (10, 'heroic')])
K4_X = kb([(0, 420), (1, 420), (2.1, 820, 'io'), (10, 820)])
def k4_face(tt):
    b = tt / B
    if 2.1 <= b < 2.8: return 1 if int(b * 8) % 2 == 0 else -1
    if 2.8 <= b < 3.6: return -1
    if 3.6 <= b < 4.6: return 1
    if 4.6 <= b < 5.6: return -1
    if 5.6 <= b < 6.6: return 1
    return 1
def k4_q(tt):
    q = anim(tt, K4_KEYS); b = tt / B
    if 7 <= b < 7.8: q = dict(q, wp=(b - 7) / 0.8 * 720)
    return q
def k4_lin(q, tt, gg=None):
    b = tt / B
    jy = -math.sin(clamp((b - 1) / 1.1) * math.pi) * 380 if 1 <= b < 2.1 else 0
    return figure(q, gg, track(tt, K4_X), GY + jy, 1.1, k4_face(tt), k4_q(tt), 'lin', t=tt, wind=0.9)
K4E = []  # (x_stop, row_y, sc, face, hit, vx, vy, spin, kind)
for i, (d, sd) in enumerate([(170, -1), (170, 1), (260, -1), (260, 1), (350, 1), (350, -1)]):
    K4E.append((820 + sd * d, GY, 0.95, -sd, 2.2 + i * 0.05, sd * (600 + i * 50), -700, 500, 'soldier'))
K4E += [(560, GY, 0.95, 1, 3.0, -500, -600, 0, 'soldier'), (1080, GY, 0.95, -1, 4.0, 520, -650, 0, 'soldier'), (620, GY, 0.95, 1, 5.0, -150, -300, 0, 'soldier'),
        (1020, GY, 0.95, -1, 6.0, 300, -1000, 900, 'soldier'), (1110, GY, 0.95, -1, 6.04, 400, -900, 500, 'soldier')]
for i in range(8): K4E.append((1150 + i * 70, GY - (i % 2) * 30, 0.9, -1, 8.0 + i * 0.05, 700 + i * 80, -600 - (i % 3) * 120, 500, 'soldier'))

@shot(10, cam=lambda t: (lerp(track(t, K4_X), 760, 0.5), 540 - (40 if 1 * B < t < 2.2 * B else 0), 1.0 - 0.12 * clamp((t / B - 7) / 1)),
      caps=[(0, '火场的军汉，', '一窝蜂冲了过来', ((0, 3),), ()), (2.2, '一枪一个，', '一步不退', (), ((2, 4),)), (7, '红缨一抖，', '扫倒一大片', ((0, 2),), ())],
      ev=[(0, 'step'), (0.5, 'step'), (1, 'whoosh'), (2.2, 'land'), (2.2, 'swish'), (2.3, 'hit'), (3, 'stab'), (4, 'stab'), (5, 'hit'), (6, 'hit'), (7, 'swish'), (7.4, 'swish'), (8, 'whoosh'), (8, 'hit'), (8, 'boom')], name='k_crowd')
def k4(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_snowfield(p, g, t, cam, fire_k=0.8)
    flames(p, g, 1500, GY - 200, 1200, 160, t, 6, 0.35); haze(p, 'NIGHT', 0.3)
    # 远处还在冲的人群
    for i in range(18):
        x = 1300 + (i % 9) * 90 - b * 40; y = GY - 90 - (i // 9) * 26
        mini_soldier(p, x, y, 0.5 - (i // 9) * 0.06, face=-1, thrust=0.3 + 0.2 * math.sin(t * 6 + i))
    haze(p, 'NIGHT', 0.25)
    for x_stop, y, sc, f, hb, vx, vy, spin, kind in K4E:
        start = x_stop + (900 if x_stop > 820 else -900) * (0.6 if hb < 3 else 1)
        arr = 0.8 if hb < 3 else hb - 1.2
        if b < hb:
            k = eo(clamp(b / max(0.5, arr)))
            xx = lerp(start, x_stop, k)
            figure(p, g, xx, y, sc, f, walk(t, 2.2) if k < 0.95 else 'guard', kind, t=t + hb)
        else:
            ragdoll(p, g, kind, f, sc, x_stop, t, hb * B, vx, vy, spin, slide=90)
    o = k4_lin(p, t, g)
    draw_trail(g, k4_lin, t, 9, 1 / 60, 'RED', 26, 450)
    draw_trail(g, k4_lin, t, 9, 1 / 60, 'CREAM', 12, 450)
    if 2.2 <= b < 2.9:
        k = clamp((b - 2.2) / 0.6); g.c.save(); g.c.translate(820, GY - 170); g.c.scale(1, 0.3); g.arc(0, 0, 260, 0, k * 6.28, 'CREAM', 20, 0.8); g.c.restore()
    dust(p, 820, GY, t, 2.2 * B, 1.3); shockring(p, g, 820, GY, t, 2.2 * B, 1.2)
    for hb, x, y in [(2.3, 650, 640), (2.35, 990, 640), (3, 580, 650), (4, 1060, 650), (5, 640, 700), (6, 1040, 720), (8, 1100, 620)]:
        impact(p, g, x, y, t, hb * B, 1.0, seed=int(hb * 7))
    if b >= 8:
        k = (b - 8) / 1.2
        if k < 1: g.line([(860 + k * 900, GY - 400), (860 + k * 900, GY)], 'CREAM', 30 * (1 - k), 1 - k)
    snowfall(p, t, 160, seed=12, speed=1.4, wind=200, x0=-600, x1=2000)
def k4_ov(p, g, t):
    ctr(p, g, t, '进', [(2.3, '×8'), (3, '×9'), (4, '×10'), (5, '×11'), (6, '×13'), (8, '×21')])
    onomato(p, '唰！', 820, 300, t, 2.2 * B, 100, 'CREAM', 0.6)
    onomato(p, '轰——！', 760, 300, t, 8 * B, 120, 'GOLD', 0.9)
SHOTS[-1].ov = k4_ov

@shot(3, cam=camk([(0, (700, 600, 1.15)), (3, (760, 600, 1.2))]), caps=[(0, '陆谦想跑——', '', ((0, 2),), ())], ev=[(0, 'snowstep'), (0.5, 'snowstep'), (1, 'snowstep'), (2, 'thud')], name='lq_run')
def lqrun(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_snowfield(p, g, t, cam, fire_k=0.6)
    if b < 2: figure(p, g, lerp(560, 860, b / 2), GY, 0.95, 1, walk(t, 2.6), 'lq', t=t, extra=NONE)
    else: figure(p, g, 860, GY, 0.95, -1, 'sit', 'lq', t=t, extra=NONE)
    dust(p, 860, GY, t, 2 * B, 0.7, 'SNOW')
    snowfall(p, t, 160, seed=13, speed=1.4, wind=200, x0=-600, x1=2000)

# 风雪一枪
def dragon_pts(k, t, x0=300, x1=900):
    pts = []
    for j in range(60):
        u = j / 59 * k
        x = lerp(x0, x1, u) + math.sin(u * 12 + t * 3) * 60 * (1 - u)
        y = 560 - math.sin(u * math.pi) * 200 + math.cos(u * 12 + t * 3) * 50 * (1 - u)
        pts.append((x, y))
    return pts

@shot(6, cam=camk([(0, (560, 560, 1.0)), (2.2, (500, 560, 1.28)), (2.5, (640, 560, 1.0)), (6, (640, 560, 0.95))]),
      caps=[(0, '风停了，雪悬在半空，', '', (), ()), (2.5, '风雪一枪！', '', ((0, 5),), ())],
      ev=[(0, 'riser'), (2.3, 'whoosh'), (2.5, 'bigimpact'), (2.5, 'flash'), (2.5, 'title'), (2.5, 'gong'), (3, 'wind')], name='finisher')
def fin(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_snowfield(p, g, t, cam, fire_k=0.5)
    # 雪：前 2.3 拍慢动作（越来越慢并旋向枪尖），之后爆开
    if b < 2.3:
        slow = 1 - 0.85 * clamp(b / 1.2)
        tt = 3 + t * slow
        rnd = random.Random(14)
        swirl = clamp((b - 1) / 1.3)
        for i in range(200):
            x0 = rnd.uniform(-300, 1400); y0 = rnd.uniform(0, 1000); ph = rnd.uniform(0, 6)
            x = x0 + tt * 30 + math.sin(tt + ph) * 10; y = y0 + tt * 40
            # 向林冲枪尖螺旋聚拢
            cx, cy = 420, 620
            an = math.atan2(y - cy, x - cx) + swirl * 3; r = math.hypot(x - cx, y - cy) * (1 - 0.7 * swirl)
            x, y = cx + math.cos(an) * r, cy + math.sin(an) * r
            p.ell(x, y, 3.5, 3.5, 'SNOW', a=0.9)
        p.rect(-1600, -600, 4400, 2400, 'NIGHT', a=0.25 * clamp(b / 1.2))
    lx = track(t, kb([(0, 300), (2.2, 300), (2.5, 760, 'out')]))
    q = anim(t, kb([(0, 'guard'), (1.2, 'coil'), (2.2, 'coil'), (2.5, 'thrust', 'snap'), (4, 'thrust'), (5, 'heroic')]))
    if b < 2.5:
        figure(p, g, 900, GY, 0.95, -1, 'sit', 'lq', t=t, extra=NONE)
    else:
        ragdoll(p, g, 'lq', -1, 0.95, 900, t, 2.5 * B, vx=700, vy=-800, spin=500, slide=120, extra=NONE)
    if b >= 2.25:
        k = clamp((b - 2.25) / 0.4)
        pts = dragon_pts(k, t, 200, 1000)
        fade = clamp(1 - (b - 3.2) / 1.5)
        for j in range(1, len(pts)):
            w_ = 70 * (j / len(pts)) ** 0.5
            g.line([pts[j - 1], pts[j]], 'SNOW', w_, 0.8 * fade); p.line([pts[j - 1], pts[j]], 'SNOW', w_ * 0.6, 0.9 * fade)
        hx_, hy_ = pts[-1]
        p.poly([(hx_ + 70, hy_), (hx_ - 30, hy_ - 60), (hx_ - 10, hy_), (hx_ - 30, hy_ + 60)], 'SNOW', a=fade)
        p.ell(hx_ + 10, hy_ - 18, 7, 7, 'GOLD', a=fade)
        speedlines_screen(p, t, 2.25 * B, 1.2 * B, 0, 30, 'CREAM', 15)
    o = figure(p, g, lx, GY, 1.2, 1, q, 'lin', t=t, wind=1.2 if b > 2.2 else 0.3)
    impact(p, g, 900, 620, t, 2.5 * B, 2.2, 'CREAM')
    if b >= 2.5: snowfall(p, t, 220, seed=15, speed=2.2, wind=400, x0=-600, x1=2000)
def fin_ov(p, g, t):
    big_title(p, g, '风雪一枪', 540, 240, t, 2.5 * B, size=160)
SHOTS[-1].ov = fin_ov

@shot(3, cam=camk([(0, (600, 520, 1.1)), (3, (600, 540, 0.95))], fn=lambda x: x), caps=[(0, '风雪一枪，', '仇人一个没跑掉', ((0, 4),), ())], ev=[(0, 'wind')], name='after')
def after(p, g, t):
    cam = _CAM['cur']
    bg_snowfield(p, g, t, cam, fire_k=0.7)
    flames(p, g, 600, GY - 200, 1600, 160, t, 8, 0.35); haze(p, 'NIGHT', 0.3)
    figure(p, g, 1000, GY + 112, 0.95, -1, 'lie', 'lq', rot=-90, t=t, extra=NONE)
    figure(p, g, 520, GY, 1.15, 1, 'heroic', 'lin', t=t, wind=0.6)
    snowfall(p, t, 160, seed=16, speed=1.0, wind=80, x0=-600, x1=2000)

# ======================= 9 梁山 =======================
def boat(p, x, t):
    y = 800 + math.sin(t * 2) * 4
    p.poly([(x - 140, y - 10), (x + 140, y - 10), (x + 100, y + 20), (x - 100, y + 20)], 'BLK', 'LN', 2)
    figure(p, None, x + 60, y - 10, 0.6, -1, 'idle', 'thug', t=t, extra={'wpn': 'staff', 'kind': {'hat': 'cop'}})

@shot(6, trans='slide', cam=camk([(0, (400, 540, 1.0)), (6, (620, 540, 1.0))], fn=lambda x: x),
      caps=[(0, '雪夜投奔，', '一支响箭飞过水泊', (), ((2, 4),)), (3.5, '小船来接，', '上了梁山', (), ((2, 4),))],
      ev=[(i * 0.5, 'snowstep') for i in range(4)] + [(2, 'arrow'), (2.6, 'thud')], name='lake')
def lake(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_lake(p, g, t, cam)
    boat(p, lerp(1500, 860, eo(clamp((b - 2.5) / 3))), t)
    x = lerp(200, 520, clamp(b / 2.4))
    figure(p, g, x, GY, 0.95, 1, shoulder_walk(t) if b < 2.4 else 'idle', 'lin', t=t, wind=0.5)
    if 2 <= b:
        k = clamp((b - 2) / 0.6); ax, ay = lerp(1200, 680, k), lerp(200, GY - 20, k)
        an = math.atan2(GY - 20 - 200, 680 - 1200)
        p.line([(ax, ay), (ax - math.cos(an) * 90, ay - math.sin(an) * 90)], 'BLK', 4); p.poly([(ax, ay), (ax - math.cos(an - 0.3) * 20, ay - math.sin(an - 0.3) * 20), (ax - math.cos(an + 0.3) * 20, ay - math.sin(an + 0.3) * 20)], 'CREAM')
        if k < 1: trail(g, [(lerp(1200, 680, max(0, k - i * 0.05)), lerp(200, GY - 20, max(0, k - i * 0.05))) for i in range(8, -1, -1)], 'CREAM', 10, 0.8)
    snowfall(p, t, 120, seed=17, speed=0.9, wind=50, x0=-600, x1=2000)
def lake_ov(p, g, t):
    nametag(p, 'LIANG SHAN PO', '梁山泊', 860, 260, t, 3 * B, 3 * B)
    onomato(p, '咻——', 960, 300, t, 2 * B, 80, 'CREAM', 0.8)
SHOTS[-1].ov = lake_ov

@shot(4, cam=camk([(0, (520, 600, 1.4)), (4, (520, 580, 1.5))], fn=lambda x: x),
      caps=[(0, '上船前，', '他解下葫芦，喝了一口', (), ((3, 6),))], ev=[(0.5, 'wood'), (1.5, 'gulp'), (3.4, 'breath')], name='drink')
def drink(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_lake(p, g, t, cam)
    q = anim(t, kb([(0, 'idle'), (0.8, 'drink'), (3, 'drink'), (3.6, 'idle')]))
    spear(p, 640, GY + 10, 640, GY - 330, True, t)
    o = figure(p, g, 520, GY, 1.0, 1, q, 'lin', t=t, extra={'wpn': None})
    if 0.6 <= b < 3.4:
        hx_, hy_ = o['hand']; p.ell(hx_ + 6, hy_ - 14, 9, 10, 'GOLD'); p.ell(hx_ + 10, hy_ + 6, 14, 15, 'GOLD')
    if b >= 3.4:
        k = (b - 3.4) / 0.6; hd = o['head']
        if k < 1: p.ell(hd[0] + 40 + k * 60, hd[1] + 20 - k * 20, 14 + k * 30, 10 + k * 20, 'SNOW', a=0.6 * (1 - k))
    snowfall(p, t, 90, seed=18, speed=0.6, wind=30, x0=-200, x1=1500)

# ======================= 10 收尾 + 卡 =======================
@shot(8, trans='slide', cam=camk([(0, (540, 560, 1.06)), (8, (540, 560, 0.94))], fn=lambda x: x),
      caps=[(4, '退了四步，', '只为这一枪', ((3, 4),), ((2, 5),))], ev=[(0.2, 'title'), (2, 'boom'), (4, 'gong')], name='end')
def endsh(p, g, t):
    cam = _CAM['cur']
    bg_moon(p, g, t, cam)
    snowfall(p, t, 90, seed=3, speed=0.8, wind=30, y0=-200, y1=1100)
    figure(p, g, 540, GY, 1.3, 1, 'heroic', 'lin', t=t, wind=0.3)
    embers(g, t, 30, 5, 0, W, GY, 800, 'GOLD')
def end_ov(p, g, t):
    big_title(p, g, '豹子头 · 林冲', 540, 150, t, 0.2 * B, size=88, col='CREAM')
    big_title(p, g, '退一步，进一枪', 540, 300, t, 2 * B, size=96)
SHOTS[-1].ov = end_ov

@shot(12, trans='dissolve', ev=[(0, 'whoosh'), (1, 'boom'), (4, 'flip'), (6, 'wood'), (6.6, 'wood'), (7.2, 'wood'), (7.8, 'wood'), (8.6, 'shimmer'), (11, 'gong')],
      caps=[(0, '水浒群英卡 · 第一张', '豹子头 林冲', (), ((0, 3),)), (8, '下一位好汉，', '你想看谁？', (), ())], name='card')
def card(p, g, t):
    b = t / B
    bg_moon(p, g, t, (SCX, SCY, 1), dark=True)
    k = eo(t / B)
    sx = abs(math.cos((t - 4 * B) / B * math.pi)) if 4 <= b < 5 else 1.0
    front = b < 4.5
    c = p.c; c.save(); c.translate(540, 500 + (1 - k) * 700); c.rotate((1 - k) * 2.5); c.scale(max(0.01, k * sx), max(0.01, k))
    g.c.save(); g.c.translate(540, 500 + (1 - k) * 700); g.c.rotate((1 - k) * 2.5); g.c.scale(max(0.01, k * sx), max(0.01, k))
    cw, ch = 320, 430
    g.poly([(-cw, -ch), (cw, -ch), (cw, ch), (-cw, ch)], '#00000000', 'GOLD', 6, a=0.5) if False else None
    for q_ in (g,): q_.c.rectangle(-cw, -ch, 2 * cw, 2 * ch); q_.col('GOLD', 0.6); q_.c.set_line_width(8); q_.c.stroke()
    p.poly([(-cw, -ch), (cw, -ch), (cw, ch), (-cw, ch)], '#1a120c', 'GOLD', 10)
    p.poly([(-cw + 24, -ch + 24), (cw - 24, -ch + 24), (cw - 24, ch - 24), (-cw + 24, ch - 24)], '#1a120c', 'LN', 3)
    if front:
        p.ell(0, -70, 240, 240, '#e8964f'); [p.ring(0, -70, 250 + i * 16, 'LN', 2, 0.4) for i in range(3)]
        figure(p, g, 0, 250, 1.0, 1, 'guard', 'lin', t=t)
        p.rect(-cw + 24, ch - 150, 2 * cw - 48, 126, 'RED')
        p.text('豹子头 · 林冲', 0, ch - 70, 58, 'CREAM')
        p.text('天雄星', -cw + 90, -ch + 80, 32, 'GOLD'); p.text('SSR', cw - 80, -ch + 80, 40, 'GOLD', outline='BLK')
    else:
        p.text('豹子头 · 林冲', 0, -ch + 100, 54, 'GOLD')
        rows = [('星位', '天雄星', 6), ('职位', '马军五虎将', 6.6), ('兵器', '丈八红缨枪', 7.2), ('必杀', '风雪一枪', 7.8)]
        for i, (a_, v, tb) in enumerate(rows):
            if b >= tb:
                s_ = punch(t, tb * B, 0.2, 0.3)
                p.text(a_, -cw + 70, -ch + 200 + i * 80, 36, 'LN', 'l')
                c.save(); c.translate(-cw + 220, -ch + 200 + i * 80); c.scale(s_, s_); p.text(v, 0, 0, 40, 'CREAM', 'l'); c.restore()
        for i, (a_, v) in enumerate([('枪法', 98), ('忍耐', 99), ('爆发', 95)]):
            t0 = 8.6 * B + i * 0.15
            if t < t0: continue
            kk = eo((t - t0) / 0.5); y = -ch + 540 + i * 90
            p.text(a_, -cw + 70, y + 14, 32, 'LN', 'l')
            p.rect(-cw + 180, y - 18, 2 * cw - 300, 36, '#3a2a1a')
            p.rect(-cw + 180, y - 18, (2 * cw - 300) * kk * v / 100, 36, 'GOLD'); 
            p.text(str(int(v * kk)), cw - 60, y + 14, 34, 'CREAM')
    c.restore(); g.c.restore()
    rnd = random.Random(7)
    for i in range(50):
        an = rnd.uniform(0, 6.28) + t * rnd.uniform(.3, .9); r = rnd.uniform(380, 560)
        g.ell(540 + math.cos(an) * r, 500 + math.sin(an) * r * 0.9, 4, 4, 'GOLD2', a=0.6 + 0.4 * math.sin(t * 5 + i))
