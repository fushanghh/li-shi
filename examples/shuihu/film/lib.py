import cairocffi as cairo, math, random
W, H = 1080, 1440
FPS = 30
BPM = 96.0
B = 60.0 / BPM  # 0.625s
# 版式
STAGE_T, STAGE_B = 34, 1010
CAP_T, CAP_B = 1032, 1290

def hx(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:], 16) / 255, a)

C = dict(BG='#b45f2c', BG2='#9a4c22', HILL='#8a4220', HILL2='#a3532a', BLK='#17110d', LN='#d98a45',
         CREAM='#f2dcb0', GOLD='#e8b04f', RED='#b8332a', GREEN='#3e5a46', NIGHT='#1d2233',
         NIGHT2='#2b3350', SNOW='#f4ead6', FIRE='#f2a03a', PURPLE='#5a3a5e', DRED='#7a2a22')

def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def eo(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def lerp(a, b, k): return a + (b - a) * k

def punch(t, t0, dur=0.22, amp=0.35):
    """0 -> 1+amp -> 1 弹跳"""
    if t < t0: return 0.55
    x = (t - t0) / dur
    if x >= 1: return 1.0
    if x < 0.5: return (1 + amp) * lerp(0.55, 1.0, eo(x / 0.5))
    return 1 + amp * (1 - ease((x - 0.5) / 0.5))

class P:
    def __init__(s, ctx): s.c = ctx
    def col(s, k, a=1.0):
        s.c.set_source_rgba(*hx(C.get(k, k), a))
    def poly(s, pts, col, stroke=None, w=2.5, a=1.0):
        c = s.c; c.move_to(*pts[0])
        for q in pts[1:]: c.line_to(*q)
        c.close_path(); s.col(col, a)
        if stroke: c.fill_preserve(); s.col(stroke, a); c.set_line_width(w); c.stroke()
        else: c.fill()
    def line(s, pts, col, w, a=1.0):
        c = s.c; c.move_to(*pts[0])
        for q in pts[1:]: c.line_to(*q)
        s.col(col, a); c.set_line_width(w); c.stroke()
    def ell(s, x, y, rx, ry, col, stroke=None, w=2.5, a=1.0):
        c = s.c; c.save(); c.translate(x, y); c.scale(max(rx, .01), max(ry, .01)); c.arc(0, 0, 1, 0, 6.2832); c.restore()
        s.col(col, a)
        if stroke: c.fill_preserve(); s.col(stroke, a); c.set_line_width(w); c.stroke()
        else: c.fill()
    def ring(s, x, y, r, col, w, a=1.0):
        s.c.arc(x, y, r, 0, 6.2832); s.col(col, a); s.c.set_line_width(w); s.c.stroke()
    def text(s, t, x, y, size, col, anchor='c', bold=1, outline=None, ow=None, a=1.0):
        c = s.c
        c.select_font_face("Noto Serif CJK SC", 0, bold); c.set_font_size(size)
        e = c.text_extents(t)
        dx = {'c': e[4] / 2, 'l': 0, 'r': e[4]}[anchor]
        c.move_to(x - dx, y)
        if outline:
            c.text_path(t); s.col(outline, a); c.set_line_width(ow or size * 0.16)
            c.stroke_preserve(); s.col(col, a); c.fill()
        else:
            s.col(col, a); c.show_text(t)
        return e[4]

# ---------------- 人物 ----------------
POSES = {
 # ua: 上臂角(0=下垂, 正=向前/朝向方向抬起), fa: 前臂角, th: 大腿, sh: 小腿, lean 身体前倾, wp 武器角度(相对竖直, 正=前倾)
 'stand':  dict(uaF=25, faF=60, uaB=-15, faB=-10, thF=8, shF=0, thB=-8, shB=0, lean=0, wp=0, crouch=0),
 'guard':  dict(uaF=50, faF=90, uaB=-30, faB=20, thF=22, shF=-5, thB=-20, shB=5, lean=6, wp=45, crouch=10),
 'thrust': dict(uaF=85, faF=90, uaB=60, faB=85, thF=40, shF=-10, thB=-35, shB=-5, lean=18, wp=90, crouch=26),
 'raise':  dict(uaF=160, faF=175, uaB=-40, faB=-20, thF=18, shF=0, thB=-18, shB=0, lean=-4, wp=-10, crouch=6),
 'chop':   dict(uaF=110, faF=130, uaB=70, faB=100, thF=35, shF=-12, thB=-30, shB=0, lean=14, wp=120, crouch=22),
 'sweep':  dict(uaF=70, faF=40, uaB=-60, faB=-40, thF=55, shF=-50, thB=-10, shB=10, lean=20, wp=100, crouch=40),
 'punch':  dict(uaF=88, faF=90, uaB=-40, faB=40, thF=30, shF=-10, thB=-30, shB=0, lean=14, wp=0, crouch=16),
 'kick':   dict(uaF=-30, faF=10, uaB=-50, faB=-30, thF=95, shF=90, thB=-5, shB=0, lean=-10, wp=0, crouch=0),
 'back':   dict(uaF=10, faF=20, uaB=-20, faB=-5, thF=-5, shF=0, thB=-30, shB=-10, lean=-10, wp=-15, crouch=4),
 'fist':   dict(uaF=150, faF=200, uaB=-20, faB=0, thF=20, shF=0, thB=-15, shB=0, lean=4, wp=0, crouch=6),
 'bound':  dict(uaF=-5, faF=-5, uaB=5, faB=5, thF=3, shF=0, thB=-3, shB=0, lean=0, wp=0, crouch=0),
 'kneel':  dict(uaF=20, faF=40, uaB=-20, faB=-10, thF=80, shF=-10, thB=10, shB=-90, lean=10, wp=0, crouch=60),
 'run1':   dict(uaF=50, faF=90, uaB=-50, faB=-10, thF=45, shF=-30, thB=-35, shB=-70, lean=14, wp=30, crouch=10),
 'run2':   dict(uaF=-40, faF=10, uaB=45, faB=90, thF=-30, shF=-60, thB=40, shB=-20, lean=14, wp=30, crouch=10),
 'pray':   dict(uaF=45, faF=110, uaB=40, faB=110, thF=2, shF=0, thB=-2, shB=0, lean=8, wp=0, crouch=0),
 'cower':  dict(uaF=120, faF=160, uaB=110, faB=150, thF=15, shF=0, thB=-10, shB=0, lean=-12, wp=0, crouch=10),
 'fan':    dict(uaF=60, faF=120, uaB=-10, faB=30, thF=10, shF=0, thB=-10, shB=0, lean=-6, wp=0, crouch=0),
 'point':  dict(uaF=90, faF=95, uaB=-20, faB=20, thF=10, shF=0, thB=-10, shB=0, lean=-4, wp=0, crouch=0),
 'swing':  dict(uaF=100, faF=60, uaB=80, faB=40, thF=40, shF=-10, thB=-35, shB=0, lean=10, wp=150, crouch=24),
}

def mix_pose(a, b, k):
    A, Bp = POSES[a] if isinstance(a, str) else a, POSES[b] if isinstance(b, str) else b
    return {key: lerp(A[key], Bp[key], k) for key in A}

def pose_at(t, keys):
    """keys: [(time, pose)] 每段在 0.35 拍内到位, 然后定格(皮影敲板)"""
    if t <= keys[0][0]: return dict(POSES[keys[0][1]]) if isinstance(keys[0][1], str) else keys[0][1]
    for i in range(len(keys) - 1):
        t0, p0 = keys[i]; t1, p1 = keys[i + 1]
        if t0 <= t < t1:
            return mix_pose(p0, p1, 0.0)
    for i in range(len(keys) - 1, 0, -1):
        pass
    return dict(POSES[keys[-1][1]]) if isinstance(keys[-1][1], str) else keys[-1][1]

def pose_track(t, keys, snap=0.16):
    """keys: [(t_hit, pose)]，在 t_hit 前 snap 秒开始过渡、t_hit 到位"""
    prev = keys[0][1]
    for th, p in keys:
        if t < th - snap: return mix_pose(prev, prev, 0)
        if t < th: return mix_pose(prev, p, ease((t - (th - snap)) / snap))
        prev = p
    return mix_pose(prev, prev, 0)

def limb(p, x, y, a1, a2, l1, l2, w, face):
    """从(x,y)出发, 角度(度, 0=向下, 正=朝面向方向)"""
    r1 = math.radians(a1); r2 = math.radians(a2)
    x1 = x + face * math.sin(r1) * l1; y1 = y + math.cos(r1) * l1
    x2 = x1 + face * math.sin(r2) * l2; y2 = y1 + math.cos(r2) * l2
    p.line([(x, y), (x1, y1), (x2, y2)], 'LN', w + 4)
    p.line([(x, y), (x1, y1), (x2, y2)], 'BLK', w)
    return (x2, y2)

def figure(p, x, gy, sc=1.0, face=1, pose='stand', kind='lin', rot=0.0, alpha=1.0, t=0.0, extra=None):
    """kind: lin 林冲 / thug 狗腿子 / guard 军汉 / soldier 禁军 / gyn 高衙内 / gq 高俅 / lu 鲁智深 / cop 公差 / hong 洪教头
       chai 柴进 / lq 陆谦 / wife 林娘子 / zhuang 庄客"""
    P_ = POSES[pose] if isinstance(pose, str) else pose
    c = p.c; c.save(); c.translate(x, gy); c.scale(sc, sc)
    if rot: c.translate(0, -120); c.rotate(math.radians(rot) * face); c.translate(0, 120)
    cr = P_['crouch']
    hip = (0, -168 + cr)
    lean = math.radians(P_['lean'])
    sh = (hip[0] + face * math.sin(lean) * 170, hip[1] - math.cos(lean) * 170)
    big = kind in ('lu',)
    robe = {'lin': 'BLK', 'thug': 'BLK', 'guard': 'BLK', 'soldier': 'BLK', 'gyn': 'GREEN', 'gq': 'RED', 'lu': 'DRED',
            'cop': 'BLK', 'hong': 'BLK', 'chai': 'PURPLE', 'lq': 'GREEN', 'wife': 'RED', 'zhuang': 'BLK'}[kind]
    limbw = 28 if big else 20
    # 披风(林冲)
    if kind == 'lin':
        fl = math.sin(t * 6) * 10
        p.poly([(sh[0] - face * 30, sh[1] + 8), (sh[0] + face * 20, sh[1] + 8),
                (hip[0] - face * (70 + fl), hip[1] + 120), (hip[0] - face * (140 + fl * 2), hip[1] + 100)], 'BLK')
    # 后腿/后臂
    legL = 84
    if kind != 'wife':
        ft = limb(p, hip[0] - face * 10, hip[1], P_['thB'], P_['thB'] + P_['shB'], legL, legL, limbw + 8, face)
        p.poly([(ft[0] - 14, ft[1] - 6), (ft[0] + face * 30, ft[1] - 6), (ft[0] + face * 30, ft[1] + 8), (ft[0] - 14, ft[1] + 8)], 'BLK', 'LN', 2)
    bh = limb(p, sh[0] - face * 28, sh[1] + 12, P_['uaB'], P_['uaB'] + (P_['faB'] - P_['uaB']) * 0.6, 58, 54, limbw, face)
    # 躯干
    tw = 54 if big else 40
    if kind in ('wife',):
        p.poly([(sh[0] - 26, sh[1]), (sh[0] + 26, sh[1]), (hip[0] + 60, hip[1] + 170), (hip[0] - 60, hip[1] + 170)], robe, 'LN')
    else:
        p.poly([(sh[0] - tw, sh[1] - 4), (sh[0] + tw, sh[1] - 4), (hip[0] + tw * 0.9, hip[1] + 10), (hip[0] - tw * 0.9, hip[1] + 10)], robe, 'LN', 2.5)
        if kind in ('gyn', 'gq', 'lu', 'chai', 'lq', 'cop', 'hong'):
            p.poly([(hip[0] - tw, hip[1]), (hip[0] + tw, hip[1]), (hip[0] + tw * 1.25, hip[1] + 95), (hip[0] - tw * 1.25, hip[1] + 95)], robe, 'LN', 2.5)
    if kind == 'lin':
        mx, my = (sh[0] + hip[0]) / 2, (sh[1] + hip[1]) / 2
        p.line([(sh[0] - 24, sh[1] + 6), (mx, my - 10), (sh[0] + 24, sh[1] + 6)], 'LN', 2.5)
        p.poly([(hip[0] - 34, hip[1] - 22), (hip[0] + 34, hip[1] - 22), (hip[0] + 34, hip[1] - 8), (hip[0] - 34, hip[1] - 8)], 'RED')
        for k in range(-2, 3): p.line([(hip[0] + k * 13, hip[1] - 4), (hip[0] + k * 16, hip[1] + 40)], 'LN', 2)
        for sgn in (-1, 1):
            p.poly([(sh[0] + sgn * 22, sh[1] - 10), (sh[0] + sgn * 56, sh[1] - 2), (sh[0] + sgn * 56, sh[1] + 26), (sh[0] + sgn * 24, sh[1] + 20)], 'BLK', 'LN', 2)
        # 葫芦
        p.ell(hip[0] - face * 30, hip[1] + 6, 7, 7, 'GOLD'); p.ell(hip[0] - face * 31, hip[1] + 22, 11, 12, 'GOLD')
    if kind in ('guard', 'soldier'):
        p.line([(sh[0] - 24, sh[1] + 20), (hip[0] + 24, hip[1] - 10)], 'LN', 2)
        p.line([(sh[0] + 24, sh[1] + 20), (hip[0] - 24, hip[1] - 10)], 'LN', 2)
    if kind == 'lu':
        p.line([(sh[0] - 30, sh[1]), (hip[0] + 30, hip[1])], 'GOLD', 5)  # 袈裟带
    # 前腿
    if kind != 'wife':
        ft = limb(p, hip[0] + face * 10, hip[1], P_['thF'], P_['thF'] + P_['shF'], legL, legL, limbw + 8, face)
        p.poly([(ft[0] - 14, ft[1] - 6), (ft[0] + face * 30, ft[1] - 6), (ft[0] + face * 30, ft[1] + 8), (ft[0] - 14, ft[1] + 8)], 'BLK', 'LN', 2)
    # 头
    hx_, hy_ = sh[0] + face * math.sin(lean) * 40, sh[1] - 46
    head(p, hx_, hy_, kind, face, extra)
    # 前臂 + 武器
    fh = limb(p, sh[0] + face * 28, sh[1] + 12, P_['uaF'], P_['faF'], 58, 54, limbw, face)
    weapon = (extra or {}).get('weapon', {'lin': 'spear', 'guard': 'spear', 'soldier': 'spear', 'cop': 'staff', 'hong': 'staff',
                                           'lu': 'chan', 'thug': None, 'gyn': 'fan', 'zhuang': 'staff', 'lq': 'knife'}.get(kind))
    if weapon:
        wa = math.radians(P_['wp'])
        dx, dy = face * math.sin(wa), -math.cos(wa)
        if weapon == 'spear': spear(p, fh[0] - dx * 110, fh[1] - dy * 110, fh[0] + dx * 190, fh[1] + dy * 190, red=(kind == 'lin'))
        elif weapon == 'staff': p.line([(fh[0] - dx * 110, fh[1] - dy * 110), (fh[0] + dx * 150, fh[1] + dy * 150)], 'BLK', 9); p.line([(fh[0] + dx * 120, fh[1] + dy * 120), (fh[0] + dx * 150, fh[1] + dy * 150)], 'RED', 9)
        elif weapon == 'chan':
            ex, ey = fh[0] + dx * 190, fh[1] + dy * 190
            p.line([(fh[0] - dx * 110, fh[1] - dy * 110), (ex, ey)], 'BLK', 11)
            p.ell(ex, ey, 26, 26, 'CREAM'); p.ell(ex, ey, 12, 12, 'BLK')
            p.ell(fh[0] - dx * 110, fh[1] - dy * 110, 14, 10, 'CREAM')
        elif weapon == 'fan':
            p.poly([(fh[0], fh[1]), (fh[0] + face * 40, fh[1] - 40), (fh[0] + face * 56, fh[1] - 10)], 'CREAM')
        elif weapon == 'knife':
            p.line([(fh[0], fh[1]), (fh[0] + dx * 70, fh[1] + dy * 70)], 'CREAM', 7)
        elif weapon == 'blade':
            p.line([(fh[0], fh[1]), (fh[0] + dx * 120, fh[1] + dy * 120)], 'CREAM', 9)
    p.ell(fh[0], fh[1], 11 if not big else 14, 11 if not big else 14, 'CREAM')
    c.restore()
    return dict(hand=(x + fh[0] * sc, gy + fh[1] * sc), head=(x + hx_ * sc, gy + hy_ * sc))

def spear(p, x0, y0, x1, y1, red=True):
    p.line([(x0, y0), (x1, y1)], 'BLK', 8); p.line([(x0, y0), (x1, y1)], 'LN', 1.5)
    a = math.atan2(y1 - y0, x1 - x0); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    Pp = lambda d, o: (x1 + dx * d + nx * o, y1 + dy * d + ny * o)
    p.poly([Pp(0, -5), Pp(8, -5), Pp(8, 5), Pp(0, 5)], 'GOLD')
    p.poly([Pp(8, 0), Pp(24, -11), Pp(62, -6), Pp(86, 0), Pp(62, 6), Pp(24, 11)], 'CREAM')
    if red:
        for k in range(7):
            o = (k - 3) * 6
            p.poly([Pp(2, o * 0.3 - 2), Pp(2, o * 0.3 + 2), Pp(-44 - abs(o) * .5, o * 1.8 + 3), Pp(-48 - abs(o) * .5, o * 1.8 - 3)], 'RED')

def head(p, x, y, kind, face, extra=None):
    big = kind == 'lu'
    if kind == 'lin':
        p.poly([(x - 26, y - 22), (x - 30, y + 30), (x - 34, y + 62), (x - 18, y + 60), (x - 16, y)], 'BLK')
        p.poly([(x + 26, y - 22), (x + 30, y + 30), (x + 34, y + 62), (x + 18, y + 60), (x + 16, y)], 'BLK')
    r = 30 if big else 22
    # 脸
    p.poly([(x - r, y - 20), (x + r, y - 20), (x + r * .95, y + 10), (x + 6, y + 34), (x - 6, y + 34), (x - r * .95, y + 10)], 'CREAM')
    # 五官(朝向)
    ex = x + face * 6
    p.poly([(ex - 2, y - 2), (ex - 14, y - 6), (ex - 12, y + 1)], 'BLK'); p.poly([(ex + 4, y - 2), (ex + 16, y - 6), (ex + 14, y + 1)], 'BLK')
    p.line([(ex - 15, y - 12), (ex - 3, y - 9)], 'BLK', 3); p.line([(ex + 3, y - 9), (ex + 17, y - 12)], 'BLK', 3)
    if kind == 'lin':
        if (extra or {}).get('seal', True): p.poly([(x - face * 14 - 4, y + 6), (x - face * 14 + 4, y + 6), (x - face * 14 + 4, y + 14), (x - face * 14 - 4, y + 14)], 'GOLD')
        p.poly([(x - 24, y - 22), (x + 24, y - 22), (x + 22, y - 12), (x, y - 16), (x - 22, y - 12)], 'BLK')
        # 毡笠 + 红缨
        p.poly([(x - 56, y - 22), (x - 20, y - 32), (x + 20, y - 32), (x + 56, y - 22), (x + 48, y - 17), (x - 48, y - 17)], 'BLK', 'LN', 2)
        p.poly([(x - 22, y - 30), (x - 19, y - 54), (x + 19, y - 54), (x + 22, y - 30)], 'BLK', 'LN', 2)
        for k in range(5):
            a = -math.pi / 2 + (k - 2) * 0.28
            p.poly([(x, y - 56), (x + 34 * math.cos(a) - 3, y - 60 + 30 * math.sin(a)), (x + 34 * math.cos(a) + 3, y - 60 + 30 * math.sin(a))], 'RED')
    elif kind == 'lu':
        p.poly([(x - r, y - 20), (x + r, y - 20), (x + r, y - 30), (x, y - 40), (x - r, y - 30)], 'CREAM')
        for k in range(3): p.ell(x - 10 + k * 10, y - 30, 2.5, 2.5, 'LN')
        p.poly([(x - 22, y + 14), (x + 22, y + 14), (x + 16, y + 40), (x - 16, y + 40)], 'BLK')  # 络腮胡
        p.ell(x, y + 64, 40, 10, 'GOLD')  # 念珠
    elif kind == 'gyn':
        p.poly([(x - 22, y - 20), (x + 22, y - 20), (x + 18, y - 42), (x - 18, y - 42)], 'BLK')
        p.line([(x - 30, y - 36), (x + 30, y - 36)], 'BLK', 5)
        p.ell(x + face * 2, y + 22, 5, 3, 'RED')
    elif kind == 'gq':
        p.poly([(x - 24, y - 20), (x + 24, y - 20), (x + 20, y - 46), (x - 20, y - 46)], 'BLK')
        p.line([(x - 70, y - 36), (x + 70, y - 36)], 'BLK', 6)  # 长翅乌纱
        p.poly([(x - 14, y + 18), (x + 14, y + 18), (x, y + 50)], 'BLK')
    elif kind in ('guard', 'soldier'):
        p.poly([(x - 26, y - 16), (x + 26, y - 16), (x + 16, y - 40), (x, y - 50), (x - 16, y - 40)], 'BLK', 'LN', 2)
        p.line([(x, y - 50), (x, y - 64)], 'RED', 5)
    elif kind == 'cop':
        p.poly([(x - 30, y - 20), (x + 30, y - 20), (x + 20, y - 40), (x - 20, y - 40)], 'BLK', 'LN', 2)
        p.poly([(x - 30, y - 22), (x - 46, y - 10), (x - 36, y - 28)], 'BLK')
    elif kind in ('thug', 'zhuang'):
        p.poly([(x - 24, y - 20), (x + 24, y - 20), (x + 20, y - 32), (x - 20, y - 32)], 'BLK')
        p.line([(x - face * 24, y - 24), (x - face * 44, y - 14)], 'RED' if kind == 'thug' else 'BLK', 5)
    elif kind == 'hong':
        p.poly([(x - 24, y - 20), (x + 24, y - 20), (x + 14, y - 46), (x - 14, y - 46)], 'BLK')
        p.poly([(x - 18, y + 14), (x + 18, y + 14), (x, y + 44)], 'BLK')
    elif kind == 'chai':
        p.poly([(x - 22, y - 20), (x + 22, y - 20), (x + 16, y - 44), (x - 16, y - 44)], 'GOLD')
        p.poly([(x - 10, y + 22), (x + 10, y + 22), (x, y + 34)], 'BLK')
    elif kind == 'lq':
        p.poly([(x - 22, y - 20), (x + 22, y - 20), (x + 18, y - 40), (x - 18, y - 40)], 'BLK')
        p.poly([(x - 8, y + 22), (x + 8, y + 22), (x, y + 32)], 'BLK')
    elif kind == 'wife':
        p.poly([(x - 26, y - 22), (x - 30, y + 40), (x - 16, y + 38), (x - 16, y)], 'BLK')
        p.poly([(x + 26, y - 22), (x + 30, y + 40), (x + 16, y + 38), (x + 16, y)], 'BLK')
        p.ell(x, y - 34, 22, 16, 'BLK'); p.line([(x - 6, y - 46), (x + 20, y - 58)], 'GOLD', 3)
        p.ell(x + face * 2, y + 22, 4, 3, 'RED')

# ---------------- 特效 ----------------
def burst(p, x, y, t, t0, size=120, col='GOLD'):
    k = (t - t0) / 0.45
    if k < 0 or k > 1: return
    a = 1 - k
    r = size * eo(k)
    p.ring(x, y, r, col, 6 * a + 1, a)
    p.ring(x, y, r * 0.6, col, 3 * a + 1, a * 0.7)
    for i in range(14):
        an = i * 2 * math.pi / 14 + t0
        r1, r2 = r * 0.7, r * 1.25
        p.line([(x + math.cos(an) * r1, y + math.sin(an) * r1), (x + math.cos(an) * r2, y + math.sin(an) * r2)], col, 5 * a + 1, a)
    rnd = random.Random(int(t0 * 1000))
    for i in range(18):
        an = rnd.uniform(0, 6.28); sp = rnd.uniform(0.6, 1.5) * size * 1.3
        p.ell(x + math.cos(an) * sp * eo(k), y + math.sin(an) * sp * eo(k) + 40 * k * k, 4 * a + 1, 4 * a + 1, 'CREAM', a=a)

def smoke(p, x, y, t, t0, size=60):
    k = (t - t0) / 0.6
    if k < 0 or k > 1: return
    a = 1 - k
    rnd = random.Random(int(t0 * 997))
    for i in range(7):
        an = rnd.uniform(0, 6.28); d = size * eo(k) * rnd.uniform(.6, 1.2)
        r = size * 0.45 * (0.5 + k)
        p.ell(x + math.cos(an) * d, y + math.sin(an) * d * 0.5, r, r * 0.8, 'CREAM', 'BLK', 3, a=a * 0.95)

def speedlines(p, x0, y0, x1, y1, t, t0, dur=0.3, n=6, col='CREAM'):
    k = (t - t0) / dur
    if k < 0 or k > 1: return
    a = 1 - k
    rnd = random.Random(int(t0 * 31))
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
    for i in range(n):
        o = rnd.uniform(-60, 60); s = rnd.uniform(0, 0.3); e = s + rnd.uniform(0.3, 0.6)
        p.line([(x0 + dx * s + nx * o, y0 + dy * s + ny * o), (x0 + dx * e + nx * o, y0 + dy * e + ny * o)], col, 4, a)

def onomato(p, txt, x, y, t, t0, size=90, col='CREAM', dur=0.9):
    if t < t0 or t > t0 + dur: return
    s = punch(t, t0, 0.2, 0.4); a = 1 if t < t0 + dur - 0.2 else (t0 + dur - t) / 0.2
    c = p.c; c.save(); c.translate(x, y); c.rotate(-0.12); c.scale(s, s)
    p.text(txt, 0, 0, size, col, outline='BLK', ow=size * 0.18, a=a)
    c.restore()

def big_title(p, txt, x, y, t, t0, t1=None, size=130, col='GOLD'):
    if t < t0 or (t1 and t > t1): return
    s = punch(t, t0, 0.25, 0.45)
    a = 1.0
    if t1 and t > t1 - 0.25: a = (t1 - t) / 0.25
    c = p.c; c.save(); c.translate(x, y); c.scale(s, s)
    p.text(txt, 0, 0, size, col, outline='BLK', ow=size * 0.14, a=a)
    c.restore()

def counter(p, label, val, t, t_last, x=1040, y=80):
    s = punch(t, t_last, 0.2, 0.3) if t_last is not None else 1
    c = p.c; c.save()
    p.poly([(x - 230, y - 26), (x, y - 26), (x, y + 86), (x - 230, y + 86)], 'BLK', 'LN', 3, a=0.85)
    p.text(label, x - 115, y + 4, 26, 'LN', bold=0)
    c.translate(x - 115, y + 70); c.scale(s, s)
    p.text(val, 0, 0, 58, 'GOLD', outline='BLK', ow=6)
    c.restore()

def nametag(p, py, cn, x, y, t, t0, dur=2.5):
    if t < t0 or t > t0 + dur: return
    a = min(1, (t - t0) / 0.15, (t0 + dur - t) / 0.25)
    p.text(py, x, y, 18, 'CREAM', bold=0, a=a)
    p.text(cn, x, y + 36, 32, 'CREAM', a=a, outline='BLK', ow=4)

def snow(p, t, n=90, seed=1, speed=1.0, frozen=None, top=STAGE_T, bottom=STAGE_B, wind=40):
    rnd = random.Random(seed)
    tt = frozen if frozen is not None else t
    for i in range(n):
        x0 = rnd.uniform(-100, W); v = rnd.uniform(60, 140) * speed; r = rnd.uniform(2, 5); ph = rnd.uniform(0, 100)
        y = top + ((ph * 37 + tt * v) % (bottom - top))
        x = (x0 + tt * wind + math.sin(tt * 2 + ph) * 12) % W
        p.ell(x, y, r, r, 'SNOW', a=0.9)

def fire(p, x, gy, w, h, t, seed=3):
    rnd = random.Random(seed)
    for i in range(int(w / 18)):
        fx = x - w / 2 + i * 18 + rnd.uniform(-6, 6)
        fh = h * (0.5 + 0.5 * abs(math.sin(t * 7 + i * 1.3))) * rnd.uniform(.6, 1)
        p.poly([(fx - 16, gy), (fx + 16, gy), (fx + 4 * math.sin(t * 9 + i), gy - fh)], 'FIRE', a=0.9)
        p.poly([(fx - 8, gy), (fx + 8, gy), (fx + 3 * math.sin(t * 11 + i), gy - fh * 0.6)], 'GOLD', a=0.95)

def cloud(p, x, y, s=1.0, col='BLK'):
    p.poly([(x - 46 * s, y), (x - 30 * s, y - 22 * s), (x, y - 30 * s), (x + 30 * s, y - 22 * s), (x + 46 * s, y)], col)
    p.ring(x - 12 * s, y - 12 * s, 8 * s, 'LN', 2.5); p.ring(x + 12 * s, y - 12 * s, 8 * s, 'LN', 2.5)

# ---------------- 版式 ----------------
def frame_chrome(p, cap1='', cap2='', hl1=(), hl2=(), t=0, cap_t0=0):
    """上花边 + 分隔线 + 字幕区 + 底部彩陶纹"""
    p.poly([(0, 0), (W, 0), (W, STAGE_T), (0, STAGE_T)], 'BLK')
    for i in range(0, W, 40):
        p.line([(i + 6, 26), (i + 6, 10), (i + 26, 10), (i + 26, 20), (i + 16, 20)], 'LN', 3)
    p.poly([(0, STAGE_B), (W, STAGE_B), (W, H), (0, H)], '#120d0a')
    p.line([(0, STAGE_B + 4), (W, STAGE_B + 4)], 'LN', 3)
    for i in range(0, W, 40):
        p.line([(i + 6, STAGE_B + 22), (i + 6, STAGE_B + 10), (i + 26, STAGE_B + 10), (i + 26, STAGE_B + 18)], 'LN', 2.5)
    # 底部陶纹
    p.poly([(0, CAP_B), (W, CAP_B), (W, H), (0, H)], '#c9733a')
    p.line([(0, CAP_B + 6), (W, CAP_B + 6)], 'BLK', 5); p.line([(0, H - 8), (W, H - 8)], 'BLK', 5)
    for i in range(10):
        cx = 54 + i * 108; cy = (CAP_B + H) / 2
        for r in (36, 24, 12): p.ring(cx, cy, r, 'BLK', 4)
        p.ell(cx, cy, 4, 4, 'BLK')
    for i in range(0, W, 54):
        p.line([(i, CAP_B + 24), (i + 27, CAP_B + 18), (i + 54, CAP_B + 24)], 'BLK', 3)
        p.line([(i, H - 24), (i + 27, H - 30), (i + 54, H - 24)], 'BLK', 3)
    # 字幕：逐行出现
    def cap(line, hl, y, t_on):
        if not line or t < t_on: return
        a = min(1, (t - t_on) / 0.18)
        p.c.select_font_face("Noto Serif CJK SC", 0, 1); p.c.set_font_size(54)
        tw = p.c.text_extents(line)[4]; x = W / 2 - tw / 2
        for ch_i, ch in enumerate(line):
            colr = 'GOLD' if any(ch_i in range(a_, b_) for a_, b_ in hl) else 'CREAM'
            p.c.move_to(x, y); p.col(colr, a); p.c.show_text(ch)
            x += p.c.text_extents(ch)[4]
    cap(cap1, hl1, 1140, cap_t0)
    cap(cap2, hl2, 1222, cap_t0 + B * 2)

def hl(s, *words):
    out = []
    for w_ in words:
        i = s.find(w_)
        if i >= 0: out.append((i, i + len(w_)))
    return tuple(out)

def stage_bg(p, col='BG', hills=True, col_h='HILL', col_h2='HILL2', seed=0, t=0):
    p.poly([(0, STAGE_T), (W, STAGE_T), (W, STAGE_B), (0, STAGE_B)], col)
    rnd = random.Random(seed)
    if hills:
        pts = [(0, 760)]
        for i in range(9): pts.append((i * 140 + rnd.uniform(-20, 20), 640 + rnd.uniform(-60, 40)))
        pts += [(W, 700), (W, 900), (0, 900)]
        p.poly(pts, col_h2)
        pts = [(0, 820)]
        for i in range(8): pts.append((i * 160 + 60, 730 + rnd.uniform(-40, 40)))
        pts += [(W, 800), (W, 900), (0, 900)]
        p.poly(pts, col_h)

def ground(p, gy=880, col='BLK', t=0):
    p.poly([(0, gy), (W, gy), (W, STAGE_B), (0, STAGE_B)], col)
    p.line([(0, gy + 4), (W, gy + 4)], 'LN', 2.5)
    for i in range(0, W + 80, 80):
        p.line([(i + 20, gy + 40), (i + 40, gy + 62), (i + 20, gy + 84)], 'LN', 3)

def grain(p, seed=5):
    rnd = random.Random(seed)
    for i in range(500):
        p.ell(rnd.uniform(0, W), rnd.uniform(STAGE_T, STAGE_B), 1.2, 1.2, 'BLK', a=0.12)
