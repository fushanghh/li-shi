"""v2 人物：铠甲剪影 + 刻线，关节骨架，双手兵器 IK，披风二次运动"""
import math
from engine import *

# 姿势：角度制。ua/fa 前臂(朝向方向为正)，ub/fb 后臂，th/sh 腿（sh 为膝盖弯曲，负=向后弯），lean 躯干前倾，wp 兵器角(0=竖直向上, 90=水平朝前)，cr 下蹲
BASE = dict(uaF=20, faF=40, uaB=-12, faB=-8, thF=6, shF=0, thB=-6, shB=0, lean=0, wp=0, cr=0, head=0)
def mk(**k):
    d = dict(BASE); d.update(k); return d
POSES = {
 'idle':     mk(uaF=18, faF=50, uaB=-14, faB=-6, thF=10, thB=-10, wp=4),
 'heroic':   mk(uaF=30, faF=80, uaB=-30, faB=-20, thF=16, shF=-2, thB=-16, wp=6, lean=-3),
 'guard':    mk(uaF=55, faF=95, uaB=25, faB=80, thF=30, shF=-12, thB=-26, shB=-6, lean=8, wp=75, cr=16),
 'guardH':   mk(uaF=60, faF=110, uaB=40, faB=100, thF=26, shF=-8, thB=-22, shB=-4, lean=4, wp=60, cr=10),
 'coil':     mk(uaF=10, faF=60, uaB=-30, faB=40, thF=34, shF=-30, thB=-30, shB=-20, lean=-6, wp=88, cr=36),
 'thrust':   mk(uaF=88, faF=90, uaB=70, faB=88, thF=58, shF=-6, thB=-44, shB=-4, lean=24, wp=90, cr=44),
 'thrustHi': mk(uaF=110, faF=115, uaB=95, faB=110, thF=40, shF=-6, thB=-36, shB=-6, lean=14, wp=118, cr=24),
 'raiseO':   mk(uaF=165, faF=185, uaB=150, faB=175, thF=20, shF=-4, thB=-20, lean=-8, wp=-20, cr=6),
 'smash':    mk(uaF=95, faF=110, uaB=80, faB=100, thF=44, shF=-16, thB=-36, shB=-4, lean=26, wp=125, cr=40),
 'sweepL':   mk(uaF=60, faF=40, uaB=30, faB=10, thF=70, shF=-70, thB=-14, shB=-80, lean=28, wp=100, cr=86),
 'spinA':    mk(uaF=95, faF=95, uaB=-80, faB=-90, thF=30, shF=-10, thB=-30, lean=0, wp=95, cr=20),
 'blockH':   mk(uaF=140, faF=160, uaB=150, faB=165, thF=24, shF=-10, thB=-24, shB=-4, lean=-2, wp=90, cr=24),
 'parry':    mk(uaF=70, faF=130, uaB=20, faB=90, thF=26, shF=-6, thB=-30, lean=-8, wp=35, cr=14),
 'jump':     mk(uaF=120, faF=150, uaB=100, faB=140, thF=80, shF=-110, thB=20, shB=-100, lean=6, wp=80, cr=0),
 'land':     mk(uaF=70, faF=110, uaB=50, faB=90, thF=70, shF=-80, thB=-30, shB=-60, lean=20, wp=110, cr=70),
 'palm':     mk(uaF=90, faF=88, uaB=-50, faB=-10, thF=44, shF=-6, thB=-36, lean=16, cr=28),
 'palm2':    mk(uaF=86, faF=86, uaB=86, faB=86, thF=40, shF=-6, thB=-34, lean=18, cr=26),
 'grab':     mk(uaF=70, faF=120, uaB=60, faB=110, thF=24, shF=-6, thB=-24, lean=6, cr=14),
 'throw':    mk(uaF=170, faF=160, uaB=160, faB=150, thF=40, shF=-20, thB=-30, lean=-24, cr=30),
 'kick':     mk(uaF=-40, faF=10, uaB=60, faB=90, thF=100, shF=-6, thB=-8, lean=-18, cr=0),
 'duck':     mk(uaF=40, faF=90, uaB=-20, faB=40, thF=70, shF=-110, thB=-20, shB=-100, lean=40, cr=100),
 'fist':     mk(uaF=150, faF=210, uaB=40, faB=110, thF=26, shF=-6, thB=-22, lean=6, cr=10),
 'fistLow':  mk(uaF=20, faF=30, uaB=-10, faB=0, thF=10, thB=-12, lean=-4, cr=2),
 'stepBack': mk(uaF=10, faF=20, uaB=-24, faB=-10, thF=-4, thB=-34, shB=-10, lean=-10, cr=4),
 'kneel':    mk(uaF=10, faF=30, uaB=-10, faB=-4, thF=88, shF=-88, thB=12, shB=-100, lean=14, cr=78),
 'bound':    mk(uaF=-4, faF=-4, uaB=4, faB=4, thF=4, thB=-4, head=12),
 'cower':    mk(uaF=130, faF=170, uaB=120, faB=160, thF=20, shF=-10, thB=-14, lean=-14, cr=16),
 'hurt':     mk(uaF=-60, faF=-80, uaB=60, faB=100, thF=40, shF=-30, thB=-30, shB=-30, lean=-30, cr=20),
 'point':    mk(uaF=92, faF=96, uaB=-16, faB=20, thF=10, thB=-10, lean=-6),
 'fan':      mk(uaF=60, faF=130, uaB=-10, faB=30, thF=10, thB=-10, lean=-8),
 'pray':     mk(uaF=40, faF=120, uaB=34, faB=118, thF=2, thB=-2, lean=10),
 'laugh':    mk(uaF=50, faF=140, uaB=-40, faB=-20, thF=10, thB=-10, lean=-16, head=-14),
 'walkA':    mk(uaF=-24, faF=0, uaB=24, faB=40, thF=22, shF=-4, thB=-20, shB=-24, lean=4, wp=10),
 'walkB':    mk(uaF=24, faF=50, uaB=-24, faB=-10, thF=-18, shF=-30, thB=22, shB=-2, lean=4, wp=10),
 'swingL':   mk(uaF=-60, faF=-70, uaB=-40, faB=-60, thF=30, shF=-10, thB=-30, lean=-10, wp=-110, cr=20),
 'swingR':   mk(uaF=100, faF=80, uaB=80, faB=60, thF=44, shF=-10, thB=-38, lean=18, wp=100, cr=30),
 'drink':    mk(uaF=150, faF=200, uaB=-10, faB=20, thF=12, thB=-12, lean=-12, head=-20, wp=6),
 'lie':      mk(uaF=170, faF=170, uaB=160, faB=170, thF=4, thB=-4, cr=0),
 'sit':      mk(uaF=40, faF=70, uaB=-10, faB=30, thF=90, shF=-90, thB=86, shB=-86, cr=80),
}

def P_(x):
    return POSES[x] if isinstance(x, str) else x

def blend(a, b, k):
    A, Bp = P_(a), P_(b); return {key: A[key] + (Bp[key] - A[key]) * k for key in A}

def anim(t, keys):
    """keys: [(t, pose, ease?)] 到 t 时到位。ease 默认 eio；'snap' 为出拳类(eback)"""
    if t <= keys[0][0]: return dict(P_(keys[0][1]))
    for i in range(len(keys) - 1):
        t0, p0 = keys[i][0], keys[i][1]; t1, p1 = keys[i + 1][0], keys[i + 1][1]
        e = keys[i + 1][2] if len(keys[i + 1]) > 2 else 'io'
        if t0 <= t < t1:
            x = (t - t0) / (t1 - t0)
            k = {'io': eio, 'snap': lambda v: eback(v, 1.6), 'out': eo, 'in': ei, 'lin': lambda v: v}[e](x)
            return blend(p0, p1, k)
    return dict(P_(keys[-1][1]))

def walk(t, speed=1.0, phase=0.0):
    k = 0.5 + 0.5 * math.sin((t * speed * 2 * math.pi / (2 * B)) + phase)
    return blend('walkA', 'walkB', k)

KIND = {
 'lin':    dict(armor='hero', robe=None, hat='lin', wpn='spear', bulk=1.0, cape=True, face='lin'),
 'soldier':dict(armor='soldier', robe=None, hat='helm', wpn='spear', bulk=0.95, cape=False, face='plain'),
 'guard':  dict(armor='soldier', robe=None, hat='helm2', wpn='spear', bulk=0.98, cape=False, face='plain'),
 'thug':   dict(armor=None, robe=None, hat='band', wpn=None, bulk=0.95, cape=False, face='plain', jacket='BLK2'),
 'cop':    dict(armor=None, robe='BLK2', hat='cop', wpn='staff', bulk=0.95, cape=False, face='plain'),
 'gyn':    dict(armor=None, robe='GREEN', hat='scholar', wpn='fan', bulk=0.92, cape=False, face='dandy'),
 'gq':     dict(armor=None, robe='RED', hat='wing', wpn=None, bulk=1.05, cape=False, face='beard'),
 'lu':     dict(armor=None, robe='DRED', hat='bald', wpn='chan', bulk=1.35, cape=False, face='lu'),
 'hong':   dict(armor=None, robe='BLK2', hat='tall', wpn='staff', bulk=1.0, cape=False, face='beard'),
 'chai':   dict(armor=None, robe='PURPLE', hat='gold', wpn=None, bulk=0.98, cape=True, face='plain'),
 'lq':     dict(armor=None, robe='GREEN', hat='scholar', wpn='knife', bulk=0.92, cape=False, face='sly'),
 'fuan':   dict(armor=None, robe='BLK2', hat='band', wpn='knife', bulk=0.95, cape=False, face='plain'),
 'wife':   dict(armor=None, robe='RED', hat='bun', wpn=None, bulk=0.85, cape=False, face='lady', dress=True),
 'seller': dict(armor=None, robe='WOOD', hat='band', wpn='blade', bulk=0.95, cape=False, face='beard'),
}

def _limb(p, A, Bp, wa, wb, bands=0, col='BLK', ln='LN', etch=True):
    dx, dy = Bp[0] - A[0], Bp[1] - A[1]; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
    pts = [(A[0] + nx * wa, A[1] + ny * wa), (Bp[0] + nx * wb, Bp[1] + ny * wb), (Bp[0] - nx * wb, Bp[1] - ny * wb), (A[0] - nx * wa, A[1] - ny * wa)]
    p.poly(pts, col, ln if etch else None, 2.2)
    for i in range(bands):
        k = 0.25 + 0.6 * i / max(1, bands - 1) if bands > 1 else 0.6
        w_ = lerp(wa, wb, k) * 0.92
        cx, cy = A[0] + dx * k, A[1] + dy * k
        p.line([(cx + nx * w_, cy + ny * w_), (cx - nx * w_, cy - ny * w_)], ln, 2)
    p.ell(Bp[0], Bp[1], wb, wb, col)

def _pt(o, ang, L, face):
    r = math.radians(ang); return (o[0] + face * math.sin(r) * L, o[1] + math.cos(r) * L)

def _ik(S, T, l1, l2, face, bend=1):
    dx, dy = T[0] - S[0], T[1] - S[1]; d = min(math.hypot(dx, dy), l1 + l2 - 0.5)
    a = math.atan2(dy, dx)
    c = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d); c = clamp(c, -1, 1)
    b = math.acos(c) * bend * face
    E = (S[0] + math.cos(a + b) * l1, S[1] + math.sin(a + b) * l1)
    return E

def figure(p, g, x, gy, sc=1.0, face=1, pose='idle', kind='lin', rot=0.0, t=0.0, wind=0.0, extra=None, alpha=1.0):
    """返回关键点（世界坐标）: hand, tip, head, chest"""
    ex = extra or {}
    K = dict(KIND[kind]); K.update(ex.get('kind', {}))
    Q = P_(pose) if isinstance(pose, (str,)) else pose
    c = p.c; c.save(); c.translate(x, gy); c.scale(sc, sc)
    if g is not None: g.c.save(); g.c.translate(x, gy); g.c.scale(sc, sc)
    if rot:
        for q in ([p, g] if g is not None else [p]):
            q.c.translate(0, -150); q.c.rotate(math.radians(rot) * face); q.c.translate(0, 150)
    bk = K['bulk']
    cr = Q['cr']; thL, shL = 92, 92
    hip = (0.0, -(thL + shL + 6) + cr)
    lean = math.radians(Q['lean'])
    torso = 150
    sh = (hip[0] + face * math.sin(lean) * torso, hip[1] - math.cos(lean) * torso)
    neck = (sh[0] + face * math.sin(lean) * 16, sh[1] - math.cos(lean) * 16)
    hd = (neck[0] + face * math.sin(lean) * 26, neck[1] - math.cos(lean) * 26 - 6)
    lw = 17 * bk          # 手臂宽
    legw = 21 * bk
    out = {}
    # ---- 披风（最后层）
    if K.get('cape'):
        fl = math.sin(t * 5.3) * 12 + wind * 60
        ccol = 'BLK' if kind == 'lin' else K['robe']
        tail = [(sh[0] - face * 30 * bk, sh[1] + 4), (sh[0] - face * (60 + fl * .3), sh[1] + 70),
                (hip[0] - face * (110 + fl), hip[1] + 120 - wind * 40), (hip[0] - face * (150 + fl * 1.6), hip[1] + 150 - wind * 80),
                (hip[0] - face * (60 + fl * .6), hip[1] + 165), (sh[0] + face * 10, sh[1] + 30)]
        p.curve(tail, None, 1, close=True, fill=ccol)
        p.curve(tail[:4], 'LN', 2)
    # ---- 后腿
    def leg(sign, th, shb):
        Hp = (hip[0] + face * sign * 12 * bk, hip[1])
        Kn = _pt(Hp, th, thL, face); An = _pt(Kn, th + shb, shL, face)
        if K['armor'] or not K.get('dress'):
            _limb(p, Hp, Kn, legw, legw * 0.85, 0)
            _limb(p, Kn, An, legw * 0.85, legw * 0.7, 2 if K['armor'] else 0)
            if K['armor']: p.ell(Kn[0], Kn[1], legw * 0.95, legw * 0.8, 'BLK', 'LN', 2)  # 护膝
            fx = face * math.cos(math.radians(th + shb)) if False else face
            p.poly([(An[0] - face * 12, An[1] - 10), (An[0] + face * 34, An[1] - 2), (An[0] + face * 36, An[1] + 10), (An[0] - face * 14, An[1] + 10)], 'BLK', 'LN', 2)
        return Kn, An
    if not K.get('dress'): leg(-1, Q['thB'], Q['shB'])
    # ---- 后臂（双手兵器用 IK）
    S_B = (sh[0] - face * 30 * bk, sh[1] + 12)
    S_F = (sh[0] + face * 30 * bk, sh[1] + 12)
    E_F = _pt(S_F, Q['uaF'], 70, face); H_F = _pt(E_F, Q['faF'], 64, face)
    wpn = ex.get('wpn', K['wpn'])
    wa = math.radians(Q['wp']); wdx, wdy = face * math.sin(wa), -math.cos(wa)
    two = wpn in ('spear', 'staff', 'chan') and not ex.get('one_hand')
    if two:
        HB = (H_F[0] - wdx * 78, H_F[1] - wdy * 78)
        EB = _ik(S_B, HB, 70, 64, face, bend=-1)
        if math.hypot(HB[0] - S_B[0], HB[1] - S_B[1]) > 132: HB = _pt(EB, math.degrees(math.atan2(HB[0] - EB[0], HB[1] - EB[1])) * face, 64, face)
    else:
        EB = _pt(S_B, Q['uaB'], 70, face); HB = _pt(EB, Q['faB'], 64, face)
    _limb(p, S_B, EB, lw, lw * 0.85, 0); _limb(p, EB, HB, lw * .85, lw * .7, 3 if K['armor'] else 0)
    p.ell(HB[0], HB[1], 10 * bk, 10 * bk, 'CREAM')
    # ---- 躯干
    c.save(); c.translate(hip[0], hip[1]); c.rotate(lean * face)
    tw = 46 * bk; ww = 36 * bk
    robe = K['robe']
    if K.get('dress'):
        sp = 70
        p.poly([(-30, -torso + 10), (30, -torso + 10), (40, 0), (sp + 10, 180), (-sp - 10, 180), (-40, 0)], robe, 'LN', 2.2)
        p.line([(0, -torso + 30), (0, 170)], 'GOLD', 2); p.rect(-34, -40, 68, 14, 'GOLD')
        p.curve([(-50, 120), (0, 132), (50, 120)], 'GOLD', 2)
    elif robe:
        legspread = (Q['thF'] - Q['thB'])
        sp = min(46 * bk + abs(legspread) * 0.7, 84 * bk)
        p.poly([(-tw, -torso), (tw, -torso), (ww + 6, -6), (sp, 150 - cr * 0.5), (-sp, 150 - cr * 0.5), (-ww - 6, -6)], robe, 'LN', 2.2)
        p.line([(face * 8, -torso + 4), (-face * 24, -30)], 'LN', 2.5)  # 交领
        p.rect(-ww - 2, -24, ww * 2 + 4, 16, 'BLK' if robe != 'BLK2' else 'RED')
        if kind == 'lu':
            p.line([(-tw + 4, -torso + 6), (ww, -10)], 'GOLD', 9)
            for k in range(6): p.line([(-tw + 18 + k * 14, -torso + 18 + k * 18), (-tw + 30 + k * 14, -torso + 12 + k * 18)], 'RED2', 3)
        if kind in ('gq', 'chai', 'gyn'):
            p.rect(-22, -torso + 40, 44, 50, 'GOLD', a=0.9); p.rect(-16, -torso + 46, 32, 38, robe)
        for k in (-1, 1): p.line([(k * (ww - 4), 0), (k * (sp - 10), 140 - cr * 0.5)], 'LN2', 1.5)
    else:
        # 铠甲 / 短打
        body = 'BLK' if K['armor'] else K.get('jacket', 'BLK')
        p.poly([(-tw, -torso), (tw, -torso), (ww, -4), (-ww, -4)], body, 'LN', 2.2)
        if K['armor'] == 'hero':
            # 胸甲 V + 护心镜
            p.poly([(-tw + 6, -torso + 8), (0, -torso + 54), (tw - 6, -torso + 8), (tw - 8, -torso + 22), (0, -torso + 70), (-tw + 8, -torso + 22)], 'BLK', 'LN', 2)
            p.ell(0, -torso + 86, 14, 14, 'BLK', 'GOLD', 3); p.ell(0, -torso + 86, 5, 5, 'GOLD')
            for k in range(4): p.line([(-ww + 6, -torso + 104 + k * 10), (ww - 6, -torso + 104 + k * 10)], 'LN2', 1.6)
            # 腰带
            p.rect(-ww - 4, -18, (ww + 4) * 2, 18, 'RED'); p.rect(-10, -20, 20, 22, 'GOLD'); p.rect(-5, -15, 10, 12, 'RED2')
            # 前裙甲（尖）+ 侧裙流苏
            p.poly([(-20, 0), (20, 0), (16, 96), (0, 116), (-16, 96)], 'BLK', 'LN', 2)
            for k in (-8, 0, 8): p.line([(k, 8), (k * 0.8, 92)], 'LN2', 1.4)
            for sgn in (-1, 1):
                p.poly([(sgn * 20, 0), (sgn * (ww + 14), 0), (sgn * (ww + 22), 78), (sgn * 22, 84)], 'BLK', 'LN', 2)
                for k in range(5): p.line([(sgn * (24 + k * 7), 10), (sgn * (25 + k * 8), 80)], 'LN2', 1.3)
            # 葫芦
            p.ell(-face * (ww + 6), 4, 7, 8, 'GOLD'); p.ell(-face * (ww + 7), 22, 12, 13, 'GOLD'); p.line([(-face * (ww + 6), -6), (-face * (ww + 2), -14)], 'RED', 2)
        elif K['armor'] == 'soldier':
            for k in range(5): p.line([(-tw + 6, -torso + 24 + k * 20), (tw - 6, -torso + 24 + k * 20)], 'LN2', 1.6)
            p.rect(-ww - 2, -16, (ww + 2) * 2, 14, 'RED2')
            p.poly([(-ww, 0), (ww, 0), (ww + 10, 66), (-ww - 10, 66)], 'BLK', 'LN', 2)
            for k in range(-2, 3): p.line([(k * 12, 4), (k * 14, 62)], 'LN2', 1.3)
        else:
            p.line([(face * 6, -torso + 4), (-face * 18, -20)], 'LN2', 2)
            p.rect(-ww - 2, -16, (ww + 2) * 2, 12, 'RED' if kind == 'thug' else 'BLK2')
    c.restore()
    # ---- 肩甲（世界坐标）
    if K['armor'] == 'hero':
        for sgn in (-1, 1):
            cx_, cy_ = sh[0] + sgn * 36 * bk, sh[1] + 10
            for k, r in enumerate((34, 28, 22)):
                p.c.save(); p.c.translate(cx_, cy_ + k * 12); p.c.scale(1, 0.62)
                p.c.new_sub_path(); p.c.arc(0, 0, r, math.pi, 2 * math.pi); p.c.close_path(); p.col('BLK'); p.c.fill_preserve(); p.col('LN'); p.c.set_line_width(2.5); p.c.stroke()
                p.c.restore()
            p.ell(cx_, cy_ - 4, 5, 5, 'GOLD')
    elif K['armor'] == 'soldier':
        for sgn in (-1, 1):
            p.c.save(); p.c.translate(sh[0] + sgn * 34, sh[1] + 10); p.c.scale(1, 0.6)
            p.c.new_sub_path(); p.c.arc(0, 0, 26, math.pi, 2 * math.pi); p.c.close_path(); p.col('BLK'); p.c.fill_preserve(); p.col('LN'); p.c.set_line_width(2); p.c.stroke(); p.c.restore()
    # ---- 前腿
    if not K.get('dress'): Kn, An = leg(1, Q['thF'], Q['shF'])
    # ---- 头
    head(p, hd[0], hd[1], K, face, Q.get('head', 0), ex)
    out['head'] = (x + hd[0] * sc, gy + hd[1] * sc)
    out['chest'] = (x + (sh[0] + hip[0]) / 2 * sc, gy + (sh[1] + hip[1]) / 2 * sc)
    # ---- 兵器
    tip = H_F
    if wpn:
        if wpn == 'spear':
            tip = spear(p, H_F[0] - wdx * 150, H_F[1] - wdy * 150, H_F[0] + wdx * 200, H_F[1] + wdy * 200, red=(kind == 'lin'), t=t)
        elif wpn == 'staff':
            a0 = (H_F[0] - wdx * 150, H_F[1] - wdy * 150); a1 = (H_F[0] + wdx * 170, H_F[1] + wdy * 170)
            p.line([a0, a1], 'BLK', 10); p.line([a0, a1], 'WOOD', 4)
            p.line([(H_F[0] + wdx * 150, H_F[1] + wdy * 150), a1], 'RED', 10); tip = a1
        elif wpn == 'chan':
            a0 = (H_F[0] - wdx * 130, H_F[1] - wdy * 130); a1 = (H_F[0] + wdx * 210, H_F[1] + wdy * 210)
            p.line([a0, a1], 'BLK', 12); p.line([a0, a1], 'LN', 2)
            p.ell(a1[0], a1[1], 30, 30, 'CREAM', 'BLK', 4); p.ell(a1[0], a1[1], 11, 11, 'BLK')
            for k in range(4):
                an = k * math.pi / 2 + t; p.ell(a1[0] + math.cos(an) * 30, a1[1] + math.sin(an) * 30, 6, 6, 'GOLD')
            p.poly([(a0[0] - 14, a0[1] - 6), (a0[0] + 14, a0[1] - 6), (a0[0], a0[1] + 30)], 'CREAM')
            tip = a1
        elif wpn == 'blade':
            a1 = (H_F[0] + wdx * 150, H_F[1] + wdy * 150); nx, ny = -wdy, wdx
            p.poly([(H_F[0] + wdx * 16 + nx * 6, H_F[1] + wdy * 16 + ny * 6), (a1[0] + nx * 4, a1[1] + ny * 4), (a1[0] + wdx * 20, a1[1] + wdy * 20), (a1[0] - nx * 10, a1[1] - ny * 10), (H_F[0] + wdx * 16 - nx * 8, H_F[1] + wdy * 16 - ny * 8)], 'CREAM', 'BLK', 2)
            p.line([(H_F[0] + nx * 16, H_F[1] + ny * 16), (H_F[0] - nx * 16, H_F[1] - ny * 16)], 'GOLD', 6)
            tip = a1
        elif wpn == 'knife':
            a1 = (H_F[0] + wdx * 70, H_F[1] + wdy * 70); p.line([H_F, a1], 'CREAM', 7); tip = a1
        elif wpn == 'fan':
            for k in range(7):
                an = -0.4 + k * 0.17
                p.line([H_F, (H_F[0] + face * math.cos(an) * 56, H_F[1] - math.sin(an) * 56 - 20)], 'CREAM', 5)
            tip = H_F
    _limb(p, S_F, E_F, lw, lw * 0.85, 0); _limb(p, E_F, H_F, lw * .85, lw * .7, 3 if K['armor'] else 0)
    if K['armor'] == 'hero': p.rect(H_F[0] - 13, H_F[1] - 13, 0, 0, 'BLK')
    p.ell(H_F[0], H_F[1], 11 * bk, 11 * bk, 'CREAM')
    c.restore()
    if g is not None: g.c.restore()
    def W_(q): return (x + q[0] * sc, gy + q[1] * sc) if not rot else (x + q[0] * sc, gy + q[1] * sc)
    out['hand'] = W_(H_F); out['tip'] = W_(tip); out['handB'] = W_(HB)
    return out

def spear(p, x0, y0, x1, y1, red=True, t=0.0):
    p.line([(x0, y0), (x1, y1)], 'BLK', 9); p.line([(x0, y0), (x1, y1)], 'LN', 1.6)
    a = math.atan2(y1 - y0, x1 - x0); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    Pp = lambda d, o: (x1 + dx * d + nx * o, y1 + dy * d + ny * o)
    p.poly([Pp(-6, -6), Pp(10, -6), Pp(10, 6), Pp(-6, 6)], 'GOLD')
    p.poly([Pp(10, 0), Pp(26, -12), Pp(66, -7), Pp(92, 0), Pp(66, 7), Pp(26, 12)], 'CREAM', 'BLK', 1.5)
    p.line([Pp(18, 0), Pp(80, 0)], 'LN2', 1.5)
    if red:
        for k in range(9):
            o = (k - 4) * 5
            sway = math.sin(t * 9 + k) * 6
            p.poly([Pp(-2, o * 0.3 - 2.5), Pp(-2, o * 0.3 + 2.5), Pp(-50 - abs(o) * .4, o * 2 + 3 + sway), Pp(-56 - abs(o) * .4, o * 2 - 3 + sway)], 'RED')
    return Pp(92, 0)

def head(p, x, y, K, face, tilt=0, ex=None):
    ex = ex or {}
    c = p.c; c.save(); c.translate(x, y); c.rotate(math.radians(tilt) * face)
    hat = K['hat']; fc = K['face']; big = K['bulk'] > 1.2
    r = 30 if big else 24
    # 头发（林冲长发）
    if fc == 'lin':
        p.poly([(-28, -24), (-34, 30), (-40, 80), (-22, 76), (-18, 0)], 'BLK')
        p.poly([(28, -24), (34, 30), (40, 80), (22, 76), (18, 0)], 'BLK')
    if fc == 'lady':
        p.poly([(-28, -22), (-34, 50), (-18, 46), (-16, 0)], 'BLK'); p.poly([(28, -22), (34, 50), (18, 46), (16, 0)], 'BLK')
    # 脸：尖下巴
    p.poly([(-r, -22), (r, -22), (r * .96, 8), (r * .5, 26), (0, 38), (-r * .5, 26), (-r * .96, 8)], 'CREAM')
    # 发际（美人尖）
    if fc in ('lin', 'plain', 'sly', 'dandy', 'beard', 'lady'):
        p.poly([(-r - 2, -24), (r + 2, -24), (r, -12), (6, -14), (0, -6), (-6, -14), (-r, -12)], 'BLK')
    ex_ = face * 5
    # 眼睛：锐利斜眼 + 浓眉
    for sgn in (-1, 1):
        cx_ = ex_ + sgn * 11
        p.poly([(cx_ - 8, -2 + sgn * 0), (cx_ + 8, -5), (cx_ + 5, 1), (cx_ - 6, 2)], 'BLK')
        p.poly([(cx_ - 10 * sgn, -12 + (2 if sgn < 0 else 0)), (cx_ + 10 * sgn, -16), (cx_ + 10 * sgn, -12), (cx_ - 10 * sgn, -8)], 'BLK')
    p.line([(ex_, 4), (ex_ + face * 3, 14)], 'BLK', 2)
    if fc == 'lin':
        if ex.get('seal', True):
            sx = -face * 15
            p.rect(sx - 5, 10, 10, 10, 'GOLD')
        p.line([(ex_ - 6, 24), (ex_ + 6, 24)], 'RED2', 2.5)
    if fc in ('beard',):
        p.poly([(-16, 16), (16, 16), (8, 64), (0, 74), (-8, 64)], 'BLK')
    if fc == 'lu':
        p.curve([(-r - 2, 0), (-r, 30), (-12, 50), (0, 56), (12, 50), (r, 30), (r + 2, 0), (r - 6, 18), (0, 30), (-r + 6, 18)], None, 1, close=True, fill='BLK')
        for k in range(3): p.ell(-10 + k * 10, -32, 2.5, 2.5, 'LN')
        p.poly([(-r, -22), (r, -22), (r - 2, -30), (0, -40), (-r + 2, -30)], 'CREAM')
    if fc == 'dandy': p.ell(ex_, 22, 5, 3, 'RED')
    if fc == 'lady': p.ell(ex_, 22, 4, 3, 'RED')
    if fc == 'sly': p.poly([(ex_ - 10, 18), (ex_ + 10, 18), (ex_, 22)], 'BLK')
    # 帽子
    if hat == 'lin':
        p.poly([(-62, -22), (-22, -34), (22, -34), (62, -22), (54, -16), (-54, -16)], 'BLK', 'LN', 2)
        p.poly([(-24, -32), (-20, -58), (20, -58), (24, -32)], 'BLK', 'LN', 2)
        p.line([(-22, -38), (22, -38)], 'GOLD', 3)
        for k in range(7):
            a = -math.pi / 2 + (k - 3) * 0.24
            p.poly([(0, -60), (36 * math.cos(a) - 3, -64 + 34 * math.sin(a)), (36 * math.cos(a) + 3, -64 + 34 * math.sin(a))], 'RED')
        p.ell(0, -60, 6, 6, 'GOLD')
    elif hat in ('helm', 'helm2'):
        p.poly([(-30, -14), (-28, -30), (-14, -46), (0, -52), (14, -46), (28, -30), (30, -14)], 'BLK', 'LN', 2)
        p.line([(-28, -22), (28, -22)], 'LN', 2)
        p.poly([(-30, -14), (-36, 20), (-24, 18), (-22, -8)], 'BLK'); p.poly([(30, -14), (36, 20), (24, 18), (22, -8)], 'BLK')
        p.line([(0, -52), (0, -68)], 'BLK', 4)
        p.poly([(0, -66), (-8, -84), (8, -84)], 'RED' if hat == 'helm' else 'GOLD')
    elif hat == 'band':
        p.poly([(-26, -20), (26, -20), (22, -34), (-22, -34)], 'BLK'); p.line([(-26, -24), (26, -24)], 'RED', 5)
        p.line([(-face * 26, -24), (-face * 50, -12)], 'RED', 4)
    elif hat == 'cop':
        p.poly([(-32, -20), (32, -20), (24, -44), (-24, -44)], 'BLK', 'LN', 2)
        p.poly([(-30, -36), (-52, -26), (-46, -40)], 'BLK'); p.poly([(30, -36), (52, -26), (46, -40)], 'BLK')
    elif hat == 'scholar':
        p.poly([(-24, -20), (24, -20), (20, -44), (-20, -44)], 'BLK'); p.line([(-34, -38), (34, -38)], 'BLK', 5)
    elif hat == 'wing':
        p.poly([(-26, -20), (26, -20), (22, -50), (-22, -50)], 'BLK', 'GOLD', 2)
        p.line([(-80, -40), (80, -40)], 'BLK', 7); p.ell(-80, -40, 6, 6, 'BLK'); p.ell(80, -40, 6, 6, 'BLK')
    elif hat == 'tall':
        p.poly([(-24, -20), (24, -20), (14, -56), (-14, -56)], 'BLK')
    elif hat == 'gold':
        p.poly([(-24, -20), (24, -20), (18, -46), (0, -56), (-18, -46)], 'GOLD', 'BLK', 2)
    elif hat == 'bun':
        p.ell(0, -36, 22, 16, 'BLK'); p.line([(-8, -46), (24, -60)], 'GOLD', 3); p.ell(24, -60, 4, 4, 'RED')
    c.restore()

def fig_tip_path(fn, t, n=8, dt=1 / 60.0, key='tip'):
    """在 t 之前采样武器尖轨迹（无绘制）"""
    import cairocffi as cairo
    pts = []
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 4, 4); q = P(cairo.Context(s))
    for i in range(n, -1, -1):
        pts.append(fn(q, t - i * dt)[key])
    return pts
