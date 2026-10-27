"""水浒·林冲 —— 纸雕山河造型。豹头环眼、燕颔虎须、白毡笠、脸上金印、花枪挑酒葫芦、石青披风。"""
from people import *


def lin_head(L, x, y, r, expr='angry'):
    # 宽下颌（燕颔）的脸
    face = []
    for i in range(36):
        a = 2 * math.pi * i / 36
        rx = r * (1.05 if math.cos(a) > 0 else 0.95); ry = r * 1.1
        px, py = x + rx * math.cos(a), y + ry * math.sin(a)
        if 0.12 < a < 0.45: px += r * 0.14           # 鼻
        if 0.5 < a < 1.6: px += r * 0.08; py += r * 0.06   # 方下颌
        face.append((px, py))
    L.ell(x - r * 0.62, y + r * 0.08, r * 0.2, r * 0.28, P['skin2'])
    L.poly(face, P['skin'], 0.6)
    # 金印（刺配的面印）
    L.poly([(x - r * 0.05, y + r * 0.25), (x + r * 0.18, y + r * 0.23), (x + r * 0.19, y + r * 0.5), (x - r * 0.04, y + r * 0.52)], P['jin'], 0.3)
    # 环眼
    ex, ey = x + r * 0.45, y - r * 0.08
    L.ell(ex, ey, r * 0.2, r * 0.2, P['bai'], amp=0.3)
    L.ell(ex + r * 0.05, ey + 1, r * 0.1, r * 0.1, P['mo'], amp=0.2)
    L.ell(ex + r * 0.02, ey - r * 0.03, r * 0.03, r * 0.03, P['bai'], amp=0.05)
    # 浓眉，压成一道怒势
    b = [(ex - r * 0.32, ey - r * 0.38), (ex + r * 0.28, ey - r * 0.18)] if expr == 'angry' else [(ex - r * 0.3, ey - r * 0.32), (ex + r * 0.28, ey - r * 0.3)]
    L.poly([b[0], b[1], (b[1][0] + 2, b[1][1] + 10), (b[0][0], b[0][1] + 13)], P['mo'], 0.5)
    # 虎须：下颌一圈短而硬的须
    pts = [(x - r * 0.15, y + r * 0.55)]
    for k in range(9):
        u = k / 8; bx = x - r * 0.15 + r * 0.95 * u; by = y + r * (0.62 + 0.45 * math.sin(u * math.pi))
        pts.append((bx + r * 0.05, by + (r * 0.32 if k % 2 else 0)))
    pts += [(x + r * 0.85, y + r * 0.5), (x + r * 0.55, y + r * 0.62), (x + r * 0.3, y + r * 0.66)]
    L.poly(pts, P['mo'], 0.8)
    L.poly([(x + r * 0.3, y + r * 0.45), (x + r * 0.85, y + r * 0.36), (x + r * 0.9, y + r * 0.5), (x + r * 0.32, y + r * 0.56)], P['mo'], 0.5)  # 髭
    L.line([(x + r * 0.5, y + r * 0.66), (x + r * 0.78, y + r * 0.64)], P['zhu2'], 4)   # 抿嘴
    # 鬓发
    L.poly(ellipse_pts(x - r * 0.2, y - r * 0.3, r * 0.92, r * 0.85, 20, math.pi * 0.8, math.pi * 1.6), P['mo'], 0.8)
    # 白范阳毡笠 + 红缨
    L.poly([(x - r * 1.75, y - r * 0.55), (x - r * 0.6, y - r * 0.85), (x + r * 0.7, y - r * 0.85), (x + r * 1.85, y - r * 0.5),
            (x + r * 1.7, y - r * 0.35), (x - r * 1.6, y - r * 0.38)], P['bai'], 1.0)
    L.poly(ellipse_pts(x, y - r * 0.85, r * 0.72, r * 0.85, 20, math.pi, 2 * math.pi), P['bai'], 0.8)
    L.line([(x - r * 0.7, y - r * 0.9), (x + r * 0.72, y - r * 0.92)], P['zhe2'], 4, 0.7)
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.32
        L.poly([(x + r * 0.05 * (k - 3), y - r * 1.6), (x + r * 1.0 * math.cos(a), y - r * 1.65 + r * 1.0 * math.sin(a) * 0.4 + r * 0.9),
                (x + r * 1.0 * math.cos(a) + 6, y - r * 1.6 + r * 0.9)], P['zhu'], 0.6)
    L.ell(x, y - r * 1.68, r * 0.16, r * 0.16, P['jin'])
    # 笠带
    L.line([(x - r * 0.62, y - r * 0.3), (x - r * 0.5, y + r * 0.7)], P['zhe2'], 2.5, 0.6)


def flower_spear(L, hx, hy, a, length=520, gourd=True, wind=0.0):
    """花枪斜扛：从手处沿角度 a（0=向上）延伸"""
    dx, dy = math.sin(a), -math.cos(a)
    tail = (hx - dx * 170, hy - dy * 170); tip = (hx + dx * length, hy + dy * length)
    L.line([tail, tip], P['zhe2'], 12)
    L.line([tail, tip], P['zhe'], 4, 0.6)
    nx, ny = -dy, dx
    L.poly([(tip[0] + nx * 9, tip[1] + ny * 9), (tip[0] + dx * 70, tip[1] + dy * 70), (tip[0] - nx * 9, tip[1] - ny * 9)], P['tie'], 0.4)
    L.poly([(tip[0] + nx * 4, tip[1] + ny * 4), (tip[0] + dx * 60, tip[1] + dy * 60), (tip[0] - nx * 1, tip[1] - ny * 1)], P['bai'], 0.2)
    # 红缨，被风吹向左
    for k in range(6):
        L.poly([(tip[0], tip[1]), (tip[0] - 70 - k * 8 + wind, tip[1] + 18 + k * 9), (tip[0] - 40 - k * 6 + wind, tip[1] + 30 + k * 7)], P['zhu'] if k % 2 else P['zhu2'], 0.8)
    if gourd:   # 酒葫芦挂在枪杆上
        gx, gy = hx + dx * (length - 110), hy + dy * (length - 110)
        L.line([(gx, gy), (gx - 6, gy + 50)], P['mo2'], 3)
        L.ell(gx - 6, gy + 66, 16, 16, P['huang']); L.ell(gx - 6, gy + 104, 26, 28, P['huang'])
        L.poly([(gx - 22, gy + 84), (gx + 10, gy + 84), (gx + 10, gy + 90), (gx - 22, gy + 90)], P['zhu'], 0.3)


def linchong(L, x, y, s=1.0, wind=0.0, expr='angry'):
    c = L.c; c.save(); c.translate(x, y); c.scale(s, s)
    sy = -330; hr = 42
    # 披风（石青，被北风吹向左后方）
    cape = [(-40, sy), (30, sy)]
    for i in range(8):
        u = i / 7
        cape.append((-60 - 220 * u - wind * u, sy + 30 + 300 * u + 25 * math.sin(u * 7 + wind * 0.05)))
    cape += [(-150 - wind * 0.4, sy + 360), (-60, sy + 260)]
    L.poly(cape, P['qing2'], 1.6)
    L.poly([(-40, sy + 10), (-120 - wind * 0.3, sy + 160), (-90, sy + 180), (-30, sy + 60)], P['qing'], 1.0)
    # 后臂扯住披风
    arm(L, -8, sy + 10, -0.35, 0.5, 100, 92, P['mo2'], 16, cuff=P['bai'])
    # 腿：弓步，绑腿白
    for (fx, kx, col) in ((-62, -40, P['mo2']), (58, 34, P['mo'])):
        L.poly([(kx - 22, -150), (kx + 18, -150), (fx + 16, -20), (fx - 18, -20)], col, 0.8)
        L.poly([(kx - 16 + (fx - kx) * 0.45, -110), (kx + 16 + (fx - kx) * 0.45, -110), (fx + 15, -30), (fx - 16, -30)], P['bai'], 0.6)
        for k in range(4):
            yy = -100 + k * 18; xx = kx + (fx - kx) * (0.5 + k * 0.12)
            L.line([(xx - 16, yy), (xx + 16, yy + 8)], P['xuan3'], 2)
        L.poly([(fx - 22, -24), (fx + 22, -24), (fx + 44, 0), (fx - 24, 0)], P['mo'], 0.6)
    # 皂色短打 + 朱红腰带
    L.poly([(-46, sy), (50, sy), (62, sy + 150), (74, -130), (-70, -130), (-56, sy + 150)], P['mo2'], 1.0)
    L.poly([(4, sy + 6), (26, sy + 2), (6, sy + 120), (-12, sy + 118)], P['xuan3'], 0.5)   # 交领白里
    L.poly([(-62, sy + 150), (66, sy + 150), (66, sy + 176), (-62, sy + 176)], P['zhu'], 0.6)
    L.poly([(30, sy + 170), (52, sy + 168), (70, sy + 260), (46, sy + 262)], P['zhu2'], 0.6)   # 带梢
    L.poly([(-70, -130), (74, -130), (80, -110), (-74, -110)], P['qing2'], 0.5)
    # 脖子+头
    L.poly([(-10, sy - 2), (16, sy - 2), (14, sy - 34), (-8, sy - 34)], P['skin2'], 0.4)
    lin_head(L, 8, sy - 34 - hr, hr, expr)
    # 前臂握枪于肩前，枪斜指右上
    hx, hy = arm(L, 12, sy + 14, 0.9, -2.1, 98, 90, P['mo2'], 17, cuff=P['bai'])
    c.restore()
    return x + hx * s, y + hy * s


def draw_spear_for(L, x, y, s, wind=0.0):
    """枪画在人物前一层，避免被身体挡住"""
    c = L.c; c.save(); c.translate(x, y); c.scale(s, s)
    sy = -330
    ex, ey = 12 + 98 * math.sin(0.9), sy + 14 + 98 * math.cos(0.9)
    hx, hy = ex + 90 * math.sin(-1.2), ey + 90 * math.cos(-1.2)
    flower_spear(L, hx, hy, 0.5, 440, True, wind)
    L.ell(hx + 2, hy + 2, 11, 11, P['skin'], amp=0.4)
    c.restore()
