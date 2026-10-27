from frame import *

NONE = {'wpn': None}
NOSEAL = {'seal': False}
NS_NW = {'wpn': None, 'seal': False}

def push_alpha(p, a, fn):
    p.c.push_group(); fn(); p.c.pop_group_to_source(); p.c.paint_with_alpha(a)

# ======================= 1 开场 =======================
@shot(7, cam=camk([(0, (540, 600, 0.86)), (7, (540, 540, 1.02))], fn=lambda x: x),
      caps=[(0, '水浒群英 · 第一集', '豹子头 林冲', (), ((0, 3),))], ev=[(0, 'thunder'), (0, 'flash'), (1, 'title'), (3, 'whoosh'), (5, 'whoosh')], name='open1')
def o1(p, g, t):
    cam = SHOTS_CAM(t)
    bg_moon(p, g, t, cam)
    snowfall(p, t, 90, seed=3, speed=0.8, wind=30, y0=-200, y1=1100)
    q = anim(t, kb([(0, 'heroic'), (3, 'heroic'), (4, 'guardH'), (5.5, 'guardH'), (6.5, 'heroic')]))
    figure(p, g, 540, GY, 1.3, 1, q, 'lin', t=t, wind=0.3, extra=NOSEAL)
    if t < 0.4:
        lightning(g, 180, -200, 300, 700, t, 1, 1 - t / 0.4); lightning(g, 900, -200, 820, 600, t, 2, 1 - t / 0.4)
    embers(g, t, 30, 5, 0, W, GY, 800, 'GOLD')
def o1_ov(p, g, t):
    big_title(p, g, '豹子头 · 林冲', 540, 160, t, 1 * B, size=88, col='CREAM')
    nametag(p, 'BAO ZI TOU', '天雄星', 820, 300, t, 1.5 * B, 4 * B)
SHOTS[-1].ov = o1_ov

def SHOTS_CAM(t, _c={}):
    return _CAM['cur']
_CAM = {'cur': (SCX, SCY, 1.0)}

@shot(3, cam=camk([(0, (540, 600, 1.0)), (3, (540, 600, 1.08))], fn=lambda x: x), ev=[(0, 'boom'), (0.1, 'title')], name='face')
def o2(p, g, t):
    bg_moon(p, g, t, _CAM['cur'], dark=True)
    p.c.save(); p.c.translate(540, 690); p.c.scale(4.3, 4.3)
    g.c.save(); g.c.translate(540, 690); g.c.scale(4.3, 4.3)
    p.poly([(-12, 30), (12, 30), (10, 52), (-10, 52)], 'CREAM'); p.poly([(-70, 70), (-24, 46), (0, 64), (24, 46), (70, 70), (80, 120), (-80, 120)], 'BLK', 'LN', 0.8); p.ell(0, 84, 5, 5, 'GOLD')
    head(p, 0, 0, KIND['lin'], 1, 0, NOSEAL)
    p.c.restore(); g.c.restore()
    snowfall(p, t, 60, seed=9, speed=0.5, wind=20, size=1.6)
def o2_ov(p, g, t):
    big_title(p, g, '退一步，进一枪', 540, 170, t, 0.1 * B, size=104)
SHOTS[-1].ov = o2_ov

def seal_fly(p, g, t, t0, t1, x0, y0, x1, y1, s0=1.6, s1=0.22):
    if t < t0 or t > t1: return
    k = ei((t - t0) / (t1 - t0))
    x, y = lerp(x0, x1, k), lerp(y0, y1, k)
    for i in range(6):
        kk = max(0, k - i * 0.05); xx, yy = lerp(x0, x1, kk), lerp(y0, y1, kk)
        g.ell(xx, yy, 30 * (1 - i / 6), 30 * (1 - i / 6), 'GOLD', a=0.5 * (1 - i / 6))
    s = lerp(s0, s1, k)
    p.c.save(); p.c.translate(x, y); p.c.rotate(k * 9); p.c.scale(s, s)
    p.poly([(-50, -50), (50, -50), (50, 50), (-50, 50)], 'GOLD', 'BLK', 6); p.text('配', 0, 26, 70, 'BLK'); p.c.restore()

@shot(7, cam=camk([(0, (540, 560, 1.0)), (1, (600, 470, 1.35)), (2, (600, 470, 1.35)), (2.6, (540, 560, 1.0)), (7, (540, 560, 0.97))]),
      caps=[(0, '朝廷的金印飞过来，', '他一步不躲', (), ((4, 6),)), (3, '八十万禁军的枪法，', '全在这一杆红缨', (), ((5, 8),))],
      ev=[(0, 'whoosh'), (1, 'stamp'), (1, 'flash'), (2.2, 'whoosh'), (3, 'swish'), (3.5, 'swish'), (4.5, 'hit'), (4.5, 'boom'), (5.5, 'shimmer')], name='open3')
def o3(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_moon(p, g, t, cam)
    snowfall(p, t, 90, seed=3, speed=0.8, wind=30, y0=-200, y1=1100)
    keys = kb([(0, 'heroic'), (2, 'heroic'), (2.6, 'raiseO'), (4.1, 'coil'), (4.5, 'thrust', 'snap'), (5.6, 'thrust'), (6.6, 'heroic')])
    q = anim(t, keys)
    if 2.6 * B <= t < 4.1 * B:  # 头顶舞花枪
        q = dict(q); q['wp'] = -20 + (t - 2.6 * B) / (1.5 * B) * 720
    fn = lambda qq, tt: figure(qq, None, 540, GY, 1.3, 1, (lambda q2: (dict(q2, wp=-20 + (tt - 2.6 * B) / (1.5 * B) * 720) if 2.6 * B <= tt < 4.1 * B else q2))(anim(tt, keys)), 'lin', t=tt)
    o = figure(p, g, 540, GY, 1.3, 1, q, 'lin', t=t, wind=0.3 + (0.6 if b > 2.5 else 0), extra={'seal': b >= 1})
    if b > 2.5: draw_trail(g, fn, t, 10, 1 / 60, 'CREAM', 30, 400)
    hd = o['head']
    seal_fly(p, g, t, 0, 1 * B, 1150, 0, hd[0] - 20, hd[1] + 16)
    impact(p, g, hd[0] - 20, hd[1] + 16, t, 1 * B, 0.8)
    impact(p, g, o['tip'][0], o['tip'][1], t, 4.5 * B, 1.3)
    if b > 4.5:
        k = t - 4.5 * B; rnd = random.Random(5)
        for i in range(60):
            an = rnd.uniform(0, 6.28) + k * rnd.uniform(.5, 1.5); r = rnd.uniform(150, 520) * eo(k * 2)
            g.ell(540 + math.cos(an) * r, 520 + math.sin(an) * r * 0.8, 4, 4, 'GOLD2', a=clamp(1.5 - k))
def o3_ov(p, g, t):
    onomato(p, '啪！', 760, 330, t, 1 * B, 90, 'GOLD')
SHOTS[-1].ov = o3_ov

# ======================= 2 校场 =======================
DRILL = ['guard', 'thrust', 'raiseO', 'smash', 'guard', 'thrust', 'thrustHi', 'smash', 'coil', 'thrust', 'raiseO', 'smash', 'thrust', 'heroic']
def drill_pose(tt):
    keys = [(0, 'guard')]
    for i, ps in enumerate(DRILL): keys.append(((i + 1) * B, ps, 'snap' if ps in ('thrust', 'smash', 'thrustHi') else 'io'))
    return anim(tt, keys)
def drill_thrust(tt):
    q = drill_pose(tt); return clamp((q['wp'] - 0) / 110)

@shot(14, trans='slide', cam=camk([(0, (330, 640, 1.45)), (3.4, (360, 630, 1.45)), (4.2, (640, 560, 0.95)), (7.4, (660, 560, 0.95)), (8.2, (900, 640, 0.58)), (14, (920, 650, 0.55))]),
      caps=[(0, '东京校场，', '林教头一声令下', (), ((0, 3),)), (4, '一个变一万，', '一万变八十万', (), ()), (8, '八十万禁军教头，', '一杆红缨枪 镇京城', ((0, 7),), ((6, 9),))],
      ev=[(i, 'taiko') for i in range(1, 14)] + [(0, 'wood'), (4, 'boom'), (4, 'whoosh'), (8, 'whoosh'), (8, 'title'), (8, 'boom')], name='drill')
def drill(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_drill(p, g, t, cam)
    p.rect(-1600, GY + 300, 4400, 600, 'BLK')
    platform(p, 230, GY - 110)
    n_rows = 2 if b < 4 else (10 if b < 8 else 34)
    # 远处小兵（由远及近）
    if b >= 4:
        big = b >= 8
        R = 26 if big else 9
        for r in range(R - 1, -1, -1):
            u = r / (R - 1)
            yy = (lerp(GY + 330, GY - 30, u) if big else lerp(GY + 130, GY - 20, u))
            s = lerp(0.62, 0.2, u) if big else lerp(0.5, 0.26, u)
            cols = int(lerp(26, 70, u)) if big else 18
            span = 46
            x0 = 420 if big else 470
            th = drill_thrust(t - r * 0.02)
            rnd = random.Random(r)
            for i in range(cols):
                mini_soldier(p, x0 + i * span * s * 1.6, yy, s, face=-1, thrust=th)
            if r == R // 2: haze(p, 'BG', 0.18)
    # 近处两排 = 10 人
    for r in range(1, -1, -1) if b < 8 else ():
        for i in range(5):
            x = 520 + i * 120 + r * 60; gy = GY + 4 - r * 26
            figure(p, None, x, gy, 0.62 - r * 0.04, -1, drill_pose(t - (i * 0.015 + r * 0.03)), 'soldier', t=t)
    keys_tip = lambda qq, tt: figure(qq, None, 230, GY - 110, 0.9, 1, drill_pose(tt), 'lin', t=tt)
    o = figure(p, g, 230, GY - 110, 0.9, 1, drill_pose(t), 'lin', t=t, wind=0.4)
    draw_trail(g, keys_tip, t, 8, 1 / 60, 'CREAM', 22, 500)
    i = int(b)
    if 1 <= i < 14 and DRILL[i - 1] in ('thrust', 'smash', 'thrustHi'):
        impact(p, g, o['tip'][0], o['tip'][1], t, i * B, 0.5, seed=i)
def drill_ov(p, g, t):
    b = t / B
    val, tl = ('×10', 0.0) if b < 4 else (('×1万', 4 * B) if b < 8 else ('×80万', 8 * B))
    counter(p, g, '禁军', val, t, tl)
    big_title(p, g, '八十万禁军教头', 500, 270, t, 8 * B, size=92)
    nametag(p, 'DONG JING', '东京 · 校场', 140, 120, t, 0.2, 3 * B, 'l')
SHOTS[-1].ov = drill_ov

# ======================= 3 岳庙 =======================
THUG_X = [820, 900, 980, 1060, 120, 1140]
@shot(6, trans='slide', cam=camk([(0, (520, 540, 1.0)), (6, (680, 540, 1.0))], fn=lambda x: x),
      caps=[(0, '岳庙进香，', '娘子正在上香', ((0, 2),), ()), (3, '高衙内带着一帮狗腿子，', '拦住了去路', ((0, 3),), ())],
      ev=[(0, 'wood'), (2, 'step'), (2.5, 'step'), (3, 'step'), (3.5, 'step'), (4.5, 'laugh')], name='temple1')
def tm1(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_temple(p, g, t, cam)
    wp = 'pray' if b < 4.3 else 'cower'
    figure(p, g, 520, GY, 0.95, 1 if b < 4.3 else -1 if False else 1, wp, 'wife', t=t)
    k = clamp((b - 2) / 2)
    arrive = k >= 1
    gx = lerp(1500, 680, eo(k))
    q = walk(t, 1.2) if not arrive else anim(t - 4 * B, kb([(0, 'idle'), (0.5, 'fan'), (2, 'laugh')]))
    figure(p, g, gx, GY, 0.95, -1, q, 'gyn', t=t)
    for i in range(5):
        x = lerp(1620 + i * 90, 800 + i * 90, eo(k))
        figure(p, g, x, GY, 0.9, -1, walk(t, 1.2, i) if not arrive else ('laugh' if (i + int(b * 2)) % 3 == 0 else 'idle'), 'thug', t=t)
def tm1_ov(p, g, t):
    nametag(p, 'LIN NIANG ZI', '林娘子', 200, 380, t, 0.3 * B, 3 * B, 'l')
    nametag(p, 'GAO YA NEI', '花花太岁 · 高衙内', 640, 380, t, 3.2 * B, 2.5 * B)
    onomato(p, '小娘子~', 760, 300, t, 4.5 * B, 66, 'CREAM', 1.2)
SHOTS[-1].ov = tm1_ov

@shot(2, cam=camk([(0, (300, 560, 1.0)), (2, (300, 540, 1.3))]), ev=[(0.8, 'boom'), (0.8, 'whoosh')], name='temple2')
def tm2(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_temple(p, g, t, (cam[0] + 900, cam[1], cam[2]))
    q = anim(t, kb([(0, 'idle'), (0.6, 'guard')]))
    figure(p, g, 300, GY, 1.1, 1, q, 'lin', t=t, wind=0.5, extra=NS_NW)
    speedlines_screen(p, t, 0.8 * B, 1.2 * B, 0, 20, 'CREAM', 4)
def tm2_ov(p, g, t):
    onomato(p, '住手！', 700, 330, t, 0.8 * B, 140, 'CREAM', 1.2)
SHOTS[-1].ov = tm2_ov

LINF_KEYS = kb([(0, 'jump'), (1, 'land', 'in'), (1.6, 'guard'), (2.6, 'guard'), (3, 'palm', 'snap'), (3.7, 'guard'), (4.4, 'grab'), (5, 'throw', 'snap'), (5.7, 'guard'),
               (6.5, 'duck', 'out'), (7, 'sweepL', 'snap'), (7.8, 'guard'), (8.5, 'kick', 'snap'), (9.1, 'guard'), (9.5, 'palm2', 'snap'), (10.4, 'guard'), (11.4, 'guard'), (12, 'grab'), (12.6, 'fist')])
LINF_X = kb([(0, -150), (1, 470, 'out'), (2.5, 470), (2.8, 430), (4, 430), (4.4, 480), (11, 480), (12, 1000, 'io'), (14, 1000)])
LINF_FACE = [(0, 1), (8.1, -1), (9.2, 1)]
def face_at(t, lst):
    f = lst[0][1]
    for b0, v in lst:
        if t >= b0 * B: f = v
    return f
@shot(14, cam=lambda t: (track(t, kb([(0, (560, 560, 1.0)), (10.5, (580, 560, 1.0)), (12, (860, 520, 1.12)), (14, (880, 520, 1.15))])) if True else None),
      caps=[(0, '狗腿子一拥而上，', '来一个，飞一个', ((0, 3),), ((3, 4), (6, 7))), (11, '一把揪住高衙内，', '拳头举了起来', (), ())],
      ev=[(0, 'whoosh'), (1, 'land'), (3, 'hit'), (4.4, 'grab'), (5, 'whoosh'), (5.5, 'hit'), (6.5, 'swish'), (7, 'hit'), (8, 'thud'), (8.5, 'hit'), (8.9, 'clang'), (9.5, 'hit'), (11.2, 'whoosh'), (12, 'grab'), (12.6, 'boom')], name='temple_fight')
def tmf(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_temple(p, g, t, cam)
    figure(p, g, 250, GY, 0.95, 1, 'cower', 'wife', t=t)
    # 高衙内：先在右侧，后被揪起
    if b < 12:
        figure(p, g, 1200, GY, 0.95, -1, 'fan' if b < 3 else 'cower', 'gyn', t=t)
    else:
        lift = eo((b - 12) / 0.6) * 70
        figure(p, g, 1110 - lift * 0.3, GY - lift, 0.95, -1, 'cower', 'gyn', t=t)
    lx = track(t, LINF_X); jump_h = 0
    if b < 1: jump_h = -math.sin(clamp(b) * math.pi) * 300
    face = face_at(t, LINF_FACE)
    keys = LINF_KEYS
    fn = lambda qq, tt: figure(qq, None, track(tt, LINF_X), GY, 1.0, face_at(tt, LINF_FACE), anim(tt, keys), 'lin', t=tt, extra=NS_NW)
    # 狗腿子
    # 1：冲上来挨一掌
    if b < 3:
        x1 = lerp(820, 600, eo((b - 2) / 0.9)) if b >= 2 else 820
        figure(p, g, x1, GY, 0.95, -1, 'palm' if b >= 2.5 else 'guard', 'thug', t=t)
    else: ragdoll(p, g, 'thug', -1, 0.95, 600, t, 3 * B, vx=700, vy=-420, spin=0, slide=160)
    # 2/3：被摔
    if b < 4.4:
        figure(p, g, lerp(900, 600, eo((b - 3.8) / 0.6)) if b > 3.8 else 900, GY, 0.95, -1, 'palm' if b > 4 else 'guard', 'thug', t=t)
    elif b < 5:
        k = (b - 4.4) / 0.6; ang = k * 180
        figure(p, g, lerp(600, 520, k), GY - math.sin(k * math.pi) * 260 - 40, 0.95, -1, 'hurt', 'thug', rot=-ang, t=t)
    else: ragdoll(p, g, 'thug', -1, 0.95, 520, t, 5 * B, vx=650, vy=-500, spin=500, slide=120)
    if b < 5.5:
        figure(p, g, lerp(980, 720, eo((b - 3.9) / 0.8)) if b > 3.9 else 980, GY, 0.95, -1, 'guard', 'thug', t=t)
    else: ragdoll(p, g, 'thug', -1, 0.95, 720, t, 5.5 * B, vx=520, vy=-380, spin=0, slide=200)
    # 4：持棍 → 被扫飞
    if b < 7:
        x4 = lerp(1060, 640, eo((b - 5.6) / 0.7)) if b > 5.6 else 1060
        q4 = anim(t, kb([(5.6, 'guard'), (6.2, 'raiseO'), (6.6, 'smash', 'snap')]))
        figure(p, g, x4, GY, 0.95, -1, q4, 'thug', t=t, extra={'wpn': 'staff'})
    else: ragdoll(p, g, 'thug', -1, 0.95, 640, t, 7 * B, vx=260, vy=-1150, spin=900, slide=60, extra={'wpn': 'staff'})
    # 5：从左背后偷袭 → 被后踢撞香炉
    if b < 8.5:
        x5 = lerp(-80, 330, eo((b - 7.4) / 0.9)) if b > 7.4 else -80
        figure(p, g, x5, GY, 0.95, 1, 'palm' if b > 8 else walk(t, 2), 'thug', t=t)
    else: ragdoll(p, g, 'thug', 1, 0.95, 330, t, 8.5 * B, vx=-520, vy=-500, spin=0, slide=40)
    # 6：右侧 → 双掌飞出画外
    if b < 9.5:
        x6 = lerp(1140, 640, eo((b - 8.3) / 0.9)) if b > 8.3 else 1140
        figure(p, g, x6, GY, 0.95, -1, 'guard', 'thug', t=t)
    else: ragdoll(p, g, 'thug', -1, 0.95, 640, t, 9.5 * B, vx=1400, vy=-700, spin=900, slide=0)
    # 林冲
    o = figure(p, g, lx, GY + jump_h, 1.0, face, anim(t, keys), 'lin', t=t, wind=0.5 if b < 12 else 0.2, extra=NS_NW)
    if b < 11.2: draw_trail(g, lambda qq, tt: dict(tip=fn(qq, tt)['hand']), t, 6, 1 / 60, 'CREAM', 18, 700) if False else None
    if b < 1: speedlines_screen(p, t, 0, B, 0, 16, 'CREAM', 2, 0.5)
    if 11 <= b < 12: speedlines_screen(p, t, 11 * B, B, 0, 18, 'CREAM', 7)
    dust(p, lx, GY, t, 1 * B, 1.0); shockring(p, g, lx, GY, t, 1 * B, 1.0)
    hits = [(3, 640, 640), (5.5, 700, 620), (7, 700, 700), (8.5, 360, 640), (9.5, 600, 640)]
    for hb, hx_, hy_ in hits: impact(p, g, hx_, hy_, t, hb * B, 0.8, seed=int(hb))
    dust(p, 900, GY, t, 3.4 * B, 0.6); dust(p, 860, GY, t, 7.6 * B, 0.7); dust(p, 300, GY, t, 8.9 * B, 0.6)
    impact(p, g, 1100, 560, t, 12.6 * B, 0.5, 'CREAM')
def tmf_ov(p, g, t):
    b = t / B
    marks = [(3, '×1'), (5.5, '×3'), (7, '×4'), (8.5, '×5'), (9.5, '×6')]
    cur = None
    for mb, v in marks:
        if b >= mb: cur = (v, mb * B)
    if cur: counter(p, g, '打飞', cur[0], t, cur[1])
    for mb, txt, x, y in [(3, '啪！', 760, 360), (5.5, '咚！', 820, 400), (7, '砰！', 700, 300), (8.5, '哐！', 280, 420), (9.5, '飞！', 820, 340)]:
        onomato(p, txt, x, y, t, mb * B, 96, 'GOLD', 0.6)
SHOTS[-1].ov = tmf_ov

@shot(4, cam=camk([(0, (1000, 470, 1.7)), (4, (1000, 470, 2.05))], fn=lambda x: x),
      caps=[(0, '拳头举到半空，', '他听见三个字——', (), ()), (1.5, '“我爹，', '是高太尉”', (), ((0, 3),))],
      ev=[(1, 'boom'), (1, 'title'), (2, 'tremble')], name='fist')
def fist(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_temple(p, g, t, cam)
    if b >= 1:
        k = eo((b - 1) / 1.2)
        p.c.push_group(); figure(p, None, 860, GY + 300, 2.6 * lerp(0.6, 1, k), -1, 'point', 'gq', t=t); pat = p.c.pop_group()
        p.c.set_source_rgba(0.25, 0.06, 0.03, 0.8 * k); p.c.mask(pat)
        p.rect(-1600, -600, 4400, 2400, 'RED2', a=0.25 * k)
    jit = math.sin(t * 70) * 4 if b > 2 else 0
    figure(p, g, 1110, GY - 70, 0.95, -1, 'cower', 'gyn', t=t)
    figure(p, g, 1000 + jit, GY, 1.0, 1, 'fist', 'lin', t=t, extra=NS_NW)
def fist_ov(p, g, t):
    big_title(p, g, '高太尉', 540, 230, t, 1 * B, size=140, col='CREAM')
SHOTS[-1].ov = fist_ov

@shot(6, cam=camk([(0, (820, 560, 1.15)), (6, (760, 560, 1.0))]),
      caps=[(0, '拳头放下了，', '他往后退了一步', (), ((5, 8),))], ev=[(0.5, 'thud'), (2, 'step'), (2, 'wood'), (3, 'laugh'), (4, 'step'), (4.5, 'step'), (5, 'step')], name='temple_back')
def tmb(p, g, t):
    cam = _CAM['cur']; b = t / B
    bg_temple(p, g, t, cam)
    figure(p, g, 250 + clamp((b - 3) / 3) * 400, GY, 0.95, 1, 'cower' if b < 3 else walk(t, 1.0), 'wife', t=t)
    # 高衙内：跌坐 → 起身大笑 → 走
    if b < 0.5: figure(p, g, 1110, GY - 70 * (1 - b / 0.5), 0.95, -1, 'cower', 'gyn', t=t)
    elif b < 2.5: figure(p, g, 1110, GY, 0.95, -1, 'sit', 'gyn', t=t)
    elif b < 4: figure(p, g, 1110, GY, 0.95, -1, 'laugh', 'gyn', t=t)
    else: figure(p, g, 1110 + (b - 4) * 140, GY, 0.95, 1, walk(t, 1.2), 'gyn', t=t)
    lx = track(t, kb([(0, 1000), (1.7, 1000), (2.2, 880, 'out')]))
    q = anim(t, kb([(0, 'fist'), (0.8, 'fistLow'), (1.7, 'fistLow'), (2.2, 'stepBack', 'out'), (3.5, 'idle')]))
    figure(p, g, lx, GY, 1.0, 1, q, 'lin', t=t, extra=NS_NW)
    footstep(p, g, 900, t, 2 * B)
def tmb_ov(p, g, t):
    if t >= 2 * B: counter(p, g, '退', '×1', t, 2 * B)
    onomato(p, '哈哈哈！', 900, 330, t, 3 * B, 80, 'CREAM', 1.5)
SHOTS[-1].ov = tmb_ov
