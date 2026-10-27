"""纸雕人物：中等比例（头≈身高1/5.5），矿物色纸片拼成，关节处一颗金铆钉（皮影的血脉），
3/4 侧脸，五官用墨线+朱砂点，衣服上有镂空纹样。"""
from zd import *


def seg_quad(L, x0, y0, x1, y1, w0, w1, col):
    a = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(a), math.cos(a)
    pts = [(x0 + nx * w0, y0 + ny * w0)]
    pts += [(x1 + nx * w1, y1 + ny * w1)] + ellipse_pts(x1, y1, w1, w1, 10, a - math.pi / 2, a + math.pi / 2)[1:-1][::1]
    pts += [(x1 - nx * w1, y1 - ny * w1), (x0 - nx * w0, y0 - ny * w0)]
    pts += ellipse_pts(x0, y0, w0, w0, 10, a + math.pi / 2, a + 3 * math.pi / 2)[1:-1]
    L.poly(pts, col, 0.7)


def rivet(L, x, y, r=4.5):
    L.ell(x, y, r, r, P['jin'], amp=0.2); L.ell(x - 1, y - 1, r * 0.4, r * 0.4, P['jin2'], amp=0.1)


def arm(L, sx, sy, a1, a2, l1, l2, col, w=15, hand=P['skin'], cuff=None, hold=None):
    ex, ey = sx + l1 * math.sin(a1), sy + l1 * math.cos(a1)
    hx, hy = ex + l2 * math.sin(a1 + a2), ey + l2 * math.cos(a1 + a2)
    seg_quad(L, sx, sy, ex, ey, w, w * 0.9, col)
    seg_quad(L, ex, ey, hx, hy, w * 0.9, w * 1.15, col)   # 袖口略放
    if cuff: seg_quad(L, ex + (hx - ex) * 0.8, ey + (hy - ey) * 0.8, hx, hy, w * 1.1, w * 1.2, cuff)
    if hold: hold(L, hx, hy, a1 + a2)
    L.ell(hx + 3 * math.sin(a1 + a2), hy + 3 * math.cos(a1 + a2), 9, 9, hand, amp=0.4)
    rivet(L, sx, sy); rivet(L, ex, ey, 3.5)
    return hx, hy


def cloud_holes(cx, cy, r):
    """如意云头镂空"""
    hs = []
    for k in range(3):
        a = -math.pi / 2 + (k - 1) * 0.9
        hs.append(ellipse_pts(cx + r * 0.9 * math.cos(a), cy + r * 0.9 * math.sin(a) + r * 0.6, r * 0.42, r * 0.42, 12))
    return hs


def head(L, x, y, r, hat=None, skin=P['skin'], beard=None, expr='calm', hair=P['mo']):
    """3/4 右向侧脸：脸型+鼻尖+耳；五官极简。expr: calm / angry / shock / smile / sad"""
    face = []
    for i in range(30):
        a = 2 * math.pi * i / 30
        rx = r * (1.0 if math.cos(a) > 0 else 0.92); ry = r * 1.15
        px, py = x + rx * math.cos(a), y + ry * math.sin(a)
        if 0.15 < a < 0.5: px += r * 0.12   # 鼻尖
        if 0.6 < a < 1.2: py += r * 0.05; px -= r * 0.02  # 下巴
        face.append((px, py))
    L.ell(x - r * 0.62, y + r * 0.1, r * 0.2, r * 0.28, P['skin2'])
    L.poly(face, skin, 0.6)
    if hair:
        L.poly(ellipse_pts(x - r * 0.15, y - r * 0.35, r * 0.98, r * 0.85, 24, math.pi * 0.85, math.pi * 2.08), hair, 0.8)
    ex, ey = x + r * 0.42, y - r * 0.05
    if expr == 'shock':
        L.ell(ex, ey, r * 0.16, r * 0.19, P['bai']); L.ell(ex + 1, ey, r * 0.07, r * 0.07, P['mo'])
        L.ell(x + r * 0.48, y + r * 0.62, r * 0.09, r * 0.12, P['mo2'])
    else:
        if expr == 'smile':
            L.curve([(ex - r * 0.16, ey + 2), (ex - r * 0.05, ey - r * 0.12), (ex + r * 0.06, ey - r * 0.12), (ex + r * 0.17, ey + 2)], P['mo'], 3.5)
        elif expr == 'sad':
            L.line([(ex - r * 0.14, ey - 2), (ex + r * 0.14, ey + 4)], P['mo'], 4)
        else:
            L.poly([(ex - r * 0.15, ey), (ex, ey - r * 0.07), (ex + r * 0.16, ey + 1), (ex, ey + r * 0.06)], P['mo'], 0.3)
        mo = (x + r * 0.5, y + r * 0.6)
        if expr == 'smile': L.curve([(mo[0] - 10, mo[1] - 3), (mo[0] - 4, mo[1] + 6), (mo[0] + 4, mo[1] + 6), (mo[0] + 8, mo[1] - 4)], P['zhu2'], 3.5)
        else: L.line([(mo[0] - 8, mo[1]), (mo[0] + 6, mo[1] + (3 if expr == 'sad' else 0))], P['zhu2'], 3.5)
    b = {'angry': [(ex - r * 0.2, ey - r * 0.32), (ex + r * 0.2, ey - r * 0.16)], 'sad': [(ex - r * 0.2, ey - r * 0.2), (ex + r * 0.2, ey - r * 0.32)],
         'shock': [(ex - r * 0.2, ey - r * 0.42), (ex + r * 0.2, ey - r * 0.44)]}.get(expr, [(ex - r * 0.2, ey - r * 0.27), (ex + r * 0.2, ey - r * 0.27)])
    L.line(b, P['mo'], 6)
    L.ell(x + r * 0.28, y + r * 0.32, r * 0.13, r * 0.08, (0.85, 0.45, 0.4, 0.55), amp=0.2)   # 胭脂
    if beard == 'long':
        L.poly([(x + r * 0.15, y + r * 0.75), (x + r * 0.7, y + r * 0.7), (x + r * 0.55, y + r * 2.0), (x + r * 0.3, y + r * 1.7)], P['mo'], 1.2)
    elif beard == 'short':
        L.poly([(x + r * 0.1, y + r * 0.72), (x + r * 0.72, y + r * 0.66), (x + r * 0.62, y + r * 1.15), (x + r * 0.15, y + r * 1.0)], P['mo2'], 1.0)
        L.line([(x + r * 0.35, y + r * 0.5), (x + r * 0.75, y + r * 0.42)], P['mo'], 4)
    if hat: hat(L, x, y, r)


# ---------------------------------------------------------------- 帽冠
def hat_futou(L, x, y, r, wings=False):
    L.poly(ellipse_pts(x - r * 0.05, y - r * 0.55, r * 0.98, r * 0.75, 20, math.pi * 0.95, math.pi * 2.05), P['mo'], 0.6)
    L.poly([(x - r * 0.45, y - r * 1.05), (x + r * 0.2, y - r * 1.12), (x + r * 0.15, y - r * 1.55), (x - r * 0.4, y - r * 1.5)], P['mo'], 0.6)
    if wings:
        L.poly([(x - r * 0.6, y - r * 0.85), (x - r * 2.3, y - r * 1.0), (x - r * 2.3, y - r * 0.85), (x - r * 0.6, y - r * 0.68)], P['mo'], 0.4)
    else:
        L.poly([(x - r * 0.8, y - r * 0.6), (x - r * 1.5, y + r * 0.9), (x - r * 1.3, y + r * 0.95), (x - r * 0.68, y - r * 0.45)], P['mo'], 0.6)

def hat_crown(L, x, y, r):   # 帝王通天冠 + 金簪
    L.poly(ellipse_pts(x - r * 0.05, y - r * 0.5, r * 0.98, r * 0.72, 20, math.pi * 0.95, math.pi * 2.05), P['mo'], 0.6)
    L.poly([(x - r * 0.6, y - r * 0.95), (x + r * 0.5, y - r * 1.0), (x + r * 0.62, y - r * 1.75), (x - r * 0.5, y - r * 1.8)], P['huang'],
           0.6, holes=[ellipse_pts(x, y - r * 1.38, r * 0.17, r * 0.17, 12)])
    L.line([(x - r * 1.1, y - r * 1.1), (x + r * 1.1, y - r * 1.15)], P['jin'], 5)
    L.ell(x + r * 1.15, y - r * 1.15, 6, 6, P['zhu'])

def hat_helmet(L, x, y, r, plume=P['zhu']):
    L.poly(ellipse_pts(x, y - r * 0.25, r * 1.08, r * 1.0, 22, math.pi * 0.98, math.pi * 2.02), P['tie'], 0.6)
    L.poly([(x - r * 1.05, y - r * 0.3), (x - r * 1.25, y + r * 0.7), (x - r * 0.6, y + r * 0.6), (x - r * 0.5, y - r * 0.2)], P['tie2'], 0.6)
    L.poly([(x - r * 0.1, y - r * 1.2), (x + r * 0.1, y - r * 1.2), (x + r * 0.05, y - r * 1.55), (x - r * 0.05, y - r * 1.55)], P['jin'], 0.3)
    L.poly([(x, y - r * 1.5), (x - r * 0.9, y - r * 2.2), (x - r * 0.5, y - r * 1.5), (x - r * 1.1, y - r * 1.7), (x - r * 0.2, y - r * 1.3)], plume, 1.0)
    L.line([(x - r * 0.9, y - r * 0.32), (x + r * 1.02, y - r * 0.32)], P['jin'], 3)

def hat_bun(L, x, y, r):   # 女子高髻 + 步摇
    L.ell(x - r * 0.15, y - r * 1.25, r * 0.55, r * 0.5, P['mo'])
    L.ell(x - r * 0.65, y - r * 1.05, r * 0.38, r * 0.35, P['mo'])
    L.line([(x - r * 0.9, y - r * 1.35), (x + r * 0.6, y - r * 1.5)], P['jin'], 4)
    for k in range(3): L.line([(x + r * 0.55, y - r * 1.5), (x + r * 0.6 + k * 4, y - r * 1.0 + k * 6)], P['jin'], 2); L.ell(x + r * 0.6 + k * 4, y - r * 0.98 + k * 6, 4, 4, P['zhu'])
    L.ell(x + r * 0.05, y - r * 1.55, r * 0.14, r * 0.14, P['zhu'])


# ---------------------------------------------------------------- 道具
def spear(L, hx, hy, a, length=330):
    dx, dy = math.sin(a - 0.0), math.cos(a)
    L.line([(hx - 0 * dx, hy + 140), (hx, hy - length)], P['zhe2'], 5)
    L.poly([(hx - 7, hy - length), (hx, hy - length - 44), (hx + 7, hy - length)], P['tie'], 0.4)
    L.poly([(hx - 10, hy - length + 4), (hx - 18, hy - length + 30), (hx, hy - length + 14), (hx + 18, hy - length + 30), (hx + 10, hy - length + 4)], P['zhu'], 0.6)

def sword(L, hx, hy, a, length=150):
    ex, ey = hx + length * math.sin(a), hy + length * math.cos(a)
    L.line([(hx, hy), (ex, ey)], P['bai'], 6); L.line([(hx, hy), (hx + 22 * math.sin(a), hy + 22 * math.cos(a))], P['mo'], 7)
    L.line([(hx - 12 * math.cos(a), hy + 12 * math.sin(a)), (hx + 12 * math.cos(a), hy - 12 * math.sin(a))], P['jin'], 5)

def tablet(L, hx, hy, a):  # 笏板
    L.poly([(hx - 6, hy + 10), (hx + 6, hy + 10), (hx + 9, hy - 60), (hx - 3, hy - 62)], P['bai'], 0.4)

def scroll(L, hx, hy, a):
    L.poly([(hx - 10, hy - 50), (hx + 70, hy - 54), (hx + 72, hy + 40), (hx - 8, hy + 44)], P['xuan2'], 0.6)
    for k in range(4): L.line([(hx + 10 + k * 15, hy - 40), (hx + 10 + k * 15, hy + 30)], P['mo'], 2, 0.6)
    L.line([(hx - 12, hy - 54), (hx - 12, hy + 48)], P['zhe2'], 7); L.line([(hx + 74, hy - 58), (hx + 74, hy + 44)], P['zhe2'], 7)


# ---------------------------------------------------------------- 角色
ROLE = {
    'emperor': dict(robe=P['huang'], robe2=P['zhe'], sleeve=P['huang'], cuff=P['zhu'], hat=hat_crown, beard='short', belt=P['zhu'], pattern=True),
    'general': dict(robe=P['zhu2'], robe2=P['zhu'], sleeve=P['tie'], cuff=P['tie2'], hat=hat_helmet, beard='short', belt=P['jin'], armor=True),
    'official': dict(robe=P['qing'], robe2=P['qing2'], sleeve=P['qing'], cuff=P['qing2'], hat=lambda L, x, y, r: hat_futou(L, x, y, r, True), beard='long', belt=P['jin']),
    'lady': dict(robe=P['zhu'], robe2=P['zhu2'], sleeve=P['lv'], cuff=P['bai'], hat=hat_bun, beard=None, belt=P['jin'], lady=True),
    'soldier': dict(robe=P['lv2'], robe2=P['lv'], sleeve=P['tie'], cuff=P['tie2'], hat=lambda L, x, y, r: hat_helmet(L, x, y, r, P['zhu']), beard=None, belt=P['zhe2'], armor=True),
    'enemy': dict(robe=P['zi'], robe2=P['mo2'], sleeve=P['tie2'], cuff=P['mo2'], hat=lambda L, x, y, r: hat_helmet(L, x, y, r, P['qing']), beard='short', belt=P['zhe2'], armor=True),
    'farmer': dict(robe=P['zhe'], robe2=P['zhe2'], sleeve=P['zhe'], cuff=P['xuan3'], hat=lambda L, x, y, r: L.poly([(x - r * 1.6, y - r * 0.55), (x, y - r * 1.5), (x + r * 1.6, y - r * 0.55)], P['huang'], 0.8), beard=None, belt=P['mo2']),
}


def person(L, x, y, s=1.0, role='official', face=1, armB=(0.25, -0.3), armF=(-0.15, -0.6), lean=0.0, step=0.0,
           holdF=None, holdB=None, expr='calm'):
    """脚底中心 (x,y)，身高约 420*s。arm=(上臂角, 前臂相对角)，弧度，0=下垂，正=向前"""
    R = ROLE[role]; c = L.c; c.save(); c.translate(x, y); c.scale(face * s, s); c.rotate(lean)
    hr = 38  # 头半径；身高≈420 → 头≈1/5.5
    sy = -300  # 肩
    # 后臂
    arm(L, -6, sy + 8, armB[0], armB[1], 92, 88, R['robe2'] if not R.get('armor') else R['cuff'], 14, cuff=R['cuff'], hold=holdB)
    # 腿/靴
    for k, sgn in ((0, -1), (1, 1)):
        off = sgn * step * 40
        L.poly([(-14 + off * 0.3 + k * 16, -120), (2 + off * 0.3 + k * 16, -120), (6 + off + k * 12, -6), (30 + off + k * 12, 0), (-12 + off + k * 12, 0), (-12 + off + k * 12, -6)], P['mo2'], 0.6)
    # 袍
    if R.get('lady'):
        L.poly([(-30, sy + 40), (34, sy + 40), (78, -4), (-70, -4)], R['robe'], 1.0, holes=cloud_holes(4, -70, 22))
        L.poly([(-32, sy + 4), (36, sy + 4), (40, sy + 52), (-36, sy + 52)], R['sleeve'], 0.8)
        L.poly([(-36, sy + 44), (40, sy + 44), (40, sy + 56), (-36, sy + 56)], R['belt'], 0.4)
        L.curve([(-30, sy + 10), (-90, sy + 90), (-80, sy + 200), (-60, -60)], P['bai'], 7, 0.95)   # 披帛
        L.curve([(30, sy + 12), (70, sy + 100), (60, sy + 190), (90, -80)], P['bai'], 7, 0.95)
    else:
        holes = cloud_holes(6, -150, 26) if R.get('pattern') else []
        L.poly([(-36, sy), (40, sy), (52, sy + 120), (66, -18), (-60, -18), (-48, sy + 120)], R['robe'], 1.0, holes=holes)
        L.poly([(8, sy + 8), (22, sy + 4), (30, -20), (12, -20)], R['robe2'], 0.6)   # 前襟
        if R.get('armor'):
            L.poly([(-40, sy + 6), (44, sy + 6), (48, sy + 150), (-46, sy + 150)], P['tie'], 0.8)
            for yy in range(sy + 22, sy + 150, 16):
                for xx in range(-38, 44, 16): L.curve([(xx, yy), (xx + 4, yy + 8), (xx + 12, yy + 8), (xx + 16, yy)], P['tie2'], 2)
            L.ell(0, sy + 60, 18, 18, P['jin'], holes=[ellipse_pts(0, sy + 60, 8, 8, 10)])   # 护心镜
            L.poly([(-48, sy), (-70, sy + 30), (-30, sy + 34)], P['tie2'], 0.5); L.poly([(46, sy), (70, sy + 30), (30, sy + 34)], P['tie2'], 0.5)
        L.poly([(-50, sy + 140), (54, sy + 140), (54, sy + 156), (-50, sy + 156)], R['belt'], 0.4)
        # 圆领
        L.poly(ellipse_pts(4, sy + 2, 26, 12, 16, 0, math.pi), R['robe2'], 0.4)
    # 脖子+头
    L.poly([(-8, sy - 2), (14, sy - 2), (12, sy - 30), (-6, sy - 30)], P['skin2'], 0.4)
    head(L, 6, sy - 30 - hr * 1.0, hr, hat=R['hat'], beard=R['beard'], expr=expr, hair=P['mo'] if role in ('lady', 'farmer') else None)
    # 前臂
    arm(L, 8, sy + 12, armF[0], armF[1], 92, 88, R['sleeve'], 15, cuff=R['cuff'], hold=holdF)
    c.restore()
