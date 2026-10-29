"""社恐小人风 场景库 + HUD + 特效"""
from lib import *
from rig import *

# ================= 背景 =================
def floor_tiles(c, y0, y1, base, line, vp=(960, -600), n=26):
    box(c, -10, y0, W+20, y1-y0, base, lw=0)
    for i in range(-n, n+1):
        x = 960+i*150
        stroke_line(c, [(lerp(vp[0], x, (y0-vp[1])/(y1-vp[1])), y0), (x*1.0+(x-960)*.6, y1)], 2, line, .6)
    yy = y0
    k = 22
    while yy < y1:
        stroke_line(c, [(0, yy), (W, yy)], 2, line, .6); yy += k; k *= 1.35

def bg_market(c, t, cam=0):
    """超市货架区·侧面平铺（原片街景的构图：天花/墙/货架/地砖四层）"""
    g = cairo.LinearGradient(0, 0, 0, 640); g.add_color_stop_rgb(0, *hx('#fbf3e3')[:3]); g.add_color_stop_rgb(1, *hx('#f1e2c8')[:3])
    c.set_source(g); c.rectangle(0, 0, W, 700); c.fill()
    # 吊顶灯带
    box(c, -10, -10, W+20, 70, '#e6d6bb', lw=5)
    for i in range(7):
        x = (i*300+60-cam*.3) % (W+300)-150
        box(c, x, 60, 180, 18, '#fffbe8', r=9, lw=4)
        g = cairo.LinearGradient(0, 78, 0, 300); g.add_color_stop_rgba(0, 1, 1, .9, .55); g.add_color_stop_rgba(1, 1, 1, .9, 0)
        c.set_source(g); c.move_to(x+10, 78); c.line_to(x+170, 78); c.line_to(x+230, 300); c.line_to(x-50, 300); c.close_path(); c.fill()
    # 区域吊牌
    for i, (s, cc) in enumerate((('零食区', '#ff8a3d'), ('饮料区', '#3fa7d6'), ('日用品', '#7bc96f'))):
        x = (i*720+320-cam*.5) % (W+700)-350
        stroke_line(c, [(x+40, 0), (x+40, 110)], 4, OL); stroke_line(c, [(x+200, 0), (x+200, 110)], 4, OL)
        box(c, x, 105, 240, 76, cc, r=14)
        text(c, s, x+120, 140, 42, '#ffffff', stroke=OL, sw=6)
    # 货架
    sx0 = -cam % 420-420
    PROD = ['#ff5d5d', '#ffd43b', '#4dabf7', '#69db7c', '#f783ac', '#ffa94d', '#9775fa']
    rnd = random.Random(3)
    tab = [[rnd.choice(PROD) for _ in range(40)] for _ in range(4)]
    for k in range(7):
        x = sx0+k*420
        box(c, x, 230, 400, 470, '#dfe7f2', r=10)
        for j in range(4):
            yy = 300+j*105
            for m in range(6):
                pc = tab[j][(k*6+m+int(cam//420)*6) % 40]
                hh = 62 if (m+j) % 3 else 48
                box(c, x+22+m*62, yy+70-hh, 50, hh, pc, r=6, lw=4)
                box(c, x+30+m*62, yy+70-hh+12, 34, 12, '#ffffff', r=4, lw=0, a=.7)
            box(c, x+8, yy+70, 384, 16, '#b9c6d8', r=4, lw=4)
    floor_tiles(c, 700, H, '#e9e2d6', '#cfc4b2')

def bg_checkout(c, t):
    g = cairo.LinearGradient(0, 0, 0, 640); g.add_color_stop_rgb(0, *hx('#fdf0e6')[:3]); g.add_color_stop_rgb(1, *hx('#f5dccb')[:3])
    c.set_source(g); c.rectangle(0, 0, W, 700); c.fill()
    box(c, -10, -10, W+20, 70, '#e8cdb8', lw=5)
    # 远景淡货架
    for k in range(6):
        x = k*340-40
        box(c, x, 250, 320, 450, '#eadfd6', r=8, lw=4, a=1)
        for j in range(4):
            box(c, x+10, 330+j*95, 300, 12, '#d5c4b6', lw=0)
    # 收银台吊牌
    stroke_line(c, [(560, 0), (560, 120)], 4, OL); stroke_line(c, [(760, 0), (760, 120)], 4, OL)
    box(c, 500, 112, 320, 88, '#e64a4a', r=16)
    text(c, '收银台 1', 660, 156, 48, '#ffffff', stroke=OL, sw=6)
    floor_tiles(c, 700, H, '#efe6dc', '#d6c7b8')

def checkout_counter(c, t):
    # 收银台柜体（前景，人物后画则在柜体前）
    box(c, 250, 600, 560, 230, '#5b6b8c', r=12)
    box(c, 230, 580, 600, 40, '#8ea0c3', r=10)
    box(c, 260, 588, 360, 24, '#2e3550', r=8, lw=3)  # 传送带
    for i in range(9): stroke_line(c, [(275+i*38, 590), (275+i*38, 610)], 3, '#55607e')
    # 收银机
    box(c, 640, 470, 150, 110, '#dfe5ef', r=10)
    box(c, 655, 482, 120, 60, '#1f2b3d', r=6, lw=3)
    text(c, '¥36.8', 715, 512, 30, '#7CFC9A', weight='Bold')
    # 扫码器
    box(c, 600, 520, 30, 60, '#2e3550', r=8, lw=3)

def bg_subway(c, t, vp=(960, 470)):
    """地铁车厢·一点透视（原片车厢镜头复刻：亮白顶灯条/深蓝墙窗/蓝座/黄扶杆/吊环）"""
    vx, vy = vp
    col(c, '#1d2740'); c.paint()
    # 顶棚
    poly(c, [(0, 0), (W, 0), (vx+260, vy-170), (vx-260, vy-170)], '#e9eef6', lw=4)
    for s in (-1, 1):
        poly(c, [(vx+s*120, vy-170), (vx+s*200, vy-170), (vx+s*620, 0), (vx+s*420, 0)], '#ffffff', lw=0)
    g = cairo.RadialGradient(vx, 0, 50, vx, 0, 800); g.add_color_stop_rgba(0, 1, 1, 1, .5); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.set_source(g); c.paint()
    # 侧墙
    for s in (-1, 1):
        ex = 0 if s < 0 else W
        poly(c, [(ex, 0), (vx+s*260, vy-170), (vx+s*260, vy+40), (ex, H*0.62)], '#2b3a5c', lw=4)
        # 窗
        for k in range(3):
            a0, a1 = .05+k*.3, .27+k*.3
            def P(a, yy0, yy1, f):
                x = lerp(ex, vx+s*260, a); return (x, lerp(yy0, yy1, a))
            p1 = P(a0, 150, vy-120, 0); p2 = P(a1, 150, vy-120, 0); p3 = P(a1, 470, vy-10, 0); p4 = P(a0, 470, vy-10, 0)
            poly(c, [p1, p2, p3, p4], '#15203a', lw=4)
            stroke_line(c, [(p1[0]+(p2[0]-p1[0])*.2, p1[1]+30), (p1[0]+(p2[0]-p1[0])*.6, p1[1]+30)], 6, '#d9c38a', .8)
        # 线路图条
        x0, x1 = lerp(ex, vx+s*260, .55), lerp(ex, vx+s*260, .8)
        poly(c, [(x0, lerp(70, vy-150, .55)), (x1, lerp(70, vy-150, .8)), (x1, lerp(110, vy-138, .8)), (x0, lerp(110, vy-138, .55))], '#7fd6c9', lw=3)
    # 远端门
    box(c, vx-260, vy-170, 520, 210, '#dfe6f1', lw=4)
    box(c, vx-90, vy-150, 180, 190, '#b9c4d6', lw=4)
    box(c, vx-70, vy-130, 60, 80, '#2b3a5c', lw=3); box(c, vx+10, vy-130, 60, 80, '#2b3a5c', lw=3)
    # 地板
    poly(c, [(vx-260, vy+40), (vx+260, vy+40), (W+400, H), (-400, H)], '#3a4258', lw=4)
    g = cairo.LinearGradient(0, vy+40, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, .35)
    c.set_source(g); c.move_to(vx-260, vy+40); c.line_to(vx+260, vy+40); c.line_to(W+400, H); c.line_to(-400, H); c.close_path(); c.fill()
    # 座椅
    for s in (-1, 1):
        poly(c, [(vx+s*250, vy-30), (vx+s*250, vy+40), (vx+s*900, H*.78), (vx+s*1100, H*.62)], '#2f5bb7', lw=4)
        poly(c, [(vx+s*250, vy+10), (vx+s*250, vy+40), (vx+s*900, H*.78), (vx+s*1000, H*.68)], '#3f74d6', lw=4)

def subway_poles(c, t, vp=(960, 470)):
    vx, vy = vp
    for s in (-1, 1):
        for x, top, bot, w in ((vx+s*330, 70, 700, 14), (vx+s*560, 0, 900, 18)):
            box(c, x-w/2, top, w, bot-top, '#f2c230', r=w/2, lw=4)
        # 吊环
        for k, x in enumerate((vx+s*230, vx+s*330, vx+s*440, vx+s*560)):
            ln = 60+k*18; rr = 16+k*5
            yy = 150-k*25
            stroke_line(c, [(x, yy-ln), (x, yy)], 5, '#e8ecf3')
            c.new_path(); c.arc(x, yy+rr, rr, 0, 2*math.pi); col(c, OL); c.set_line_width(10); c.stroke_preserve(); col(c, '#ffffff'); c.set_line_width(5); c.stroke()
        stroke_line(c, [(vx+s*200, 72), (vx+s*720, -40)], 10, '#c9d2e0')

# ================= HUD =================
def hud_counter(c, t, val, t_change, slash=False, accent='#ffffff'):
    """左上角“在看我”计数框（原片核心 HUD：眼睛图标+数字，切换时弹跳）"""
    x, y, w, h = 40, 36, 330, 150
    rrect(c, x, y, w, h, 26); col(c, '#1b1d2b', .9); c.fill()
    text(c, '在看我', x+225, y+30, 28, '#ffffff', weight='Bold', a=.85)
    # 眼睛
    ex, ey = x+80, y+86
    c.new_path(); c.move_to(ex-48, ey); c.curve_to(ex-20, ey-36, ex+20, ey-36, ex+48, ey); c.curve_to(ex+20, ey+36, ex-20, ey+36, ex-48, ey); c.close_path()
    col(c, '#ffffff'); c.fill()
    ell(c, ex, ey, 16, 16, '#1b1d2b', lw=0); ell(c, ex+5, ey-5, 5, 5, '#ffffff', lw=0)
    if slash: stroke_line(c, [(ex-44, ey+30), (ex+44, ey-30)], 10, '#1b1d2b'); stroke_line(c, [(ex-44, ey+30), (ex+44, ey-30)], 5, '#5ce1e6')
    k = pop(t, t_change, .3)
    sc = 1+.6*(1-k) if t >= t_change else 1
    c.save(); c.translate(x+225, y+96); c.scale(sc, sc)
    text(c, str(val), 0, 0, 84, accent)
    c.restore()

def subtitle(c, t, parts, y=960):
    """底部单行字幕：前半白字，后半关键词彩字分拍出现（原片做法）"""
    shown = [(s, h, t0) for s, h, t0 in parts if t >= t0]
    if not shown: return
    g = cairo.LinearGradient(0, H-260, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, .08, .06, .12, .55)
    c.set_source(g); c.rectangle(0, H-260, W, 260); c.fill()
    size = 66
    tot = sum(text_w(c, s, size) for s, h, t0 in shown)
    x = W/2-tot/2
    for s, h, t0 in shown:
        k = pop(t, t0, .22); w = text_w(c, s, size)
        c.save(); c.translate(x+w/2, y); c.scale(.6+.4*k, .6+.4*k)
        text(c, s, 3, 5, size, '#000000', a=.45)
        text(c, s, 0, 0, size, h, stroke='#1b1d2b', sw=8)
        c.restore(); x += w

def bubble(c, x, y, s, t, t0, fc='#e8742a', size=60, tail=1):
    if t < t0: return
    k = pop(t, t0, .25)
    c.save(); c.translate(x, y); c.scale(k, k)
    w = text_w(c, s, size)+70; h = size+50
    rrect(c, -w/2, -h/2, w, h, 22); fill_stroke(c, '#fff6ea', lw=0)
    rrect(c, -w/2, -h/2, w, h, 22); col(c, fc); c.set_line_width(8); c.stroke()
    poly(c, [(-20*tail, h/2-4), (0, h/2+34), (22*tail, h/2-4)], '#fff6ea', lw=0)
    stroke_line(c, [(-20*tail, h/2), (0, h/2+34), (22*tail, h/2)], 8, fc, cap=True)
    text(c, s, 0, 0, size, fc)
    c.restore()

# ================= 特效 =================
def gaze(c, p0, p1, t, t0, dur=.35, bulge=-160, a=1):
    """围观视线：从眼睛到主角头的青色虚线弧（原片招牌）"""
    if t < t0: return
    k = eo((t-t0)/dur)
    mid = ((p0[0]+p1[0])/2, min(p0[1], p1[1])+bulge)
    pts = qcurve(p0, mid, p1, 40)
    n = max(2, int(len(pts)*k))
    stroke_line(c, pts[:n], 9, '#13304a', .35*a, dash=[22, 14], off=-t*60)
    stroke_line(c, pts[:n], 5, '#4fd8e0', .95*a, dash=[22, 14], off=-t*60)
    ell(c, p0[0], p0[1], 9, 9, '#5ce1e6', lw=0, a=.6*a)

def speed_lines(c, x, y, t, n=5, dirx=-1, a=1):
    for i in range(n):
        yy = y+i*55-n*27
        L = 180+80*math.sin(i*1.7+t*20)
        xx = x+dirx*(60+i*25)
        stroke_line(c, [(xx, yy), (xx+dirx*L, yy)], 10, '#ffffff', .9*a)

def burst(c, x, y, r, t, colr='#ffd43b', n=16, a=1):
    c.save(); c.translate(x, y); c.rotate(t*1.5)
    for i in range(n):
        a0 = i*2*math.pi/n
        c.move_to(0, 0); c.arc(0, 0, r, a0, a0+math.pi/n*.8); c.close_path()
    col(c, colr, .55*a); c.fill(); c.restore()

def sparkle(c, x, y, s, t, colr='#ffffff'):
    k = abs(math.sin(t*12))
    star(c, x, y, s*(.5+.5*k), colr, lw=3, n=4, inner=.3)

def steam(c, x, y, t, s=1):
    for i in range(6):
        ph = (t*2.2+i/6) % 1
        sd = -1 if i % 2 else 1
        px = x+sd*(40+ph*110)*s; py = y-ph*160*s
        r = (22+ph*38)*s
        ell(c, px, py, r, r*.8, '#ffffff', lw=4, a=1-ph*.7)

def anger_mark(c, x, y, s, t):
    k = 1+.18*math.sin(t*30)
    c.save(); c.translate(x, y); c.scale(s*k, s*k)
    for a in range(4):
        c.save(); c.rotate(a*math.pi/2)
        c.new_path(); c.move_to(6, -26); c.curve_to(8, -8, 8, -8, 26, -6)
        col(c, OL); c.set_line_width(13); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke_preserve(); col(c, '#ff3b3b'); c.set_line_width(8); c.stroke()
        c.restore()
    c.restore()

def tears(c, x, y, t, side, s=1):
    """泪喷泉：两道抛物线水柱"""
    for i in range(14):
        ph = (t*2.6+i/14) % 1
        px = x+side*ph*170*s; py = y+(-120*ph+260*ph*ph)*s
        ell(c, px, py, (10-ph*3)*s, (13-ph*3)*s, '#6cc6ff', lw=3, a=1-ph*.4)

def rain_cloud(c, x, y, t, s=1):
    for i in range(10):
        ph = (t*3+i/10) % 1
        px = x-90*s+(i*37 % 180)*s; py = y+30*s+ph*170*s
        stroke_line(c, [(px, py), (px-6, py+26*s)], 5, '#6cc6ff', 1-ph)
    for dx, dy, r in ((-70, 10, 48), (-15, -15, 62), (55, 5, 50), (0, 25, 55)):
        ell(c, x+dx*s, y+dy*s, r*s, r*.8*s, '#8b93a7', lw=5)
    for dx, dy, r in ((-70, 10, 48), (-15, -15, 62), (55, 5, 50), (0, 25, 55)):
        ell(c, x+dx*s, y+dy*s, r*s-5, r*.8*s-5, '#8b93a7', lw=0)

def ring_pulse(c, x, y, t, t0, dur=.6, rmax=900):
    if not (t0 <= t < t0+dur): return
    k = (t-t0)/dur
    for j in (0, .18):
        kk = cl(k-j)
        if kk <= 0: continue
        c.new_path(); c.arc(x, y, 60+kk*rmax, 0, 2*math.pi); col(c, '#5ce1e6', (1-kk)*.9); c.set_line_width(14*(1-kk)+2); c.stroke()

def phone_pop(c, x, y, t, t0, state):
    if t < t0: return
    k = pop(t, t0, .25)
    c.save(); c.translate(x, y); c.rotate(.12); c.scale(k, k)
    box(c, -95, -170, 190, 340, '#1f2638', r=28, lw=6)
    if state == 'paying':
        box(c, -80, -150, 160, 300, '#2f7d4f', r=18, lw=0)
        text(c, '支付中', 0, -40, 34, '#ffffff')
        for i in range(8):
            a = i*math.pi/4+t*8
            ell(c, math.cos(a)*36, 40+math.sin(a)*36, 7, 7, '#ffffff', lw=0, a=.25+.75*((i/8+t*1.3) % 1))
    else:
        box(c, -80, -150, 160, 300, '#3a1218', r=18, lw=0)
        ell(c, 0, -50, 52, 52, '#ff4757', lw=5)
        stroke_line(c, [(-22, -72), (22, -28)], 12, '#ffffff'); stroke_line(c, [(22, -72), (-22, -28)], 12, '#ffffff')
        text(c, '支付失败', 0, 50, 36, '#ff6b6b')
        text(c, '网络超时', 0, 100, 24, '#ffb3b3', weight='Bold')
    c.restore()

def price_tag(c, x, y, t, t0):
    if t < t0: return
    k = pop(t, t0, .3)
    c.save(); c.translate(x, y); c.rotate(-.18+.05*math.sin(t*14)); c.scale(k, k)
    star(c, 0, 0, 175, '#ffd43b', lw=6, n=14, inner=.8)
    star(c, 0, 0, 150, '#ff3b3b', lw=0, n=14, inner=.82)
    text(c, '第2件', 0, -40, 54, '#ffffff', stroke=OL, sw=7)
    text(c, '半价', 0, 34, 84, '#ffe066', stroke=OL, sw=9)
    c.restore()

def orange(c, x, y, r, rot=0):
    ell(c, x, y, r, r, '#ff9f1c', lw=4)
    c.save(); c.translate(x, y); c.rotate(rot)
    ell(c, r*.3, -r*.35, r*.22, r*.15, '#ffd08a', lw=0)
    poly(c, [(0, -r), (r*.35, -r*1.35), (r*.1, -r*.95)], '#5cb85c', lw=3)
    c.restore()

def confetti(c, t, t0, n=60, seed=4):
    if t < t0: return
    rnd = random.Random(seed); cs = ['#ff6b6b', '#ffd43b', '#4dabf7', '#69db7c', '#f783ac', '#5ce1e6']
    for i in range(n):
        x0 = rnd.uniform(0, W); vy = rnd.uniform(300, 650); sp = rnd.uniform(-6, 6)
        y = -40+(t-t0)*vy-rnd.uniform(0, 400)
        if y < -40: continue
        c.save(); c.translate(x0+math.sin(t*3+i)*40, y); c.rotate(t*sp)
        box(c, -10, -6, 20, 12, rnd.choice(cs), lw=0); c.restore()
