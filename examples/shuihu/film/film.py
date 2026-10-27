from lib import *
import random, math

EVENTS = []      # (global_time, kind)
SHAKES = []      # (global_time, amp)
FLASH = []       # (global_time,)
_cur = {'start': 0.0, 'rec': False}

def ev(kind, beat):
    t = beat * B
    if _cur['rec']:
        EVENTS.append((_cur['start'] + t, kind))
        if kind in ('stamp', 'boom', 'crash', 'title', 'land'): SHAKES.append((_cur['start'] + t, 22 if kind != 'title' else 12))
        if kind in ('flash',): FLASH.append(_cur['start'] + t)
    return t

def bt(t): return t / B

def caps(p_t, lst):
    cur = None
    for item in lst:
        if p_t >= item[0] * B: cur = item
    return cur

# ---------- 共用小部件 ----------
def moon_stage(p, t, dark=False):
    p.poly([(0, STAGE_T), (W, STAGE_T), (W, STAGE_B), (0, STAGE_B)], '#7a3a1c' if not dark else '#3b1c0f')
    cx, cy = 540, 470
    for k in range(9, 0, -1):
        p.ring(cx, cy, 280 + k * 42 + math.sin(t * 2 + k) * 4, 'LN', 2.5, 0.35)
    p.ell(cx, cy, 290, 290, '#e8964f')
    for (x, y, r) in [(460, 380, 46), (640, 520, 30), (610, 340, 20)]: p.ell(x, y, r, r, '#d9813f')
    cloud(p, 160, 170); cloud(p, 920, 140); cloud(p, 900, 600)

def gold_particles(p, t, t0, cx=540, cy=470, n=60):
    if t < t0: return
    k = t - t0; rnd = random.Random(7)
    for i in range(n):
        r0 = rnd.uniform(120, 420); a0 = rnd.uniform(0, 6.28); sp = rnd.uniform(0.6, 1.6)
        a = a0 + k * sp; r = r0 + 30 * math.sin(k * 3 + i)
        al = min(1, k / 0.3) * (0.5 + 0.5 * math.sin(k * 6 + i))
        p.ell(cx + math.cos(a) * r, cy + math.sin(a) * r * 0.9, 4, 4, 'GOLD', a=max(0, al))

def temple(p, x, gy, s=1.0, plaque='岳庙', col='RED'):
    c = p.c
    p.poly([(x - 200 * s, gy), (x + 200 * s, gy), (x + 200 * s, gy - 20 * s), (x - 200 * s, gy - 20 * s)], 'BLK')
    for k in (-150, -60, 60, 150): p.poly([(x + (k - 10) * s, gy - 20 * s), (x + (k + 10) * s, gy - 20 * s), (x + (k + 10) * s, gy - 220 * s), (x + (k - 10) * s, gy - 220 * s)], col)
    p.poly([(x - 260 * s, gy - 220 * s), (x + 260 * s, gy - 220 * s), (x + 200 * s, gy - 300 * s), (x - 200 * s, gy - 300 * s)], 'BLK', 'LN', 2.5)
    p.poly([(x - 290 * s, gy - 210 * s), (x - 250 * s, gy - 240 * s), (x + 250 * s, gy - 240 * s), (x + 290 * s, gy - 210 * s)], 'BLK')
    p.poly([(x - 60 * s, gy - 290 * s), (x + 60 * s, gy - 290 * s), (x + 60 * s, gy - 250 * s), (x - 60 * s, gy - 250 * s)], 'GOLD', 'BLK', 3)
    p.text(plaque, x, gy - 258 * s, 30 * s, 'BLK')

def tree(p, x, gy, h=520, s=1.0, broken=0.0):
    p.poly([(x - 18 * s, gy), (x + 18 * s, gy), (x + 10 * s, gy - h), (x - 10 * s, gy - h)], 'BLK')
    for i, (dy, L, sg) in enumerate([(0.55, 120, -1), (0.7, 150, 1), (0.85, 110, -1), (0.95, 90, 1)]):
        yy = gy - h * dy
        p.line([(x, yy), (x + sg * L * s, yy - 60 * s)], 'BLK', 10 * s)
    p.ell(x, gy - h, 120 * s, 70 * s, 'BLK')

def rope(p, x, gy):
    for k in range(3): p.line([(x - 40, gy - 230 + k * 40), (x + 40, gy - 220 + k * 40)], 'CREAM', 4)

def cangue(p, hx, hy):
    p.poly([(hx - 60, hy + 34), (hx + 60, hy + 34), (hx + 60, hy + 54), (hx - 60, hy + 54)], '#6b4a2a', 'BLK', 3)

def seal_card(p, x, y, s=1.0, txt='配', col='GOLD', rot=0.0):
    c = p.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p.poly([(-50, -50), (50, -50), (50, 50), (-50, 50)], col, 'BLK', 6)
    p.text(txt, 0, 26, 70, 'BLK')
    c.restore()

def big_face(p, t, seal=True, cx=540, cy=600, sc=4.6):
    c = p.c
    p.ell(cx, cy, 430, 430, '#9a4a22'); p.ell(cx, cy, 380, 380, '#b45f2c')
    c.save(); c.translate(cx, cy); c.scale(sc, sc)
    head(p, 0, 0, 'lin', 1, {'seal': seal})
    p.poly([(-14, 34), (14, 34), (16, 80), (-16, 80)], 'CREAM')
    c.restore()

def crowd(p, x0, gy, n_cols, n_rows, sc, kind, pose, face=-1, dx=70, dy=-28, t=0, jitter=0, seed=0, shrink=0.06):
    rnd = random.Random(seed)
    for r in range(n_rows - 1, -1, -1):
        ss = sc * (1 - shrink * r)
        for i in range(n_cols):
            x = x0 + i * dx * (1 - shrink * r) + (r % 2) * dx * 0.5
            figure(p, x + rnd.uniform(-jitter, jitter), gy + r * dy, ss, face, pose, kind, t=t)

def fly_fig(p, x, gy, sc, face, kind, t, t0, vx=600, vy=-700, spin=540, pose='cower'):
    """被打飞：抛物线 + 旋转"""
    if t < t0:
        figure(p, x, gy, sc, face, 'guard' if kind not in ('wife',) else 'stand', kind, t=t); return
    k = t - t0
    xx = x + vx * k; yy = gy + vy * k + 1400 * k * k
    if yy > gy + 400: return
    figure(p, xx, yy, sc, face, pose, kind, rot=spin * k, t=t)

# ================= 场景 =================
def S0(p, t):
    """开场：雪月亮相"""
    T = {k: ev(n, b) for k, n, b in [('t1', 'title', 1), ('t2', 'boom', 2), ('fly', 'whoosh', 4), ('st', 'stamp', 5),
                                    ('p1', 'whoosh', 6), ('p2', 'hit', 7), ('p3', 'whoosh', 8), ('p4', 'hit', 9), ('end', 'gong', 10)]}
    b = bt(t)
    if 2 <= b < 4:
        moon_stage(p, t, dark=True); big_face(p, t, seal=False)
        big_title(p, '退一步，进一枪', 540, 140, t, T['t2'], size=100)
        return
    moon_stage(p, t)
    snow(p, t, 70, seed=3)
    ground(p)
    pose = pose_track(t, [(0, 'stand'), (T['p1'], 'guard'), (T['p2'], 'thrust'), (T['p3'], 'raise'), (T['p4'], 'sweep'), (10.2 * B, 'stand')])
    gold_particles(p, t, T['p1'])
    info = figure(p, 540, 880, 1.25, 1, pose, 'lin', t=t, extra={'seal': b >= 5})
    if 4 <= b < 5:
        k = ease((t - T['fly']) / B)
        hx_, hy_ = info['head']
        seal_card(p, lerp(1000, hx_ - 18, k), lerp(120, hy_ + 10, k), lerp(1.4, 0.25, k), rot=k * 6)
    burst(p, info['head'][0] - 18, info['head'][1] + 10, t, T['st'], 160)
    if b >= 6:
        burst(p, info['hand'][0], info['hand'][1], t, T['p2'], 120)
        burst(p, info['hand'][0], info['hand'][1], t, T['p4'], 120)
    if b >= 1:
        big_title(p, '豹子头 · 林冲', 540, 150, t, T['t1'], size=84, col='CREAM')
    nametag(p, 'LIN CHONG', '林冲', 820, 330, t, 0.0, 2 * B)
    onomato(p, '啪！', 720, 360, t, T['st'], 80, 'GOLD')

S0.caps = [(0, '水浒群英 · 第1集', '豹子头 林冲', (), (0, 3)), (4, '朝廷的金印飞来，', '他一步不躲', (2, 4), ()),
           (6, '八十万禁军的枪法，', '全在这一杆红缨', (), (5, 8))]

def S1(p, t):
    """教头：校场，禁军越来越多"""
    T = [ev('hit', b) for b in range(0, 12)]
    ev('wood', 0); ev('wood', 4); ev('title', 8); ev('wood', 8)
    b = bt(t)
    stage_bg(p, seed=2); ground(p)
    cyc = ['guard', 'thrust', 'raise', 'chop']
    pose = pose_track(t, [(T[i], cyc[i % 4]) for i in range(12)], snap=0.12)
    # 点将台
    p.poly([(40, 880), (300, 880), (280, 780), (60, 780)], 'BLK', 'LN', 3)
    if b < 4:
        crowd(p, 470, 880, 6, 2, 0.55, 'soldier', pose, face=-1, dx=95, dy=-60, t=t, shrink=0.1)
        val, tl = '×10', T[0]
    elif b < 8:
        crowd(p, 380, 880, 12, 5, 0.33, 'soldier', pose, face=-1, dx=58, dy=-40, t=t, shrink=0.08)
        val, tl = '×1万', T[4]
    else:
        crowd(p, 340, 880, 22, 9, 0.2, 'soldier', pose, face=-1, dx=34, dy=-26, t=t, shrink=0.05)
        val, tl = '×80万', T[8]
    info = figure(p, 170, 780, 0.75, 1, pose, 'lin', t=t)
    burst(p, info['hand'][0], info['hand'][1], t, T[int(b)], 70)
    counter(p, '禁军', val, t, tl)
    big_title(p, '八十万禁军教头', 600, 230, t, T[8], size=96)
    nametag(p, 'DONGJING', '东京校场', 120, 120, t, 0, 3 * B)

S1.caps = [(0, '东京校场一声令下，', '徒弟跟着出枪', (), ()), (4, '一个变一万，', '一万变八十万', (), ()),
           (8, '八十万禁军教头，', '一杆红缨枪 镇京城', (0, 7), (7, 10))]

def S2(p, t):
    """岳庙：调戏 → 打狗腿子 → 举拳 → 退一步"""
    ev('wood', 0); ev('whoosh', 2); ev('wood', 4)
    run = [ev('step', b) for b in (6, 6.5, 7)]
    ev('boom', 7)
    hits = [ev('hit', b) for b in (8, 9, 10, 11, 12, 13)]
    ev('whoosh', 14); ev('title', 15); ev('wood', 18); ev('step', 18); ev('laugh', 20)
    b = bt(t)
    stage_bg(p, seed=4); temple(p, 760, 880, 1.0, '岳庙')
    # 香炉
    p.poly([(500, 880), (560, 880), (570, 830), (490, 830)], 'BLK', 'LN', 2)
    for k in range(3): p.line([(515 + k * 15, 830), (515 + k * 15 + math.sin(t * 3 + k) * 6, 760)], 'CREAM', 2, 0.6)
    ground(p)
    thugX = [620, 700, 780, 860, 940, 1010]
    if b < 6:
        wife_pose = 'pray' if b < 2 else 'cower'
        figure(p, 330, 880, 0.9, 1, wife_pose, 'wife', t=t)
        if b >= 2:
            k = eo((t - 2 * B) / (2 * B))
            figure(p, lerp(1200, 520, k), 880, 0.9, -1, 'fan', 'gyn', t=t)
            for i, x in enumerate(thugX):
                figure(p, lerp(1300 + i * 80, x, k), 880, 0.85, -1, 'run1' if int(t * 4) % 2 else 'run2', 'thug', t=t)
            nametag(p, 'GAO YANEI', '花花太岁 · 高衙内', 420, 520, t, 3 * B, 3 * B)
        nametag(p, 'LIN NIANGZI', '林娘子', 190, 560, t, 0, 2 * B)
        return
    if b < 8:
        # 林冲狂奔
        stage_bg(p, seed=9); ground(p)
        x = lerp(-100, 700, (t - 6 * B) / (2 * B))
        pose = 'run1' if int(t * 5) % 2 else 'run2'
        figure(p, x, 880, 1.0, 1, pose, 'lin', t=t, extra={'weapon': None, 'seal': False})
        speedlines(p, x - 400, 600, x - 50, 600, t, 6 * B, 2 * B, 10)
        onomato(p, '住手！', 760, 300, t, 7 * B, 120, 'CREAM')
        return
    if b < 14:
        # 打狗腿子：每拍飞一个
        figure(p, 150, 880, 0.85, 1, 'cower', 'wife', t=t)
        poses = ['punch', 'kick', 'sweep', 'punch', 'kick', 'thrust']
        pose = pose_track(t, [(hits[i], poses[i]) for i in range(6)], snap=0.12)
        lx = 360 + 30 * int(b - 8)
        info = figure(p, lx, 880, 1.0, 1, pose, 'lin', t=t, extra={'weapon': None, 'seal': False})
        figure(p, 1000, 880, 0.9, -1, 'cower', 'gyn', t=t)
        for i in range(6):
            fly_fig(p, lx + 150 + i * 70, 880, 0.85, -1, 'thug', t, hits[i], vx=500 + i * 60, vy=-800 - i * 40)
        i_ = min(5, int(b - 8))
        burst(p, info['hand'][0] + 40, info['hand'][1], t, hits[i_], 130)
        onomato(p, ['砰！', '啪！', '咚！', '砰！', '啪！', '轰！'][i_], 700, 360, t, hits[i_], 96, 'GOLD', 0.5)
        counter(p, '打飞', '×%d' % (i_ + 1), t, hits[i_])
        return
    # 14-24: 揪住高衙内 → 高太尉 → 退一步
    if b < 15:
        figure(p, 560, 880, 1.0, -1, 'cower', 'gyn', t=t)
        figure(p, 420, 880, 1.0, 1, 'fist', 'lin', t=t, extra={'weapon': None, 'seal': False})
        onomato(p, '你敢！', 700, 380, t, 14 * B, 90)
        return
    if b < 18:
        p.poly([(0, STAGE_T), (W, STAGE_T), (W, STAGE_B), (0, STAGE_B)], '#5a2412')
        # 高俅巨影
        figure(p, 800, 1010, 2.0, -1, 'point', 'gq', t=t)
        sh = 6 * math.sin(t * 60) if b >= 16 else 0
        figure(p, 300 + sh, 880, 1.0, 1, 'fist', 'lin', t=t, extra={'weapon': None, 'seal': False})
        figure(p, 440, 880, 0.9, -1, 'fan', 'gyn', t=t)
        big_title(p, '我爹是高太尉', 540, 210, t, 15 * B, size=92, col='CREAM')
        return
    figure(p, 840, 880, 0.9, -1, 'fan', 'gyn', t=t)
    for i in range(4): figure(p, 950 + i * 50, 880, 0.75, -1, 'stand', 'thug', t=t)
    k = ease((t - 18 * B) / (0.5 * B))
    lx = lerp(560, 440, k)
    pose = 'back' if b < 20 else 'stand'
    figure(p, 300, 880, 0.9, 1, 'cower', 'wife', t=t)
    figure(p, lx, 880, 1.0, 1, pose, 'lin', t=t, extra={'weapon': None, 'seal': False})
    if b >= 18:
        p.line([(560, 900), (450, 900)], 'GOLD', 5); p.poly([(440, 900), (470, 888), (470, 912)], 'GOLD')
        counter(p, '退', '×1', t, 18 * B)
    onomato(p, '哈哈哈！', 840, 420, t, 20 * B, 70, 'CREAM', 2.0)

S2.caps = [(0, '岳庙进香，', '娘子被人拦住去路', (), (5, 7)), (6, '林冲一路狂奔，', '赶到庙前', (), ()),
           (8, '狗腿子一拥而上，', '来一个，飞一个', (), (5, 7)), (14, '拳头举到半空，', '他听见三个字：高太尉', (), (7, 10)),
           (18, '拳头放下，', '他退了一步', (), (3, 6))]

def S3(p, t):
    """白虎堂：买刀 → 节堂 → 军汉群殴 → 放刀 → 刺配沧州"""
    ev('wood', 0); ev('clang', 2); ev('wood', 4); ev('title', 6); ev('boom', 8)
    hits = [ev('hit', b) for b in (10, 11, 12, 13, 14, 15, 16, 17)]
    ev('clang', 18); ev('stamp', 20); ev('stamp', 22)
    b = bt(t)
    if b < 4:
        stage_bg(p, seed=11); ground(p)
        # 街市 + 卖刀人
        for i in range(4): p.poly([(60 + i * 260, 880), (220 + i * 260, 880), (220 + i * 260, 700), (140 + i * 260, 640), (60 + i * 260, 700)], 'HILL', 'BLK', 3)
        figure(p, 700, 880, 0.95, -1, 'point', 'zhuang', t=t, extra={'weapon': 'blade'})
        figure(p, 420, 880, 1.0, 1, 'stand' if b < 2 else 'point', 'lin', t=t, extra={'weapon': None, 'seal': False})
        if b >= 2:
            burst(p, 760, 640, t, 2 * B, 120, 'CREAM')
            p.line([(640, 700), (820, 600)], 'CREAM', 10)
        onomato(p, '锵——', 760, 520, t, 2 * B, 80, 'CREAM')
        return
    if b < 8:
        p.poly([(0, STAGE_T), (W, STAGE_T), (W, STAGE_B), (0, STAGE_B)], '#8a3a1e')
        for x in (120, 960): p.poly([(x - 22, 880), (x + 22, 880), (x + 22, 200), (x - 22, 200)], 'RED', 'BLK', 3)
        p.poly([(300, 130), (780, 130), (780, 260), (300, 260)], 'BLK', 'GOLD', 5)
        big_title(p, '白虎节堂', 540, 228, t, 6 * B, size=100)
        # 虎纹
        for k in range(5): p.line([(380 + k * 80, 300), (420 + k * 80, 340), (380 + k * 80, 380)], 'BLK', 12)
        ground(p)
        k = ease((t - 4 * B) / (2 * B))
        x = lerp(200, 540, k)
        figure(p, x, 880, 1.0, 1, 'run1' if (int(t * 3) % 2 and b < 6) else 'stand', 'lin', t=t, extra={'weapon': 'blade', 'seal': False})
        for i, o in enumerate((-120, 140)): figure(p, x + o, 880, 0.9, 1, 'stand', 'cop', t=t, extra={'weapon': None})
        return
    p.poly([(0, STAGE_T), (W, STAGE_T), (W, STAGE_B), (0, STAGE_B)], '#8a3a1e')
    for x in (60, 1020): p.poly([(x - 22, 880), (x + 22, 880), (x + 22, 200), (x - 22, 200)], 'RED', 'BLK', 3)
    p.poly([(340, 90), (740, 90), (740, 180), (340, 180)], 'BLK', 'GOLD', 4); p.text('白虎节堂', 540, 160, 60, 'GOLD')
    ground(p)
    if b < 10:
        figure(p, 880, 880, 1.0, -1, 'point', 'gq', t=t)
        nametag(p, 'GAO QIU', '殿帅府太尉 · 高俅', 760, 380, t, 8 * B, 2 * B)
        onomato(p, '拿下！', 820, 300, t, 8 * B, 110, 'RED')
        figure(p, 400, 880, 1.0, 1, 'guard', 'lin', t=t, extra={'weapon': 'blade', 'seal': False})
        k = eo((t - 8.5 * B) / B)
        crowd(p, lerp(-500, 60, k), 880, 4, 3, 0.7, 'guard', 'guard', face=1, dx=70, dy=-30, t=t, seed=1)
        crowd(p, lerp(1500, 620, k), 880, 4, 3, 0.7, 'guard', 'guard', face=-1, dx=70, dy=-30, t=t, seed=2)
        return
    if b < 18:
        poses = ['chop', 'sweep', 'thrust', 'swing', 'chop', 'kick', 'sweep', 'thrust']
        pose = pose_track(t, [(hits[i], poses[i]) for i in range(8)], snap=0.12)
        i_ = min(7, int(b - 10))
        face = 1 if i_ % 2 == 0 else -1
        # 每拍换机位：林冲左右换位，四周军汉一大片
        lx = 420 if face == 1 else 660
        # 背后一排排军汉
        crowd(p, 60, 720, 18, 2, 0.34, 'guard', 'guard', face=-face, dx=58, dy=-34, t=t, seed=3)
        info = figure(p, lx, 880, 1.05, face, pose, 'lin', t=t, extra={'weapon': 'blade', 'seal': False})
        rnd = random.Random(i_)
        for j in range(5):
            gx = lx + face * (160 + j * 70)
            fly_fig(p, gx, 880, 0.8, -face, 'guard', t, hits[i_] + 0.02 * j, vx=face * (400 + j * 90), vy=-600 - rnd.uniform(0, 300))
        for j in range(3):
            figure(p, lx - face * (180 + j * 80), 880, 0.8, face, 'guard', 'guard', t=t)
        burst(p, info['hand'][0] + face * 60, info['hand'][1], t, hits[i_], 150)
        counter(p, '放倒军汉', '×%d' % [3, 6, 10, 15, 21, 28, 36, 45][i_], t, hits[i_])
        return
    if b < 20:
        figure(p, 880, 880, 1.0, -1, 'point', 'gq', t=t)
        crowd(p, 120, 860, 12, 2, 0.55, 'guard', 'guard', face=1, dx=75, dy=-40, t=t, seed=5)
        figure(p, 420, 880, 1.0, 1, 'kneel', 'lin', t=t, extra={'weapon': None, 'seal': False})
        if b >= 18:
            k = min(1, (t - 18 * B) / 0.4)
            p.line([(520, lerp(700, 870, k)), (640, lerp(660, 870, k))], 'CREAM', 9)
            counter(p, '退', '×2', t, 18 * B)
            onomato(p, '哐当', 640, 780, t, 18 * B, 70, 'CREAM')
        return
    if b < 22:
        figure(p, 540, 880, 1.15, 1, 'kneel', 'lin', t=t, extra={'weapon': None, 'seal': False})
        k = ease((t - 19.4 * B) / (0.6 * B))
        c = p.c; c.save(); c.translate(540, lerp(-200, 470, k)); c.rotate(-0.08)
        s_ = punch(t, 20 * B, 0.25, 0.25) if b >= 20 else 1
        c.scale(s_, s_)
        p.poly([(-300, -120), (300, -120), (300, 120), (-300, 120)], 'RED', 'BLK', 8)
        p.poly([(-280, -100), (280, -100), (280, 100), (-280, 100)], 'RED', 'CREAM', 4)
        p.text('刺配沧州', 0, 46, 130, 'CREAM')
        c.restore()
        return
    moon_stage(p, t, dark=True); big_face(p, t, seal=True)
    burst(p, 540 - 14 * 6, 560 + 10 * 6, t, 22 * B, 200)

S3.caps = [(0, '街上偶遇一口宝刀，', '他爱不释手', (), ()), (4, '太尉请他比刀，', '把他领进白虎节堂', (), (4, 8)),
           (8, '持刀闯节堂，', '反咬他要刺杀太尉', (), (7, 9)), (10, '堂上军汉一拥而上，', '放倒一片又一片', (), ()),
           (18, '刀，他自己放下了', '', (), ()), (20, '刺配沧州，', '脸上烙了金印', (0, 4), (4, 6))]

def S4(p, t):
    """野猪林：押解 → 绑树 → 禅杖天降 → 鲁智深"""
    ev('wood', 0); [ev('whip', b) for b in (1, 2, 3)]; ev('wood', 4); ev('wood', 6)
    ev('whoosh', 8); ev('clang', 9); ev('land', 10); ev('title', 10)
    hits = [ev('hit', b) for b in (12, 13)]; ev('crash', 14); ev('boom', 16); ev('wood', 18)
    b = bt(t)
    BGc = '#6a3a1a'
    if b < 4:
        stage_bg(p, BGc, col_h='#4f2a14', col_h2='#5c3218', seed=21); ground(p)
        x = 520 + (t % (2 * B)) * 10
        info = figure(p, x, 880, 1.0, 1, 'bound', 'lin', t=t, extra={'weapon': None})
        cangue(p, *info['head'])
        for i, o in enumerate((-200, 220)):
            pp = pose_track(t, [(0, 'stand'), (B, 'raise'), (1.4 * B, 'chop'), (2 * B, 'raise'), (2.4 * B, 'chop'), (3 * B, 'raise'), (3.4 * B, 'chop')])
            figure(p, x + o, 880, 0.95, 1 if o < 0 else -1, pp, 'cop', t=t)
        nametag(p, 'DONG CHAO', '公差 · 董超', 170, 420, t, 0, 3 * B)
        nametag(p, 'XUE BA', '公差 · 薛霸', 760, 420, t, 0, 3 * B)
        onomato(p, '啪！', 440, 470, t, B, 70); onomato(p, '啪！', 640, 430, t, 2 * B, 70); onomato(p, '快走！', 780, 360, t, 3 * B, 70)
        return
    # 野猪林
    p.poly([(0, STAGE_T), (W, STAGE_T), (W, STAGE_B), (0, STAGE_B)], '#4a2a16')
    for x, h in [(80, 700), (260, 620), (900, 680), (1020, 600), (700, 560)]:
        tree(p, x, 880, h, 1.0)
    big = b >= 14
    if not big: tree(p, 520, 880, 640, 1.2)
    ground(p)
    if b < 8:
        p.ell(540, 400, 600, 600, '#000000', a=0.25 * min(1, (t - 4 * B) / B))
        info = figure(p, 520, 880, 1.0, 1, 'bound', 'lin', t=t, extra={'weapon': None})
        cangue(p, *info['head']); rope(p, 520, 880)
        figure(p, 340, 880, 1.0, 1, 'raise', 'cop', t=t)
        figure(p, 700, 880, 1.0, -1, 'raise', 'cop', t=t)
        if b >= 6: counter(p, '退', '×3', t, 6 * B)
        return
    if b < 10:
        info = figure(p, 520, 880, 1.0, 1, 'bound', 'lin', t=t, extra={'weapon': None})
        cangue(p, *info['head']); rope(p, 520, 880)
        cp = 'raise' if b < 9 else 'cower'
        figure(p, 340, 880, 1.0, 1, cp, 'cop', t=t)
        figure(p, 700, 880, 1.0, -1, cp, 'cop', t=t)
        # 禅杖旋转飞来
        k = min(1, (t - 8 * B) / B)
        cx, cy = lerp(-100, 520, k), lerp(80, 560, k)
        if b < 9.2:
            c = p.c; c.save(); c.translate(cx, cy); c.rotate(t * 20)
            p.line([(-150, 0), (150, 0)], 'BLK', 14); p.ell(150, 0, 30, 30, 'CREAM'); p.ell(150, 0, 14, 14, 'BLK'); p.ell(-150, 0, 16, 12, 'CREAM')
            c.restore()
            speedlines(p, cx - 300, cy - 230, cx, cy, t, 8 * B, B, 8)
        onomato(p, '呼——！', 300, 260, t, 8 * B, 110)
        burst(p, 520, 560, t, 9 * B, 220)
        if b >= 9:
            rnd = random.Random(3)
            for j in range(6):
                kk = t - 9 * B
                p.line([(520 + rnd.uniform(-200, 200) * kk * 3, 560 + (rnd.uniform(-400, 100) + 1200 * kk) * kk), (560 + rnd.uniform(-200, 200) * kk * 3, 600 + (rnd.uniform(-400, 100) + 1200 * kk) * kk)], 'BLK', 9)
            onomato(p, '咔嚓！', 760, 420, t, 9 * B, 100, 'GOLD')
        return
    if b < 12:
        k = eo((t - 10 * B) / (0.4 * B))
        info = figure(p, 360, 880, 1.0, 1, 'bound', 'lin', t=t, extra={'weapon': None}); cangue(p, *info['head']); rope(p, 360, 880)
        figure(p, 640, lerp(-300, 880, k), 1.35, -1, 'swing', 'lu', t=t)
        smoke(p, 640, 880, t, 10 * B, 120); smoke(p, 540, 890, t, 10 * B + 0.05, 90); smoke(p, 760, 890, t, 10 * B + 0.08, 90)
        figure(p, 180, 880, 0.9, 1, 'cower', 'cop', t=t); figure(p, 900, 880, 0.9, -1, 'cower', 'cop', t=t)
        big_title(p, '禅杖天降', 540, 220, t, 10 * B, size=120)
        nametag(p, 'LU ZHISHEN', '花和尚 · 鲁智深', 760, 330, t, 10.5 * B, 1.5 * B)
        return
    if b < 14:
        i_ = int(b - 12)
        pose = pose_track(t, [(hits[0], 'swing'), (hits[1], 'chop')], snap=0.12)
        info = figure(p, 520, 880, 1.35, 1 if i_ == 0 else -1, pose, 'lu', t=t)
        fly_fig(p, 760, 880, 0.9, -1, 'cop', t, hits[0], vx=500, vy=-900)
        fly_fig(p, 280, 880, 0.9, 1, 'cop', t, hits[1], vx=-500, vy=-900)
        burst(p, info['hand'][0], info['hand'][1] - 60, t, hits[i_], 200)
        onomato(p, '咚！', 540 + (200 if i_ == 0 else -200), 360, t, hits[i_], 110, 'GOLD', 0.6)
        counter(p, '打飞公差', '×%d' % (i_ + 1), t, hits[i_])
        return
    if b < 18:
        # 一禅杖打断松树
        k = ease((t - 14 * B) / (0.6 * B))
        c = p.c; c.save(); c.translate(760, 600); c.rotate(k * 1.2); c.translate(-760, -600)
        tree(p, 760, 880, 520, 1.1); c.restore()
        figure(p, 560, 880, 1.35, 1, 'swing' if b < 14.5 else 'chop', 'lu', t=t)
        figure(p, 180, 880, 0.85, 1, 'kneel', 'cop', t=t); figure(p, 300, 880, 0.85, 1, 'kneel', 'cop', t=t)
        burst(p, 760, 600, t, 14 * B, 180)
        onomato(p, '咔——嚓！', 820, 330, t, 14 * B, 100, 'GOLD', 1.2)
        onomato(p, '饶命！', 240, 560, t, 16 * B, 80, 'CREAM', 1.2)
        return
    stage_bg(p, BGc, col_h='#4f2a14', col_h2='#5c3218', seed=22); ground(p)
    x = lerp(300, 520, (t - 18 * B) / (6 * B))
    figure(p, x, 880, 1.0, 1, 'run1' if int(t * 3) % 2 else 'run2', 'lin', t=t, extra={'weapon': None})
    figure(p, x + 200, 880, 1.25, 1, 'run1' if int(t * 3 + 1) % 2 else 'run2', 'lu', t=t)
    nametag(p, 'CANGZHOU', '沧州', 900, 160, t, 20 * B, 4 * B)

S4.caps = [(0, '发配路上，', '公差一路棍棒伺候', (), ()), (4, '野猪林里绑上大树，', '他闭上眼，又退一步', (), (6, 9)),
           (8, '水火棍刚要落下——', '', (0, 3), ()), (10, '禅杖天降，', '花和尚到了', (0, 4), (1, 4)),
           (14, '一禅杖下去，', '松树断成两截', (), ()), (18, '一路护送，', '直到沧州', (), (4, 6))]

def S5(p, t):
    """柴进庄：棒打洪教头"""
    ev('wood', 0); ev('boom', 2)
    hits = [ev('clang', b) for b in (4, 5, 6)]
    ev('whoosh', 8); ev('hit', 8.5); ev('land', 9); ev('title', 9); ev('laugh', 11)
    b = bt(t)
    stage_bg(p, seed=31)
    p.poly([(0, 880), (W, 880), (W, 820), (0, 820)], '#7a3a1c')
    for i in range(6): p.poly([(i * 200 + 40, 820), (i * 200 + 80, 820), (i * 200 + 80, 600), (i * 200 + 40, 600)], 'BLK')
    ground(p)
    if b < 4:
        figure(p, 540, 880, 0.9, 1, 'stand', 'chai', t=t)
        nametag(p, 'CHAI JIN', '小旋风 · 柴进', 420, 470, t, 0, 3 * B)
        figure(p, 820, 880, 1.0, -1, 'chop' if b >= 2 else 'stand', 'hong', t=t)
        figure(p, 260, 880, 1.0, 1, 'stand', 'lin', t=t, extra={'weapon': 'staff'})
        nametag(p, 'HONG', '洪教头', 760, 470, t, 2 * B, 2 * B)
        onomato(p, '来来来！', 820, 380, t, 2 * B, 90)
        return
    if b < 8:
        i_ = min(2, int(b - 4))
        pp = pose_track(t, [(hits[0], 'chop'), (hits[1], 'guard'), (hits[2], 'chop'), (7 * B, 'guard')], snap=0.12)
        pl = pose_track(t, [(hits[0], 'guard'), (hits[1], 'raise'), (hits[2], 'guard')], snap=0.12)
        figure(p, 640, 880, 1.0, -1, pp, 'hong', t=t)
        figure(p, 420, 880, 1.0, 1, pl, 'lin', t=t, extra={'weapon': 'staff'})
        burst(p, 530, 600, t, hits[i_], 120)
        counter(p, '回合', '×%d' % (i_ + 1), t, hits[i_])
        return
    if b < 11:
        k = (t - 8.5 * B)
        figure(p, 360, 880, 1.0, 1, 'sweep' if b >= 8.3 else 'guard', 'lin', t=t, extra={'weapon': 'staff'})
        if b < 8.5:
            figure(p, 620, 880, 1.0, -1, 'chop', 'hong', t=t)
        elif b < 9:
            figure(p, 620, 880 - 300 * math.sin(min(1, k / (0.5 * B)) * math.pi), 1.0, -1, 'cower', 'hong', rot=min(1, k / (0.5 * B)) * 180, t=t)
        else:
            figure(p, 660, 920, 1.0, -1, 'cower', 'hong', rot=-90, t=t)
            smoke(p, 640, 880, t, 9 * B, 110)
        speedlines(p, 300, 860, 700, 860, t, 8.3 * B, 0.3, 6)
        onomato(p, '啪！', 700, 520, t, 9 * B, 120, 'GOLD')
        big_title(p, '一棒', 540, 240, t, 9 * B, size=150)
        counter(p, '回合', '×4', t, 8.5 * B)
        return
    figure(p, 360, 880, 1.0, 1, 'stand', 'lin', t=t, extra={'weapon': 'staff'})
    figure(p, 660, 920, 1.0, -1, 'cower', 'hong', rot=-90, t=t)
    figure(p, 880, 880, 0.9, -1, 'point', 'chai', t=t)
    onomato(p, '好！', 880, 400, t, 11 * B, 100)

S5.caps = [(0, '沧州柴进庄上，', '洪教头偏要比棒', (), (0, 3)), (4, '三个回合，', '林冲只守不攻', (), ()),
           (8, '第四棒扫过去，', '洪教头躺下了', (), ())]

def S6(p, t):
    """风雪山神庙：草厅塌 → 山神庙 → 起火 → 门外三人 → 退无可退"""
    ev('wind', 0); ev('crash', 2); ev('wood', 4); ev('fire', 8); ev('boom', 8); ev('wood', 12); ev('laugh', 13)
    ev('crack', 16); ev('crack', 17); ev('boom', 18); ev('title', 18)
    b = bt(t)
    stage_bg(p, 'NIGHT', col_h='#151a28', col_h2='NIGHT2', seed=41)
    p.ell(860, 180, 70, 70, 'SNOW', a=0.85)
    if b < 4:
        ground(p, col='BLK')
        k = ease((t - 2 * B) / (0.4 * B)) if b >= 2 else 0
        # 草厅
        p.poly([(460, 880), (760, 880), (760, 680 + k * 160), (460, 680 + k * 160)], '#2a1e14', 'LN', 2)
        p.poly([(420, 690 + k * 170), (800, 690 + k * 170), (610, 560 + k * 300), ], 'SNOW')
        smoke(p, 610, 860, t, 2 * B, 160)
        figure(p, 250, 880, 1.0, 1, 'stand' if b < 2 else 'back', 'lin', t=t, extra={'weapon': 'spear'})
        onomato(p, '轰——', 700, 450, t, 2 * B, 110)
        snow(p, t, 160, seed=4, speed=1.4, wind=120)
        return
    if b < 8:
        ground(p, col='BLK')
        temple(p, 760, 880, 0.7, '山神庙', col='BLK')
        x = lerp(120, 600, (t - 4 * B) / (4 * B))
        info = figure(p, x, 880, 1.0, 1, 'run1' if int(t * 2.5) % 2 else 'run2', 'lin', t=t)
        snow(p, t, 160, seed=4, speed=1.4, wind=120)
        return
    if b < 12:
        ground(p, col='BLK')
        glow = min(1, (t - 8 * B) / B)
        p.poly([(0, STAGE_T), (W, STAGE_T), (W, 880), (0, 880)], 'FIRE', a=0.35 * glow)
        for i in range(3): p.poly([(200 + i * 260, 880), (420 + i * 260, 880), (310 + i * 260, 720)], '#2a1e14')
        fire(p, 540, 880, 900 * glow, 420 * glow, t)
        burst(p, 540, 700, t, 8 * B, 300, 'FIRE')
        onomato(p, '噼啪！', 300, 380, t, 8.5 * B, 90, 'GOLD')
        snow(p, t, 120, seed=5, speed=1.2, wind=120)
        nametag(p, 'CAOLIAOCHANG', '草料场', 820, 160, t, 8 * B, 4 * B)
        return
    if b < 16:
        ground(p, col='BLK')
        p.poly([(0, STAGE_T), (W, STAGE_T), (W, 880), (0, 880)], 'FIRE', a=0.25)
        # 左：庙门内林冲；右：门外三人
        p.poly([(0, STAGE_T), (330, STAGE_T), (330, 880), (0, 880)], '#120d0a')
        p.poly([(330, 300), (350, 300), (350, 880), (330, 880)], 'LN')
        figure(p, 170, 880, 1.0, 1, 'guard', 'lin', t=t)
        for i, (k_, po) in enumerate([('lq', 'point'), ('zhuang', 'fan'), ('cop', 'stand')]):
            figure(p, 560 + i * 170, 880, 0.95, -1, po if int(t * 2 + i) % 2 else 'stand', k_, t=t, extra={'weapon': None})
        nametag(p, 'LU QIAN', '陆谦', 520, 380, t, 12 * B, 4 * B)
        nametag(p, 'FU AN', '富安', 700, 380, t, 12.3 * B, 3.7 * B)
        nametag(p, 'CHABO', '差拨', 870, 380, t, 12.6 * B, 3.4 * B)
        onomato(p, '烧死他！', 760, 260, t, 13 * B, 90, 'CREAM', 2.5 * B)
        snow(p, t, 100, seed=6, speed=1.2, wind=120)
        return
    # 退×4 抖、裂、炸
    moon_stage(p, t, dark=True)
    p.c.save(); p.c.translate(540, 470)
    shake = 0 if b < 16 else (6 if b < 17 else 14)
    p.c.translate(math.sin(t * 70) * shake, math.cos(t * 63) * shake)
    if b < 18:
        s_ = punch(t, 16 * B, 0.2, 0.3)
        p.c.scale(2.2 * s_, 2.2 * s_)
        p.text('退×4', 0, 40, 120, 'GOLD', outline='BLK', ow=14)
        if b >= 16: p.line([(-80, -60), (-20, 0), (-50, 30), (10, 70)], 'BLK', 6)
        if b >= 17: p.line([(60, -70), (20, -10), (60, 20), (20, 80)], 'BLK', 6); p.line([(-120, 10), (-40, 20)], 'BLK', 5)
    p.c.restore()
    if b >= 18:
        rnd = random.Random(9)
        kk = t - 18 * B
        for j in range(16):
            an = rnd.uniform(0, 6.28); sp = rnd.uniform(300, 900)
            x = 540 + math.cos(an) * sp * kk; y = 470 + math.sin(an) * sp * kk + 900 * kk * kk
            p.poly([(x, y), (x + 40, y + 10), (x + 10, y + 40)], 'GOLD')
        burst(p, 540, 470, t, 18 * B, 380)
        big_title(p, '退无可退', 540, 520, t, 18 * B, size=150, col='CREAM')
    snow(p, t, 100, seed=7, speed=1.6, wind=200)

S6.caps = [(0, '风雪夜，', '草厅被大雪压塌', (0, 3), ()), (4, '他挑着酒葫芦，', '去山神庙躲一夜', (), (1, 4)),
           (8, '半夜，', '草料场烧红了半边天', (), (0, 3)), (12, '门外三个人在笑：', '火，是我们放的', (), ()),
           (16, '第四步，', '他退不下去了', (), ())]

def S7(p, t):
    """进一枪：静止 → 破门 → 群战 → 风雪一枪"""
    ev('silence', 0); ev('flash', 1); ev('crash', 1); ev('title', 1)
    hits = [ev('hit', b) for b in (3, 4, 5, 6, 7, 8, 9, 10)]
    ev('whoosh', 11); ev('silence', 12); ev('boom', 13); ev('flash', 13); ev('title', 13); ev('gong', 13); ev('wind', 14)
    b = bt(t)
    if b < 1:
        stage_bg(p, 'NIGHT', col_h='#151a28', col_h2='NIGHT2', seed=41); ground(p)
        p.poly([(0, STAGE_T), (330, STAGE_T), (330, 880), (0, 880)], '#120d0a')
        figure(p, 170, 880, 1.0, 1, 'guard', 'lin', t=t)
        snow(p, t, 160, seed=8, frozen=3.0, wind=120)
        return
    if b < 3:
        stage_bg(p, 'NIGHT', col_h='#151a28', col_h2='NIGHT2', seed=41); ground(p)
        p.poly([(0, STAGE_T), (W, STAGE_T), (W, 880), (0, 880)], 'FIRE', a=0.25)
        k = t - B
        rnd = random.Random(2)
        for j in range(10):
            x = 330 + rnd.uniform(0, 400) * k * 3; y = rnd.uniform(300, 860) - 200 * k + 900 * k * k
            p.poly([(x, y), (x + 60, y + 8), (x + 50, y + 30), (x - 6, y + 22)], '#2a1e14', 'LN', 2)
        info = figure(p, 420, 880, 1.25, 1, 'thrust', 'lin', t=t)
        speedlines(p, 0, 600, 600, 600, t, B, 0.5, 12)
        big_title(p, '进一枪', 640, 260, t, B, size=160)
        snow(p, t, 160, seed=8, wind=300, speed=2)
        return
    if b < 11:
        stage_bg(p, 'NIGHT', col_h='#151a28', col_h2='NIGHT2', seed=42)
        p.poly([(0, STAGE_T), (W, STAGE_T), (W, 880), (0, 880)], 'FIRE', a=0.3)
        fire(p, 540, 700, 1100, 200, t, seed=5)
        ground(p)
        i_ = min(7, int(b - 3))
        face = 1 if i_ % 2 == 0 else -1
        lx = 380 if face == 1 else 700
        poses = ['thrust', 'sweep', 'raise', 'thrust', 'chop', 'sweep', 'thrust', 'swing']
        pose = pose_track(t, [(hits[i], poses[i]) for i in range(8)], snap=0.12)
        names = [('cop', '差拨'), ('zhuang', '富安')] + [('soldier', '')] * 6
        kind = names[i_][0]
        crowd(p, 50 if face == 1 else 90, 720, 18, 2, 0.34, 'soldier', 'guard', face=-face, dx=58, dy=-34, t=t, seed=11 + i_)
        info = figure(p, lx, 880, 1.15, face, pose, 'lin', t=t)
        n_ = 1 if i_ < 2 else 5
        rnd = random.Random(i_ + 50)
        for j in range(n_):
            fly_fig(p, lx + face * (200 + j * 70), 880, 0.85, -face, kind, t, hits[i_] + 0.02 * j, vx=face * (420 + j * 80), vy=-700 - rnd.uniform(0, 300))
        for j in range(3):
            figure(p, lx - face * (190 + j * 80), 880, 0.8, face, 'guard', 'soldier', t=t)
        burst(p, info['hand'][0] + face * 120, info['hand'][1], t, hits[i_], 160)
        if i_ < 2: nametag(p, '', names[i_][1], lx + face * 200, 400, t, hits[i_] - 0.3, 0.6)
        counter(p, '进', '×%d' % [1, 2, 7, 13, 20, 28, 37, 50][i_], t, hits[i_])
        snow(p, t, 120, seed=9, wind=250, speed=1.8)
        return
    if b < 13:
        stage_bg(p, 'NIGHT', col_h='#151a28', col_h2='NIGHT2', seed=43); ground(p)
        p.poly([(0, STAGE_T), (W, STAGE_T), (W, 880), (0, 880)], 'FIRE', a=0.2)
        k = min(1, (t - 11 * B) / B)
        figure(p, lerp(600, 840, k), 880, 0.95, 1, 'run1' if int(t * 6) % 2 else 'run2', 'lq', t=t, extra={'weapon': None})
        figure(p, 300, 880, 1.1, 1, 'guard', 'lin', t=t)
        snow(p, t, 160, seed=10, frozen=(11.9 * B if b >= 12 else None), wind=250)
        nametag(p, 'LU QIAN', '陆谦', 780, 420, t, 11 * B, B)
        if b >= 12:
            p.poly([(0, STAGE_T), (W, STAGE_T), (W, STAGE_B), (0, STAGE_B)], 'BLK', a=0.35)
        return
    # 风雪一枪：雪卷白龙
    stage_bg(p, 'NIGHT', col_h='#151a28', col_h2='NIGHT2', seed=43); ground(p)
    kk = t - 13 * B
    fl = max(0, 1 - kk / 0.4)
    # 白龙：沿螺旋的雪团
    for j in range(140):
        u = j / 140.0
        prog = min(1, kk / (1.2 * B))
        if u > prog: break
        x = lerp(320, 960, u) + math.sin(u * 14 + t * 4) * 70 * (1 - u * 0.5)
        y = 600 - math.sin(u * math.pi) * 260 + math.cos(u * 14 + t * 4) * 40
        r = 30 * (1 - u * 0.6) + 6
        p.ell(x, y, r, r, 'SNOW', a=0.85)
    if kk < 3 * B:
        hx_ = lerp(320, 960, min(1, kk / (1.2 * B))); hy_ = 600 - math.sin(min(1, kk / (1.2 * B)) * math.pi) * 260
        p.poly([(hx_ + 50, hy_), (hx_ - 30, hy_ - 50), (hx_ - 20, hy_), (hx_ - 30, hy_ + 50)], 'SNOW')
        p.ell(hx_ + 6, hy_ - 14, 6, 6, 'GOLD')
    figure(p, 280, 880, 1.25, 1, 'thrust', 'lin', t=t)
    if b < 15: figure(p, 880, 880, 0.95, -1, 'cower', 'lq', t=t, extra={'weapon': None})
    else: figure(p, 900, 940, 0.95, -1, 'cower', 'lq', rot=-90, t=t, extra={'weapon': None})
    burst(p, 880, 640, t, 14.2 * B, 300)
    gold_particles(p, t, 13 * B, 600, 560, 50)
    big_title(p, '风雪一枪', 540, 230, t, 13 * B, size=150)
    snow(p, t, 160, seed=11, wind=300, speed=2)
    if fl > 0: p.poly([(0, STAGE_T), (W, STAGE_T), (W, STAGE_B), (0, STAGE_B)], 'CREAM', a=fl)

S7.caps = [(0, '雪，停了一拍', '', (0, 1), ()), (1, '庙门炸开，', '这一回，他往前走', (), ()),
           (3, '一枪一个，', '一步不退', (), (2, 4)), (11, '陆谦想跑——', '', (), ()), (13, '风雪一枪，', '仇人一个没跑掉', (0, 4), ())]

def S8(p, t):
    """梁山 → 回到开场"""
    ev('wood', 0); ev('wind', 0); ev('title', 6); ev('boom', 8); ev('gong', 10)
    b = bt(t)
    if b < 6:
        stage_bg(p, 'NIGHT', col_h='#151a28', col_h2='NIGHT2', seed=51)
        # 梁山 + 水
        p.poly([(560, 760), (760, 420), (860, 520), (960, 380), (1080, 600), (1080, 760)], 'BLK')
        p.poly([(0, 760), (W, 760), (W, STAGE_B), (0, STAGE_B)], '#1e2a2a')
        for i in range(8): p.line([(i * 140 + (t * 30) % 140, 820), (i * 140 + 60 + (t * 30) % 140, 810)], 'SNOW', 3, 0.6)
        x = lerp(100, 420, (t / (6 * B)))
        figure(p, x, 780, 0.9, 1, 'run1' if int(t * 2.5) % 2 else 'run2', 'lin', t=t)
        nametag(p, 'LIANGSHAN', '梁山泊', 820, 300, t, 1 * B, 5 * B)
        snow(p, t, 120, seed=12, speed=1.0, wind=60)
        return
    moon_stage(p, t)
    snow(p, t, 70, seed=3)
    ground(p)
    gold_particles(p, t, 6 * B)
    figure(p, 540, 880, 1.25, 1, 'stand', 'lin', t=t)
    big_title(p, '豹子头 · 林冲', 540, 140, t, 6 * B, size=84, col='CREAM')
    big_title(p, '退一步，进一枪', 540, 275, t, 8 * B, size=96)

S8.caps = [(0, '雪夜投奔，', '上了梁山', (), (2, 4)), (6, '退了四步，', '只为这一枪', (3, 4), (2, 5))]

def S9(p, t):
    """弹卡"""
    ev('whoosh', 0); ev('boom', 1); ev('whoosh', 4); ev('flip', 4)
    stats = [ev('wood', b) for b in (6, 7, 8, 9, 10, 11)]
    ev('gong', 12)
    b = bt(t)
    moon_stage(p, t, dark=True)
    gold_particles(p, t, 0)
    c = p.c
    k = eo(t / B)
    if b < 4:
        sx = 1.0
    elif b < 5:
        sx = abs(math.cos((t - 4 * B) / B * math.pi))
    else:
        sx = 1.0
    front = b < 4.5
    c.save(); c.translate(540, 520 + (1 - k) * 600); c.rotate((1 - k) * 2.5); c.scale(max(0.01, k * sx), max(0.01, k))
    cw, ch = 330, 440
    p.poly([(-cw, -ch), (cw, -ch), (cw, ch), (-cw, ch)], '#1a120c', 'GOLD', 10)
    p.poly([(-cw + 24, -ch + 24), (cw - 24, -ch + 24), (cw - 24, ch - 24), (-cw + 24, ch - 24)], '#1a120c', 'LN', 3)
    if front:
        p.ell(0, -60, 250, 250, '#e8964f')
        c.save(); c.translate(0, 230); figure(p, 0, 0, 1.05, 1, 'guard', 'lin', t=t); c.restore()
        p.poly([(-cw + 24, ch - 150), (cw - 24, ch - 150), (cw - 24, ch - 24), (-cw + 24, ch - 24)], 'RED')
        p.text('豹子头 · 林冲', 0, ch - 70, 60, 'CREAM')
        p.text('天雄星', -cw + 90, -ch + 80, 34, 'GOLD')
        p.text('SSR', cw - 80, -ch + 80, 40, 'GOLD', outline='BLK')
    else:
        p.text('豹子头 · 林冲', 0, -ch + 100, 56, 'GOLD')
        rows = [('星位', '天雄星'), ('职位', '马军五虎将'), ('武器', '红缨枪'), ('必杀', '风雪一枪')]
        for i, (a_, v) in enumerate(rows):
            if t >= stats[min(i, 5)] - 0.05:
                s_ = punch(t, stats[min(i, 5)], 0.2, 0.25)
                p.text(a_, -cw + 70, -ch + 200 + i * 80, 38, 'LN', 'l')
                c.save(); c.translate(-cw + 230, -ch + 200 + i * 80); c.scale(s_, s_); p.text(v, 0, 0, 42, 'CREAM', 'l'); c.restore()
        bars = [('攻击', 95), ('防御', 88), ('速度', 92)]
        for i, (a_, v) in enumerate(bars):
            t0 = stats[min(5, 4 + (i > 0))] + i * 0.2
            if t < t0: continue
            kk = eo((t - t0) / 0.4)
            y = -ch + 540 + i * 90
            p.text(a_, -cw + 70, y + 14, 34, 'LN', 'l')
            p.poly([(-cw + 180, y - 18), (cw - 120, y - 18), (cw - 120, y + 18), (-cw + 180, y + 18)], '#3a2a1a')
            p.poly([(-cw + 180, y - 18), (lerp(-cw + 180, cw - 120, kk * v / 100), y - 18), (lerp(-cw + 180, cw - 120, kk * v / 100), y + 18), (-cw + 180, y + 18)], 'GOLD')
            p.text(str(int(v * kk)), cw - 60, y + 14, 36, 'CREAM')
    c.restore()

S9.caps = [(0, '水浒群英卡', '第1张', (), ()), (6, '豹子头林冲', '下一位，你想看谁？', (), ())]

SCENES = [('open', 12, S0), ('jiaotou', 12, S1), ('yuemiao', 24, S2), ('baihu', 24, S3), ('yezhu', 24, S4),
          ('hong', 14, S5), ('shenmiao', 20, S6), ('kill', 20, S7), ('end', 12, S8), ('card', 14, S9)]
STARTS = []
_acc = 0.0
for n, nb, f in SCENES:
    STARTS.append(_acc); _acc += nb * B
TOTAL = _acc

def collect():
    EVENTS.clear(); SHAKES.clear(); FLASH.clear()
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 8, 8); p = P(cairo.Context(s))
    for (n, nb, f), st in zip(SCENES, STARTS):
        _cur['start'] = st; _cur['rec'] = True
        try: f(p, 0.0)
        except Exception as e: raise
        _cur['rec'] = False
    EVENTS.sort()

def render(tg, surf):
    c = cairo.Context(surf); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    p = P(c)
    idx = max(i for i, st in enumerate(STARTS) if tg >= st - 1e-9)
    n, nb, f = SCENES[idx]; t = tg - STARTS[idx]
    # 震屏
    dx = dy = 0
    for ts, amp in SHAKES:
        if 0 <= tg - ts < 0.25:
            k = 1 - (tg - ts) / 0.25
            dx += math.sin(tg * 90) * amp * k; dy += math.cos(tg * 77) * amp * k
    c.save()
    c.rectangle(0, STAGE_T, W, STAGE_B - STAGE_T); c.clip()
    if dx or dy:
        c.translate(W / 2 + dx, (STAGE_T + STAGE_B) / 2 + dy); c.scale(1.04, 1.04); c.translate(-W / 2, -(STAGE_T + STAGE_B) / 2)
    f(p, t)
    grain(p, 5)
    for ts in FLASH:
        if 0 <= tg - ts < 0.2: p.poly([(0, 0), (W, 0), (W, H), (0, H)], 'CREAM', a=1 - (tg - ts) / 0.2)
    c.restore()
    cp = caps(t, getattr(f, 'caps', []))
    if cp:
        frame_chrome(p, cp[1], cp[2], (cp[3],) if cp[3] else (), (cp[4],) if cp[4] else (), t=t, cap_t0=cp[0] * B)
    else:
        frame_chrome(p)
    p.text('水浒群英', 1040, STAGE_T + 30, 22, 'CREAM', 'r', 0, a=0.5)

collect()
