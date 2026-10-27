import math, random
from core import *
from chibi2 import chibi, ped
from sets import vgrad, palace, book_page, lantern
from props import tagbox, hall, crate, coin, gate
from winter import *

# ---------------------------------------------------------------- presets（清代为主；所有帽子两侧部件随呼吸/走路/说话弹动）
QEMP = dict(hatk='nuanmao_emp', robe='qing_emp', collar='qing', patch='dragon')        # 清帝 暖帽红缨
QTJ = dict(hatk='nuanmao_plain', robe='eunuch', collar='qing')                         # 清 太监 暖帽红缨
QTJ2 = dict(hatk='nuanmao_plain', robe=(0.30, 0.38, 0.55), collar='qing')
QOFF = dict(hatk='nuanmao', robe='qing_blue', collar='qing', patch='square')           # 清官 花翎
QFEI = dict(hatk='qitou', robe='rose', collar='qing')                                  # 妃嫔 旗头
QTH = dict(hatk='qitou', robe=(0.88, 0.64, 0.22), collar='qing', patch='dragon')       # 皇太后
QDY = dict(hatk='qitou', robe=(0.55, 0.62, 0.66), collar='qing')                       # 答应
MEMP = dict(hatk='yishan', robe='ming_emp', collar='round', patch='dragon')            # 明帝 翼善冠(帽翅已修正)
MTJ = dict(hatk='eunuch', robe=(0.32, 0.36, 0.54), collar='round')                     # 明 内侍
KID = dict(hatk='hair', robe=(0.30, 0.56, 0.88), collar='v')

SC = []


def shot(D, src=''):
    def deco(fn):
        SC.append(dict(fn=fn, D=D, src=src))
        return fn
    return deco


def walk2(t, x0, x1, t0=0, d=1.0):
    u = seg(t, t0, t0 + d)
    x = lerp(x0, x1, ease(u))
    if 0 < u < 1:
        return x, (t - t0) * 2.6, None
    return x, 0.0, (t - t0 - d) if t >= t0 + d else None


def databg(c, T, col=DATAB):
    vgrad(c, 0, H, lt(col, 0.06), dk(col, 0.8))
    dust(c, T, 9, 40, (0.75, 0.85, 1.0), 0.25)


def endbg(c, T):
    vgrad(c, 0, H, (0.32, 0.22, 0.16), (0.20, 0.13, 0.10))
    c.rectangle(0, 860, W, H - 860); rgba(c, (0.16, 0.11, 0.08)); c.fill()
    dust(c, T, 4, 40, (1, 0.85, 0.6), 0.25)


def label(c, s_, x, y, t, t0, col=GOLDL, size=40, lx=None, ly=None):
    """pop-in tag with optional leader line to (lx, ly)"""
    p = pop(t, t0, 0.3)
    rec(t0, 'pop')
    if p <= 0.01:
        return
    if lx is not None:
        c.move_to(x, y); c.line_to(lerp(x, lx, eout(seg(t, t0, t0 + 0.3))), lerp(y, ly, eout(seg(t, t0, t0 + 0.3))))
        rgba(c, col, 0.9); c.set_line_width(3); c.stroke()
        c.arc(lx, ly, 7 * p, 0, TAU); rgba(c, col); c.fill()
    c.save(); c.translate(x, y); c.scale(p, p)
    tagbox(c, s_, 0, 0, 1.0, col, size)
    c.restore()


def note(c, s_, t, x=80, y=1050):
    text(c, s_, x, y, 26, (0.80, 0.80, 0.84), fin(t, 0.3), shadow=0.6)


def panel(c, x, y, w, h, a=1.0, col=(0.14, 0.09, 0.08), edge=GOLDD):
    rr(c, x, y, w, h, 14); c.set_source_rgba(col[0], col[1], col[2], 0.88 * a); c.fill_preserve()
    rgba(c, edge, a); c.set_line_width(2.5); c.stroke()


def arrow(c, x0, y0, x1, y1, col=GOLDL, a=1.0, w=8, p=1.0):
    if p <= 0:
        return
    xe, ye = lerp(x0, x1, p), lerp(y0, y1, p)
    c.move_to(x0, y0); c.line_to(xe, ye); rgba(c, col, a); c.set_line_width(w); c.stroke()
    ang = math.atan2(y1 - y0, x1 - x0)
    c.move_to(xe + math.cos(ang) * 18, ye + math.sin(ang) * 18)
    c.line_to(xe + math.cos(ang + 2.5) * 22, ye + math.sin(ang + 2.5) * 22)
    c.line_to(xe + math.cos(ang - 2.5) * 22, ye + math.sin(ang - 2.5) * 22); c.close_path(); c.fill()


def cross(c, x, y, r, t, t0, col=REDL):
    p = eout(seg(t, t0, t0 + 0.3))
    if p <= 0:
        return
    rec(t0, 'seal')
    c.set_line_cap(cairo.LINE_CAP_ROUND); rgba(c, col); c.set_line_width(12)
    c.move_to(x - r, y - r); c.line_to(x - r + 2 * r * p, y - r + 2 * r * p); c.stroke()
    if p > 0.5:
        q = (p - 0.5) * 2
        c.move_to(x + r, y - r); c.line_to(x + r - 2 * r * q, y - r + 2 * r * q); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)


# =================================================================== 0 钩子（冷蓝）
