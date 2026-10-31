# 慕夏画风 × 关节木偶：通用全身侧面人物（朝右，flip 朝左），8 头身
import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from nv import *

class J:
    def __init__(s, c, x, y, a=0): s.c = c; s.x = x; s.y = y; s.a = a
    def __enter__(s): s.c.save(); s.c.translate(s.x, s.y); s.c.rotate(-s.a); return s.c
    def __exit__(s, *e): s.c.restore()

def taper(L, w0, w1):
    return [(-w0, 0), (-w0 * .7, -w0 * .7), (0, -w0), (w0 * .7, -w0 * .7), (w0, 0), (w1 * 1.04, L * .5), (w1, L), (w1 * .7, L + w1 * .7), (0, L + w1), (-w1 * .7, L + w1 * .7), (-w1, L), (-w1 * 1.04, L * .5)]

def layer(c, bbox, drawfn, outline=True):
    """bbox 内离屏绘制，再错位垫深棕剪影（慕夏粗外轮廓）"""
    x0, y0, w, h = [int(v) for v in bbox]
    w = max(8, w); h = max(8, h)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); g = cairo.Context(s); g.translate(-x0, -y0); drawfn(g); s.flush()
    if outline:
        sh = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); gs = cairo.Context(sh); gs.set_source_rgb(*LINE); gs.mask_surface(s, 0, 0)
        for dx, dy in ((-1.5, -1.5), (3, 4), (1.5, 2)):
            c.set_source_surface(sh, x0 + dx, y0 + dy); c.paint()
    c.set_source_surface(s, x0, y0); c.paint()

SK = dict(skin=C['skin'], skinD=C['skinD'])

# ---------------- 头 ----------------
def head(g, s, o, t=0, blink=0):
    hair = o.get('hairc', C['hair']); kind = o.get('hair', 'gaoji'); male = o.get('male', False); mouth = o.get('mouth', 'closed')
    skin = o.get('skin', C['skin'])
    # 背后的发髻/冠（先画）
    if kind == 'wanji' or kind == 'grey':
        hc = hx('d8d2c6') if kind == 'grey' else hair
        ell(g, -70 * s, -10 * s, 34 * s, 30 * s, hc, 2.4)
    fp = [(-20 * s, -94 * s), (30 * s, -80 * s), (50 * s, -44 * s), (54 * s, -22 * s), (72 * s, 6 * s), (58 * s, 18 * s), (61 * s, 30 * s),
          (56 * s, 38 * s), (59 * s, 48 * s), (46 * s, 72 * s), (20 * s, 86 * s), (-30 * s, 70 * s), (-62 * s, 20 * s), (-64 * s, -50 * s)]
    if male: fp[4] = (76 * s, 8 * s); fp[9] = (50 * s, 76 * s); fp[10] = (22 * s, 92 * s)
    shape(g, fp, skin, 2.4, n=6)
    if not male and o.get('blush', True):
        rg = cairo.RadialGradient(26 * s, 26 * s, 2, 26 * s, 26 * s, 26 * s); rg.add_color_stop_rgba(0, *C['blush'], 0.55); rg.add_color_stop_rgba(1, *C['blush'], 0)
        g.set_source(rg); g.arc(26 * s, 26 * s, 26 * s, 0, TAU); g.fill()
    if o.get('age', 0): ink(g, [(30 * s, 30 * s), (40 * s, 50 * s)], 1.6, LINE, 0.5, 4); ink(g, [(24 * s, -4 * s), (40 * s, 0)], 1.4, LINE, 0.4, 4)
    shape(g, [(-12 * s, -14 * s), (2 * s, -12 * s), (4 * s, 16 * s), (-10 * s, 22 * s)], skin, 2)
    if not male and kind not in ('nun',): ell(g, -4 * s, 24 * s, 4 * s, 7 * s, C['gold'], 1.4)
    bw = 6 * s if male else 4 * s
    bro = o.get('brow', 0)
    ink(g, [(16 * s, -44 * s + bro * 4 * s), (34 * s, -48 * s + bro * 8 * s), (50 * s, -42 * s + bro * 12 * s)], bw, hair if kind != 'grey' else hx('9a948a'), 0.8, 6)
    if blink > 0.5 or o.get('eyes') == 'closed':
        ink(g, [(22 * s, -14 * s), (34 * s, -10 * s), (46 * s, -14 * s)], 3, LINE, 0.6, 6)
    else:
        ey = o.get('eyes') == 'wide'
        g.new_path(); smooth_path(g, [(22 * s, -16 * s), (40 * s, -24 * s if ey else -22 * s), (46 * s, -14 * s), (34 * s, -6 * s if ey else -8 * s)], True, 6); g.set_source_rgb(*hx('fbf6ee')); g.fill()
        ell(g, 40 * s, -15 * s, 4 * s, 5.5 * s, hx('3a2a20'), 0)
        ink(g, [(20 * s, -15 * s), (34 * s, -24 * s), (48 * s, -16 * s)], 3, LINE, 0.6, 6)
    if not male and kind in ('gaoji',): ell(g, 36 * s, -58 * s, 4 * s, 5 * s, C['red'], 1)
    mc = C['red'] if not male else hx('a0503a')
    if mouth == 'open':
        shape(g, [(44 * s, 36 * s), (60 * s, 34 * s), (56 * s, 50 * s), (46 * s, 48 * s)], hx('7a2a22'), 1.8, n=4)
    elif mouth == 'smile':
        ink(g, [(46 * s, 40 * s), (52 * s, 42 * s), (59 * s, 36 * s)], 3, mc, 1.2, 4)
    else:
        ink(g, [(47 * s, 38 * s), (58 * s, 37 * s)], 3.2, mc, 1.4, 4)
    if o.get('beard'):
        bc = hx('d8d2c6') if o.get('age') else hair
        shape(g, [(30 * s, 56 * s), (56 * s, 54 * s), (58 * s, 80 * s), (40 * s, 140 * s * o.get('beard', 1)), (20 * s, 90 * s)], bc, 2)
        ink(g, [(40 * s, 30 * s), (60 * s, 30 * s), (70 * s, 40 * s)], 4 * s, bc, 1, 4)
    # 发型
    if kind == 'nun':
        shape(g, [(-64 * s, -6 * s), (-72 * s, -70 * s), (-30 * s, -104 * s), (24 * s, -98 * s), (50 * s, -60 * s), (20 * s, -66 * s), (-20 * s, -56 * s), (-40 * s, -20 * s)], hx('b8b4a8'), 2.4)
        return
    hc = hx('d8d2c6') if kind == 'grey' else hair
    cap = [(-66 * s, -10 * s), (-74 * s, -76 * s), (-34 * s, -112 * s), (26 * s, -104 * s), (52 * s, -62 * s), (22 * s, -70 * s), (-14 * s, -56 * s), (-30 * s, -26 * s), (-50 * s, 10 * s)]
    if kind in ('short', 'guapi', 'bob'):
        cap = [(-66 * s, 0), (-74 * s, -76 * s), (-34 * s, -110 * s), (30 * s, -104 * s), (56 * s, -66 * s), (30 * s, -60 * s), (-10 * s, -60 * s), (-26 * s, -30 * s), (-40 * s, 6 * s)]
        if kind == 'bob': cap = [(-70 * s, 40 * s), (-80 * s, -60 * s), (-34 * s, -112 * s), (30 * s, -106 * s), (58 * s, -64 * s), (34 * s, -64 * s), (0, -50 * s), (-20 * s, 0), (-34 * s, 46 * s)]
    shape(g, cap, hc, 2.4)
    ink(g, [(-60 * s, -60 * s), (-30 * s, -96 * s), (10 * s, -98 * s)], 3, C['hairHi'] if kind != 'grey' else hx('f2eee6'), 1, 6)
    if kind == 'gaoji':
        shape(g, [(-62 * s, -88 * s), (-80 * s, -168 * s), (-30 * s, -214 * s), (18 * s, -176 * s), (8 * s, -96 * s)], hc, 2.4)
        ink(g, [(-90 * s, -120 * s), (30 * s, -150 * s)], 4, C['gold'], 2, 4)
        fl = o.get('flower', C['poppy'])
        for (fx, fy, col) in ((-38 * s, -208 * s, C['gold']), (14 * s, -150 * s, fl), (-76 * s, -126 * s, fl)):
            for j in range(5):
                a = j / 5 * TAU + t
                ell(g, fx + math.cos(a) * 9 * s, fy + math.sin(a) * 9 * s, 9 * s, 6 * s, col, 1.5, a)
            ell(g, fx, fy, 4 * s, 4 * s, C['gold'], 1.2)
    elif kind in ('wanji', 'grey'):
        ink(g, [(-100 * s, -20 * s), (-40 * s, 0)], 4, C['gold'], 2, 4)
        if kind == 'grey':   # 抹额
            ink(g, [(-60 * s, -70 * s), (-10 * s, -86 * s), (40 * s, -74 * s)], 12 * s, hx('3a3050'), 6 * s, 6); ell(g, 6 * s, -84 * s, 7 * s, 6 * s, hx('6fb0a0'), 1.4)
        else:
            ell(g, -40 * s, -96 * s, 8 * s, 8 * s, o.get('flower', C['poppy']), 1.4)
    elif kind == 'guan':   # 周汉男子：发髻+小冠+缨
        ell(g, -24 * s, -112 * s, 26 * s, 20 * s, hc, 2.2)
        shape(g, [(-56 * s, -112 * s), (-50 * s, -150 * s), (10 * s, -158 * s), (14 * s, -116 * s)], hx('2c2622'), 2.2, n=2)
        ink(g, [(-70 * s, -128 * s), (36 * s, -132 * s)], 3.4, C['gold'], 2, 3)
        ink(g, [(-12 * s, -70 * s), (-6 * s, 20 * s), (30 * s, 70 * s)], 2.4, hx('2c2622'), 1, 4)
    elif kind == 'fangjin':   # 明 方巾
        shape(g, [(-72 * s, -50 * s), (-80 * s, -150 * s), (30 * s, -156 * s), (36 * s, -60 * s)], hx('2c2622'), 2.4, n=1)
        ink(g, [(-76 * s, -100 * s), (32 * s, -104 * s)], 2, hx('5a5048'), 1, 2)
    elif kind == 'guapi':   # 瓜皮帽
        shape(g, [(-70 * s, -60 * s), (-64 * s, -104 * s), (-20 * s, -124 * s), (30 * s, -110 * s), (44 * s, -66 * s)], hx('2c2622'), 2.4)
        ink(g, [(-68 * s, -66 * s), (42 * s, -70 * s)], 6 * s, hx('4a3f38'), 3, 4); ell(g, -12 * s, -128 * s, 7 * s, 6 * s, C['red'], 1.6)
    elif kind == 'mourn':   # 丧服首绖
        shape(g, [(-62 * s, -88 * s), (-70 * s, -128 * s), (-20 * s, -146 * s), (6 * s, -100 * s)], hc, 2.2)
        ink(g, [(-72 * s, -70 * s), (-10 * s, -96 * s), (44 * s, -78 * s)], 12 * s, hx('eee6d2'), 8 * s, 4)
        ink(g, [(-72 * s, -70 * s), (-96 * s, -10 * s), (-90 * s, 40 * s)], 8 * s, hx('eee6d2'), 4 * s, 4)

# ---------------- 姿势 ----------------
BPM = 112.0
def walk_pose(ph, stride=1.0):
    a = math.sin(ph * TAU)
    return dict(nhip=0.38 * a * stride, nkn=-0.3 * max(0, -a) - 0.05, fhip=-0.38 * a * stride, fkn=-0.3 * max(0, a) - 0.05,
                nsh=-0.30 * a * stride, nel=0.5, fsh=0.30 * a * stride, fel=0.3, bob=8 * abs(math.cos(ph * TAU)))

def mix(p, q, k):
    o = dict(p)
    for kk, v in q.items(): o[kk] = lerp(p.get(kk, 0), v, k) if isinstance(v, (int, float)) else v
    return o

def ease(x): x = cl(x); return x * x * (3 - 2 * x)
def back_out(x):
    x = cl(x); s = 1.7; x -= 1; return x * x * ((s + 1) * x + s) + 1

# ---------------- 全身 ----------------
def fig(c, x, yfeet, h, pose=None, t=0, outline=True, **o):
    """o: male, hair, hairc, beard, age, mouth, eyes, brow, flip, body('skirt','robe','aoqun','changshan','suit','dress','mourn'),
       top/bot/bot2/belt/trim 颜色, pibo(颜色或 None), sit('chair'/'kneel'), near/far(道具函数, 手坐标系), wind, magua(颜色)"""
    p = dict(nsh=0, nel=0.4, fsh=0, fel=0.3, nhip=0, nkn=0, fhip=0, fkn=0, head=0, body=0, bob=0); p.update(pose or {})
    u = h / 800.0; out = {}
    flip = o.get('flip', False); body = o.get('body', 'skirt'); sit = o.get('sit')
    top = o.get('top', hx('f4ecda')); bot = o.get('bot', hx('3f7f6a')); bot2 = o.get('bot2', tuple(v * 0.8 for v in bot))
    belt = o.get('belt', C['red']); trim = o.get('trim', C['gold']); wind = o.get('wind', 1.0); pibo = o.get('pibo', None)
    sleeve = o.get('sleeve', 'wide' if body in ('skirt', 'robe', 'mourn') else 'narrow')
    def draw(g):
        g.save(); g.translate(x, yfeet)
        if flip: g.scale(-1, 1)
        g.scale(u, u)
        drop = 290 if sit == 'kneel' else (200 if sit == 'chair' else 0)
        g.translate(0, -400 + p['bob'] + drop)
        def up(): g.save(); g.translate(0, -150); g.rotate(-p['body']); g.translate(0, 150)
        lw = 2.4 / u
        if pibo and not sit:
            up()
            pts = [(-60, -230)] + [(-60 - q * 360 * wind, -200 + q * 110 + math.sin(q * 5 - t * 4) * 46 * (0.3 + q)) for q in [i / 10 for i in range(1, 11)]]
            e = pts[-1]; pts += spiral(e[0] - 20, e[1], 30, 0, 1.2, 1, 14)[1:]
            g.set_source_rgb(*tuple(v * 0.85 for v in pibo)); ribbon_path(g, dense(pts, 4), lambda q: 32 * (1 - q) + 6); g.fill(); ink(g, pts, 2.2, LINE, 0.8, 4); g.restore()
        def arm(sh, el, near, prop):
            col = top if near else tuple(v * 0.9 for v in top)
            if o.get('magua') is not None: col = o['magua'] if near else tuple(v * 0.85 for v in o['magua'])
            if body == 'suit': col = o.get('jacket', hx('3a3f4a')) if near else tuple(v * 0.8 for v in o.get('jacket', hx('3a3f4a')))
            sk = o.get('skin', C['skin']) if near else C['skinD']
            with J(g, -6 if near else -30, -250, sh) as c1:
                shape(c1, taper(150, 30, 26), col, lw)
                with J(c1, 0, 150, el - sh) as c2:
                    if sleeve == 'wide':
                        shape(c2, [(-26, 0), (26, 0), (40, 90), (64, 170), (30, 176), (-30, 150), (-26, 60)], col, lw)
                        ink(c2, [(40, 92), (60, 168)], 2, LINE, 0.6, 4)
                        if trim and body != 'mourn': ink(c2, [(-28, 148), (30, 174)], 10, trim, 6, 3)
                        hy = 150
                    else:
                        shape(c2, taper(130, 24, 20), col, lw)
                        if body in ('aoqun',): ink(c2, [(-20, 122), (20, 122)], 10, trim, 8, 2)
                        if body == 'suit': ink(c2, [(-16, 132), (16, 132)], 7, hx('f4f0e8'), 7, 2)
                        hy = 136
                    with J(c2, 4, hy, 0) as c3:
                        shape(c3, [(-14, 0), (14, 0), (18, 30), (10, 52), (-8, 50), (-16, 26)], sk, lw)
                        m = c3.get_matrix(); out['hand_n' if near else 'hand_f'] = m.transform_point(0, 40)
                        if prop: prop(c3)
        up(); arm(p['fsh'], p['fsh'] + p['fel'], False, o.get('far')); g.restore()
        # ---- 下身 ----
        def footpos(hip, kn, near):
            L1, L2 = 200, 190
            kx = L1 * math.sin(hip); ky = L1 * math.cos(hip); fx = kx + L2 * math.sin(hip + kn); fy = ky + L2 * math.cos(hip + kn)
            return (kx, ky), (fx + (14 if near else -10), fy)
        shoe = o.get('shoe', belt)
        if sit == 'chair':
            for near in (False, True):
                dx = 0 if near else -14
                shape(g, [(170 + dx, 380), (240 + dx, 376), (262 + dx, 392), (170 + dx, 398)], shoe if near else tuple(v * .7 for v in shoe), lw)
            sk_ = [(-62, -190 if body == 'skirt' else -110), (62, -190 if body == 'skirt' else -110), (70, -20), (220, -10), (238, 40), (226, 384), (150, 390), (156, 60), (-80, 50), (-78, -40)]
            shape(g, sk_, bot, lw)
            ink(g, [(60, 10), (200, 20)], 5, bot2, 1, 4); ink(g, [(190, 60), (196, 370)], 5, bot2, 1, 4); ink(g, [(170, 60), (172, 370)], 4, bot2, 1, 4)
        elif sit == 'kneel':
            sk_ = [(-62, -190 if body == 'skirt' else -110), (62, -190 if body == 'skirt' else -110), (100, 20), (190, 70), (214, 108), (200, 112), (-90, 112), (-96, 40), (-74, -40)]
            shape(g, sk_, bot, lw)
            for k in range(4): ink(g, [(-40 + k * 40, 0), (-30 + k * 56, 106)], 4, bot2, 1, 4)
        else:
            kN, fN = footpos(p['nhip'], p['nkn'], True); kF, fF = footpos(p['fhip'], p['fkn'], False)
            legs_vis = body in ('suit', 'dress', 'changshan_short')
            if legs_vis:
                lc = o.get('legc', hx('2e3038') if body == 'suit' else o.get('skin', C['skin']))
                for (hip, kn, near) in ((p['fhip'], p['fkn'], False), (p['nhip'], p['nkn'], True)):
                    cc = lc if near else tuple(v * 0.8 for v in lc)
                    with J(g, 0, 0, hip) as l1:
                        shape(l1, taper(200, 34 if body == 'suit' else 24, 26 if body == 'suit' else 18), cc, lw)
                        with J(l1, 0, 200, kn) as l2:
                            shape(l2, taper(190, 26 if body == 'suit' else 18, 20 if body == 'suit' else 12), cc, lw)
                            with J(l2, 0, 190, -(hip + kn)) as l3:
                                shape(l3, [(-24, -10), (40, -10), (64, 6), (60, 18), (-24, 18)], shoe if near else tuple(v * .7 for v in shoe), lw)
            else:
                for (fx, fy), near in ((fF, False), (fN, True)):
                    sc = shoe if near else tuple(v * .7 for v in shoe)
                    shape(g, [(fx - 30, fy - 10), (fx + 40, fy - 14), (fx + 66, fy - 30), (fx + 70, fy - 6), (fx + 40, fy + 8), (fx - 30, fy + 8)], sc, lw)
            front = max(fN[0], fF[0]) + 30; back = min(fN[0], fF[0]) - 40
            if body == 'skirt':
                sk_ = [(-62, -190), (62, -190), (90, 40), (front + 10, 360), (front, 392), (front - 60, 384), ((front + back) / 2, 396), (back + 30, 384), (back - 10, 394),
                       (back - 50 - 30 * wind, 380), (-100, 200), (-78, 0)]
                shape(g, sk_, bot, lw)
                g.save(); g.new_path(); smooth_path(g, sk_, True, 8); g.clip()
                for k in range(-4, 6):
                    x0 = k * 34
                    ink(g, [(x0 * 0.4, -180), (x0 * 0.8 + 6 * math.sin(t + k), 100), (x0 * 1.6 + (front + back) * 0.15, 400)], 7, bot2, 1.5, 6)
                for k in range(14):
                    fx = back - 60 + k * (front - back + 90) / 13; ell(g, fx, 360, 9, 9, trim, 1.4); ell(g, fx, 360, 3, 3, belt, 0)
                g.restore()
            elif body in ('robe', 'mourn', 'changshan', 'aoqun'):
                hem = 372 if body != 'aoqun' else 392
                top_y = -120
                sk_ = [(-64, top_y), (64, top_y), (74, 40), (front + 4, hem - 20), (front - 4, hem), ((front + back) / 2, hem + 6), (back, hem), (back - 4 - 10 * wind, hem - 10), (-80, 120), (-72, 0)]
                shape(g, sk_, bot, lw)
                g.save(); g.new_path(); smooth_path(g, sk_, True, 8); g.clip()
                for k in range(-2, 4): ink(g, [(k * 30, top_y + 20), (k * 34 + (front + back) * 0.2, hem)], 4, bot2, 1, 4)
                if body in ('robe', 'changshan'): ink(g, [(back - 30, hem - 4), (front + 10, hem - 6)], 12, trim if body == 'robe' else bot2, 12, 2)
                if body == 'aoqun':   # 马面裙褶
                    for k in range(8): ink(g, [(back + k * (front - back) / 7, 200), (back + k * (front - back) / 7, hem)], 3, bot2, 2, 2)
                    ink(g, [(back - 30, hem - 30), (front + 10, hem - 30)], 18, trim, 18, 2)
                g.restore()
            elif body == 'dress':
                sk_ = [(-60, -120), (60, -120), (80, 60), (110, 160), (-110, 160), (-80, 60)]
                shape(g, sk_, bot, lw)
        # ---- 上身 ----
        up()
        if body == 'skirt':
            tor = [(-58, -262), (-20, -282), (30, -280), (62, -256), (60, -200), (52, -180), (-56, -180), (-64, -210)]
            shape(g, tor, top, lw)
            shape(g, [(-2, -282), (40, -270), (54, -200), (6, -196)], o.get('bra', hx('e9c070')), lw)
            shape(g, [(-64, -196), (64, -196), (64, -172), (-64, -172)], belt, lw, n=1)
            if not sit:
                for k in range(2): ink(g, [(30 + k * 16, -174), (40 + k * 18, -80), (30 + k * 24, 20 + k * 30)], 8, belt, 2, 6)
        elif body in ('robe', 'mourn', 'changshan', 'aoqun'):
            ln = 100 if body == 'aoqun' else -100
            tor = [(-62, -262), (-20, -284), (30, -282), (64, -256), (66, -150), (70, ln), (-74, ln), (-70, -160)]
            if body == 'aoqun': tor = [(-62, -262), (-20, -284), (30, -282), (64, -256), (70, -100), (96, 170), (-100, 170), (-74, -100)]
            if body == 'aoqun' and sit: tor = [(-62, -262), (-20, -284), (30, -282), (64, -256), (70, -60), (200, -10), (214, 50), (-86, 50), (-74, -100)]
            shape(g, tor, top, lw)
            if body in ('robe', 'mourn', 'aoqun'):   # 交领右衽
                ink(g, [(-10, -282), (30, -236), (60, -170)], 14, trim if body != 'mourn' else hx('d8cfb8'), 10, 4)
            else:
                ink(g, [(-14, -282), (30, -282)], 12, bot2, 10, 2); ink(g, [(30, -278), (50, -230), (66, -200)], 3, LINE, 2, 4)
            if body in ('robe', 'mourn'):
                shape(g, [(-72, -134), (68, -134), (70, -110), (-74, -110)], belt, lw, n=1)
                ink(g, [(50, -114), (60, -40), (54, 40)], 8, belt, 3, 4)
                if body == 'mourn': ink(g, [(-74, -122), (70, -122)], 10, hx('b8a888'), 10, 2)
            if body == 'aoqun' and not sit: ink(g, [(-100, 166), (96, 166)], 12, trim, 12, 2)
            if body == 'aoqun' and sit: ink(g, [(-84, 46), (212, 46)], 12, trim, 12, 2)
            if o.get('magua') is not None:
                shape(g, [(-66, -264), (-20, -286), (30, -284), (66, -258), (72, -60), (-78, -60)], o['magua'], lw)
                for k in range(4): ell(g, 34, -240 + k * 46, 5, 5, C['gold'], 1)
        elif body == 'suit':
            tor = [(-60, -262), (-20, -284), (30, -282), (64, -256), (68, -120), (72, 20), (-76, 20), (-70, -150)]
            shape(g, tor, o.get('jacket', hx('3a3f4a')), lw)
            shape(g, [(0, -282), (34, -280), (40, -180), (14, -150)], hx('f4f0e8'), lw)
            ink(g, [(24, -276), (28, -200), (24, -150)], 10, o.get('tie', C['red']), 4, 3)
            ink(g, [(0, -282), (30, -200), (50, -120)], 4, LINE, 2, 4)
        elif body == 'dress':
            tor = [(-58, -262), (-20, -282), (30, -280), (62, -256), (60, -140), (-62, -140)]
            shape(g, tor, bot, lw); shape(g, [(-62, -150), (62, -150), (62, -126), (-62, -126)], belt, lw, n=1)
        # 颈 + 头
        shape(g, [(-14, -300), (-12, -270), (22, -270), (20, -306)], C['skinD'], lw)
        if body == 'suit': ink(g, [(-12, -282), (22, -280)], 10, hx('f4f0e8'), 8, 2)
        with J(g, 4, -350, p['head']) as gh:
            head(gh, 0.56, o, t=t, blink=o.get('blink', 0))
            m = gh.get_matrix(); out['head'] = m.transform_point(0, -40); out['top'] = m.transform_point(0, -110); out['mouth'] = m.transform_point(56 * .56, 40 * .56)
        if pibo and not sit:
            ink(g, [(-60, -230), (-10, -262), (50, -240), (70, -180), (64, -100)], 30, pibo, 6, 6)
            ink(g, [(-60, -230), (-10, -262), (50, -240), (70, -180), (64, -100)], 2.2, LINE, 0.8, 6)
        if body == 'mourn' and o.get('kasaya'): pass
        if o.get('kasaya'): ink(g, [(-58, -262), (20, -230), (60, -150), (70, -60)], 26, o['kasaya'], 4, 6)
        arm(p['nsh'], p['nsh'] + p['nel'], True, o.get('near'))
        g.restore()
        g.restore()
    bw = h * 1.5; bh = h * 1.45
    x0 = int(x - bw / 2); y0 = int(yfeet - h * 1.25)
    layer(c, (x0, y0, bw, bh), draw, outline)
    return {k: (v[0] + x0, v[1] + y0) for k, v in out.items()}

# ---------------- 常用手持道具（手坐标系：y 沿前臂向下） ----------------
def p_hongbao(g):
    g.save(); g.translate(0, 46); g.rotate(0.3)
    shape(g, [(-22, -30), (22, -30), (22, 30), (-22, 30)], hx('c8322a'), 2.2, n=1)
    ell(g, 0, -6, 9, 9, hx('e6b84a'), 1.4); g.restore()
def p_brush(g):
    ink(g, [(-30, 30), (40, 40)], 6, hx('6b4528'), 4, 2); shape(g, [(-30, 26), (-46, 30), (-30, 34)], hx('222222'), 1.2, n=2)
def p_bolt(g):   # 一匹帛
    g.save(); g.translate(0, 60)
    shape(g, [(-50, -24), (50, -24), (50, 24), (-50, 24)], hx('e9e2cc'), 2.4, n=1)
    ell(g, -50, 0, 10, 24, hx('d8cfb0'), 2); ink(g, [(-30, -24), (-30, 24)], 2, hx('c9a24a'), 2, 2); g.restore()
def p_coins(g):   # 一串钱
    for k in range(9): ell(g, 0, 40 + k * 9, 11, 5, hx('b89a4a'), 1.4)
    ink(g, [(0, 30), (0, 120)], 2, hx('8a5a30'), 2, 2)
def p_ye(g):   # 谒（木牍名刺）
    g.save(); g.translate(0, 46); g.rotate(-0.2)
    shape(g, [(-16, -50), (16, -50), (16, 50), (-16, 50)], hx('e2c48e'), 2.4, n=1); g.restore()
def p_bowl(g):
    g.save(); g.translate(0, 56); shape(g, [(-30, -10), (30, -10), (20, 14), (-20, 14)], hx('c9a06a'), 2.2, n=2); ell(g, 0, -10, 30, 6, hx('8a3a2a'), 1.6); g.restore()
def p_silver(g):   # 银锭
    g.save(); g.translate(0, 56)
    shape(g, [(-30, 0), (-20, -14), (-10, -4), (10, -4), (20, -14), (30, 0), (20, 14), (-20, 14)], hx('dcdcd8'), 2.2); g.restore()
def p_phone(g):
    g.save(); g.translate(0, 46); g.rotate(-1.2)
    shape(g, [(-16, -30), (16, -30), (16, 30), (-16, 30)], hx('22262c'), 2.2, n=1); shape(g, [(-12, -24), (12, -24), (12, 24), (-12, 24)], hx('9fd6c8'), 1, n=1); g.restore()
def p_book(g):
    g.save(); g.translate(0, 50)
    shape(g, [(-34, -26), (34, -26), (34, 26), (-34, 26)], hx('c8322a'), 2.2, n=1); shape(g, [(-12, -18), (12, -18), (12, 18), (-12, 18)], hx('f3e6c4'), 1.4, n=1); g.restore()
