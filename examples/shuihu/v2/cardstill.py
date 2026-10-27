"""彩色酷炫英雄卡剧照：正面 / 背面"""
import sys, math, random
from chars import *
from bgs import *
import cairocffi as cairo
from PIL import Image

RAINBOW = ['#38f2ff', '#5b7cff', '#c45bff', '#ff4fa3', '#ffb443', '#fff07a', '#5bffb0', '#38f2ff']

def rgba(h, a=1.0): return hx(h, a)

def rrect_path(c, x, y, w, h, r):
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -1.5708, 0); c.arc(x + w - r, y + h - r, r, 0, 1.5708)
    c.arc(x + r, y + h - r, r, 1.5708, 3.1416); c.arc(x + r, y + r, r, 3.1416, 4.7124); c.close_path()

def lin_grad(x0, y0, x1, y1, cols, a=1.0, shift=0.0):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    n = len(cols) - 1
    for i, col in enumerate(cols): g.add_color_stop_rgba((i / n + shift) % 1.0001 if shift else i / n, *rgba(col, a))
    return g

def grad_text(c, txt, x, y, size, cols, anchor='c', outline='#0b0716', ow=None, vertical=True):
    c.select_font_face("Noto Serif CJK SC", 0, 1); c.set_font_size(size)
    e = c.text_extents(txt); dx = {'c': e[4] / 2, 'l': 0, 'r': e[4]}[anchor]
    c.move_to(x - dx, y); c.text_path(txt)
    c.set_source_rgba(*rgba(outline)); c.set_line_width(ow or size * 0.18); c.stroke_preserve()
    if vertical: c.set_source(lin_grad(0, y - size, 0, y + size * 0.15, cols))
    else: c.set_source(lin_grad(x - dx, 0, x - dx + e[4], 0, cols))
    c.fill()
    return e[4]

def hexagon(c, x, y, r, rot=0.0):
    for i in range(6):
        a = rot + i * math.pi / 3; (c.move_to if i == 0 else c.line_to)(x + r * math.cos(a), y + r * math.sin(a))
    c.close_path()

def background(p, g, t):
    c = p.c
    c.set_source(lin_grad(0, STAGE_T, 0, STAGE_B, ['#07051a', '#1d0f3d', '#3a0f3a', '#120a24']))
    c.rectangle(0, STAGE_T, W, SH); c.fill()
    cx, cy = 540, 520
    for k in range(48):  # 彩色放射光
        a = k / 48 * 6.2832 + t * 0.05; a2 = a + 0.045
        col = RAINBOW[k % 7]
        p.poly([(cx, cy), (cx + 1400 * math.cos(a), cy + 1400 * math.sin(a)), (cx + 1400 * math.cos(a2), cy + 1400 * math.sin(a2))], col, a=0.10)
    p.radial(cx, cy, 620, '#ff4fa3', 0.35, 0); p.radial(cx, cy, 420, '#ffb443', 0.35, 0)
    for i in range(6): g.ring(cx, cy, 470 + i * 34, RAINBOW[i], 2.5, 0.35)
    rnd = random.Random(9)
    for i in range(110):  # 雪 + 彩色光粒
        x, y = rnd.uniform(0, W), rnd.uniform(STAGE_T, STAGE_B)
        if i % 3: p.ell(x, y, 2.4, 2.4, 'SNOW', a=0.7)
        else: g.ell(x, y, 3.5, 3.5, RAINBOW[i % 7], a=0.9)
    for i in range(14):
        x, y = rnd.uniform(40, W - 40), rnd.uniform(STAGE_T + 30, STAGE_B - 30); star(g, x, y, rnd.uniform(8, 18), RAINBOW[i % 7], 0.9)

def card_shell(p, g, cw, ch, theme):
    c = p.c
    # 投影 + 外发光
    rrect_path(c, -cw + 16, -ch + 22, 2 * cw, 2 * ch, 34); c.set_source_rgba(0, 0, 0, 0.55); c.fill()
    rrect_path(g.c, -cw - 14, -ch - 14, 2 * cw + 28, 2 * ch + 28, 40); g.c.set_source(lin_grad(-cw, -ch, cw, ch, RAINBOW, 0.8)); g.c.set_line_width(14); g.c.stroke()
    # 镭射彩虹边框
    rrect_path(c, -cw - 12, -ch - 12, 2 * cw + 24, 2 * ch + 24, 40); c.set_source(lin_grad(-cw, -ch, cw, ch, RAINBOW)); c.fill()
    rrect_path(c, -cw - 4, -ch - 4, 2 * cw + 8, 2 * ch + 8, 34); c.set_source(lin_grad(-cw, ch, cw, -ch, ['#fff3c4', '#d79a2b', '#fff3c4', '#a8701c', '#fff3c4'])); c.fill()
    # 卡面主色渐变
    rrect_path(c, -cw + 6, -ch + 6, 2 * cw - 12, 2 * ch - 12, 30); c.set_source(lin_grad(0, -ch, 0, ch, theme)); c.fill()
    # 四角金饰
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (cw - 30), sy * (ch - 30)
            c.move_to(x, y - sy * 0); hexagon(c, x, y, 16, 0.52); c.set_source(lin_grad(x - 16, y - 16, x + 16, y + 16, ['#fff3c4', '#d79a2b'])); c.fill()
            hexagon(c, x, y, 8, 0.52); c.set_source_rgba(*rgba('#ff4fa3')); c.fill()
            g.ell(x, y, 10, 10, '#ff8fd0', a=0.8)

def holo(p, cw, ch, t, band_x):
    c = p.c; c.save(); rrect_path(c, -cw + 6, -ch + 6, 2 * cw - 12, 2 * ch - 12, 30); c.clip()
    c.set_line_width(2)  # 细斜纹镭射
    for i in range(-60, 60):
        x = i * 18; c.move_to(x - ch, -ch); c.line_to(x + ch, ch)
        c.set_source_rgba(*rgba(RAINBOW[i % 7], 0.045)); c.stroke()
    g_ = cairo.LinearGradient(band_x - 160, -ch, band_x + 160, ch)  # 斜向闪光带
    for s_, a_ in [(0, 0), (0.42, 0.0), (0.5, 0.42), (0.58, 0.0), (1, 0)]: g_.add_color_stop_rgba(s_, 1, 1, 1, a_)
    c.set_source(g_); c.paint()
    g2 = cairo.LinearGradient(band_x - 260, -ch, band_x + 260, ch)
    for s_, col in zip([0, .3, .45, .55, .7, 1], ['#000000', '#38f2ff', '#c45bff', '#ff4fa3', '#ffb443', '#000000']):
        cc = rgba(col); g2.add_color_stop_rgba(s_, cc[0], cc[1], cc[2], 0.18 if 0 < s_ < 1 else 0)
    c.set_source(g2); c.paint()
    c.restore()

def front(p, g, t):
    cw, ch = 300, 438
    c = p.c
    c.save(); g.c.save(); c.translate(540, 520); g.c.translate(540, 520); c.rotate(-0.035); g.c.rotate(-0.035)
    card_shell(p, g, cw, ch, ['#123a7a', '#1d5fa8', '#3a1f6e', '#140a2a'])
    # 画框
    ax0, ay0, aw, ah = -cw + 28, -ch + 96, 2 * cw - 56, 560
    c.save(); rrect_path(c, ax0, ay0, aw, ah, 18); c.clip()
    c.set_source(lin_grad(0, ay0, 0, ay0 + ah, ['#0e1c4a', '#3d2a7a', '#c8467a', '#ff9a3c'])); c.paint()
    for k in range(5): p.ring(0, ay0 + 230, 150 + k * 26, RAINBOW[k + 1], 3, 0.45)
    p.radial(0, ay0 + 230, 260, '#ffd27a', 0.6, 0)
    p.ell(0, ay0 + 230, 150, 150, '#ffcf7a'); p.ell(0, ay0 + 230, 135, 135, '#ffe2a8')
    # 远山剪影 + 雪
    pts = [(ax0, ay0 + ah)]
    for i in range(9): pts.append((ax0 + i * aw / 8, ay0 + ah - 120 - (60 if i % 2 else 0) - (i % 3) * 18))
    pts.append((ax0 + aw, ay0 + ah)); p.poly(pts, '#1a0f2e')
    p.rect(ax0, ay0 + ah - 70, aw, 70, '#0d0818')
    rnd = random.Random(4)
    for i in range(45): p.ell(ax0 + rnd.uniform(0, aw), ay0 + rnd.uniform(0, ah), 2.5, 2.5, 'SNOW', a=0.85)
    figure(p, g, 10, ay0 + ah - 64, 0.98, 1, 'guard', 'lin', t=0.4, wind=0.6)
    impact(p, g, 215, ay0 + 228, 0.12, 0.0, 0.42, col='#9ff6ff')
    c.restore()
    rrect_path(c, ax0, ay0, aw, ah, 18); c.set_source(lin_grad(ax0, ay0, ax0 + aw, ay0 + ah, ['#fff3c4', '#d79a2b', '#fff3c4'])); c.set_line_width(5); c.stroke()
    # 顶栏：星位徽章 + SSR
    hexagon(c, -cw + 74, -ch + 52, 40, 0.52); c.set_source(lin_grad(0, -ch + 12, 0, -ch + 92, ['#fff3c4', '#d79a2b'])); c.fill()
    hexagon(c, -cw + 74, -ch + 52, 32, 0.52); c.set_source_rgba(*rgba('#140a2a')); c.fill()
    g.ring(-cw + 74, -ch + 52, 38, '#38f2ff', 4, 0.6)
    grad_text(c, '天雄', -cw + 74, -ch + 62, 26, ['#ffffff', '#ffe08a'], ow=6)
    grad_text(c, '天罡星 · 第六位', 10, -ch + 64, 30, ['#ffffff', '#ffe08a'], ow=6)
    grad_text(c, 'SSR', cw - 100, -ch + 70, 50, ['#38f2ff', '#c45bff', '#ff4fa3', '#ffb443'], ow=9, vertical=False)
    g.text('SSR', cw - 100, -ch + 70, 50, '#ff8fd0', a=0.7)
    # 名牌
    ny = ch - 150
    rrect_path(c, -cw + 28, ny, 2 * cw - 56, 120, 16); c.set_source(lin_grad(-cw, 0, cw, 0, ['#7a0f22', '#d8283a', '#ff5a3c', '#d8283a', '#7a0f22'])); c.fill()
    rrect_path(c, -cw + 28, ny, 2 * cw - 56, 120, 16); c.set_source(lin_grad(-cw, 0, cw, 0, ['#fff3c4', '#d79a2b', '#fff3c4'])); c.set_line_width(4); c.stroke()
    grad_text(c, '豹子头 · 林冲', 0, ny + 70, 60, ['#ffffff', '#ffe08a', '#ffb443'], ow=10)
    for i in range(5): star(p, -100 + i * 50, ny + 102, 11, '#ffe08a'); star(g, -100 + i * 50, ny + 102, 9, '#ffd27a', 0.8)
    holo(p, cw, ch, t, -250)
    c.restore(); g.c.restore()

def radar(p, g, cx, cy, R, vals, labels, cols):
    c = p.c; n = len(vals)
    for k in range(1, 5):
        for i in range(n):
            a = -math.pi / 2 + i * 2 * math.pi / n; r = R * k / 4
            (c.move_to if i == 0 else c.line_to)(cx + r * math.cos(a), cy + r * math.sin(a))
        c.close_path(); c.set_source_rgba(1, 1, 1, 0.18); c.set_line_width(1.5); c.stroke()
    pts = []
    for i, v in enumerate(vals):
        a = -math.pi / 2 + i * 2 * math.pi / n; pts.append((cx + R * v / 100 * math.cos(a), cy + R * v / 100 * math.sin(a)))
        c.move_to(cx, cy); c.line_to(cx + R * math.cos(a), cy + R * math.sin(a)); c.set_source_rgba(1, 1, 1, 0.15); c.stroke()
        lx, ly = cx + (R + 40) * math.cos(a), cy + (R + 40) * math.sin(a) + 10
        grad_text(c, labels[i], lx, ly, 26, ['#ffffff', cols[i]], ow=5)
    for i, (x, y) in enumerate(pts): (c.move_to if i == 0 else c.line_to)(x, y)
    c.close_path()
    rg = cairo.RadialGradient(cx, cy, 0, cx, cy, R)
    for s_, col in [(0, '#ff4fa3'), (0.6, '#c45bff'), (1, '#38f2ff')]: cc = rgba(col); rg.add_color_stop_rgba(s_, cc[0], cc[1], cc[2], 0.6)
    c.set_source(rg); c.fill_preserve(); c.set_source_rgba(*rgba('#9ff6ff')); c.set_line_width(3); c.stroke()
    for (x, y), col in zip(pts, cols): p.ell(x, y, 7, 7, col); g.ell(x, y, 9, 9, col, a=0.9)

def back(p, g, t):
    cw, ch = 300, 438
    c = p.c
    c.save(); g.c.save(); c.translate(540, 520); g.c.translate(540, 520); c.rotate(0.03); g.c.rotate(0.03)
    card_shell(p, g, cw, ch, ['#2a0f4a', '#14205a', '#0c2f4f', '#0a0a22'])
    # 底纹：大号“雄”字水印 + 星图
    c.select_font_face("Noto Serif CJK SC", 0, 1); c.set_font_size(420); c.move_to(-210, 150); c.set_source_rgba(1, 1, 1, 0.04); c.show_text('雄')
    grad_text(c, '豹子头 · 林冲', 0, -ch + 80, 54, ['#ffffff', '#ffe08a', '#ffb443'], ow=9)
    grad_text(c, '马军五虎将 · 前八十万禁军教头', 0, -ch + 122, 22, ['#9ff6ff', '#c9b6ff'], ow=4)
    c.move_to(-cw + 40, -ch + 142); c.line_to(cw - 40, -ch + 142); c.set_source(lin_grad(-cw, 0, cw, 0, RAINBOW)); c.set_line_width(3); c.stroke()
    rows = [('星位', '天雄星', '#38f2ff'), ('兵器', '丈八红缨枪', '#ff4fa3'), ('必杀', '风雪一枪', '#ffb443')]
    for i, (k, v, col) in enumerate(rows):
        y = -ch + 196 + i * 60
        rrect_path(c, -cw + 36, y - 34, 2 * cw - 72, 48, 12); c.set_source(lin_grad(-cw, 0, cw, 0, [col, '#00000000'], 0.35)); c.fill()
        hexagon(c, -cw + 64, y - 10, 15, 0.52); c.set_source_rgba(*rgba(col)); c.fill(); g.ell(-cw + 64, y - 10, 12, 12, col, a=0.8)
        p.text(k, -cw + 92, y, 28, col, 'l'); p.text(v, -cw + 180, y, 30, 'CREAM', 'l')
    radar(p, g, 0, 120, 120, [98, 86, 99, 95, 80], ['枪法', '马术', '忍耐', '爆发', '谋略'], ['#ff4fa3', '#5bffb0', '#38f2ff', '#ffb443', '#c45bff'])
    # 底部彩色数值条
    stats = [('攻', 95, ['#ff3c5a', '#ffb443']), ('防', 88, ['#3c8cff', '#38f2ff']), ('速', 92, ['#7a3cff', '#ff4fa3'])]
    for i, (k, v, cols) in enumerate(stats):
        y = ch - 140 + i * 40
        p.text(k, -cw + 50, y + 10, 26, 'GOLD2')
        rrect_path(c, -cw + 80, y - 10, 2 * cw - 200, 22, 11); c.set_source_rgba(1, 1, 1, 0.12); c.fill()
        rrect_path(c, -cw + 80, y - 10, (2 * cw - 200) * v / 100, 22, 11); c.set_source(lin_grad(-cw + 80, 0, cw - 120, 0, cols)); c.fill()
        g.rect(-cw + 80 + (2 * cw - 200) * v / 100 - 10, y - 10, 10, 22, cols[1], a=0.9)
        grad_text(c, str(v), cw - 70, y + 10, 30, ['#ffffff', cols[1]], ow=5)
    holo(p, cw, ch, t, -150)
    c.restore(); g.c.restore()

def render(which, out):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); gs = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s); gc = cairo.Context(gs)
    for cc in (c, gc): cc.set_line_cap(1); cc.set_line_join(1)
    p = P(c, gc); g = p.g
    background(p, g, 1.0)
    (front if which == 'front' else back)(p, g, 1.0)
    cap = (0, '水浒群英卡 · 第一张', '豹子头 林冲', (), ((0, 3),)) if which == 'front' else (0, '下一位好汉，', '你想看谁？', (), ())
    chrome(p, cap, t=5)
    a = composite(s, gs)
    Image.frombuffer('RGBA', (W, H), a.tobytes(), 'raw', 'BGRA', 0, 1).convert('RGB').save(out)

if __name__ == '__main__':
    render('front', 'card_front.png'); render('back', 'card_back.png')
