"""社恐小人风 角色骨架：正面站姿、大圆头、超大卫衣、细长腿、白球鞋；表情库"""
from lib import *

SKIN = '#f6cfae'; SKIN_D = '#e9b48f'
HERO = dict(hoodie='#c58ca0', hood_d='#a86f84', pants='#2c3557', hair='#3b2a2c',
            hairstyle='pony', skin=SKIN, shoe='#ffffff', glasses=False, lash=True)

def _arm(c, sx, sy, a1, a2, L1, L2, w, f, skin, side, hand='open'):
    # a1/a2 角度：0=垂直向下，正值向外张开（side=+1 右臂向右）
    r1 = math.radians(a1); r2 = math.radians(a1+a2)
    ex, ey = sx+side*L1*math.sin(r1), sy+L1*math.cos(r1)
    hx_, hy_ = ex+side*L2*math.sin(r2), ey+L2*math.cos(r2)
    tube(c, [(sx, sy), (ex, ey), (hx_, hy_)], w, f)
    rr = w*.55 if hand != 'fist' else w*.62
    ell(c, hx_, hy_, rr, rr, skin, lw=4)
    return hx_, hy_

def face(c, x, y, r, e, look=(0, 0), t=0, P=None):
    """e: neutral / shock / star / angry / cry / laugh / smile / side / down"""
    P = P or {}
    u = r/11
    ex = 4.3*u; ey = y+.8*u
    lx, ly = max(-1.3, min(1.3, look[0])), max(-1.3, min(1.3, look[1]))
    lash = P.get('lash', False)
    if e in ('angry',):
        # 红脸
        c.save(); c.new_path(); ellipse(c, x, y, r*1.05, r); c.clip()
        g = cairo.LinearGradient(0, y-r, 0, y+r)
        g.add_color_stop_rgba(0, *hx('#e8463a', .85)); g.add_color_stop_rgba(.75, *hx('#e8463a', .35)); g.add_color_stop_rgba(1, *hx('#e8463a', 0))
        c.set_source(g); c.paint(); c.restore()
    if e in ('star', 'laugh', 'smile', 'cry'):
        for s in (-1, 1): ell(c, x+s*6.3*u, y+4*u, 2.2*u, 1.2*u, '#f59bb0', lw=0, a=.8)
    # ---- 眼睛 ----
    for s in (-1, 1):
        cx = x+s*ex
        if e == 'star':
            sc = 1+.12*math.sin(t*30)
            star(c, cx, ey, 3.6*u*sc, '#ffd43b', lw=3, rot=s*.2+t*3)
        elif e == 'laugh':
            stroke_line(c, [(cx-2.4*u, ey+.6*u), (cx, ey-1.6*u), (cx+2.4*u, ey+.6*u)], 1.1*u, OL)
        elif e == 'cry':
            stroke_line(c, [(cx-2.4*u, ey-1*u), (cx, ey+.8*u), (cx+2.4*u, ey-1*u)], 1.1*u, OL)
        elif e == 'angry':
            ell(c, cx, ey+.5*u, 2.4*u, 2.0*u, '#ffffff', lw=3)
            ell(c, cx+lx*u, ey+.8*u, 1.1*u, 1.1*u, OL, lw=0)
        elif e == 'down':
            stroke_line(c, [(cx-2*u, ey+1.2*u), (cx+2*u, ey+1.2*u)], .9*u, OL)
        else:
            big = 1.25 if e == 'shock' else 1
            ell(c, cx, ey, 2.5*u*big, 2.9*u*big, '#ffffff', lw=3)
            pr = (1.0 if e == 'shock' else 1.25)*u
            ell(c, cx+lx*u, ey+ly*u, pr, pr, OL, lw=0)
            if lash: stroke_line(c, [(cx+s*1.8*u, ey-2.4*u*big), (cx+s*3.3*u, ey-3.4*u*big)], .7*u, OL)
    # ---- 眉毛 ----
    for s in (-1, 1):
        cx = x+s*ex
        if e == 'angry':
            stroke_line(c, [(cx+s*3*u, ey-4.6*u), (cx-s*1.8*u, ey-2.6*u)], 1.5*u, OL)
        elif e == 'cry':
            stroke_line(c, [(cx+s*2.8*u, ey-3.4*u), (cx-s*1.8*u, ey-5.2*u)], 1.2*u, OL)
        elif e in ('shock',):
            stroke_line(c, [(cx-2*u, ey-6.2*u), (cx+2*u, ey-6.6*u)], 1.1*u, OL)
        elif e in ('star', 'laugh', 'smile'):
            c.new_path(); c.arc(cx, ey-2.6*u, 2.4*u, math.pi*1.15, math.pi*1.85); col(c, OL); c.set_line_width(1.1*u); c.stroke()
        elif e == 'side':
            stroke_line(c, [(cx-2.2*u, ey-4.4*u+s*.6*u), (cx+2.2*u, ey-4.4*u-s*.6*u)], 1.1*u, OL)
        else:
            stroke_line(c, [(cx-2.1*u, ey-4.4*u), (cx+2.1*u, ey-4.4*u)], 1.1*u, OL)
    # ---- 嘴 ----
    my = y+6.4*u
    if e == 'shock':
        ell(c, x, my, 1.6*u, 2.1*u, '#7a2b2b', lw=3)
    elif e == 'star':
        c.new_path(); c.move_to(x-4*u, my-1.2*u); c.curve_to(x-3*u, my+5*u, x+3*u, my+5*u, x+4*u, my-1.2*u); c.close_path()
        fill_stroke(c, '#7a2b2b', lw=3)
        ell(c, x, my+2.2*u, 1.8*u, .9*u, '#ef6f7b', lw=0)
    elif e == 'laugh':
        o = 1+.25*math.sin(t*40)
        c.new_path(); c.move_to(x-4.6*u, my-2*u); c.curve_to(x-3.6*u, my+6.5*u*o, x+3.6*u, my+6.5*u*o, x+4.6*u, my-2*u); c.close_path()
        fill_stroke(c, '#7a2b2b', lw=3)
        c.save(); c.new_path(); c.move_to(x-4.6*u, my-2*u); c.curve_to(x-3.6*u, my+6.5*u*o, x+3.6*u, my+6.5*u*o, x+4.6*u, my-2*u); c.close_path(); c.clip()
        box(c, x-5*u, my-2.4*u, 10*u, 1.4*u, '#ffffff', lw=0)
        ell(c, x, my+4.4*u*o, 2.6*u, 1.6*u, '#ef6f7b', lw=0); c.restore()
    elif e == 'angry':
        w_ = 4.4*u; h_ = 2.6*u
        box(c, x-w_, my-h_/2, 2*w_, h_, '#ffffff', r=.8*u, lw=3)
        for i in range(1, 4): stroke_line(c, [(x-w_+i*w_/2, my-h_/2), (x-w_+i*w_/2, my+h_/2)], 1.5, OL)
        stroke_line(c, [(x-w_, my), (x+w_, my)], 1.5, OL)
    elif e == 'cry':
        wob = math.sin(t*35)*.6*u
        c.new_path(); c.move_to(x-3.6*u, my+2*u)
        c.curve_to(x-1.5*u, my-2.5*u+wob, x+1.5*u, my-2.5*u-wob, x+3.6*u, my+2*u)
        c.curve_to(x+1.2*u, my+.4*u, x-1.2*u, my+.4*u, x-3.6*u, my+2*u); c.close_path()
        fill_stroke(c, '#7a2b2b', lw=3)
    elif e == 'smile':
        c.new_path(); c.arc(x, my-1.8*u, 2.6*u, .2*math.pi, .8*math.pi); col(c, OL); c.set_line_width(1*u); c.stroke()
    elif e == 'down':
        stroke_line(c, [(x-1.2*u, my), (x+1.2*u, my)], .8*u, OL)
    else:
        c.new_path(); c.arc(x, my-1.4*u, 1.6*u, .25*math.pi, .75*math.pi); col(c, OL); c.set_line_width(.9*u); c.stroke()

def hair_back(c, x, y, r, P, t=0):
    hs = P.get('hairstyle'); hc = P.get('hair', '#2b2b2b')
    if hs == 'pony':
        sw = math.sin(t*9)*8*r/50*P.get('swing', 1)
        # 高马尾：头顶后方甩向右侧
        c.new_path()
        c.move_to(x+.15*r, y-1.08*r)
        c.curve_to(x+1.0*r+sw*.5, y-1.9*r, x+1.9*r+sw, y-.9*r, x+1.55*r+sw*1.4, y+.55*r)
        c.curve_to(x+1.45*r+sw, y-.35*r, x+1.0*r, y-.8*r, x+.35*r, y-.7*r); c.close_path()
        fill_stroke(c, hc, lw=4)
    elif hs == 'long':
        c.new_path(); c.move_to(x-1.1*r, y-.2*r)
        c.curve_to(x-1.25*r, y+1.0*r, x-1.0*r, y+1.6*r, x-.6*r, y+1.7*r)
        c.line_to(x+.6*r, y+1.7*r); c.curve_to(x+1.0*r, y+1.6*r, x+1.25*r, y+1.0*r, x+1.1*r, y-.2*r); c.close_path()
        fill_stroke(c, hc, lw=4)
    elif hs == 'bun':
        ell(c, x, y-1.12*r, .38*r, .32*r, hc, lw=4)

def hair_front(c, x, y, r, P):
    hs = P.get('hairstyle'); hc = P.get('hair', '#2b2b2b')
    if hs == 'bald': return
    c.new_path()
    if hs in ('pony', 'long'):
        # 齐刘海+侧分
        c.move_to(x-1.06*r, y+.05*r)
        c.curve_to(x-1.12*r, y-1.25*r, x+1.12*r, y-1.25*r, x+1.06*r, y+.05*r)
        c.curve_to(x+.95*r, y-.35*r, x+.7*r, y-.48*r, x+.45*r, y-.42*r)
        c.line_to(x+.3*r, y-.62*r); c.line_to(x+.05*r, y-.4*r); c.line_to(x-.2*r, y-.58*r)
        c.line_to(x-.45*r, y-.38*r); c.curve_to(x-.75*r, y-.48*r, x-.95*r, y-.35*r, x-1.06*r, y+.05*r)
    else:
        c.move_to(x-1.04*r, y-.3*r)
        c.curve_to(x-1.1*r, y-1.25*r, x+1.1*r, y-1.25*r, x+1.04*r, y-.3*r)
        c.curve_to(x+.6*r, y-.68*r, x-.2*r, y-.8*r, x-1.04*r, y-.3*r)
    c.close_path(); fill_stroke(c, hc, lw=4)
    if hs == 'pony':
        ell(c, x+.45*r, y-1.0*r, .17*r, .14*r, '#ff7a90', lw=3)  # 发圈

def head(c, x, y, r, e, P, t=0, look=(0, 0), tilt=0, skip_long=False):
    c.save(); c.translate(x, y); c.rotate(tilt); x0, y0 = 0, 0
    if not (skip_long and P.get('hairstyle') == 'long'): hair_back(c, x0, y0, r, P, t)
    sk = P.get('skin', SKIN)
    for s in (-1, 1): ell(c, x0+s*1.02*r, y0+.15*r, .2*r, .24*r, sk, lw=4)
    ell(c, x0, y0, r*1.04, r, sk, lw=5)
    face(c, x0, y0, r, e, look, t, P)
    hair_front(c, x0, y0, r, P)
    if P.get('glasses'):
        u = r/11
        for s in (-1, 1): ell(c, x0+s*4.3*u, y0+.8*u, 3.3*u, 3.3*u, None, lw=3)
        stroke_line(c, [(x0-1*u, y0+.5*u), (x0+1*u, y0+.5*u)], 3, OL)
    c.restore()

def person(c, x, y, h, P, e='neutral', t=0, look=(0, 0), arms=((8, 4), (8, 4)), legs=(0, 0),
           tilt=0, lean=0, squash=1.0, hands=('open', 'open'), hold=None):
    """x,y=两脚中点地面；h=身高。arms=((左上臂角,左前臂角),(右...))；legs=(左脚dx,右脚dx 以u计)"""
    u = h/100
    c.save(); c.translate(x, y); c.scale(1/squash**.3, squash); c.translate(-x, -y)
    hip = y-40*u
    if P.get('hairstyle') == 'long': hair_back(c, x, y-85.5*u, 12.5*u, P, t)
    # 腿
    for s, d in ((-1, legs[0]), (1, legs[1])):
        fx = x+s*5*u+d*u
        lift = max(0, -abs(d)*.0)  # reserved
        tube(c, [(x+s*5*u, hip), (fx, y-4.5*u)], 7*u, P['pants'])
        ell(c, fx+s*1.2*u, y-2.2*u, 5.4*u, 2.6*u, P.get('shoe', '#fff'), lw=4)
    # 躯干
    c.save(); c.translate(x, hip); c.rotate(math.radians(lean)); c.translate(-x, -hip)
    top = y-73*u
    c.new_path(); c.move_to(x-13*u, top+3*u)
    c.curve_to(x-15.5*u, top+18*u, x-14*u, top+30*u, x-13*u, hip+4*u)
    c.line_to(x+13*u, hip+4*u); c.curve_to(x+14*u, top+30*u, x+15.5*u, top+18*u, x+13*u, top+3*u)
    c.curve_to(x+6*u, top-1*u, x-6*u, top-1*u, x-13*u, top+3*u); c.close_path()
    fill_stroke(c, P['hoodie'])
    c.new_path(); c.move_to(x+8*u, top+2*u); c.curve_to(x+12*u, top+18*u, x+12*u, top+30*u, x+11*u, hip+3*u)
    c.line_to(x+13*u, hip+3*u); c.curve_to(x+14*u, top+30*u, x+15.5*u, top+18*u, x+13*u, top+3*u); c.close_path()
    col(c, P['hood_d'], .55); c.fill()
    # 下摆罗纹
    box(c, x-13*u, hip+.5*u, 26*u, 3.6*u, P['hood_d'], r=1.5*u, lw=4)
    # 袋鼠兜
    c.new_path(); c.move_to(x-8*u, hip-1*u); c.line_to(x-6.5*u, hip-11*u); c.line_to(x+6.5*u, hip-11*u); c.line_to(x+8*u, hip-1*u); c.close_path()
    fill_stroke(c, P['hood_d'], lw=4)
    # 帽兜领
    c.new_path(); c.move_to(x-7*u, top+.5*u); c.curve_to(x-6*u, top+7*u, x+6*u, top+7*u, x+7*u, top+.5*u)
    c.curve_to(x+4*u, top+3.5*u, x-4*u, top+3.5*u, x-7*u, top+.5*u); c.close_path(); fill_stroke(c, P['hood_d'], lw=4)
    for s in (-1, 1): stroke_line(c, [(x+s*2.2*u, top+4*u), (x+s*2.6*u, top+13*u)], 2.6, '#f4efe6')
    # 手臂
    hp = []
    for s, (a1, a2), hd in ((-1, arms[0], hands[0]), (1, arms[1], hands[1])):
        hp.append(_arm(c, x+s*12*u, top+5*u, a1, a2, 15*u, 14*u, 6.5*u, P['hoodie'], P.get('skin', SKIN), s, hd))
    if hold: hold(c, hp)
    hy = top-12.5*u
    head(c, x, hy, 12.5*u, e, P, t, look, math.radians(tilt), skip_long=True)
    c.restore()
    c.restore()
    return dict(head=(x, hy), r=12.5*u, hands=hp)

def bust(c, x, y, s, P, e='side', look=(3, 0), t=0, glow=0):
    """前景大半身：肩膀半圆+大头（原片画面底部左右两角的围观群众）"""
    u = s/100
    if P.get('hairstyle') == 'long': hair_back(c, x, y-42*u, 26*u, P, t)
    c.new_path(); c.move_to(x-48*u, y+10*u); c.curve_to(x-46*u, y-30*u, x+46*u, y-30*u, x+48*u, y+10*u); c.close_path()
    fill_stroke(c, P['hoodie'])
    head(c, x, y-42*u, 26*u, e, P, t, look, skip_long=True)
    if glow:
        for sd in (-1, 1):
            ell(c, x+sd*10.2*u+max(-1.3,min(1.3,look[0]))*2.4*u, y-40*u, 3.4*u, 3.4*u, '#5ce1e6', lw=0, a=.55*glow)
    return (x, y-40*u)
