"""搞笑风 · 角色引擎 v2（2026-10-29 定稿画风：苏糖/王大美那套）
粗黑描边 #1c1a1f、大头、斜眼、红厚唇、大腮红。
所有角色共用一套骨架，用参数 P 换脸、换发型、换衣服、换道具 —— 长相不能重样，衣服按剧情换装。

用法：
    from juese import person, head, CAST
    info = person(c, x, 脚底y, 缩放, P, e='neutral', look=1, arms=('hold','hip'), props=('phone',None), legs=(0,0), t=0)
    info['head'] -> 头中心 (x,y)，给 gaze() 连视线用
表情 e：neutral 日常 / happy 喜 / angry 怒 / cry 哀 / laugh 乐 / shock 惊 / side 斜眼瞟（围观路人）
"""
import cairocffi as cairo, math

OL = '#1c1a1f'
LW = 6
FONT = 'Noto Sans SC'


# ============================================================ 基础绘图
def hx(h, a=1.0):
    s = h.lstrip('#'); s = ''.join(ch*2 for ch in s) if len(s) == 3 else s
    return (int(s[:2], 16)/255, int(s[2:4], 16)/255, int(s[4:], 16)/255, a)


def col(c, h, a=1): c.set_source_rgba(*hx(h, a))


def shade(h, k=.82):
    r, g, b, _ = hx(h); return '#%02x%02x%02x' % (int(r*255*k), int(g*255*k), int(b*255*k))


def fs(c, f, lw=LW, a=1, oc=OL):
    if f: col(c, f, a); c.fill_preserve()
    if lw:
        col(c, oc, a); c.set_line_width(lw)
        c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    else: c.new_path()


def ell(c, x, y, rx, ry, f, lw=LW, a=1):
    c.new_path(); c.save(); c.translate(x, y); c.scale(max(rx, .1), max(ry, .1))
    c.arc(0, 0, 1, 0, 2*math.pi); c.restore(); fs(c, f, lw, a)


def _trace(c, segs):
    c.new_path()
    for s in segs:
        if s[0] == 'm': c.move_to(*s[1:])
        elif s[0] == 'l': c.line_to(*s[1:])
        else: c.curve_to(*s[1:])


def path(c, segs, f, lw=LW, a=1, close=True):
    _trace(c, segs)
    if close: c.close_path()
    fs(c, f, lw, a)


def poly(c, pts, f, lw=LW, a=1):
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path(); fs(c, f, lw, a)


def line(c, pts, w=LW, h=OL, a=1, curve=False):
    c.new_path(); c.move_to(*pts[0])
    if curve and len(pts) == 4: c.curve_to(*pts[1], *pts[2], *pts[3])
    else:
        for p in pts[1:]: c.line_to(*p)
    col(c, h, a); c.set_line_width(w); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()


def tube(c, pts, w, f):
    for ww, cc in ((w+2*LW, OL), (w, f)): line(c, pts, ww, cc)


def label(c, s, x, y, size, h, stroke=None):
    c.select_font_face(FONT+' Black', 0, 1); c.set_font_size(size)
    w = c.text_extents(s)[4]; c.new_path(); c.move_to(x-w/2, y+size*.36); c.text_path(s)
    if stroke: col(c, stroke); c.set_line_width(size*.14); c.stroke_preserve()
    col(c, h); c.fill()


# ============================================================ 默认参数
BASE = dict(
    sex='f', skin='#fde3cf', blush='#f49a9a', blush_a=.55,
    face='oval',            # oval 鹅蛋 / round 圆 / square 方 / long 长 / v 尖下巴
    hair='bob', hair_c='#9b6a47', hair_c2=None,
    brow='soft', brow_c='#6e4a33',
    eye='side',             # side 半眯斜眼 / round 圆眼 / dot 豆豆眼 / sleepy 困眼 / fox 吊梢眼
    lash=True, glasses=None,  # None / 'round' / 'square' / 'sun'
    mouth='pout',           # pout 嘟嘴 / thick 红厚唇 / line 一字 / smirk 歪嘴 / frown 撇嘴 / grin 憨笑
    lip='#e0606e',
    extras=(),              # folds 法令纹 / mole 痣 / stubble 胡茬 / mustache 八字胡 / freckles 雀斑 / eyebags 黑眼圈 / pearl 珍珠耳钉 / hoop 圈耳环 / necklace 四叶草项链
    top='polo', top_c='#f6efe2', top_c2=None, top_text=None,
    bottom='jeans', bottom_c='#9db8d9',
    shoes='sneaker', shoes_c='#ffffff',
    bw=1.0,                 # 体宽：0.9 瘦 / 1 标准 / 1.25 壮
    height=1.0,
)


def mk(**kw):
    P = dict(BASE); P.update(kw); return P


# ============================================================ 头部
def head_path(c, P):
    f = P['face']
    w = {'round': 120, 'square': 116, 'long': 102, 'v': 106}.get(f, 112)
    h = {'round': 118, 'long': 136}.get(f, 124)
    c.new_path(); c.move_to(-w, -16)
    c.curve_to(-w-2, -h+28, -w*.57, -h-4, 0, -h-4)
    c.curve_to(w*.57, -h-4, w+2, -h+28, w, -16)
    if f == 'square':
        c.curve_to(w, 70, w*.8, h-6, 0, h); c.curve_to(-w*.8, h-6, -w, 70, -w, -16)
    elif f == 'v':
        c.curve_to(w-4, 50, w*.5, h-10, 0, h+4); c.curve_to(-w*.5, h-10, -w+4, 50, -w, -16)
    elif f == 'round':
        c.curve_to(w+4, 70, w*.62, h, 0, h); c.curve_to(-w*.62, h, -w-4, 70, -w, -16)
    else:
        c.curve_to(w-2, 56, w*.62, h-12, 0, h-4); c.curve_to(-w*.62, h-12, -w+2, 56, -w, -16)
    c.close_path()
    return w, h


def hair_back(c, P):
    H, st = P['hair_c'], P['hair']
    if st == 'bob':
        path(c, [('m', -118, -50), ('c', -138, -160, 138, -160, 118, -50),
                 ('c', 124, 20, 128, 70, 150, 112), ('c', 128, 122, 112, 112, 100, 122),
                 ('c', 90, 112, 80, 116, 70, 106), ('l', -70, 106),
                 ('c', -80, 116, -90, 112, -100, 122), ('c', -112, 112, -128, 122, -150, 112),
                 ('c', -128, 70, -124, 20, -118, -50)], H)
    elif st == 'long':
        path(c, [('m', -120, -50), ('c', -140, -160, 140, -160, 120, -50),
                 ('c', 128, 50, 132, 120, 140, 180), ('l', -140, 180),
                 ('c', -132, 120, -128, 50, -120, -50)], H)
    elif st == 'clipbun':   # 齐下巴波波 + 鲨鱼夹丸子
        path(c, [('m', -126, -40), ('c', -148, -150, 148, -150, 126, -40),
                 ('c', 136, 20, 136, 70, 146, 96), ('l', -146, 96), ('c', -136, 70, -136, 20, -126, -40)], H)
        ell(c, 0, -150, 50, 38, H)
    elif st == 'ponytail':
        path(c, [('m', 100, -110), ('c', 190, -130, 210, -10, 170, 80), ('c', 160, 20, 150, -40, 96, -70)], H)
        ell(c, 104, -100, 14, 14, P.get('acc_c', '#ff6f91'), lw=4)
    elif st == 'curly':     # 大妈小卷
        for i in range(16):
            a = math.pi*(1.05+i/15*0.9)-math.pi*0.0
            ell(c, 128*math.cos(a), -20+120*math.sin(a), 34, 34, H)
        for s in (-1, 1):
            for k in range(3): ell(c, s*128, -10+k*36, 30, 30, H)
    elif st == 'buns':      # 双丸子
        for s in (-1, 1): ell(c, s*92, -118, 40, 38, H)


def hair_front(c, P):
    H, st = P['hair_c'], P['hair']
    HL = shade(H, 1.22) if H not in ('#1c1a1f',) else '#4a4452'
    if st in ('bob', 'long'):
        path(c, [('m', -116, -20), ('c', -124, -150, 124, -150, 116, -20),
                 ('c', 104, -64, 70, -90, 0, -92), ('c', -70, -90, -104, -64, -116, -20)], H)
        line(c, [(0, -128), (0, -92)], 4)
        if P.get('bangs', True):
            for x0, x1, w in ((-62, -70, 13), (-40, -44, 14), (-18, -18, 14), (18, 16, 14), (40, 44, 14), (62, 70, 13)):
                path(c, [('m', x0-w, -94), ('c', x0-w, -70, x1-4, -56, x1, -46),
                         ('c', x1+4, -60, x0+w, -76, x0+w, -94)], H, lw=4)
        for s in (-1, 1):
            path(c, [('m', s*112, -40), ('c', s*94, 10, s*88, 50, s*78, 96),
                     ('c', s*98, 80, s*110, 40, s*120, 0)], H)
        line(c, [(-60, -116), (-24, -124)], 5, HL)
    elif st == 'clipbun':
        c.save(); c.translate(0, -150)
        clip = P.get('acc_c', '#f6c445')
        path(c, [('m', -70, -6), ('c', -60, -36, 60, -36, 70, -6), ('l', 70, 8), ('c', 40, 0, -40, 0, -70, 8)], clip)
        for i in range(-3, 4):
            line(c, [(i*18, 2), (i*18, 22)], 10); line(c, [(i*18, 2), (i*18, 20)], 4, clip)
        c.restore()
        path(c, [('m', -126, -36), ('c', -130, -150, 130, -150, 126, -36),
                 ('l', 112, -60), ('l', 96, -76), ('l', 70, -70), ('l', 46, -79), ('l', 20, -72),
                 ('l', -6, -80), ('l', -32, -72), ('l', -58, -79), ('l', -84, -70), ('l', -104, -77)], H)
    elif st == 'ponytail':
        path(c, [('m', -116, -20), ('c', -124, -150, 124, -150, 116, -20),
                 ('c', 100, -70, 40, -60, -20, -100), ('c', -60, -70, -100, -60, -116, -20)], H)
        line(c, [(-50, -118), (0, -126)], 5, HL)
    elif st == 'curly':
        path(c, [('m', -118, -30), ('c', -124, -150, 124, -150, 118, -30), ('c', 60, -80, -60, -80, -118, -30)], H)
        for i in range(9):
            x = -96+i*24; ell(c, x, -70-10*math.sin(i*1.3)-20*(1-abs(x)/110), 22, 20, H, lw=5)
    elif st == 'buns':
        path(c, [('m', -116, -20), ('c', -124, -150, 124, -150, 116, -20),
                 ('c', 90, -80, 30, -86, 0, -84), ('c', -30, -86, -90, -80, -116, -20)], H)
    elif st == 'crop':      # 男生短碎发
        path(c, [('m', -116, -10), ('c', -126, -150, 126, -150, 116, -10),
                 ('l', 108, -56), ('l', 88, -70), ('l', 64, -62), ('l', 40, -76), ('l', 14, -66),
                 ('l', -10, -78), ('l', -36, -66), ('l', -60, -76), ('l', -84, -64), ('l', -106, -60)], H)
        line(c, [(-40, -122), (10, -130)], 5, HL)
    elif st == 'side_part':  # 油头侧分
        path(c, [('m', -116, -12), ('c', -126, -150, 126, -156, 116, -12),
                 ('c', 112, -70, 60, -96, -30, -86), ('c', -70, -82, -104, -54, -116, -12)], H)
        line(c, [(-30, -86), (40, -128), (90, -110)], 4, HL)
        line(c, [(-40, -124), (-30, -88)], 4)
    elif st == 'buzz':      # 寸头
        c.save(); head_path(c, P); c.clip()
        path(c, [('m', -130, -30), ('c', -130, -160, 130, -160, 130, -30), ('c', 80, -70, -80, -70, -130, -30)], H, lw=0, a=.9)
        c.restore()
        line(c, [(-110, -30), (-80, -66), (0, -80), (80, -66), (110, -30)], 4, OL, a=.5)
    elif st == 'bald':      # 地中海
        for s in (-1, 1):
            path(c, [('m', s*116, -40), ('c', s*126, -70, s*118, -80, s*96, -88), ('c', s*104, -50, s*106, -20, s*112, 6)], H)
        ell(c, -30, -100, 22, 10, '#ffffff', lw=0, a=.6)


def ears(c, P):
    w = 112 if P['face'] != 'round' else 120
    for s in (-1, 1): ell(c, s*(w-4), 8, 14, 22, P['skin'])
    ex = P['extras']
    if 'pearl' in ex:
        for s in (-1, 1): ell(c, s*(w-2), 30, 6, 6, '#ffffff', lw=3)
    if 'hoop' in ex:
        for s in (-1, 1): c.new_path(); c.arc(s*(w-2), 40, 12, 0, 6.3); col(c, '#f2c14e'); c.set_line_width(4); c.stroke()


def brows(c, P, e):
    bc = P['brow_c']; thick = {'thick': 10, 'thin': 5}.get(P['brow'], 7)
    for s in (-1, 1):
        if e == 'angry': pts = [(s*78, -60), (s*48, -48), (s*18, -30)]; w = thick+2
        elif e in ('cry',): pts = [(s*78, -38), (s*50, -50), (s*20, -60)]; w = thick+1
        elif e in ('happy', 'laugh'): pts = [(s*78, -54), (s*50, -66), (s*20, -60)]; w = thick
        elif e == 'shock': pts = [(s*76, -66), (s*48, -80), (s*20, -72)]; w = thick
        elif P['brow'] == 'arch': pts = [(s*82, -50), (s*60, -68), (s*22, -60)]; w = thick
        elif P['brow'] == 'flat': pts = [(s*78, -54), (s*48, -58), (s*20, -56)]; w = thick
        else: pts = [(s*78, -52), (s*50, -62), (s*20, -58)]; w = thick
        line(c, pts, w+4, OL); line(c, pts, max(w-2, 2), bc)


def _almond(c, cx, cy, s, top=-11, bot=12, ww=28):
    c.new_path(); c.move_to(cx-ww, cy+2); c.curve_to(cx-14, cy+top-3, cx+16, cy+top-3, cx+ww, cy-2)
    c.curve_to(cx+14, cy+bot, cx-14, cy+bot, cx-ww, cy+2); c.close_path()


def eyes(c, P, e, look):
    kind = P['eye']; lash = P['lash']
    for s in (-1, 1):
        cx, cy = s*46, -22
        if e in ('neutral', 'side') and kind == 'dot':
            ell(c, cx+look*4, cy, 7, 9, OL, lw=0)
            if e == 'side': line(c, [(cx-14, cy-8), (cx+14, cy-8)], 5)
        elif e in ('neutral', 'side') and kind == 'round':
            ell(c, cx, cy, 22, 24, '#ffffff', lw=4)
            ell(c, cx+look*10, cy+2, 11, 12, OL, lw=0); ell(c, cx+look*10-4, cy-3, 3.5, 3.5, '#ffffff', lw=0)
            if e == 'side': line(c, [(cx-24, cy-6), (cx+24, cy-6)], 8)
        elif e in ('neutral', 'side'):
            top = -14 if kind != 'sleepy' else -4
            _almond(c, cx, cy, s, top=top); fs(c, '#ffffff', 4)
            c.save(); _almond(c, cx, cy, s, top=top); c.clip()
            lk = look if e == 'neutral' else (1.4 if look >= 0 else -1.4)
            ell(c, cx+lk*12, cy+1, 11, 11, '#3a2a22', lw=0); ell(c, cx+lk*12, cy+1, 6, 6, OL, lw=0)
            ell(c, cx+lk*12-4, cy-3, 3, 3, '#ffffff', lw=0)
            c.restore()
            lid = cy-11 if kind != 'sleepy' else cy-3
            line(c, [(cx-30, cy), (cx-14, lid), (cx+16, lid), (cx+30, cy-3)], 8)
            if kind == 'fox': line(c, [(cx+s*26, cy-4), (cx+s*42, cy-16)], 6)
            if lash: line(c, [(cx+s*28, cy-2), (cx+s*40, cy-10)], 5)
            line(c, [(cx-22, lid-7), (cx+22, lid-8)], 3, OL, a=.45)
        elif e == 'happy':
            line(c, [(cx-24, cy+6), (cx-12, cy-14), (cx+12, cy-14), (cx+24, cy+6)], 8, curve=True)
            if lash: line(c, [(cx+s*22, cy+2), (cx+s*34, cy-8)], 5)
        elif e == 'angry':
            c.new_path(); c.move_to(cx-s*28, cy+2); c.line_to(cx+s*28, cy-12)
            c.curve_to(cx+s*30, cy+10, cx+s*10, cy+16, cx-s*6, cy+14)
            c.curve_to(cx-s*20, cy+12, cx-s*26, cy+8, cx-s*28, cy+2); c.close_path(); fs(c, '#ffffff', 4)
            ell(c, cx, cy+4, 6, 6, OL, lw=0)
            line(c, [(cx-s*30, cy+2), (cx+s*30, cy-13)], 8)
        elif e == 'shock':
            ell(c, cx, cy-4, 26, 30, '#ffffff', lw=4); ell(c, cx, cy-2, 6, 6, OL, lw=0)
        elif e == 'cry':
            line(c, [(cx-s*22, cy-12), (cx+s*6, cy-2), (cx-s*22, cy+8)], 8)
        elif e == 'laugh':
            line(c, [(cx+s*22, cy-12), (cx-s*8, cy-2), (cx+s*22, cy+8)], 8)
    g = P['glasses']
    if g:
        fc = '#1c1a1f'
        for s in (-1, 1):
            if g == 'round': c.new_path(); c.arc(s*46, -22, 34, 0, 6.3)
            else: c.new_path(); c.rectangle(s*46-36, -48, 72, 50)
            if g == 'sun': col(c, '#222', .92); c.fill_preserve()
            else: col(c, '#ffffff', .15); c.fill_preserve()
            col(c, fc); c.set_line_width(6); c.stroke()
        line(c, [(-12, -24), (12, -24)], 6, fc)


def nose(c, P):
    line(c, [(2, 0), (-6, 26), (0, 32), (8, 30)], 5)


def face_extras(c, P, e):
    ex = P['extras']
    if 'folds' in ex:
        k = 1.2 if e in ('happy', 'laugh', 'angry') else 1
        for s in (-1, 1): line(c, [(s*24, 36), (s*38*k, 52), (s*44*k, 74)], 4, OL, a=.7)
    if 'eyebags' in ex:
        for s in (-1, 1): line(c, [(s*46-20, -2), (s*46-6, 8), (s*46+6, 8), (s*46+20, -2)], 6, '#8c6fb0', a=.4, curve=True)
    if 'freckles' in ex:
        for s in (-1, 1):
            for (x, y) in ((70, 26), (82, 36), (62, 40)): ell(c, s*x, y, 2.4, 2.4, '#b9775a', lw=0)
    if 'mole' in ex: ell(c, 42, 70, 3.5, 3.5, OL, lw=0)
    if 'stubble' in ex:
        c.save(); head_path(c, P); c.clip()
        for i in range(40):
            x = -70+(i*37 % 140); y = 70+(i*53 % 50)
            if abs(x) < 70-((y-70)*.6): ell(c, x, y, 1.6, 1.6, '#555', lw=0, a=.7)
        c.restore()
    if 'mustache' in ex:
        path(c, [('m', 0, 50), ('c', -20, 40, -46, 46, -50, 62), ('c', -30, 56, -12, 58, 0, 58),
                 ('c', 12, 58, 30, 56, 50, 62), ('c', 46, 46, 20, 40, 0, 50)], P['hair_c'], lw=4)


def mouth(c, P, e):
    L = P['lip'] if P['sex'] == 'f' else '#c9707a'
    if e in ('neutral', 'side'):
        m = P['mouth']
        if m == 'pout':
            path(c, [('m', -24, 74), ('c', -18, 60, -4, 58, 0, 66), ('c', 4, 58, 18, 60, 24, 74), ('c', 18, 80, -18, 80, -24, 74)], L, lw=5)
            path(c, [('m', -22, 75), ('c', -10, 80, 10, 80, 22, 75), ('c', 22, 98, -22, 98, -22, 75)], L, lw=5)
            line(c, [(-8, 86), (6, 85)], 4, '#ffffff', a=.6)
        elif m == 'thick':
            path(c, [('m', -40, 86), ('c', -30, 70, -16, 66, -6, 72), ('c', -2, 68, 2, 68, 6, 72),
                     ('c', 16, 66, 30, 70, 40, 86), ('c', 20, 84, -20, 84, -40, 86)], L, lw=5)
            path(c, [('m', -36, 87), ('c', -20, 84, 20, 84, 36, 87), ('c', 26, 108, -26, 108, -36, 87)], L, lw=5)
        elif m == 'line': line(c, [(-20, 80), (20, 80)], 6)
        elif m == 'smirk': line(c, [(-22, 82), (8, 82), (26, 70)], 6)
        elif m == 'frown': line(c, [(-26, 88), (-10, 78), (10, 78), (26, 88)], 6, curve=True)
        elif m == 'grin':
            path(c, [('m', -30, 74), ('c', -10, 80, 10, 80, 30, 74), ('c', 24, 100, -24, 100, -30, 74)], '#ffffff', lw=5)
        return
    def cavity(segs, tongue, teeth_top=True, teeth_bot=False):
        path(c, segs, '#7a1f2c', lw=0)
        c.save(); _trace(c, segs); c.close_path(); c.clip()
        if teeth_top: c.rectangle(-70, 50, 140, 26); col(c, '#ffffff'); c.fill()
        if teeth_bot: c.rectangle(-70, 104, 140, 30); col(c, '#ffffff'); c.fill()
        if tongue: ell(c, *tongue, '#f07c8a', lw=0)
        c.restore()
        _trace(c, segs); c.close_path()
        col(c, L); c.set_line_width(12 if P['sex'] == 'f' else 0.1); c.stroke_preserve(); col(c, OL); c.set_line_width(4); c.stroke()
    if e == 'happy':
        cavity([('m', -46, 72), ('c', -16, 80, 16, 80, 46, 72), ('c', 40, 118, -40, 118, -46, 72)], (0, 108, 22, 12))
    elif e == 'angry':
        cavity([('m', -38, 72), ('c', -16, 64, 16, 64, 38, 72), ('l', 34, 106), ('c', 12, 112, -12, 112, -34, 106)], None, True, True)
    elif e == 'cry':
        cavity([('m', -42, 84), ('l', -26, 72), ('l', -8, 80), ('l', 8, 72), ('l', 26, 80), ('l', 42, 84),
                ('l', 34, 114), ('l', 12, 106), ('l', -10, 116), ('l', -34, 108)], (0, 104, 15, 7), False)
    elif e == 'laugh':
        cavity([('m', -50, 66), ('c', -16, 60, 16, 60, 50, 66), ('c', 46, 136, -46, 136, -50, 66)], (0, 120, 28, 18))
    elif e == 'shock':
        path(c, [('m', -18, 80), ('c', -18, 56, 18, 56, 18, 80), ('c', 18, 112, -18, 112, -18, 80)], '#7a1f2c', lw=5)


def fx(c, e, t=0):
    if e == 'angry':
        c.save(); c.translate(98, -112); c.rotate(.3)
        for a in range(4):
            c.save(); c.rotate(a*math.pi/2)
            line(c, [(6, -6), (10, -22), (22, -10)], 11); line(c, [(6, -6), (10, -22), (22, -10)], 6, '#e63946')
            c.restore()
        c.restore()
    if e == 'cry':
        wob = math.sin(t*30)*6
        for s in (-1, 1):
            c.new_path(); c.move_to(s*66, -4); c.curve_to(s*110, -50+wob, s*170, -10, s*195, 70+wob)
            col(c, '#7fd3f7'); c.set_line_width(26); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke_preserve()
            col(c, OL); c.set_line_width(3); c.stroke()
        r = 18+6*math.sin(t*8)
        ell(c, 22, 52, r, r*.9, '#cdeefd', lw=3, a=.85); ell(c, 15, 45, 5, 4, '#ffffff', lw=0)
    if e == 'happy':
        for (x, y, r) in ((-150, -90, 16), (160, -60, 12), (140, -150, 9)):
            c.new_path()
            for i in range(8):
                rr = r if i % 2 == 0 else r*.35; a = i*math.pi/4+t*3
                (c.move_to if i == 0 else c.line_to)(x+rr*math.cos(a), y+rr*math.sin(a))
            c.close_path(); fs(c, '#ffd43b', 3)
    if e == 'laugh':
        for i, (x, y, s, r) in enumerate(((185, -120, 60, .3), (200, -20, 52, .2), (175, 70, 40, .15))):
            c.save(); c.translate(x, y+math.sin(t*20+i)*6); c.rotate(r); label(c, '哈', 0, 0, s, '#ff8a3d', OL); c.restore()
    if e == 'shock':
        for i in range(3):
            line(c, [(-130-i*14, -120+i*30), (-150-i*14, -150+i*30)], 6)
            line(c, [(130+i*14, -120+i*30), (150+i*14, -150+i*30)], 6)


def head(c, x, y, s, P, e='neutral', look=1, tilt=0, t=0):
    c.save(); c.translate(x, y); c.scale(s); c.rotate(tilt)
    hair_back(c, P); ears(c, P)
    head_path(c, P); fs(c, P['skin'])
    if e == 'angry':
        c.save(); head_path(c, P); c.clip()
        g = cairo.LinearGradient(0, -130, 0, 130)
        g.add_color_stop_rgba(0, *hx('#e8463a', .75)); g.add_color_stop_rgba(.7, *hx('#e8463a', .2)); g.add_color_stop_rgba(1, *hx('#e8463a', 0))
        c.set_source(g); c.paint(); c.restore()
    ba = .75 if e in ('happy', 'laugh', 'cry') else P['blush_a']
    if ba > 0:
        for sd in (-1, 1): ell(c, sd*78, 30, 26, 19, P['blush'], lw=0, a=ba)
    face_extras(c, P, e)
    hair_front(c, P)
    brows(c, P, e); eyes(c, P, e, look); nose(c, P); mouth(c, P, e)
    fx(c, e, t)
    c.restore()


# ============================================================ 身体
ARM = {  # (肘, 手) 相对肩膀，画面右侧手臂；左侧自动镜像
    'down': ((30, 80), (24, 160)), 'hip': ((66, 90), (8, 142)), 'hold': ((40, 92), (-16, 130)),
    'up': ((60, -60), (66, -150)), 'point': ((74, 20), (150, 10)), 'cover': ((46, 30), (-60, -90)),
    'both_up': ((70, -50), (40, -150)), 'shrug': ((70, 40), (110, -10)), 'phone_ear': ((50, 40), (-40, -110)),
}


def _prop(c, kind, x, y, s):
    if not kind: return
    if kind == 'phone':
        c.save(); c.translate(x, y-20); c.rotate(-.15)
        poly(c, [(-22, -40), (22, -40), (22, 40), (-22, 40)], '#2b2d3a', lw=5)
        poly(c, [(-16, -32), (16, -32), (16, 30), (-16, 30)], '#ffd1dc', lw=0); c.restore()
    elif kind == 'cup':
        poly(c, [(x-30, y-90), (x+30, y-90), (x+24, y), (x-24, y)], '#e7c9a6')
        line(c, [(x+6, y-90), (x+16, y-140)], 12); line(c, [(x+6, y-90), (x+16, y-140)], 6, '#ff8fb1')
    elif kind == 'bag':     # 购物袋
        poly(c, [(x-40, y+20), (x+40, y+20), (x+48, y+130), (x-48, y+130)], '#ffffff')
        line(c, [(x-24, y+20), (x-14, y-6), (x+14, y-6), (x+24, y+20)], 5)
        ell(c, x-12, y+60, 16, 16, '#ff9a3c', lw=4); line(c, [(x+8, y+40), (x+30, y+80)], 12, '#7bd65a')
    elif kind == 'basket':  # 超市篮子
        poly(c, [(x-70, y+10), (x+70, y+10), (x+58, y+90), (x-58, y+90)], '#e84a5f')
        for k in range(-50, 60, 20): line(c, [(x+k, y+20), (x+k*.85, y+80)], 4, '#ffffff')
    elif kind == 'thermos':
        poly(c, [(x-24, y-100), (x+24, y-100), (x+24, y+4), (x-24, y+4)], '#e84a5f')
    elif kind == 'briefcase':
        poly(c, [(x-60, y+10), (x+60, y+10), (x+60, y+90), (x-60, y+90)], '#6b4a34')
        line(c, [(x-20, y+10), (x-20, y-6), (x+20, y-6), (x+20, y+10)], 6)
    elif kind == 'scanner':
        poly(c, [(x-14, y-60), (x+14, y-60), (x+14, y+10), (x-14, y+10)], '#3a3d4a')
        line(c, [(x, y-60), (x, y-90)], 4, '#ff3b3b')


def arm(c, P, side, pose, prop, sleeve, shoulder):
    if isinstance(pose, str): (ex_, ey_), (hx_, hy_) = ARM.get(pose, ARM['down'])
    else: (ex_, ey_), (hx_, hy_) = pose
    sx, sy = shoulder
    e = (sx+side*ex_, sy+ey_); h = (sx+side*hx_, sy+hy_)
    w = 44*P['bw']**.5
    tube(c, [(sx, sy), e, h], w, sleeve)
    if prop in ('basket', 'briefcase', 'bag'): _prop(c, prop, h[0], h[1], side)
    ell(c, h[0], h[1], 18, 16, P['skin'])
    if prop not in ('basket', 'briefcase', 'bag'): _prop(c, prop, h[0], h[1], side)
    return h


def _bottom(c, P, legs):
    k, bc = P['bottom'], P['bottom_c']
    if k == 'skirt':
        for sd, off in ((-1, legs[0]), (1, legs[1])):
            tube(c, [(sd*40, -150), (sd*44+off, -40)], 34, P['skin'])
        poly(c, [(-104*P['bw'], -210), (104*P['bw'], -210), (130*P['bw'], -110), (-130*P['bw'], -110)], bc)
        return
    for sd, off in ((-1, legs[0]), (1, legs[1])):
        x_in, x_out = sd*4, sd*84*P['bw']
        bot = -36 if k != 'shorts' else -120
        poly(c, [(x_in, -200), (x_out, -200), (sd*86*P['bw']+off, bot), (sd*20+off, bot)], bc)
        if k == 'jeans': line(c, [(sd*44+off*.3, -170), (sd*50+off*.7, -44)], 3, shade(bc, .85))
        if k == 'shorts': tube(c, [(sd*50+off*.6, -120), (sd*52+off, -40)], 40, P['skin'])
        if k == 'pajama':
            for yy in (-170, -120, -70): ell(c, sd*50+off*(.6+yy/-400), yy, 8, 8, '#ffffff', lw=0, a=.8)


def _shoes(c, P, legs):
    k, sc = P['shoes'], P['shoes_c']
    for sd, off in ((-1, legs[0]), (1, legs[1])):
        if k == 'heels':
            poly(c, [(sd*20+off, -40), (sd*70+off, -40), (sd*90+off, -4), (sd*20+off, -4)], sc)
            continue
        if k == 'boot':
            poly(c, [(sd*20+off, -70), (sd*90+off, -70), (sd*112+off, -2), (sd*14+off, -2)], sc); continue
        path(c, [('m', sd*14+off, -40), ('c', sd*40+off, -52, sd*86+off, -52, sd*104+off, -22),
                 ('l', sd*106+off, -2), ('l', sd*12+off, -2)], sc)
        if k == 'sneaker': line(c, [(sd*14+off, -12), (sd*104+off, -12)], 4, '#d9d9e0')
        if k == 'slipper': line(c, [(sd*30+off, -36), (sd*80+off, -36)], 8, shade(sc, .8))


def _top(c, P):
    k, tc = P['top'], P['top_c']; bw = P['bw']; tc2 = P['top_c2'] or shade(tc, .88)
    W1, W2 = 104*bw, 120*bw
    torso = [('m', -W1, -380), ('c', -50, -398, 50, -398, W1, -380),
             ('c', W2+4, -310, W2+10, -250, W2-2, -190), ('c', 60, -176, -60, -176, -W2+2, -190),
             ('c', -W2-10, -250, -W2-4, -310, -W1, -380)]
    path(c, [('m', -30, -420), ('l', 30, -420), ('l', 30, -380), ('l', -30, -380)], P['skin'], lw=5)   # 脖子
    path(c, torso, tc)
    if k == 'polo':
        for xx in range(-96, 100, 16): line(c, [(xx*bw, -360), (xx*bw*1.08, -200)], 2, tc2)
        poly(c, [(-30, -392), (30, -392), (0, -300)], P['skin'], lw=5)
        if 'necklace' in P['extras']:
            line(c, [(-26, -386), (-12, -340), (0, -326), (12, -340), (26, -386)], 2, '#d4a94a')
            for a in range(4): ell(c, 6*math.cos(a*math.pi/2), -320+6*math.sin(a*math.pi/2), 6, 6, '#ffffff', lw=2)
        for sd in (-1, 1):
            poly(c, [(sd*30, -392), (sd*96, -380), (sd*60, -326), (sd*8, -310)], tc, lw=5)
        for yy in (-286, -256): ell(c, 0, yy, 7, 7, '#ffffff', lw=3)
    elif k == 'cardigan':
        poly(c, [(-40, -378), (40, -378), (12, -230), (-12, -230)], P['top_c2'] or '#c9b6e8', lw=5)
        for yy in (-210, -176): ell(c, -24, yy, 10, 10, '#c98a4b', lw=4)
        for sd in (-1, 1):
            poly(c, [(sd*50, -230), (sd*104*bw, -232), (sd*106*bw, -176), (sd*52, -174)], tc, lw=5)
    elif k == 'hoodie':
        path(c, [('m', -70, -396), ('c', -40, -350, 40, -350, 70, -396), ('c', 40, -380, -40, -380, -70, -396)], tc2, lw=5)
        for sd in (-1, 1): line(c, [(sd*18, -370), (sd*20, -300)], 6, '#ffffff')
        poly(c, [(-60, -250), (60, -250), (76, -196), (-76, -196)], tc2, lw=5)
    elif k == 'tshirt':
        path(c, [('m', -36, -392), ('c', -20, -366, 20, -366, 36, -392)], P['skin'], lw=5)
    elif k in ('shirt', 'suit'):
        poly(c, [(-34, -394), (34, -394), (0, -330)], '#ffffff', lw=5)
        tie = P.get('tie_c', '#c0392b')
        poly(c, [(-8, -360), (8, -360), (14, -250), (0, -232), (-14, -250)], tie, lw=4)
        if k == 'suit':
            for sd in (-1, 1):
                poly(c, [(sd*34, -394), (sd*W1, -380), (sd*W2*.9, -200), (sd*20, -200), (sd*30, -300)], tc, lw=5)
                poly(c, [(sd*34, -394), (sd*60, -372), (sd*40, -320), (sd*22, -300)], tc2, lw=4)
            ell(c, 0, -216, 6, 6, OL, lw=0)
        else:
            for yy in (-310, -270, -230): ell(c, 0, yy, 5, 5, '#ffffff', lw=3)
    elif k == 'apron':      # 超市店员
        path(c, [('m', -36, -392), ('c', -20, -366, 20, -366, 36, -392)], P['skin'], lw=5)
        ac = P.get('apron_c', '#e84a5f')
        poly(c, [(-60, -360), (60, -360), (80, -180), (-80, -180)], ac)
        line(c, [(-60, -360), (-40, -400)], 6); line(c, [(60, -360), (40, -400)], 6)
        poly(c, [(20, -330), (54, -330), (54, -312), (20, -312)], '#ffffff', lw=3)
    elif k == 'puffer':
        for yy in (-320, -260, -205): line(c, [(-W2, yy), (-60, yy+6), (60, yy+6), (W2, yy)], 4, tc2, curve=True)
        line(c, [(0, -392), (0, -190)], 5)
    elif k == 'vest':       # 马甲配条纹打底
        stripes = P.get('inner_c', '#f7f2ea')
        poly(c, [(-50, -392), (50, -392), (40, -190), (-40, -190)], stripes, lw=5)
        for yy in range(-370, -200, 24): line(c, [(-46, yy), (46, yy)], 6, '#9a6a47')
        for sd in (-1, 1): poly(c, [(sd*40, -392), (sd*W1, -380), (sd*W2, -190), (sd*36, -190)], tc, lw=5)
    elif k == 'dress':
        path(c, [('m', -36, -392), ('c', -20, -366, 20, -366, 36, -392)], P['skin'], lw=5)
        line(c, [(-W2+6, -230), (W2-6, -230)], 8, tc2)
    elif k == 'uniform':    # 保安/地铁工作人员
        poly(c, [(-30, -394), (30, -394), (0, -340)], '#ffffff', lw=5)
        for sd in (-1, 1): poly(c, [(sd*50, -360), (sd*86, -364), (sd*86, -330), (sd*50, -330)], tc2, lw=4)
        ell(c, -60, -300, 14, 16, '#f2c14e', lw=4)
    if P['top_text']:
        label(c, P['top_text'], 0, -280, 34, P.get('text_c', '#e63946'))


def person(c, x, y, s, P, e='neutral', look=1, arms=('down', 'down'), props=(None, None),
           legs=(0, 0), t=0, tilt=0, lean=0, squash=1.0, head_tilt=0):
    """(x,y)=双脚中点；站立总高约 700*s。arms/props 顺序：(画面左手, 画面右手)"""
    c.save(); c.translate(x, y); c.scale(s*(2-squash)**.5, s*squash*P['height']); c.rotate(math.radians(lean))
    sleeve = P['top_c'] if P['top'] not in ('vest', 'apron', 'tshirt', 'dress') else (
        P.get('inner_c', '#f7f2ea') if P['top'] == 'vest' else P['skin'] if P['top'] in ('tshirt', 'dress') and P.get('short_sleeve', True) else P['top_c'])
    if P['top'] in ('apron', 'tshirt', 'dress'): sleeve = P.get('sleeve_c', P['skin'] if P['top'] != 'apron' else P.get('inner_c', '#ffffff'))
    _bottom(c, P, legs); _shoes(c, P, legs)
    # 后侧手臂先画（举起时在身体后）
    _top(c, P)
    hands = []
    for side, pose, prop in ((-1, arms[0], props[0]), (1, arms[1], props[1])):
        hands.append(arm(c, P, side, pose, prop, sleeve, (side*104*P['bw'], -362)))
    m = c.get_matrix()
    c.restore()
    hx_, hy_ = m.transform_point(0, -530)
    head(c, hx_, hy_, s, P, e, look, tilt=head_tilt, t=t)
    return {'head': (hx_, hy_), 'hands': [m.transform_point(*h) for h in hands]}


# ============================================================ 预设角色（长相各不相同）
CAST = {
    # 女主：苏糖 25岁，层次波波+空气刘海，嘟嘴斜眼，奶白针织polo
    'sutang': mk(extras=('necklace',)),
    # 王大美 35岁 东北大姐：鲨鱼夹丸子、纹眉、红厚唇、法令纹、痣、豆沙绿开衫
    'damei': mk(face='square', hair='clipbun', hair_c='#6b3424', brow='arch', brow_c='#4a3a3a', mouth='thick', lip='#d9384a',
                extras=('folds', 'mole', 'pearl'), top='cardigan', top_c='#8fc4a0', top_c2='#c9b6e8',
                bottom='pants', bottom_c='#2d3142', shoes='boot', shoes_c='#d9b48a', bw=1.15),
    # 闺蜜 小鹿：高马尾、圆眼、尖下巴、雀斑、粉卫衣
    'xiaolu': mk(face='v', hair='ponytail', hair_c='#2a2222', eye='round', mouth='grin', extras=('freckles',),
                 top='hoodie', top_c='#f59bb0', bottom='skirt', bottom_c='#3b3f5c', shoes='sneaker'),
    # 男同事 阿杰：短碎发、豆豆眼、方脸、胡茬、格子衬衫（衬衫+领带）
    'ajie': mk(sex='m', face='square', hair='crop', hair_c='#1f1d24', brow='thick', brow_c='#1f1d24', eye='dot', lash=False,
               mouth='line', blush_a=.25, extras=('stubble',), top='shirt', top_c='#9fc3e8', bottom='pants', bottom_c='#3a3f55',
               shoes='leather', shoes_c='#3b2a24', bw=1.15),
    # 领导 王总：地中海、圆眼镜、八字胡、西装
    'boss': mk(sex='m', face='round', hair='bald', hair_c='#2c2a30', brow='thick', brow_c='#2c2a30', eye='dot', lash=False,
               glasses='round', mouth='frown', blush_a=.3, extras=('mustache',), top='suit', top_c='#3b4466', tie_c='#d63031',
               bottom='pants', bottom_c='#3b4466', shoes='leather', shoes_c='#1f1d24', bw=1.3),
    # 超市阿姨：小卷发、吊梢眼、红围裙、圈耳环
    'ayi': mk(face='round', hair='curly', hair_c='#4a2f25', eye='fox', brow='arch', mouth='smirk', lip='#c2185b',
              extras=('folds', 'hoop'), top='apron', top_c='#f2e6d0', apron_c='#e84a5f', inner_c='#f2e6d0',
              bottom='pants', bottom_c='#4b4b5c', shoes='slipper', shoes_c='#7bd65a', bw=1.2),
    # 地铁小哥：寸头、困眼、黑眼圈、黄卫衣
    'xiaoge': mk(sex='m', face='long', hair='buzz', hair_c='#2a2a2a', eye='sleepy', lash=False, mouth='line', blush_a=.2,
                 extras=('eyebags',), top='hoodie', top_c='#f2c14e', bottom='jeans', bottom_c='#5b7db8', shoes='sneaker'),
    # 精致姐姐：长直发不留刘海、吊梢眼、墨镜、连衣裙高跟
    'jiejie': mk(face='v', hair='long', bangs=False, hair_c='#1f1a1a', eye='fox', brow='arch', brow_c='#2a2222',
                 mouth='thick', lip='#b0213a', extras=('hoop',), top='dress', top_c='#2f2f3a', top_c2='#c9a227',
                 bottom='skirt', bottom_c='#2f2f3a', shoes='heels', shoes_c='#b0213a', bw=.92),
}


if __name__ == '__main__':
    import sys
    W, H = 1920, 1080
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(sf)
    col(c, '#eef1f6'); c.paint()
    names = [('sutang', '苏糖·女主', 'neutral', ('hold', 'down'), ('phone', None)),
             ('damei', '王大美', 'side', ('hold', 'hip'), ('thermos', None)),
             ('xiaolu', '闺蜜小鹿', 'happy', ('up', 'down'), (None, None)),
             ('ajie', '同事阿杰', 'shock', ('down', 'hold'), (None, 'phone')),
             ('boss', '王总', 'angry', ('hip', 'point'), (None, None)),
             ('ayi', '超市阿姨', 'laugh', ('cover', 'hold'), (None, 'scanner')),
             ('xiaoge', '地铁小哥', 'side', ('phone_ear', 'down'), ('phone', None)),
             ('jiejie', '精致姐姐', 'cry', ('down', 'down'), (None, 'bag'))]
    for i, (k, nm, e, a, pr) in enumerate(names):
        x = 260+(i % 4)*460; y = 505 if i < 4 else 1035
        person(c, x, y-38, .56, CAST[k], e=e, look=-1 if i > 3 else 1, arms=a, props=pr, t=.3)
        label(c, nm, x, y+2, 30, OL)
    sf.write_to_png(sys.argv[1] if len(sys.argv) > 1 else 'cast.png')
