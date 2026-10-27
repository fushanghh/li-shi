"""chibi2: flat Q-style characters in the 'Song takeaway' sample style.
Head ~= body, white round face + pink blush, two white ball hands in front,
trapezoid robe + collar, darker sleeves, NO black outline (same-hue darker edge).
Origin = feet centre. s=1 -> ~330 px tall.
"""
import math
from core import *

FACE = (0.99, 0.96, 0.92)
FACEL = (0.86, 0.78, 0.70)
BLUSH = (0.97, 0.62, 0.64)
EYE = (0.14, 0.10, 0.09)
HATK = (0.13, 0.11, 0.11)
SWEAT = (0.45, 0.72, 0.98)
MOUTH = (0.78, 0.22, 0.20)
SMUL = 1.15

ROBES = {
    'ming_emp': (0.93, 0.70, 0.18),   # 明黄
    'qing_emp': (0.95, 0.76, 0.22),
    'red_off': (0.72, 0.20, 0.16),    # 明 绯袍
    'blue_off': (0.25, 0.32, 0.50),
    'eunuch': (0.42, 0.30, 0.42),
    'merchant': (0.50, 0.36, 0.24),
    'brown': (0.55, 0.38, 0.24),
    'blue': (0.30, 0.42, 0.62),
    'green': (0.32, 0.48, 0.36),
    'qing_blue': (0.20, 0.25, 0.38),  # 石青 褂
    'soldier': (0.50, 0.22, 0.18),
    'song_emp': (0.86, 0.36, 0.20),   # 宋 赭红袍
    'tang_emp': (0.90, 0.64, 0.20),   # 唐 赭黄袍
    'pink': (0.92, 0.55, 0.62),
    'rose': (0.80, 0.30, 0.42),
    'lilac': (0.62, 0.50, 0.78),
    'teal': (0.25, 0.55, 0.55),
    'qing_lady': (0.45, 0.62, 0.78),
    'han_black': (0.24, 0.22, 0.27),
    'han_red': (0.66, 0.24, 0.18),
    'empress': (0.80, 0.22, 0.24),
}


def _hand(c, x, y, a, r=15):
    c.arc(x, y, r, 0, TAU); rgba(c, FACE, a); c.fill_preserve()
    rgba(c, FACEL, a); c.set_line_width(2); c.stroke()


def _arm(c, x0, y0, x1, y1, col, a, w=34):
    rgba(c, dk(col, 0.80), a); c.set_line_width(w); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)


def eyes_mouth(c, expr, T, a, hy, d=0):
    ex1, ex2, ey = -27 + d, 27 + d, hy + 6
    blink = (T % 3.3) > 3.18 and expr in ('calm', 'sad', 'angry', 'worry')
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    rgba(c, EYE, a)
    if expr in ('happy', 'laugh', 'cheer') or blink:
        c.set_line_width(5)
        for ex in (ex1, ex2):
            if blink:
                c.move_to(ex - 9, ey + 1); c.line_to(ex + 9, ey + 1)
            else:
                c.move_to(ex - 10, ey + 4); c.curve_to(ex - 5, ey - 8, ex + 5, ey - 8, ex + 10, ey + 4)
            c.stroke()
    elif expr == 'cold':
        c.set_line_width(5)
        for ex, sg in ((ex1, 1), (ex2, -1)):
            c.move_to(ex - 10 * sg, ey - 8); c.line_to(ex + 8 * sg, ey); c.line_to(ex - 10 * sg, ey + 8); c.stroke()
    elif expr in ('shock', 'excited'):
        for ex in (ex1, ex2):
            c.arc(ex, ey - 2, 15, 0, TAU); rgba(c, (1, 1, 1), a); c.fill_preserve()
            rgba(c, EYE, a); c.set_line_width(4); c.stroke()
            c.arc(ex + 1, ey, 6.5, 0, TAU); c.fill()
    else:
        for ex in (ex1, ex2):
            ell(c, ex, ey, 6.5, 8); c.fill()
            rgba(c, (1, 1, 1), a); c.arc(ex + 2, ey - 3, 2.2, 0, TAU); c.fill(); rgba(c, EYE, a)
    # brows
    c.set_line_width(4)
    if expr == 'angry':
        c.move_to(ex1 - 12, ey - 24); c.line_to(ex1 + 8, ey - 15); c.stroke()
        c.move_to(ex2 + 12, ey - 24); c.line_to(ex2 - 8, ey - 15); c.stroke()
    elif expr in ('sad', 'worry', 'cold'):
        c.move_to(ex1 - 11, ey - 15); c.line_to(ex1 + 8, ey - 22); c.stroke()
        c.move_to(ex2 + 11, ey - 15); c.line_to(ex2 - 8, ey - 22); c.stroke()
    # blush
    rgba(c, BLUSH, 0.75 * a)
    ell(c, ex1 - 12, ey + 22, 14, 8.5); c.fill(); ell(c, ex2 + 12, ey + 22, 14, 8.5); c.fill()
    mx, my = d, ey + 27
    if expr in ('laugh', 'excited', 'cheer'):
        c.move_to(mx - 17, my - 5); c.curve_to(mx - 14, my + 22, mx + 14, my + 22, mx + 17, my - 5); c.close_path()
        rgba(c, MOUTH, a); c.fill()
        ell(c, mx, my + 10, 8, 4); rgba(c, (0.95, 0.55, 0.55), a); c.fill()
        if expr == 'excited':
            c.rectangle(mx - 13, my - 5, 26, 5); rgba(c, (1, 1, 1), a); c.fill()
    elif expr == 'shock':
        ell(c, mx, my + 4, 8, 11); rgba(c, MOUTH, a); c.fill()
    elif expr == 'cold':   # chattering zigzag mouth
        rgba(c, EYE, a); c.set_line_width(3.5)
        jit = math.sin(T * 40) * 2
        c.move_to(mx - 16, my + 3)
        for k in range(1, 7):
            c.line_to(mx - 16 + k * 5.3, my + 3 + (-5 if k % 2 else 5) + jit)
        c.stroke()
    elif expr == 'happy':
        rgba(c, EYE, a); c.set_line_width(4)
        c.move_to(mx - 10, my - 1); c.curve_to(mx - 5, my + 9, mx + 5, my + 9, mx + 10, my - 1); c.stroke()
    elif expr in ('sad', 'angry', 'worry'):
        rgba(c, EYE, a); c.set_line_width(4)
        c.move_to(mx - 9, my + 6); c.curve_to(mx - 4, my - 2, mx + 4, my - 2, mx + 9, my + 6); c.stroke()
    else:
        rgba(c, EYE, a); c.set_line_width(4)
        c.move_to(mx - 7, my + 1); c.line_to(mx + 7, my + 1); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    if expr == 'cold':
        rgba(c, (0.35, 0.55, 0.95), 0.75 * a); c.set_line_width(3)
        for k in range(4):
            xx = -24 + k * 16
            c.move_to(xx, ey - 50); c.line_to(xx, ey - 30); c.stroke()
    if expr == 'sad':
        rgba(c, SWEAT, a); c.move_to(ex2 + 4, ey + 10)
        c.curve_to(ex2 + 13, ey + 26, ex2 - 5, ey + 30, ex2 + 4, ey + 10); c.fill()


def sweat(c, x, y, a, T, s=1.0):
    y = y + (T * 18) % 14
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, -18); c.curve_to(10, -2, 12, 10, 0, 12); c.curve_to(-12, 10, -10, -2, 0, -18)
    rgba(c, SWEAT, a); c.fill_preserve(); rgba(c, (0.25, 0.50, 0.85), a); c.set_line_width(2); c.stroke()
    ell(c, -3, 2, 3, 5); rgba(c, (1, 1, 1), 0.8 * a); c.fill()
    c.restore()


def flaps(T, walk=0.0, jump=0.0, talk=0.0, settle=None, expr='calm', gain=1.0):
    """spring angles (rad, + = tip up) for left/right hat side-parts; sides slightly out of phase"""
    out = []
    for i in (0, 1):
        ph = i * 0.95
        v = 0.065 * math.sin(T * 4.6 + ph) + 0.03 * math.sin(T * 9.3 + ph * 1.7)          # idle / breathing
        if talk:
            v += talk * (0.15 * math.sin(T * 13.0 + ph)) * (0.65 + 0.35 * math.sin(T * 3.1))
        if walk:
            v += 0.30 * math.sin(walk * math.pi * 2 - 1.1 + ph)                              # walking bounce (bigger)
        if settle is not None and settle >= 0:
            v += 0.34 * math.exp(-settle * 3.0) * math.sin(settle * 17.0 + ph)               # stop -> recoil
        if jump:
            v += min(jump, 40) * 0.006 * math.cos(T * 18 + ph)
        if expr in ('shock', 'excited'):
            v += 0.06 * math.sin(T * 19 + ph)
        out.append(v * gain)
    return out


def hat(c, kind, hy, r, a, T, fl=(0.0, 0.0)):
    blk = HATK
    FL = {-1: fl[0], 1: fl[1]}
    if kind == 'yishan':   # 明 翼善冠: wings sprout from BEHIND the raised back crown, sideways, tips tilted slightly up
        for sx in (-1, 1):
            q = FL[sx]
            c.save(); c.translate(sx * r * 0.40, hy - r - 2); c.rotate(-sx * (0.20 + q * 1.25))
            c.move_to(0, 0); c.line_to(sx * 58, 0); rgba(c, blk, a); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
            c.set_line_cap(cairo.LINE_CAP_BUTT)
            ell(c, sx * 94, -2, 38, 15); fill2(c, blk, a, 2.5, 1.9)
            ell(c, sx * 88, -7, 22, 3.5); rgba(c, (0.42, 0.38, 0.38), a); c.fill()
            c.restore()
        rr(c, -r * 0.58, hy - r - 32, r * 1.16, 48, 20); fill2(c, blk, a, 2.5, 1.9)       # raised back crown (山)
        c.arc(0, hy - 2, r + 3, math.pi * 1.04, math.pi * 1.96); c.close_path(); fill2(c, blk, a, 2.5, 1.9)  # front cap
        rgba(c, (0.40, 0.36, 0.36), a); c.set_line_width(2.5)
        c.arc(0, hy - 2, r * 0.82, math.pi * 1.18, math.pi * 1.82); c.stroke()
        c.rectangle(-r - 2, hy - 14, 2 * r + 4, 8); rgba(c, GOLD, a); c.fill()
    elif kind == 'wusha':  # 明 乌纱帽 with oval side wings
        for sx in (-1, 1):
            c.save(); c.translate(sx * r * 0.7, hy - r * 0.55); c.rotate(-sx * (FL[sx] * 1.25 + 0.05))
            c.move_to(0, 0); c.line_to(sx * (r * 0.3 + 12), 0)
            rgba(c, blk, a); c.set_line_width(6); c.stroke()
            ell(c, sx * (r * 0.3 + 36), 0, 38, 13); fill2(c, blk, a, 2.5, 1.9)
            ell(c, sx * (r * 0.3 + 30), -3, 22, 4); rgba(c, (0.40, 0.36, 0.36), a); c.fill()
            c.restore()
        rr(c, -r * 0.6, hy - r - 26, r * 1.2, 44, 16); fill2(c, blk, a, 2.5, 1.9)
        c.arc(0, hy - 2, r + 3, math.pi * 1.06, math.pi * 1.94); c.close_path(); fill2(c, blk, a, 2.5, 1.9)
        c.rectangle(-r - 1, hy - 16, 2 * r + 2, 7); rgba(c, (0.35, 0.30, 0.28), a); c.fill()
    elif kind in ('nuanmao', 'nuanmao_emp', 'nuanmao_plain'):  # 清 暖帽
        # red tassel dome
        tassel = (0.80, 0.16, 0.14) if kind != 'nuanmao_plain' else (0.66, 0.22, 0.17)
        c.arc(0, hy - r * 0.55, r * 0.78, math.pi, TAU); c.close_path(); fill2(c, tassel, a, 2.5, 0.7)
        c.set_source_rgba(*dk(tassel, 0.7), a); c.set_line_width(2)
        for k in range(-4, 5):
            c.move_to(k * 9, hy - r * 0.55 - r * 0.72 * math.cos(k * 0.17)); c.line_to(k * 15, hy - r * 0.55); c.stroke()
        # upturned fur brim
        c.move_to(-r - 12, hy - r * 0.35); c.curve_to(-r - 8, hy - r * 0.85, r + 8, hy - r * 0.85, r + 12, hy - r * 0.35)
        c.line_to(r + 4, hy - r * 0.12); c.curve_to(r * 0.5, hy - r * 0.38, -r * 0.5, hy - r * 0.38, -r - 4, hy - r * 0.12); c.close_path()
        fill2(c, (0.24, 0.17, 0.13), a, 2.5, 1.7)
        # red fringe side strands spilling over the brim (bounce)
        for sx in (-1, 1):
            for j in range(3):
                q = FL[sx] * (1.0 + j * 0.25)
                bx, by = sx * (r * 0.55 + j * 9), hy - r * 0.62
                ex, ey = sx * (r * 0.95 + 10 + j * 7), hy - r * 0.30 - q * 70
                c.move_to(bx, by); c.curve_to(bx + sx * 18, by + 4, ex - sx * 6, ey - 10, ex, ey)
                rgba(c, tassel, a); c.set_line_width(5); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
            c.set_line_cap(cairo.LINE_CAP_BUTT)
        if kind == 'nuanmao':   # 花翎 trailing back-left, bounces
            q = FL[-1]
            c.save(); c.translate(-r * 0.15, hy - r * 1.30); c.rotate(-0.25 - q * 1.2)
            c.move_to(0, 0); c.curve_to(-40, 20, -80, 50, -112, 96)
            rgba(c, (0.25, 0.42, 0.30), a); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
            ell(c, -112, 96, 17, 22); rgba(c, (0.20, 0.45, 0.55), a); c.fill()
            ell(c, -112, 96, 9, 12); rgba(c, (0.95, 0.80, 0.30), a); c.fill()
            ell(c, -112, 97, 4, 6); rgba(c, (0.10, 0.15, 0.35), a); c.fill()
            c.set_line_cap(cairo.LINE_CAP_BUTT); c.restore()
        if kind == 'nuanmao_emp':
            for k, rr_ in enumerate((11, 8, 6)):
                c.arc(0, hy - r * 1.36 - k * 15, rr_, 0, TAU); fill2(c, GOLDL, a, 2, 0.7)
        elif kind == 'nuanmao':
            c.arc(0, hy - r * 1.38, 9, 0, TAU); fill2(c, (0.75, 0.25, 0.22), a, 2, 0.7)
    elif kind == 'guapi':  # 瓜皮帽
        c.arc(0, hy - 4, r + 2, math.pi * 1.05, math.pi * 1.95); c.close_path(); fill2(c, blk, a, 2.5, 1.9)
        rgba(c, (0.32, 0.28, 0.27), a); c.set_line_width(2.5)
        for k in (-0.45, 0, 0.45):
            c.move_to(k * r * 0.9, hy - r * 0.98); c.line_to(k * r * 1.6, hy - r * 0.38); c.stroke()
        c.rectangle(-r - 1, hy - r * 0.42, 2 * r + 2, 9); rgba(c, (0.25, 0.22, 0.22), a); c.fill()
        c.arc(0, hy - r - 6, 10, 0, TAU); fill2(c, (0.82, 0.18, 0.15), a, 2, 0.7)
    elif kind == 'eunuch':  # 明 内侍 cap: black, tall flat back
        rr(c, -r * 0.78, hy - r - 34, r * 1.56, 60, 10); fill2(c, blk, a, 2.5, 1.9)
        c.arc(0, hy - 2, r + 3, math.pi * 1.04, math.pi * 1.96); c.close_path(); fill2(c, blk, a, 2.5, 1.9)
        c.rectangle(-r - 2, hy - 15, 2 * r + 4, 7); rgba(c, (0.55, 0.15, 0.15), a); c.fill()
    elif kind == 'helmet':
        for sx in (-1, 1):
            q = FL[sx]
            c.save(); c.translate(sx * (r + 2), hy - 8); c.rotate(sx * (0.1 - q * 1.2))
            rr(c, -12, 0, 24, 62, 9); fill2(c, (0.55, 0.20, 0.17), a, 2.5, 0.72); c.restore()
        c.move_to(0, hy - r - 50); c.line_to(0, hy - r - 10); rgba(c, (0.75, 0.62, 0.30), a); c.set_line_width(6); c.stroke()
        ell(c, 0, hy - r - 50, 10, 12); rgba(c, (0.82, 0.16, 0.14), a); c.fill()
        c.arc(0, hy, r + 6, math.pi * 1.0, TAU); c.close_path(); fill2(c, (0.40, 0.40, 0.44), a, 3, 0.6)
        c.rectangle(-r - 8, hy - 14, 2 * r + 16, 12); rgba(c, (0.75, 0.62, 0.30), a); c.fill()
    elif kind == 'fangjin':  # 方巾
        rr(c, -r * 0.85, hy - r - 26, r * 1.7, 58, 8); fill2(c, blk, a, 2.5, 1.9)
        c.arc(0, hy - 4, r + 2, math.pi * 1.06, math.pi * 1.94); c.close_path(); fill2(c, blk, a, 2.5, 1.9)
    elif kind == 'futou_song':  # 宋 直脚幞头: black cap + long straight horizontal wings
        for sx in (-1, 1):
            L = r * 0.45 + 120; dyt = -L * FL[sx] * 1.1
            x0_, y0_ = sx * r * 0.55, hy - r * 0.62
            c.move_to(x0_, y0_); c.curve_to(x0_ + sx * L * 0.4, y0_ + dyt * 0.1, x0_ + sx * L * 0.75, y0_ + dyt * 0.45, x0_ + sx * L, y0_ - 6 + dyt)
            rgba(c, blk, a); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
            rgba(c, (0.40, 0.36, 0.34), a); c.set_line_width(2)
            c.move_to(x0_ + sx * 6, y0_ - 3); c.curve_to(x0_ + sx * L * 0.4, y0_ - 3 + dyt * 0.1, x0_ + sx * L * 0.75, y0_ - 3 + dyt * 0.45, x0_ + sx * (L - 4), y0_ - 9 + dyt); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_BUTT)
        rr(c, -r * 0.66, hy - r - 34, r * 1.32, 56, 14); fill2(c, blk, a, 2.5, 1.9)
        c.arc(0, hy - 2, r + 3, math.pi * 1.04, math.pi * 1.96); c.close_path(); fill2(c, blk, a, 2.5, 1.9)
        c.rectangle(-r - 2, hy - 15, 2 * r + 4, 7); rgba(c, (0.36, 0.32, 0.30), a); c.fill()
    elif kind == 'futou_tang':  # 唐 软脚幞头: rounded tall cap + two soft tails drooping behind
        for sx in (-1, 1):
            q = FL[sx]
            c.move_to(sx * r * 0.4, hy - r * 0.9)
            c.curve_to(sx * (r + 20), hy - r * 0.8, sx * (r + 34 + q * 40), hy - r * 0.1 - q * 30, sx * (r + 22 + q * 90), hy + r * 0.45 - q * 80)
            rgba(c, blk, a); c.set_line_width(12); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_BUTT)
        ell(c, 0, hy - r - 6, r * 0.55, 36); fill2(c, blk, a, 2.5, 1.9)
        c.arc(0, hy - 2, r + 3, math.pi * 1.04, math.pi * 1.96); c.close_path(); fill2(c, blk, a, 2.5, 1.9)
        c.rectangle(-r - 2, hy - 15, 2 * r + 4, 7); rgba(c, (0.36, 0.32, 0.30), a); c.fill()
    elif kind == 'qitou':  # 清 两把头 (旗头): black hair + wide flat board + flowers + tassel
        c.arc(0, hy - 4, r + 3, math.pi * 1.02, math.pi * 1.98); c.close_path(); fill2(c, blk, a, 2.5, 1.9)
        rr(c, -r * 0.45, hy - r - 14, r * 0.9, 30, 8); fill2(c, blk, a, 2.5, 1.9)
        rr(c, -r - 46, hy - r - 34, 2 * r + 92, 34, 10); fill2(c, (0.10, 0.10, 0.14), a, 2.5, 2.4)
        rgba(c, (0.35, 0.35, 0.42), a); c.set_line_width(2)
        c.move_to(-r - 36, hy - r - 26); c.line_to(r + 36, hy - r - 26); c.stroke()
        for k, (fx, fc) in enumerate(((-36, (0.95, 0.45, 0.55)), (0, (0.98, 0.80, 0.30)), (36, (0.95, 0.45, 0.55)))):
            for j in range(5):
                ang = j * TAU / 5 + T * 0.3
                c.arc(fx + 10 * math.cos(ang), hy - r - 34 + 10 * math.sin(ang), 7, 0, TAU); rgba(c, fc, a); c.fill()
            c.arc(fx, hy - r - 34, 5, 0, TAU); rgba(c, (1, 1, 0.9), a); c.fill()
        for sx in (-1, 1):
            q = FL[sx]
            x0_, y0_ = sx * (r + 30), hy - r - 18
            c.move_to(x0_, y0_); c.curve_to(x0_, y0_ + 20, x0_ + sx * q * 50, y0_ + 40, x0_ + sx * q * 90, y0_ + 64 - abs(q) * 30)
            rgba(c, (0.85, 0.25, 0.25), a); c.set_line_width(6); c.stroke()
            c.arc(x0_ + sx * q * 90, y0_ + 66 - abs(q) * 30, 7, 0, TAU); rgba(c, GOLDL, a); c.fill()
    elif kind == 'tang_bun':  # 唐 高髻 + 花
        c.arc(0, hy - 4, r + 3, math.pi * 1.02, math.pi * 1.98); c.close_path(); fill2(c, blk, a, 2.5, 1.9)
        for sx in (-1, 1):
            ell(c, sx * 26, hy - r - 26, 26, 34); fill2(c, blk, a, 2.5, 1.9)
        for k, fx in enumerate((-44, 40)):
            for j in range(5):
                ang = j * TAU / 5
                c.arc(fx + 9 * math.cos(ang), hy - r - 4 + 9 * math.sin(ang), 7, 0, TAU); rgba(c, (0.95, 0.45, 0.50), a); c.fill()
            c.arc(fx, hy - r - 4, 5, 0, TAU); rgba(c, (1, 0.9, 0.4), a); c.fill()
        c.move_to(12, hy - r - 46); c.line_to(44, hy - r - 70); rgba(c, GOLD, a); c.set_line_width(5); c.stroke()
        c.arc(46, hy - r - 72, 6, 0, TAU); rgba(c, GOLDL, a); c.fill()
    elif kind == 'hanguan':  # 汉 进贤冠 + 冠缨 hanging both sides (bounce)
        for sx in (-1, 1):
            q = FL[sx]
            c.move_to(sx * (r - 4), hy - r * 0.40); c.curve_to(sx * (r + 10), hy - r * 0.05, sx * (r + 2), hy + r * 0.55, sx * r * 0.72, hy + r * 0.86)
            rgba(c, (0.62, 0.20, 0.16), a); c.set_line_width(6); c.stroke()
            tx, ty = sx * r * 0.72, hy + r * 0.86
            c.move_to(tx, ty); c.curve_to(tx + sx * 8, ty + 24, tx + sx * (10 + q * 70), ty + 46 - q * 30, tx + sx * (14 + q * 120), ty + 74 - abs(q) * 40)
            c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)
        c.arc(0, hy - 4, r + 2, math.pi * 1.04, math.pi * 1.96); c.close_path(); fill2(c, blk, a, 2.5, 1.9)
        c.move_to(-r * 0.55, hy - r * 0.78); c.line_to(-r * 0.30, hy - r - 58); c.line_to(r * 0.55, hy - r - 30); c.line_to(r * 0.62, hy - r * 0.80); c.close_path()
        fill2(c, blk, a, 2.5, 1.9)
        rgba(c, (0.40, 0.36, 0.36), a); c.set_line_width(3)
        c.move_to(-r * 0.22, hy - r - 44); c.line_to(r * 0.45, hy - r - 22); c.stroke()
        c.rectangle(-r - 1, hy - r * 0.42, 2 * r + 2, 10); rgba(c, (0.30, 0.27, 0.27), a); c.fill()
    elif kind == 'fengguan':  # 明 凤冠 with 博鬓 side flaps (bounce)
        c.arc(0, hy - 4, r + 3, math.pi * 1.02, math.pi * 1.98); c.close_path(); fill2(c, blk, a, 2.5, 1.9)
        for sx in (-1, 1):
            q = FL[sx]
            c.save(); c.translate(sx * r * 0.85, hy - r * 0.55); c.rotate(-sx * (0.35 + q * 1.1))
            for k in range(3):
                ell(c, sx * (26 + k * 22), 8 + k * 6, 16, 9); fill2(c, GOLDL, a, 2, 0.65)
                c.arc(sx * (26 + k * 22), 8 + k * 6, 4, 0, TAU); rgba(c, (0.25, 0.55, 0.85), a); c.fill()
            c.restore()
        c.move_to(-r * 0.9, hy - r * 0.55); c.curve_to(-r * 0.9, hy - r * 1.5, r * 0.9, hy - r * 1.5, r * 0.9, hy - r * 0.55); c.close_path()
        fill2(c, (0.22, 0.30, 0.55), a, 2.5, 0.7)
        for k, fx in enumerate((-40, 0, 40)):
            ell(c, fx, hy - r * 1.05 - (12 if k == 1 else 0), 16, 12); fill2(c, GOLDL, a, 2, 0.65)
            c.arc(fx, hy - r * 1.05 - (12 if k == 1 else 0), 5, 0, TAU); rgba(c, (0.85, 0.20, 0.25), a); c.fill()
        c.rectangle(-r * 0.9, hy - r * 0.62, r * 1.8, 10); rgba(c, GOLD, a); c.fill()
    elif kind == 'khitan':  # 辽 契丹 fur cap with long hanging fur ear-flaps (bounce)
        fur = (0.55, 0.40, 0.26)
        for sx in (-1, 1):
            q = FL[sx]
            c.save(); c.translate(sx * (r + 6), hy - r * 0.40); c.rotate(sx * (0.12 - q * 1.2))
            rr(c, -15, 0, 30, r * 0.95, 14); fill2(c, fur, a, 2.5, 0.72)
            rgba(c, dk(fur, 0.8), a); c.set_line_width(2)
            for k in range(3):
                c.move_to(-9, 18 + k * 18); c.line_to(9, 24 + k * 18); c.stroke()
            c.restore()
        c.arc(0, hy - 4, r + 4, math.pi * 1.02, math.pi * 1.98); c.close_path(); fill2(c, (0.36, 0.26, 0.18), a, 2.5, 0.7)
        rr(c, -r - 6, hy - r * 0.62, 2 * r + 12, 22, 10); fill2(c, fur, a, 2.5, 0.72)
        c.arc(0, hy - r - 6, 13, 0, TAU); fill2(c, (0.80, 0.25, 0.20), a, 2, 0.7)
    elif kind == 'yuan':  # 元 钹笠帽: round dome + wide brim + side tassels (bounce)
        c.arc(0, hy - r * 0.45, r * 0.80, math.pi, TAU); c.close_path(); fill2(c, (0.30, 0.22, 0.16), a, 2.5, 0.7)
        ell(c, 0, hy - r * 0.45, r * 1.35, 16); fill2(c, (0.42, 0.30, 0.20), a, 2.5, 0.7)
        c.arc(0, hy - r * 1.28, 10, 0, TAU); fill2(c, GOLDL, a, 2, 0.7)
        for sx in (-1, 1):
            q = FL[sx]
            x0_, y0_ = sx * r * 1.18, hy - r * 0.40
            ex, ey = x0_ + sx * q * 70, y0_ + 70 - abs(q) * 25
            c.move_to(x0_, y0_); c.curve_to(x0_, y0_ + 25, ex - sx * 4, ey - 20, ex, ey)
            rgba(c, (0.85, 0.22, 0.18), a); c.set_line_width(5); c.stroke()
            ell(c, ex, ey + 8, 8, 12); rgba(c, (0.85, 0.22, 0.18), a); c.fill()
    elif kind == 'lama':  # 黄色僧帽 with long side lappets (bounce)
        y_ = (0.98, 0.80, 0.22)
        for sx in (-1, 1):
            q = FL[sx]
            c.save(); c.translate(sx * r * 0.85, hy - r * 0.45); c.rotate(sx * (0.05 - q * 1.1))
            rr(c, -13, 0, 26, r * 1.25, 10); fill2(c, y_, a, 2.5, 0.72)
            c.restore()
        c.move_to(-r - 6, hy - r * 0.35); c.curve_to(-r * 0.9, hy - r * 1.5, -r * 0.2, hy - r * 1.95, r * 0.35, hy - r * 1.85)
        c.curve_to(r * 0.2, hy - r * 1.6, r * 0.9, hy - r * 1.3, r + 6, hy - r * 0.35); c.close_path()
        fill2(c, y_, a, 2.5, 0.72)
        rgba(c, dk(y_, 0.75), a); c.set_line_width(3)
        for k in range(-3, 4):
            c.move_to(k * 14, hy - r * 0.45); c.curve_to(k * 12, hy - r * 0.9, k * 6 + 8, hy - r * 1.3, k * 3 + 18, hy - r * 1.6); c.stroke()
        rr(c, -r - 8, hy - r * 0.48, 2 * r + 16, 18, 8); fill2(c, dk(y_, 0.9), a, 2, 0.7)
    elif kind in ('priest', 'bowler'):  # 西洋宽檐帽 / 英式圆顶礼帽: brim tips bounce
        hc = (0.12, 0.11, 0.12) if kind == 'priest' else (0.20, 0.17, 0.15)
        W_ = r * (1.45 if kind == 'priest' else 1.15)
        for sx in (-1, 1):
            q = FL[sx]
            c.save(); c.translate(0, hy - r * 0.62); c.rotate(-sx * q * 0.9)
            c.move_to(0, -8); c.curve_to(sx * W_ * 0.5, -10, sx * W_ * 0.9, -4, sx * W_, -16 - q * 30)
            c.curve_to(sx * W_ * 0.9, 10, sx * W_ * 0.5, 10, 0, 10); c.close_path()
            fill2(c, hc, a, 2.5, 2.2); c.restore()
        if kind == 'priest':
            c.arc(0, hy - r * 0.68, r * 0.72, math.pi, TAU); c.close_path(); fill2(c, hc, a, 2.5, 2.2)
        else:
            c.move_to(-r * 0.66, hy - r * 0.62); c.curve_to(-r * 0.70, hy - r * 1.55, r * 0.70, hy - r * 1.55, r * 0.66, hy - r * 0.62); c.close_path()
            fill2(c, hc, a, 2.5, 2.2)
            c.rectangle(-r * 0.66, hy - r * 0.82, r * 1.32, 10); rgba(c, (0.45, 0.20, 0.18), a); c.fill()
    elif kind == 'douli':  # 斗笠 straw hat + chin strings (bounce)
        st = (0.86, 0.70, 0.40)
        for sx in (-1, 1):
            q = FL[sx]
            x0_, y0_ = sx * r * 0.75, hy - r * 0.35
            ex, ey = x0_ + sx * (8 + q * 60), y0_ + 80 - abs(q) * 25
            c.move_to(x0_, y0_); c.curve_to(x0_, y0_ + 30, ex, ey - 30, ex, ey)
            rgba(c, (0.55, 0.38, 0.20), a); c.set_line_width(4); c.stroke()
        c.move_to(-r * 1.45, hy - r * 0.40); c.line_to(0, hy - r * 1.55); c.line_to(r * 1.45, hy - r * 0.40)
        c.curve_to(r * 0.6, hy - r * 0.25, -r * 0.6, hy - r * 0.25, -r * 1.45, hy - r * 0.40); c.close_path()
        fill2(c, st, a, 2.5, 0.72)
        rgba(c, dk(st, 0.78), a); c.set_line_width(2)
        for k in range(1, 4):
            f = k / 4.0
            c.move_to(-r * 1.45 * f, hy - r * 1.55 + (r * 1.15) * f); c.line_to(r * 1.45 * f, hy - r * 1.55 + (r * 1.15) * f); c.stroke()
    elif kind == 'hair':  # modern kid, no hat
        c.arc(0, hy - 6, r + 3, math.pi * 1.0, math.pi * 2.0); c.close_path(); fill2(c, (0.16, 0.12, 0.11), a, 2.5, 1.9)
        c.move_to(-r * 0.6, hy - r * 0.55); c.curve_to(-r * 0.2, hy - r * 0.2, r * 0.2, hy - r * 0.55, r * 0.5, hy - r * 0.35)
        c.line_to(r * 0.9, hy - r * 0.6); c.line_to(-r * 0.9, hy - r * 0.6); c.close_path(); rgba(c, (0.16, 0.12, 0.11), a); c.fill()
    elif kind == 'kidtuft':  # child: shaved head with small tuft
        c.arc(0, hy - r + 6, 18, math.pi, TAU); rgba(c, blk, a); c.fill()
        c.arc(0, hy - 6, r + 1, math.pi * 1.25, math.pi * 1.75); rgba(c, (0.30, 0.26, 0.25), a * 0.5); c.set_line_width(4); c.stroke()
    elif kind == 'bun':
        c.arc(0, hy - r - 10, 22, 0, TAU); fill2(c, blk, a, 2.5, 1.9)
        c.arc(0, hy - 6, r + 2, math.pi * 1.08, math.pi * 1.92); c.close_path(); fill2(c, blk, a, 2.5, 1.9)


def prop_draw(c, prop, hands, a, T, col):
    (lx, ly), (rx, ry) = hands
    if prop == 'book':
        cx, cy = (lx + rx) / 2, (ly + ry) / 2 - 6
        rr(c, cx - 40, cy - 32, 80, 56, 4); fill2(c, (0.85, 0.32, 0.22), a, 2.5)
        rr(c, cx - 33, cy - 26, 66, 44, 3); fill2(c, (0.97, 0.92, 0.80), a, 2)
        rgba(c, (0.45, 0.35, 0.28), a); c.set_line_width(2)
        for k in range(4):
            c.move_to(cx - 26, cy - 18 + k * 10); c.line_to(cx + 24, cy - 18 + k * 10); c.stroke()
    elif prop == 'sword':
        cx = (lx + rx) / 2; cy = (ly + ry) / 2
        c.rectangle(cx - 5, cy - 150, 10, 140); fill2(c, (0.85, 0.87, 0.90), a, 2)
        c.rectangle(cx - 26, cy - 14, 52, 9); fill2(c, GOLD, a, 2)
        c.rectangle(cx - 5, cy - 6, 10, 30); fill2(c, (0.45, 0.20, 0.15), a, 2)
    elif prop == 'bundle':
        c.move_to(rx, ry); c.line_to(rx + 70, ry - 120); rgba(c, (0.45, 0.32, 0.20), a); c.set_line_width(6); c.stroke()
        ell(c, rx + 80, ry - 120, 36, 30); fill2(c, (0.30, 0.45, 0.65), a, 2.5)
        c.move_to(rx + 66, ry - 148); c.line_to(rx + 80, ry - 136); c.line_to(rx + 94, ry - 150); rgba(c, (0.22, 0.34, 0.52), a); c.set_line_width(4); c.stroke()
    elif prop == 'basket':
        cx, cy = (lx + rx) / 2, (ly + ry) / 2 + 10
        c.move_to(cx - 44, cy - 14); c.line_to(cx + 44, cy - 14); c.line_to(cx + 34, cy + 22); c.line_to(cx - 34, cy + 22); c.close_path()
        fill2(c, (0.78, 0.60, 0.32), a, 2.5)
        for k in range(9):
            c.arc(cx - 32 + k * 8, cy - 18 + (k % 2) * 3, 4, 0, TAU); rgba(c, (0.25, 0.20, 0.16), a); c.fill()
    elif prop == 'tray':
        cx, cy = (lx + rx) / 2, (ly + ry) / 2 - 6
        ell(c, cx, cy, 60, 12); fill2(c, (0.62, 0.30, 0.18), a, 2.5)
        for dx in (-25, 20):
            c.arc(cx + dx, cy - 12, 14, math.pi, TAU); fill2(c, (0.95, 0.95, 0.95), a, 2)
    elif prop == 'abacus':
        cx, cy = (lx + rx) / 2, (ly + ry) / 2 - 8
        rr(c, cx - 50, cy - 30, 100, 56, 4); fill2(c, (0.50, 0.30, 0.16), a, 3)
        for k in range(5):
            c.move_to(cx - 40 + k * 20, cy - 24); c.line_to(cx - 40 + k * 20, cy + 20)
            rgba(c, (0.85, 0.75, 0.55), a); c.set_line_width(2); c.stroke()
            for j in range(3):
                ell(c, cx - 40 + k * 20, cy - 12 + j * 12 + 3 * math.sin(T * 9 + k), 7, 4); rgba(c, (0.20, 0.12, 0.08), a); c.fill()
    elif prop == 'key':
        cx, cy = rx + 6, ry - 30
        c.arc(cx, cy, 13, 0, TAU); rgba(c, GOLD, a); c.set_line_width(6); c.stroke()
        c.rectangle(cx - 3, cy + 12, 6, 34); rgba(c, GOLD, a); c.fill()
        c.rectangle(cx + 3, cy + 36, 10, 6); c.fill()
    elif prop == 'redbasket':   # 红箩炭 red-painted wicker basket of charcoal sticks
        cx, cy = (lx + rx) / 2, (ly + ry) / 2 + 6
        for k in range(5):
            rr(c, cx - 34 + k * 14, cy - 46 - (k % 2) * 8, 11, 44, 4); fill2(c, (0.20, 0.17, 0.16), a, 2, 1.8)
        c.move_to(cx - 46, cy - 16); c.line_to(cx + 46, cy - 16); c.line_to(cx + 36, cy + 26); c.line_to(cx - 36, cy + 26); c.close_path()
        fill2(c, (0.80, 0.24, 0.18), a, 2.5)
        rgba(c, (0.60, 0.16, 0.12), a); c.set_line_width(2)
        for k in range(5):
            c.move_to(cx - 40 + k * 20, cy - 14); c.line_to(cx - 32 + k * 16, cy + 24); c.stroke()
    elif prop == 'handwarmer':
        cx, cy = (lx + rx) / 2, (ly + ry) / 2 - 18
        glow(c, cx, cy, 70, (1.0, 0.6, 0.25), 0.35 * a)
        c.move_to(cx - 30, cy - 18); c.curve_to(cx - 18, cy - 46, cx + 18, cy - 46, cx + 30, cy - 18)
        rgba(c, GOLDD, a); c.set_line_width(5); c.stroke()
        ell(c, cx, cy, 34, 22); fill2(c, (0.85, 0.62, 0.28), a, 2.5, 0.7)
        ell(c, cx, cy - 12, 30, 9); fill2(c, (0.70, 0.48, 0.20), a, 2, 0.7)
        rgba(c, (0.35, 0.22, 0.10), a)
        for k in range(-2, 3):
            c.arc(cx + k * 10, cy - 12, 2.5, 0, TAU); c.fill()
    elif prop == 'jar':   # 炭坛
        cx, cy = rx + 4, ry - 6
        ell(c, cx, cy, 30, 34); fill2(c, (0.45, 0.36, 0.30), a, 2.5, 0.7)
        rr(c, cx - 16, cy - 44, 32, 14, 4); fill2(c, (0.38, 0.30, 0.25), a, 2, 0.7)
        glow(c, cx, cy - 44, 26, (1.0, 0.45, 0.15), 0.5 * a)
    elif prop == 'bucket':
        cx, cy = rx + 8, ry + 10
        c.move_to(cx - 28, cy - 30); c.line_to(cx + 28, cy - 30); c.line_to(cx + 22, cy + 22); c.line_to(cx - 22, cy + 22); c.close_path()
        fill2(c, (0.62, 0.44, 0.26), a, 2.5)
        c.move_to(cx - 28, cy - 30); c.curve_to(cx - 20, cy - 70, cx + 20, cy - 70, cx + 28, cy - 30); rgba(c, (0.3, 0.22, 0.15), a); c.set_line_width(3); c.stroke()
        ell(c, cx, cy - 30, 26, 6); rgba(c, (0.45, 0.70, 0.95), a); c.fill()
    elif prop == 'brush':
        cx, cy = rx, ry
        c.move_to(cx, cy); c.line_to(cx + 30, cy - 70); rgba(c, (0.55, 0.35, 0.18), a); c.set_line_width(8); c.stroke()
        c.move_to(cx - 4, cy + 6); c.line_to(cx + 4, cy - 6); c.line_to(cx - 6, cy + 22); c.close_path(); rgba(c, (0.15, 0.12, 0.10), a); c.fill()
    elif prop == 'ruler':   # 戒尺
        cx = (lx + rx) / 2; cy = (ly + ry) / 2
        c.save(); c.translate(rx, ry); c.rotate(0.55 + math.sin(T * 9) * 0.25)
        rr(c, -10, -150, 22, 160, 5); fill2(c, (0.70, 0.46, 0.24), a, 2.5)
        rgba(c, dk((0.70, 0.46, 0.24), 0.7), a); c.set_line_width(2)
        for k in range(4):
            c.move_to(-6, -130 + k * 30); c.line_to(8, -130 + k * 30); c.stroke()
        c.restore()
    elif prop == 'reed':    # 荻 芦苇秆
        c.save(); c.translate(rx, ry); c.rotate(0.9)
        c.move_to(0, 0); c.line_to(0, 160); rgba(c, (0.80, 0.68, 0.40), a); c.set_line_width(6); c.stroke()
        c.restore()
    elif prop == 'scroll':
        cx, cy = (lx + rx) / 2, (ly + ry) / 2 - 10
        c.rectangle(cx - 46, cy - 26, 92, 52); fill2(c, (0.96, 0.90, 0.74), a, 2)
        for dx in (-50, 46):
            rr(c, cx + dx, cy - 32, 8, 64, 3); fill2(c, (0.55, 0.30, 0.18), a, 2)


def chibi(c, x, yf, s=1.0, hatk='guapi', robe='brown', expr='calm', pose='hold', T=0.0, a=1.0,
          collar='v', patch=None, prop=None, walk=0.0, sw=False, d=0, p=1.0, name=None, label_pre='',
          label_a=1.0, shake=0.0, jump=0.0, queue=None, talk=0.0, settle=None, fgain=1.0, snot=False):
    if a <= 0.01 or s <= 0.01:
        return
    col = ROBES.get(robe, robe) if isinstance(robe, str) else robe
    if queue is None:
        queue = hatk in ('nuanmao', 'nuanmao_emp', 'nuanmao_plain', 'guapi')
    s = s * SMUL
    c.save()
    bob = abs(math.sin(walk * math.pi)) * 10 if walk else 0
    breathe = math.sin(T * 2.4) * 1.8
    c.translate(x + (math.sin(T * 50) * 4 * shake), yf - bob - jump)
    c.scale(s, s)
    # shadow
    c.save(); c.translate(0, bob / s + jump / s); ell(c, 0, 4, 92, 13); c.restore()
    c.set_source_rgba(0, 0, 0, 0.22 * a); c.fill()
    r = 74
    hy = -228 + breathe
    # feet
    fo = math.sin(walk * math.pi) * 14 if walk else 0
    for sx, f in ((-1, fo), (1, -fo)):
        ell(c, sx * 30 + f, -2, 24, 11); rgba(c, (0.16, 0.12, 0.10), a); c.fill()
    # hand positions
    if pose == 'hold':
        hands = [(-26, -88), (26, -88)]
    elif pose == 'raise':
        hands = [(-26, -88), (84, -190 + math.sin(T * 7) * 6)]
    elif pose == 'cheer':
        q = math.sin(T * 8) * 8
        hands = [(-92, -200 + q), (92, -200 - q)]
    elif pose == 'point':
        hands = [(-26, -88), (118, -136)]
    elif pose == 'pointl':
        hands = [(-118, -136), (26, -88)]
    elif pose == 'sword':
        hands = [(-6, -96), (6, -96)]
    elif pose == 'run':
        q = math.sin(walk * math.pi) * 34
        hands = [(-62 + q * 0.3, -104 + q), (62 - q * 0.3, -104 - q)]
    elif pose == 'shrug':
        hands = [(-96, -130), (96, -130)]
    elif pose == 'wipe':
        hands = [(-26, -88), (60, -236 + math.sin(T * 10) * 8)]
    elif pose == 'rub':
        q = math.sin(T * 12) * 8
        hands = [(-18 + q, -96), (18 - q, -96)]
    else:
        hands = [(-26, -88), (26, -88)]
    if queue:
        c.move_to(-34, -230); c.curve_to(-90, -170, -100, -110, -86, -46)
        rgba(c, (0.13, 0.11, 0.11), a); c.set_line_width(16); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        rgba(c, (0.32, 0.28, 0.27), a); c.set_line_width(2)
        for k in range(6):
            yy = -200 + k * 26; xx = -76 - 14 * math.sin((k + 0.5) / 6 * math.pi) + k * 1.0
            c.move_to(xx - 7, yy - 5); c.line_to(xx + 7, yy + 5); c.stroke()
        c.move_to(-86, -46); c.line_to(-84, -22); rgba(c, (0.80, 0.18, 0.15), a); c.set_line_width(7); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_BUTT)
    # arms behind body for raised poses
    sh = [(-56, -150), (56, -150)]
    behind = pose in ('cheer', 'raise', 'shrug', 'wipe')
    if behind:
        for (sx, sy), (hx, hy2) in zip(sh, hands):
            if abs(hx) > 40 or hy2 < -150:
                _arm(c, sx, sy, hx, hy2, col, a)
    # body trapezoid
    c.move_to(-58, -168); c.curve_to(-70, -120, -84, -50, -92, -14)
    c.curve_to(-40, -4, 40, -4, 92, -14); c.curve_to(84, -50, 70, -120, 58, -168)
    c.curve_to(30, -178, -30, -178, -58, -168); c.close_path()
    fill2(c, col, a, 3, 0.72)
    # hem band
    c.move_to(-90, -26); c.curve_to(-40, -16, 40, -16, 90, -26)
    rgba(c, dk(col, 0.82), a); c.set_line_width(5); c.stroke()
    # collar
    if collar == 'v':
        c.move_to(-30, -172); c.line_to(16, -112); c.line_to(30, -172)
        rgba(c, (0.97, 0.95, 0.90), a); c.set_line_width(9); c.stroke()
        c.move_to(-30, -172); c.line_to(16, -112); rgba(c, dk(col, 0.6), a); c.set_line_width(2); c.stroke()
    elif collar == 'round':
        c.arc(0, -174, 32, 0.15 * math.pi, 0.85 * math.pi); rgba(c, dk(col, 0.62), a); c.set_line_width(7); c.stroke()
        c.move_to(22, -150); c.curve_to(40, -138, 52, -128, 64, -118); c.set_line_width(3); c.stroke()
        c.rectangle(-84, -104, 168, 12); rgba(c, GOLD if robe in ('ming_emp', 'red_off') else dk(col, 0.6), a); c.fill()
    elif collar == 'qing':
        c.arc(0, -176, 30, 0.12 * math.pi, 0.88 * math.pi); rgba(c, dk(col, 0.55), a); c.set_line_width(8); c.stroke()
        c.move_to(4, -148); c.curve_to(30, -146, 48, -136, 60, -124); c.set_line_width(4); c.stroke()
        for k in range(3):
            c.arc(14 + k * 16, -145 + k * 7, 4, 0, TAU); rgba(c, GOLD, a); c.fill()
    if patch == 'dragon':
        c.arc(0, -132, 25, 0, TAU); rgba(c, lt(col, 0.35), a); c.fill_preserve()
        rgba(c, dk(col, 0.7), a); c.set_line_width(3); c.stroke()
        c.arc(0, -132, 15, 0.3, 5.2); c.set_line_width(3); c.stroke()
        c.arc(4, -134, 6, 0, TAU); rgba(c, dk(col, 0.7), a); c.fill()
    elif patch == 'square':
        rr(c, -26, -152, 52, 46, 3); fill2(c, (0.30, 0.25, 0.40) if robe != 'red_off' else (0.30, 0.22, 0.30), a, 2.5, 0.7)
        rgba(c, GOLDL, a); c.arc(0, -129, 10, 0, TAU); c.fill()
    # front arms (sleeves) + hands
    for (sx, sy), (hx, hy2) in zip(sh, hands):
        if not (behind and (abs(hx) > 40 or hy2 < -150)):
            _arm(c, sx, sy, hx, hy2, col, a)
    if prop and pose not in ('cheer',):
        prop_draw(c, prop, hands, a, T, col)
    for hx, hy2 in hands:
        _hand(c, hx, hy2, a)
    # head
    c.arc(0, hy, r, 0, TAU); rgba(c, FACE, a); c.fill_preserve()
    rgba(c, FACEL, a); c.set_line_width(2.5); c.stroke()
    eyes_mouth(c, expr, T, a, hy + 14, d)
    hat(c, hatk, hy, r, a, T, flaps(T, walk, jump, talk, settle, expr, fgain))
    if sw:
        sweat(c, r * 0.9, hy - 10, a, T)
    if snot:
        br = 6 + 10 * (0.5 + 0.5 * math.sin(T * 2.2))
        c.arc(d + 34, hy + 30 + br * 0.9, br, 0, TAU); rgba(c, (0.70, 0.86, 1.0), 0.55 * a); c.fill_preserve()
        rgba(c, (0.40, 0.62, 0.95), 0.9 * a); c.set_line_width(2); c.stroke()
        c.arc(d + 34 - br * 0.35, hy + 30 + br * 0.5, br * 0.22, 0, TAU); rgba(c, (1, 1, 1), 0.85 * a); c.fill()
    c.restore()
    if name:
        top = yf - bob - jump - s * (228 + 74 + 70) - (20 if hatk in ('nuanmao_emp', 'yishan', 'helmet', 'eunuch', 'qitou', 'tang_bun', 'futou_tang', 'futou_song', 'hanguan', 'fengguan', 'lama', 'khitan', 'yuan', 'bowler') else 0)
        nameplate(c, x, top, label_pre, name, a * label_a, size=38)


def ped(c, x, yf, s=1.0, col=(0.45, 0.38, 0.32), a=1.0, walk=0.0, hatk=None):
    """faceless passer-by silhouette: round head + trapezoid"""
    if a <= 0.01:
        return
    c.save()
    bob = abs(math.sin(walk * math.pi)) * 8 if walk else 0
    c.translate(x, yf - bob); c.scale(s, s)
    c.move_to(-40, -120); c.line_to(40, -120); c.line_to(58, 0); c.line_to(-58, 0); c.close_path()
    fill2(c, col, a, 3, 0.75)
    hc = lt(col, 0.45)
    c.arc(0, -158, 40, 0, TAU); fill2(c, hc, a, 3, 0.8)
    if hatk == 'guapi':
        c.arc(0, -162, 41, math.pi * 1.05, math.pi * 1.95); c.close_path(); rgba(c, dk(col, 0.55), a); c.fill()
    elif hatk == 'nuanmao':
        c.arc(0, -178, 30, math.pi, TAU); c.close_path(); rgba(c, (0.65, 0.20, 0.16), a); c.fill()
        c.rectangle(-46, -186, 92, 12); rgba(c, dk(col, 0.5), a); c.fill()
    elif hatk == 'wusha':
        c.arc(0, -162, 41, math.pi * 1.05, math.pi * 1.95); c.close_path(); rgba(c, dk(col, 0.5), a); c.fill()
        c.rectangle(-70, -182, 140, 8); c.fill()
    c.restore()


def horse(c, x, yf, s=1.0, col=(0.92, 0.88, 0.82), a=1.0, run=0.0):
    c.save(); c.translate(x, yf); c.scale(s, s)
    q = math.sin(run * math.pi * 2) * 18 if run else 0
    for lx, ph in ((-70, 1), (-45, -1), (55, -1), (80, 1)):
        c.move_to(lx, -90); c.line_to(lx + q * ph * 0.6, -4); rgba(c, dk(col, 0.7), a); c.set_line_width(14)
        c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    ell(c, 5, -120, 110, 46); fill2(c, col, a, 3)
    c.move_to(80, -140); c.line_to(120, -215); c.line_to(150, -205); c.line_to(118, -120); c.close_path(); fill2(c, col, a, 3)
    ell(c, 140, -210, 34, 20); fill2(c, col, a, 3)
    rgba(c, EYE, a); c.arc(146, -216, 4, 0, TAU); c.fill()
    c.move_to(-105, -135); c.curve_to(-140, -120, -150, -80, -138, -60); rgba(c, (0.35, 0.25, 0.18), a); c.set_line_width(12); c.stroke()
    c.move_to(118, -222); c.curve_to(100, -190, 92, -160, 84, -140); c.set_line_width(10); c.stroke()
    rr(c, -40, -172, 70, 20, 6); rgba(c, (0.75, 0.20, 0.15), a); c.fill()
    c.restore()


if __name__ == '__main__':
    import sys
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(sf)
    c.set_source_rgb(0.42, 0.13, 0.11); c.paint()
    specs = [
        ('futou_song', 'song_emp', 'happy', 'hold', 'round', 'dragon', None, '宋朝', '宋徽宗'),
        ('futou_tang', 'tang_emp', 'laugh', 'hold', 'round', 'dragon', None, '唐朝', '唐玄宗'),
        ('tang_bun', 'pink', 'happy', 'hold', 'v', None, None, '', '杨贵妃'),
        ('nuanmao_emp', 'qing_emp', 'shock', 'hold', 'qing', 'dragon', None, '清朝', '康熙'),
        ('qitou', 'qing_lady', 'calm', 'hold', 'qing', None, None, '', '妃'),
        ('kidtuft', 'qing_blue', 'happy', 'hold', 'qing', None, None, '', '皇子'),
        ('wusha', 'red_off', 'angry', 'hold', 'round', 'square', 'scroll', '', '吴可读'),
    ]
    for i, (hk, rb, ex, po, co, pa, pr, pre, nm) in enumerate(specs):
        chibi(c, 150 + i * 270, 560, 0.75, hk, rb, ex, po, T=1.0, collar=co, patch=pa, prop=pr, name=nm, label_pre=pre, sw=(i == 3))
    for i, e in enumerate(['calm', 'happy', 'laugh', 'shock', 'sad', 'angry', 'cheer']):
        chibi(c, 150 + i * 270, 1040, 0.6, 'fangjin', 'blue', e, 'cheer' if e == 'cheer' else 'hold', T=1.0)
    ped(c, 1850, 1040, 1.0)
    sf.write_to_png('t_chars.png')
