"""样片：20岁女生 去超市+坐地铁（喜怒哀乐 鬼畜版，10秒）"""
import sys, subprocess, numpy as np
from scenes import *

DUR = 10.0
HERO = dict(HERO)
B1 = dict(hoodie='#f08a3c', hood_d='#cf6d22', pants='#2c3557', hair='#2a2222', hairstyle='short')
B2 = dict(hoodie='#5fbf7a', hood_d='#3f9a5a', pants='#3b3f5c', hair='#4a2f25', hairstyle='long', lash=True)
B3 = dict(hoodie='#e44f6b', hood_d='#bf3550', pants='#2c3557', hair='#222', hairstyle='short', glasses=True)
B4 = dict(hoodie='#8d6fe0', hood_d='#6c50c0', pants='#2c3557', hair='#2a2222', hairstyle='bun')
B5 = dict(hoodie='#4f8fe0', hood_d='#356fc0', pants='#2c3557', hair='#2a2222', hairstyle='short')
B6 = dict(hoodie='#f2c14e', hood_d='#d4a12e', pants='#2c3557', hair='#3a2a20', hairstyle='long', lash=True, skin='#e8b48c')
B7 = dict(hoodie='#f59bb0', hood_d='#d97a92', pants='#2c3557', hair='#2a2222', hairstyle='long', glasses=True, lash=True, skin='#d9a27b')
B8 = dict(hoodie='#6ccfb5', hood_d='#45ad93', pants='#2c3557', hair='#222', hairstyle='short', glasses=True)

# ---------------- 鬼畜时间重映射 ----------------
# (起, 止, 循环窗口起, 窗口长, 效果)
LOOPS = [(1.20, 2.04, 1.00, .28, 'zoom'),
         (3.55, 4.75, 3.30, .30, 'shake'),
         (6.20, 7.10, 5.85, .30, 'zoomout'),
         (9.00, 9.88, 8.20, .22, 'mirror')]
def remap(T):
    for a, b, w0, wl, fx in LOOPS:
        if a <= T < b:
            n = int((T-a)//wl); ph = ((T-a) % wl)/wl
            return w0+ph*wl, fx, n, ph
    return T, None, 0, 0

def cam_push(c, cx, cy, z):
    c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)

# ---------------- 镜头 ----------------
def S1(c, t, T):
    cam = t*40
    bg_market(c, t, cam)
    price_tag(c, 1330, 420, t, .45)
    if t >= .95:
        burst(c, 900, 420, 900, t, '#fff3a8', a=ramp(t, .95, 1.1))
    hx_ = lerp(480, 860, ramp(t, 0, .65)) if t < 2.04 else lerp(860, 2400, eo((T-2.04)/.42))
    # 路人
    pA = person(c, 1560, 900, 500, B1, e='side' if t > .9 else 'neutral', t=t, look=(-1.3, 0) if t > .9 else (0, 0), arms=((10, 5), (25, 60)))
    pB = person(c, 230, 920, 470, B2, e='side' if t > .9 else 'neutral', t=t, look=(1.3, 0) if t > .9 else (0, 0))
    walk = t < .65
    sw = math.sin(t*22)*10 if walk else 0
    jump = 0; e = 'neutral'; arms = ((8+sw, 5), (8-sw, 5)); legs = (sw*.5, -sw*.5); sq = 1; tilt = 0; lean = 0; look = (0, 0)
    if .6 <= t < .95: e = 'shock'; look = (1.3, -.5); arms = ((40, 60), (40, 60))
    if t >= .95:
        e = 'star'; ph = (t-.95)
        jump = abs(math.sin(ph*9))*110; arms = ((165, 15), (165, 15)); legs = (-6, 6); sq = 1.08 if jump > 60 else .94
    if T >= 2.04: e = 'star'; jump = 0; arms = ((70, 20), (110, -30)); legs = (-14, 14); lean = 14; sq = 1
    hero = person(c, hx_, 900-jump, 560, HERO, e=e, t=T, look=look, arms=arms, legs=legs, squash=sq, lean=lean)
    if t >= .95 and T < 2.04:
        for i, (dx, dy) in enumerate(((-230, -260), (220, -300), (-260, 40), (250, 0))):
            sparkle(c, hx_+dx, 900-jump+dy-300, 34, t+i*.3, '#fff59d')
    if T >= 2.04: speed_lines(c, hx_-120, 650, T, 6, -1)
    if t > 1.0:
        gaze(c, (pA['head'][0]-14, pA['head'][1]+4), hero['head'], t, 1.0)
        gaze(c, (pB['head'][0]+14, pB['head'][1]+4), hero['head'], t, 1.05)
    return hero

def S2(c, t, T):
    bg_checkout(c, t)
    # 收银员在柜台后
    cash = person(c, 470, 860, 500, B3, e='side' if t > 3.35 else 'smile', t=t, look=(1.3, 0))
    checkout_counter(c, t)
    angry = t >= 3.3
    shake = (math.sin(T*90)*14 if angry else 0)
    q = []
    for i, (x, P) in enumerate(((1330, B4), (1560, B2), (1780, B5))):
        q.append(person(c, x, 920, 520-i*10, P, e='side' if t > 3.35 else 'neutral', t=t+i, look=(-1.3, 0) if t > 3.35 else (0, 0), arms=((10, 5), (10, 5))))
    e = 'smile'; arms = ((10, 5), (60, 95)); look = (1, -1)
    if 3.0 <= t < 3.3: e = 'shock'; arms = ((40, 60), (60, 95))
    if angry: e = 'angry'; arms = ((150, -40), (150, -40))
    hero = person(c, 980+shake, 920, 560, HERO, e=e, t=T, look=look, arms=arms, hands=('fist', 'fist') if angry else ('open', 'open'), legs=(-4, 4) if not angry else (-10, 10))
    if not angry:
        phone_pop(c, 1170, 310, t, 2.6, 'paying' if t < 3.0 else 'fail')
    else:
        phone_pop(c, 1240, 330, t, 3.0, 'fail')
        hx_, hy_ = hero['head']
        steam(c, hx_, hy_-90, T, 1.1)
        anger_mark(c, hx_+95, hy_-70, 1.5, T)
        for p in q: gaze(c, (p['head'][0]-14, p['head'][1]+4), hero['head'], t, 3.35+.05*q.index(p))
        gaze(c, (cash['head'][0]+14, cash['head'][1]+4), hero['head'], t, 3.45, bulge=-120)
    return hero

def orange_state(t, i):
    """袋子破后橘子的抛射+弹跳+滚动"""
    rnd = random.Random(i*7+1)
    x0, y0 = 1110, 640
    vx = rnd.uniform(-520, 520); vy = rnd.uniform(-650, -250); g = 2200
    floor = 840+rnd.uniform(-20, 140)
    tt = t-5.5
    if tt < 0: return None
    x, y = x0+vx*tt, y0+vy*tt+.5*g*tt*tt
    if y > floor:
        # 首次落地时间
        t1 = (-vy+math.sqrt(vy*vy+2*g*(floor-y0)))/g
        tb = tt-t1; v2 = (vy+g*t1)*.45
        yb = floor-(v2*tb-.5*g*tb*tb)
        y = min(floor, yb) if tb < 2*v2/g else floor
        x = x0+vx*t1+vx*.6*min(tb, 1.2)-.25*vx*.6*min(tb, 1.2)**2/1.2
    return x, y, (x-x0)/30

def SUB(c, t, T, phase):
    bg_subway(c, t)
    down = phase == 2
    looker = (not down) and t >= 5.85
    # 远处坐着的半身
    mids = []
    for x, y, s, P, lk in ((430, 700, 240, B8, 1.3), (1490, 700, 240, B6, -1.3), (640, 640, 170, B3, 1.3), (1290, 640, 170, B1, -1.3)):
        e = 'down' if down else ('side' if looker else 'neutral')
        mids.append((bust(c, x, y, s, P, e=e, look=(lk, 0) if looker else (0, 0), t=t, glow=1 if looker else 0), x, y, s))
        if down: phone_glow(c, x, y-s*.16, s)
    subway_poles(c, t)
    stands = []
    for x, P, lk in ((640, B4, 1.3), (1290, B5, -1.3)):
        arms = ((165, 5), (12, 5)) if x < 900 else ((12, 5), (165, 5))
        if down: arms = ((165, 5), (40, 95)) if x < 900 else ((40, 95), (165, 5))
        p = person(c, x, 800, 470, P, e='down' if down else ('side' if looker else 'neutral'), t=t, look=(lk, 0) if looker else (0, 0), arms=arms)
        if down:
            hh = p['hands'][1] if x < 900 else p['hands'][0]
            box(c, hh[0]-18, hh[1]-50, 36, 62, '#1f2638', r=7, lw=3); box(c, hh[0]-13, hh[1]-44, 26, 46, '#9fe8ff', r=4, lw=0)
        stands.append(p)
    # 地上的橘子（第4镜保留）
    obs = [orange_state(t if phase == 1 else 7.49, i) for i in range(9)]
    if phase == 2 or t >= 5.5:
        for i, o in enumerate(obs):
            if o: orange(c, o[0], o[1], 26, o[2])
    # 主角
    e = 'smile'; arms = ((10, 5), (20, -5)); tilt = 0; jump = 0; look = (0, 0)
    if phase == 1 and 5.5 <= t < 5.8: e = 'shock'; arms = ((40, 60), (60, 60))
    if phase == 1 and t >= 5.8: e = 'cry'; arms = ((25, 120), (25, 120))
    if phase == 2:
        e = 'shock' if t < 8.1 else 'laugh'; look = (0, -1)
        if t >= 8.1:
            jump = abs(math.sin((t-8.1)*10))*60; tilt = -8+6*math.sin(t*20)
            arms = ((150+20*math.sin(t*18), 20), (150-20*math.sin(t*18), 20))
    sq = 1.0
    hero = person(c, 960, 820-jump, 560, HERO, e=e, t=T, look=look, arms=arms, tilt=tilt, squash=sq,
                  hold=(bag_hold(t) if phase == 1 and t < 5.5 else None))
    hx_, hy_ = hero['head']
    if phase == 1 and 5.5 <= t < 5.8:
        hh = hero['hands'][1]; torn_bag(c, hh)
    if phase == 1 and t >= 5.8:
        tears(c, hx_-30, hy_+5, T, -1); tears(c, hx_+30, hy_+5, T, 1)
        rain_cloud(c, hx_, hy_-210, T, 1.0)
    if phase == 2 and t >= 8.1:
        for i, (dx, dy, cc) in enumerate(((-300, -120, '#ff6b6b'), (280, -170, '#ffd43b'), (-250, 120, '#4dabf7'), (300, 90, '#69db7c'))):
            if t >= 8.1+i*.08:
                k = pop(t, 8.1+i*.08, .2)
                c.save(); c.translate(hx_+dx, hy_+dy); c.rotate(math.sin(T*20+i)*.2); c.scale(k, k)
                text(c, '哈', 0, 0, 96, cc, stroke=OL, sw=9); c.restore()
    # 前景大头（原片车厢底部两角的围观者）
    fgs = []
    for x, y, s, P, lk in ((150, 1150, 560, B7, 1.3), (470, 1210, 380, B1, 1.3), (1770, 1150, 560, B6, -1.3), (1450, 1210, 380, B8, -1.3)):
        e2 = 'down' if down else ('side' if looker else 'neutral')
        fgs.append(bust(c, x, y, s, P, e=e2, look=(lk, -.6) if looker else (0, 0), t=t, glow=1 if looker else 0))
        if down: phone_glow(c, x, y-s*.12, s)
    if looker:
        k = 0
        for p in [m[0] for m in mids]+[(s_['head'][0], s_['head'][1]) for s_ in stands]+fgs:
            gaze(c, p, (hx_, hy_-10), t, 5.85+k*.04, bulge=-180); k += 1
    if phase == 2:
        ring_pulse(c, hx_, hy_, t, 7.5, .7, 1300)
        confetti(c, t, 8.1)
    return hero

def phone_glow(c, x, y, s):
    u = s/100
    box(c, x-16*u, y-8*u, 32*u, 20*u, '#1f2638', r=3*u, lw=3)
    box(c, x-13*u, y-5.5*u, 26*u, 15*u, '#9fe8ff', r=2*u, lw=0)

def bag_hold(t):
    def f(c, hp):
        hx_, hy_ = hp[1]
        stroke_line(c, [(hx_-20, hy_), (hx_-30, hy_+40)], 6, OL); stroke_line(c, [(hx_+20, hy_), (hx_+30, hy_+40)], 6, OL)
        c.new_path(); c.move_to(hx_-55, hy_+35); c.line_to(hx_+55, hy_+35); c.line_to(hx_+65, hy_+170); c.curve_to(hx_+20, hy_+190, hx_-20, hy_+190, hx_-65, hy_+170); c.close_path()
        fill_stroke(c, '#f7f7f2')
        for i, (dx, dy) in enumerate(((-28, 40), (8, 30), (36, 48))): orange(c, hx_+dx, hy_+dy, 22)
        text(c, '超市', hx_, hy_+110, 34, '#e64a4a')
    return f

def torn_bag(c, hp):
    hx_, hy_ = hp
    stroke_line(c, [(hx_-20, hy_), (hx_-30, hy_+40)], 6, OL); stroke_line(c, [(hx_+20, hy_), (hx_+30, hy_+40)], 6, OL)
    poly(c, [(hx_-55, hy_+35), (hx_+55, hy_+35), (hx_+60, hy_+120), (hx_+35, hy_+95), (hx_+15, hy_+130), (hx_-10, hy_+92), (hx_-35, hy_+125), (hx_-60, hy_+110)], '#f7f7f2')

# ---------------- 主渲染 ----------------
def frame(T):
    t, fx, n, ph = remap(T)
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(sf)
    c.save()
    # 鬼畜镜头：每次循环开头猛推，随后回弹
    z = 1.0; foc = (960, 420)
    if fx == 'zoom': z = 1.0+.28*(1-eo(ph*1.6)) if n % 2 == 0 else 1.0+.16*(1-eo(ph*1.6))
    if fx == 'shake': z = 1.12+.1*(n % 2)
    if fx == 'zoomout': z = 1.22-.22*eo(ph)
    if fx == 'mirror': z = 1.1+.12*(1-eo(ph*1.5))
    # 常规轻推镜
    if fx is None:
        if T < 2.5: z = 1.0+.04*ramp(T, .9, 1.2)
        elif T < 5.0: z = 1.0+.08*ramp(T, 3.3, 3.45)
        else: z = 1.0+.05*ramp(T, 5.8, 6.0)
    if T < 2.5: foc = (900, 380)
    elif T < 5.0: foc = (1000, 360)
    else: foc = (960, 330)
    if fx == 'shake' or (3.3 <= T < 3.55):
        c.translate(math.sin(T*97)*18, math.cos(T*83)*14)
    cam_push(c, foc[0], foc[1], z)
    if fx == 'mirror' and n % 2 == 1:
        c.translate(W, 0); c.scale(-1, 1)
    if T < 2.5: S1(c, t, T)
    elif T < 5.0: S2(c, t, T)
    elif T < 7.5: SUB(c, t, T, 1)
    else: SUB(c, t, T, 2)
    c.restore()
    # HUD（不随镜头）
    if T < 2.5: hud_counter(c, T, 3 if T >= 1.0 else 0, 1.0)
    elif T < 5.0: hud_counter(c, T, 30 if T >= 3.35 else 3, 3.35)
    elif T < 7.8: hud_counter(c, T, 300 if T >= 5.85 else 30, 5.85, accent='#ffffff')
    else: hud_counter(c, T, 0, 7.8, slash=True, accent='#5ce1e6')
    SUBS = [[('超市第二件半价，', '#ffffff', .15), ('冲冲冲！', '#ff8a3d', 1.2)],
            [('结账，', '#ffffff', 2.55), ('网卡了？！', '#ff5a5a', 3.05)],
            [('坐个地铁，', '#ffffff', 5.05), ('袋子破了……', '#4dabf7', 5.6)],
            [('原来，', '#ffffff', 7.55), ('根本没人在看我！', '#5ce1e6', 7.95)]]
    idx = 0 if T < 2.5 else 1 if T < 5 else 2 if T < 7.5 else 3
    subtitle(c, T, SUBS[idx])
    sf.flush()
    a = np.ndarray((H, W, 4), np.uint8, sf.get_data())[:, :, :3].copy()  # BGR
    # 后期：RGB 错位 / 闪色（鬼畜循环开头 2 帧）
    if fx and ph*{'zoom': .28, 'shake': .3, 'zoomout': .3, 'mirror': .22}[fx] < 2/FPS:
        a[:, :, 2] = np.roll(a[:, :, 2], 18, axis=1); a[:, :, 0] = np.roll(a[:, :, 0], -18, axis=1)
        if fx == 'shake': a = np.clip(a.astype(np.int16)+np.array([-40, -40, 70], np.int16), 0, 255).astype(np.uint8)
        if fx == 'mirror' and n % 2: a = 255-a
    # 切镜白闪
    for tc in (2.5, 5.0):
        if tc <= T < tc+2/FPS: a = (a.astype(np.uint16)+255)//2
    return a[:, :, ::-1].tobytes()

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'silent.mp4'
    if len(sys.argv) > 2:  # 单帧预览
        from PIL import Image
        for tt in sys.argv[2:]:
            Image.frombytes('RGB', (W, H), frame(float(tt))).save(f'{out}_{tt}.png')
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
    for i in range(int(DUR*FPS)):
        p.stdin.write(frame(i/FPS))
    p.stdin.close(); p.wait()
