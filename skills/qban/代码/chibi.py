"""chibi.py —— 大头Q版历史人物（cairo 矢量，逐帧可动）

用法：
    from chibi import chibi
    chibi(c, x, yf, s=1.0, era='tang', role='official', pose='bow', face=1,
          expr='calm', walk=None, prop=None, T=0, a=1.0, robe=None)

坐标：x 为人物中心，yf 为脚底线；s=1 时全身约 300px，头直径约 136px（头身比约 1:1.2）。
era  : 'qinhan' | 'tang' | 'song' | 'ming' | 'qing' —— 决定帽子/发型/服饰细节
role : 'official' 官员 | 'scholar' 书生 | 'emperor' 皇帝 | 'peasant' 农民 | 'soldier' 士兵
       | 'merchant' 商人 | 'lady' 女子 | 'kid' 小孩
pose : 'stand' | 'bow' 作揖 | 'kneel' 跪 | 'raise' 举手/举杯 | 'hold' 双手捧物 | 'point' 指
       | 'cheer' 欢呼 | 'think' 托腮
expr : 'calm' | 'happy' | 'shock' | 'sad' | 'angry' | 'sleep'
walk : None 或相位（弧度，随时间递增即走路+弹跳）
prop : None | 'scroll' 卷轴 | 'cup' 酒杯 | 'tablet' 笏板 | 'hoe' 锄头 | 'spear' 长枪
       | 'lantern' 灯笼 | 'seal' 印 | 'coin' 铜钱 | 'book' 书 | 'token' 令牌 | 'sickle' 镰刀
T    : 全局时间（秒），用于眨眼、呼吸、灯笼摆动
"""
import math
import cairocffi as cairo

SKIN = (0.98, 0.86, 0.74)
BLUSH = (0.95, 0.55, 0.50)
INK = (0.13, 0.09, 0.08)
HAIR = (0.12, 0.09, 0.08)
LINE = (0.16, 0.10, 0.08)
RIM = (0.62, 0.50, 0.40)   # 黑色帽子/头发的亮边
GOLD = (0.92, 0.70, 0.30)
GOLDL = (1.0, 0.85, 0.48)
RED = (0.76, 0.18, 0.14)
CREAM = (0.95, 0.89, 0.76)
BROWN = (0.48, 0.32, 0.20)
STEEL = (0.80, 0.82, 0.85)

# 朝代 × 身份 → 袍色
ROBES = {
    ('tang', 'official'): (0.55, 0.25, 0.55),   # 唐 紫/绯/绿/青 按品级，默认紫
    ('song', 'official'): (0.72, 0.20, 0.16),
    ('ming', 'official'): (0.74, 0.17, 0.15),   # 明 绯袍 + 补子
    ('qing', 'official'): (0.14, 0.15, 0.24),   # 清 石青补褂
    ('qinhan', 'official'): (0.16, 0.14, 0.14), # 秦尚黑
    ('nanbei', 'official'): (0.30, 0.32, 0.50), # 南北朝 褒衣博带
    ('han', 'official'): (0.48, 0.16, 0.14),
    'bandit': (0.24, 0.20, 0.18),
    'emperor': (0.95, 0.72, 0.22),
    'scholar': (0.86, 0.82, 0.70),
    'peasant': (0.60, 0.50, 0.36),
    'soldier': (0.62, 0.20, 0.16),
    'merchant': (0.30, 0.42, 0.50),
    'lady': (0.86, 0.42, 0.40),
    'kid': (0.40, 0.58, 0.66),
}


def _rgba(c, col, a):
    c.set_source_rgba(col[0], col[1], col[2], a)


def _dk(col, k=0.72):
    return tuple(v * k for v in col)


def _fill_line(c, col, a, w=3.2):
    """填色 + 干净深色描边（规则：线条清楚，不要光晕）"""
    _rgba(c, col, a); c.fill_preserve()
    # 深色帽/发在暗背景上会消失：改用暖灰亮边勾出轮廓
    _rgba(c, RIM if sum(col[:3]) < 0.6 else LINE, a); c.set_line_width(w); c.stroke()


def _ell(c, x, y, rx, ry):
    c.save(); c.translate(x, y); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()


def _rr(c, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


def _robe_col(era, role, robe):
    if robe:
        return robe
    return ROBES.get((era, role)) or ROBES.get(role) or ROBES['scholar']


# ------------------------------------------------------------------ face
def _face(c, expr, T, a, hx=6, hy=-200):
    """三分侧：五官整体向朝向一侧偏 hx"""
    blink = (T % 3.7) > 3.58
    ey = hy + 8
    ex1, ex2 = hx - 24, hx + 20
    _rgba(c, INK, a)
    if expr == 'sleep' or blink:
        c.set_line_width(4); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for ex in (ex1, ex2):
            c.move_to(ex - 8, ey); c.curve_to(ex - 4, ey + 5, ex + 4, ey + 5, ex + 8, ey); c.stroke()
    elif expr == 'happy':
        c.set_line_width(4.5); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for ex in (ex1, ex2):
            c.move_to(ex - 8, ey + 3); c.curve_to(ex - 4, ey - 7, ex + 4, ey - 7, ex + 8, ey + 3); c.stroke()
    elif expr == 'shock':
        for ex in (ex1, ex2):
            _ell(c, ex, ey, 8, 10); c.fill()
            _rgba(c, (1, 1, 1), a); c.arc(ex + 2, ey - 3, 3, 0, 6.283); c.fill(); _rgba(c, INK, a)
    else:
        for ex in (ex1, ex2):
            _ell(c, ex, ey, 6, 8); c.fill()
            _rgba(c, (1, 1, 1), a); c.arc(ex + 2, ey - 3, 2.2, 0, 6.283); c.fill(); _rgba(c, INK, a)
    # 眉
    c.set_line_width(3.5); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if expr == 'angry':
        c.move_to(ex1 - 10, ey - 20); c.line_to(ex1 + 8, ey - 13); c.stroke()
        c.move_to(ex2 + 10, ey - 20); c.line_to(ex2 - 8, ey - 13); c.stroke()
    elif expr == 'sad':
        c.move_to(ex1 - 10, ey - 13); c.line_to(ex1 + 8, ey - 20); c.stroke()
        c.move_to(ex2 + 10, ey - 13); c.line_to(ex2 - 8, ey - 20); c.stroke()
    # 腮红
    _rgba(c, BLUSH, 0.55 * a)
    _ell(c, ex1 - 6, ey + 18, 10, 6); c.fill(); _ell(c, ex2 + 6, ey + 18, 10, 6); c.fill()
    # 嘴
    mx, my = hx - 2, ey + 22
    _rgba(c, INK, a); c.set_line_width(3.5)
    if expr == 'shock':
        _ell(c, mx, my + 2, 6, 8); c.fill()
    elif expr == 'happy':
        c.move_to(mx - 8, my - 2); c.curve_to(mx - 4, my + 8, mx + 4, my + 8, mx + 8, my - 2); c.close_path()
        _rgba(c, (0.70, 0.22, 0.20), a); c.fill()
    elif expr in ('sad', 'angry'):
        c.move_to(mx - 6, my + 4); c.curve_to(mx - 2, my - 2, mx + 2, my - 2, mx + 6, my + 4); c.stroke()
    else:
        c.move_to(mx - 5, my); c.curve_to(mx - 2, my + 4, mx + 2, my + 4, mx + 5, my); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    if expr == 'sad':  # 泪滴
        _rgba(c, (0.55, 0.78, 0.95), a); c.move_to(ex2 + 4, ey + 8)
        c.curve_to(ex2 + 12, ey + 22, ex2 - 4, ey + 26, ex2 + 4, ey + 8); c.fill()


# ------------------------------------------------------------------ hats / hair
def _hair_base(c, a, hy=-200, r=68):
    c.arc(0, hy, r + 1, math.pi * 1.02, math.pi * 1.98); c.close_path(); _fill_line(c, HAIR, a, 2.6)


def _headwear(c, era, role, a, T, hy=-200, r=68):
    top = hy - r
    if role == 'lady':
        _hair_base(c, a, hy, r)
        _rgba(c, HAIR, a)
        if era == 'tang':           # 唐 高髻
            _ell(c, -6, top - 22, 30, 34); _fill_line(c, HAIR, a, 2.6); _ell(c, -34, top + 2, 22, 22); _fill_line(c, HAIR, a, 2.6)
            _rgba(c, GOLD, a); c.arc(16, top - 18, 7, 0, 6.283); c.fill()
            c.set_line_width(3); c.move_to(16, top - 18); c.line_to(42, top - 34); c.stroke()
            _rgba(c, RED, a); _ell(c, 0, hy - 30, 4, 6); c.fill()   # 花钿
        elif era == 'qing':          # 清 两把头
            _rr(c, -70, top - 30, 140, 26, 10); _fill_line(c, HAIR, a, 2.6)
            _rgba(c, (0.85, 0.30, 0.45), a); c.arc(40, top - 22, 11, 0, 6.283); c.fill()
        else:                        # 宋明 发髻
            _ell(c, -10, top - 12, 26, 22); _fill_line(c, HAIR, a, 2.6)
            _rgba(c, GOLD, a); c.set_line_width(4); c.move_to(-40, top - 14); c.line_to(22, top - 22); c.stroke()
        return
    if role == 'kid':
        _hair_base(c, a, hy, r); _rgba(c, HAIR, a)
        c.arc(-40, top + 4, 20, 0, 6.283); _fill_line(c, HAIR, a, 2.6); c.arc(40, top + 4, 20, 0, 6.283); _fill_line(c, HAIR, a, 2.6)  # 双丫髻
        _rgba(c, RED, a); c.rectangle(-46, top + 18, 16, 5); c.fill(); c.rectangle(30, top + 18, 16, 5); c.fill()
        return
    if role == 'peasant':
        _hair_base(c, a, hy, r)
        c.move_to(-100, top + 34); c.line_to(0, top - 30); c.line_to(100, top + 34); c.close_path()   # 斗笠
        _fill_line(c, (0.90, 0.78, 0.50), a)
        _rgba(c, (0.66, 0.52, 0.30), a); c.set_line_width(2)
        for k in (-60, -30, 0, 30, 60):
            c.move_to(0, top - 28); c.line_to(k * 1.55, top + 32); c.stroke()
        return
    if role == 'soldier':
        c.arc(0, hy - 6, r + 6, math.pi, 2 * math.pi); c.close_path(); _fill_line(c, STEEL if era != 'qinhan' else (0.55, 0.45, 0.32), a)
        _rgba(c, RED, a); c.move_to(-6, top - 6); c.curve_to(-20, top - 40, 20, top - 44, 10, top - 6); c.fill()  # 红缨
        _rgba(c, _dk(STEEL), a); c.rectangle(-r - 8, hy - 10, 2 * r + 16, 10); c.fill()
        return
    if era == 'qing':
        _hair_base(c, a, hy, r)
        # 辫子
        _rgba(c, HAIR, a); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(-50, hy + 10); c.curve_to(-78, hy + 60, -66, hy + 110, -80, hy + 150 + 4 * math.sin(T * 3)); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_BUTT)
        if role in ('official', 'emperor', 'merchant', 'scholar'):
            c.move_to(-r - 6, top + 34); c.line_to(r + 6, top + 34); c.line_to(r - 4, top + 6); c.line_to(-r + 4, top + 6); c.close_path()
            _fill_line(c, (0.16, 0.13, 0.12), a)                          # 暖帽沿
            c.arc(0, top + 12, r - 10, math.pi, 2 * math.pi); c.close_path(); _fill_line(c, (0.85, 0.16, 0.12), a)  # 红缨顶
            bead = GOLDL if role == 'emperor' else ((0.25, 0.45, 0.85) if role == 'official' else (0.4, 0.3, 0.25))
            _rgba(c, bead, a); c.arc(0, top - 50, 11, 0, 6.283); c.fill()
        return
    if role == 'bandit':
        _hair_base(c, a, hy, r)
        _ell(c, -4, top - 4, 24, 18); _fill_line(c, HAIR, a, 2.6)
        _rgba(c, RED, a); c.rectangle(-r, hy - 46, 2 * r, 14); c.fill()
        c.set_line_width(7); c.move_to(-r + 4, hy - 40); c.curve_to(-r - 30, hy - 30, -r - 40, hy - 10 + 4 * math.sin(T * 4), -r - 50, hy + 6); c.stroke()
        return
    if era == 'nanbei' and role in ('official', 'scholar'):   # 笼冠（漆纱笼冠）
        _hair_base(c, a, hy, r)
        if role == 'official':
            c.move_to(-58, top + 30); c.line_to(-46, top - 58); c.line_to(46, top - 58); c.line_to(58, top + 30); c.close_path()
            _rgba(c, (0.10, 0.09, 0.09), 0.78 * a); c.fill_preserve(); _rgba(c, RIM, a); c.set_line_width(3); c.stroke()
            _rgba(c, RIM, 0.5 * a); c.set_line_width(1.5)
            for k in range(1, 6):
                yy = top + 30 - k * 15; c.move_to(-58 + k * 2, yy); c.line_to(58 - k * 2, yy); c.stroke()
            _rgba(c, (0.85, 0.75, 0.55), a); c.set_line_width(3); c.move_to(-56, hy - 6); c.curve_to(-50, hy + 44, 40, hy + 54, 52, hy - 6); c.stroke()
        else:
            _ell(c, -2, top - 4, 24, 20); _fill_line(c, HAIR, a, 2.6)
            _rgba(c, (0.2, 0.18, 0.16), a); c.rectangle(-18, top - 20, 36, 12); c.fill()
        return
    # ---- 冠帽类
    if role == 'emperor':
        _hair_base(c, a, hy, r)
        if era in ('qinhan', 'tang', 'song', 'ming', 'nanbei'):
            # 冕旒：平板 + 前后垂珠
            c.move_to(-r - 18, top - 4); c.line_to(r + 18, top - 14); c.line_to(r + 18, top - 2); c.line_to(-r - 18, top + 8); c.close_path()
            _fill_line(c, HAIR, a)
            _rr(c, -30, top - 4, 60, 30, 8); _fill_line(c, HAIR, a)
            for k in range(7):
                xx = -r - 8 + k * (2 * r + 16) / 6; yy = top + 6 - k * 1.6
                _rgba(c, GOLD, a); c.set_line_width(2); c.move_to(xx, yy); c.line_to(xx, yy + 34); c.stroke()
                _rgba(c, (0.95, 0.30, 0.25) if k % 2 else GOLDL, a); c.arc(xx, yy + 38, 5, 0, 6.283); c.fill()
        return
    if era == 'qinhan':                    # 冠：长冠/高冠 + 缨
        _hair_base(c, a, hy, r)
        _ell(c, 0, top + 2, 22, 16); _fill_line(c, HAIR, a, 2.6)
        c.move_to(-14, top + 4); c.curve_to(-20, top - 70, 30, top - 80, 26, top + 4); c.close_path()
        _fill_line(c, (0.10, 0.08, 0.07), a)
        _rgba(c, (0.85, 0.75, 0.55), a); c.set_line_width(3); c.move_to(-56, hy - 10); c.curve_to(-50, hy + 40, 40, hy + 50, 52, hy - 10); c.stroke()
        return
    if role in ('scholar', 'merchant') and era in ('tang', 'song'):   # 唐宋书生/商人：幅巾
        era = '_plain'
    if era == 'tang':                       # 唐 软脚幞头：圆顶 + 两条下垂软脚
        c.arc(0, hy - 8, r + 4, math.pi * 1.0, math.pi * 2.0); c.close_path(); _fill_line(c, HAIR, a)
        _ell(c, -4, top - 4, 34, 30); _fill_line(c, HAIR, a)
        _rgba(c, HAIR, a); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND)
        sw = 5 * math.sin(T * 2.2)
        c.move_to(-50, top + 16); c.curve_to(-92, top + 30, -96 + sw, top + 80, -86 + sw, top + 112); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_BUTT)
        return
    if era == 'song':                       # 宋 直脚幞头：长长的平直双翅
        c.arc(0, hy - 8, r + 4, math.pi, 2 * math.pi); c.close_path(); _fill_line(c, HAIR, a)
        _rr(c, -44, top - 30, 88, 44, 14); _fill_line(c, HAIR, a)
        wob = 2 * math.sin(T * 3)
        c.rectangle(-170, top - 6 + wob, 340, 11); _fill_line(c, HAIR, a, 2.4)
        return
    if era == 'ming':                       # 明 乌纱帽：前低后高 + 两侧椭圆展角；书生戴网巾/方巾
        if role == 'scholar':
            c.arc(0, hy - 8, r + 4, math.pi, 2 * math.pi); c.close_path(); _fill_line(c, HAIR, a)
            c.move_to(-50, top + 20); c.line_to(-46, top - 34); c.line_to(46, top - 34); c.line_to(50, top + 20); c.close_path()
            _fill_line(c, HAIR, a)  # 四方平定巾
            return
        c.arc(0, hy - 8, r + 4, math.pi, 2 * math.pi); c.close_path(); _fill_line(c, HAIR, a)
        _rr(c, -40, top - 34, 80, 50, 18); _fill_line(c, HAIR, a)
        for sg in (-1, 1):
            c.save(); c.translate(sg * 92, top - 6); c.rotate(sg * 0.12)
            _ell(c, 0, 0, 34, 15); c.restore(); _fill_line(c, HAIR, a, 2.4)
            _rgba(c, HAIR, a); c.set_line_width(4); c.move_to(sg * 40, top - 6); c.line_to(sg * 60, top - 6); c.stroke()
        return
    # 默认：书生幅巾
    c.arc(0, hy - 8, r + 4, math.pi, 2 * math.pi); c.close_path(); _fill_line(c, HAIR, a)
    _ell(c, -6, top - 6, 26, 20); _fill_line(c, HAIR, a)


# ------------------------------------------------------------------ props
def _prop(c, prop, x, y, a, T):
    if prop is None:
        return
    if prop == 'scroll':
        _rr(c, x - 10, y - 46, 20, 92, 4); _fill_line(c, CREAM, a, 2.4)
        _rgba(c, BROWN, a); c.rectangle(x - 15, y - 52, 30, 8); c.fill(); c.rectangle(x - 15, y + 44, 30, 8); c.fill()
    elif prop == 'cup':
        c.move_to(x - 16, y - 18); c.line_to(x + 16, y - 18); c.line_to(x + 8, y + 6); c.line_to(x - 8, y + 6); c.close_path()
        _fill_line(c, GOLD, a, 2.4)
        _rgba(c, GOLD, a); c.rectangle(x - 3, y + 6, 6, 10); c.fill(); c.rectangle(x - 10, y + 14, 20, 4); c.fill()
    elif prop == 'tablet':   # 笏板
        _rr(c, x - 9, y - 60, 18, 84, 7); _fill_line(c, (0.94, 0.92, 0.84), a, 2.4)
    elif prop in ('hoe', 'spear', 'sickle'):
        _rgba(c, BROWN, a); c.set_line_width(7); c.move_to(x, y + 70); c.line_to(x, y - 130); c.stroke()
        if prop == 'hoe':
            c.move_to(x, y - 130); c.line_to(x + 36, y - 120); c.line_to(x + 30, y - 98); c.line_to(x, y - 112); c.close_path(); _fill_line(c, STEEL, a, 2.4)
        elif prop == 'spear':
            c.move_to(x, y - 180); c.line_to(x + 11, y - 130); c.line_to(x - 11, y - 130); c.close_path(); _fill_line(c, STEEL, a, 2.4)
            _rgba(c, RED, a); c.arc(x, y - 124, 9, 0, 6.283); c.fill()
        else:
            c.new_path(); c.arc(x + 26, y - 130, 26, math.pi, 1.9 * math.pi); _rgba(c, STEEL, a); c.set_line_width(8); c.stroke()
    elif prop == 'lantern':
        sw = 0.12 * math.sin(T * 2.5)
        c.save(); c.translate(x, y); c.rotate(sw)
        _rgba(c, BROWN, a); c.set_line_width(3); c.move_to(0, 0); c.line_to(0, 26); c.stroke()
        g = cairo.RadialGradient(0, 56, 0, 0, 56, 70); g.add_color_stop_rgba(0, 1, 0.8, 0.4, 0.45 * a); g.add_color_stop_rgba(1, 1, 0.8, 0.4, 0)
        c.set_source(g); c.arc(0, 56, 70, 0, 6.283); c.fill()
        _ell(c, 0, 56, 24, 30); _fill_line(c, RED, a, 2.4)
        _rgba(c, GOLD, a); c.rectangle(-14, 24, 28, 6); c.fill(); c.rectangle(-14, 82, 28, 6); c.fill()
        c.restore()
    elif prop == 'seal':
        _rr(c, x - 18, y - 22, 36, 36, 6); _fill_line(c, RED, a, 2.4)
        _rgba(c, GOLD, a); c.arc(x, y - 30, 10, 0, 6.283); c.fill()
    elif prop == 'coin':
        c.arc(x, y, 22, 0, 6.283); _fill_line(c, GOLD, a, 2.4)
        _rgba(c, _dk(GOLD, 0.6), a); c.rectangle(x - 7, y - 7, 14, 14); c.fill()
    elif prop == 'book':
        _rr(c, x - 26, y - 20, 52, 38, 4); _fill_line(c, (0.30, 0.40, 0.55), a, 2.4)
        _rgba(c, CREAM, a); c.rectangle(x - 14, y - 14, 10, 26); c.fill()
    elif prop == 'token':   # 令牌
        c.move_to(x - 18, y + 30); c.line_to(x - 18, y - 30); c.line_to(x, y - 44); c.line_to(x + 18, y - 30); c.line_to(x + 18, y + 30); c.close_path()
        _fill_line(c, (0.80, 0.62, 0.26), a, 2.4)
        _rgba(c, RED, a); c.rectangle(x - 9, y - 20, 18, 36); c.fill()


# ------------------------------------------------------------------ main
def chibi(c, x, yf, s=1.0, era='tang', role='official', pose='stand', face=1, expr='calm',
          walk=None, prop=None, T=0.0, a=1.0, robe=None, p=1.0, belly=0.0, hair=None, tear=0.0, sweat=0.0):
    """p: 动作完成度 0→1（作揖弯腰、下跪、举手的过渡），配合 ease() 用"""
    if a <= 0:
        return
    global HAIR
    _oh = HAIR
    if hair: HAIR = hair
    col = _robe_col(era, role, robe)
    dcol = _dk(col)
    c.save(); c.translate(x, yf); c.scale(s * face, s)
    c.set_line_join(cairo.LINE_JOIN_ROUND)

    hop = -abs(math.sin(walk)) * 14 if walk is not None else 0
    breathe = 2.0 * math.sin(T * 2.4)
    sw = math.sin(walk) * 12 if walk is not None else 0

    # 影子
    _rgba(c, (0, 0, 0), 0.25 * a); _ell(c, 0, 0, 60, 10); c.fill()

    kneel = p if pose == 'kneel' else 0.0
    c.translate(0, hop + 34 * kneel)

    # 脚
    if kneel < 0.5:
        for fx in (-20 + sw, 18 - sw):
            _ell(c, fx + 6, -6, 17, 9); _fill_line(c, INK, a, 2)
    # 身体（短袍，梯形圆角）
    bw_top, bw_bot, by0 = 40, 62, -128 + breathe * 0.3
    if pose == 'kneel':
        bw_bot = 70 + 10 * kneel
    c.move_to(-bw_top, by0); c.line_to(bw_top, by0)
    c.curve_to(bw_top + 8, by0 + 50, bw_bot, -40, bw_bot + 2, -8)
    c.curve_to(20, -2, -20, -2, -bw_bot - 2, -8)
    c.curve_to(-bw_bot, -40, -bw_top - 8, by0 + 50, -bw_top, by0)
    c.close_path(); _fill_line(c, col, a)
    if belly > 0:
        _ell(c, 34, -58, 34 * belly, 40 * belly); _fill_line(c, col, a)
    # 交领 / 圆领
    _rgba(c, LINE, a); c.set_line_width(3)
    if era == 'tang' or era == 'song':
        c.move_to(-26, by0 + 2); c.curve_to(-10, by0 + 22, 10, by0 + 22, 26, by0 + 2); c.stroke()   # 圆领袍
    else:
        _rgba(c, CREAM, a); c.set_line_width(7)
        c.move_to(-22, by0 + 2); c.line_to(16, by0 + 46); c.stroke()                               # 交领
        _rgba(c, LINE, a); c.set_line_width(2); c.move_to(-22, by0 + 2); c.line_to(16, by0 + 46); c.stroke()
    # 腰带
    belt = GOLD if role in ('official', 'emperor') else _dk(col, 0.55)
    _rr(c, -bw_top - 10, -82, 2 * bw_top + 20, 12, 5); _fill_line(c, belt, a, 2)
    # 补子（明清官员）
    if role == 'official' and era in ('ming', 'qing'):
        _rr(c, -20, by0 + 20, 40, 34, 4); _fill_line(c, (0.95, 0.80, 0.42), a, 2)
        _rgba(c, RED if era == 'ming' else (0.30, 0.50, 0.80), a); c.arc(0, by0 + 37, 8, 0, 6.283); c.fill()
    if role == 'emperor':
        _rgba(c, RED, a); c.set_line_width(4)
        c.move_to(-24, by0 + 30); c.curve_to(-6, by0 + 12, 6, by0 + 50, 24, by0 + 30); c.stroke()  # 龙纹示意
    if role == 'soldier':
        _rr(c, -bw_top + 4, by0 + 8, 2 * bw_top - 8, 40, 6); _fill_line(c, STEEL if era != 'qinhan' else (0.55, 0.45, 0.32), a, 2.4)

    # 手臂（短粗袖子 + 圆手）
    sl = dcol
    hand = None   # 主手（前手）位置，用于道具
    c.set_line_cap(cairo.LINE_CAP_ROUND)

    def arm(x0, y0, x1, y1, w=26):
        _rgba(c, LINE, a); c.set_line_width(w + 6); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
        _rgba(c, sl, a); c.set_line_width(w); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
        c.arc(x1, y1, 11, 0, 6.283); _fill_line(c, SKIN, a, 2.6)

    bow = p if pose == 'bow' else 0.0
    if pose == 'bow':
        arm(30, by0 + 16, 34 + 4 * bow, by0 + 44 - 6 * bow)
        hand = (40, by0 + 40)
    elif pose == 'raise':
        ex = 40 + 36 * p; ey = by0 + 40 - 100 * p
        arm(30, by0 + 16, ex, ey); hand = (ex + 4, ey - 12)
        arm(-28, by0 + 16, -48, by0 + 64)
    elif pose == 'cheer':
        arm(30, by0 + 16, 58, by0 - 60 * p + 40); arm(-28, by0 + 16, -58, by0 - 60 * p + 40)
        hand = (60, by0 - 60 * p + 30)
    elif pose == 'point':
        arm(-28, by0 + 16, -46, by0 + 64)
        arm(30, by0 + 16, 30 + 60 * p, by0 + 30 - 16 * p); hand = (34 + 60 * p, by0 + 26 - 16 * p)
        _rgba(c, SKIN, a); c.set_line_width(7); c.move_to(hand[0], hand[1] + 2); c.line_to(hand[0] + 16, hand[1]); c.stroke()
    elif pose == 'hold':
        arm(-26, by0 + 16, 16, by0 + 52); arm(30, by0 + 16, 46, by0 + 50); hand = (34, by0 + 40)
    elif pose == 'think':
        arm(-28, by0 + 16, -46, by0 + 64); arm(30, by0 + 16, 34, by0 - 6); hand = (36, by0 - 10)
    elif pose == 'kneel':
        arm(30, by0 + 16, 40, by0 + 60 + 14 * kneel); arm(-28, by0 + 16, -36, by0 + 60 + 14 * kneel)
        hand = (44, by0 + 60)
    else:
        swa = math.sin(walk) * 14 if walk is not None else 0
        arm(-28, by0 + 16, -46 - swa, by0 + 64); arm(30, by0 + 16, 46 + swa, by0 + 64); hand = (50 + swa, by0 + 60)
    c.set_line_cap(cairo.LINE_CAP_BUTT)

    # 头（大头：r=68，作揖时前倾）
    c.save()
    if bow:
        c.translate(6 * bow, 4 * bow); c.rotate(0.14 * bow)
    if pose == 'kneel':
        c.translate(6 * kneel, 6 * kneel); c.rotate(0.15 * kneel)
    hy = -200 + breathe
    _rgba(c, SKIN, a); c.rectangle(-12, hy + 56, 24, 22); c.fill()   # 脖
    _ell(c, 0, hy, 68, 64); _fill_line(c, SKIN, a)
    c.arc(-62, hy + 6, 11, 0, 6.283); _fill_line(c, SKIN, a, 2.4)    # 耳（后侧）
    _headwear(c, era, role, a, T, hy, 68)
    _face(c, expr, T, a, 8, hy)
    if pose == 'think':
        c.set_line_width(5); _rgba(c, GOLDL, a)
        c.select_font_face("Noto Serif CJK SC", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        c.set_font_size(56); c.move_to(54, hy - 64); c.show_text('?')
    c.restore()

    # 作揖：双手合抱于胸前（画在头前一层）
    if pose == 'bow':
        _rr(c, 18, by0 + 30 - 8 * bow, 44, 30, 14); _fill_line(c, sl, a, 2.6)
        c.arc(56, by0 + 42 - 8 * bow, 12, 0, 6.283); _fill_line(c, SKIN, a, 2.4)

    if hand and prop:
        _prop(c, prop, hand[0], hand[1], a, T)
    if sweat > 0:
        for k, (dx, dy) in enumerate(((58, -250), (70, -215))):
            ph = (T * 1.2 + k * 0.5) % 1.0
            _rgba(c, (0.65, 0.85, 1.0), sweat * a * (1 - ph * 0.6)); yy = dy + ph * 30
            c.move_to(dx, yy - 14); c.curve_to(dx + 9, yy, dx + 7, yy + 9, dx, yy + 9); c.curve_to(dx - 7, yy + 9, dx - 9, yy, dx, yy - 14); c.fill()
    if tear > 0:
        for k, dx in enumerate((-16, 28)):
            ph = (T * 1.6 + k * 0.37) % 1.0
            _rgba(c, (0.55, 0.80, 1.0), tear * a * (1 - ph)); c.arc(dx, -186 + ph * 70, 6, 0, 6.283); c.fill()
    c.restore()
    HAIR = _oh


if __name__ == '__main__':
    # 自检：输出一张角色总表 chibi_sheet.png
    W, H = 1920, 1080
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.20, 0.13, 0.10); g.add_color_stop_rgb(1, 0.10, 0.07, 0.06)
    c.set_source(g); c.paint()
    rows = [
        [('qinhan', 'official', 'bow', 'calm', 'tablet'), ('tang', 'official', 'stand', 'calm', 'tablet'),
         ('song', 'official', 'hold', 'happy', 'scroll'), ('ming', 'official', 'point', 'angry', None),
         ('qing', 'official', 'stand', 'calm', 'seal'), ('tang', 'emperor', 'raise', 'happy', 'cup')],
        [('song', 'scholar', 'think', 'calm', None), ('ming', 'peasant', 'stand', 'sad', 'sickle'),
         ('song', 'soldier', 'stand', 'angry', 'spear'), ('tang', 'lady', 'hold', 'happy', 'lantern'),
         ('qing', 'merchant', 'cheer', 'happy', 'coin'), ('ming', 'kid', 'kneel', 'shock', None)],
    ]
    font_ok = True
    for ri, row in enumerate(rows):
        for ci, (era, role, pose, expr, prop) in enumerate(row):
            x = 180 + ci * 312; yf = 470 + ri * 500
            chibi(c, x, yf, 1.0, era, role, pose, 1, expr, None, prop, T=1.0)
            c.select_font_face("Noto Serif CJK SC", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            c.set_font_size(30); c.set_source_rgb(1, 0.85, 0.48)
            t = f"{era}·{role}·{pose}"; e = c.text_extents(t); c.move_to(x - e[2] / 2, yf + 44); c.show_text(t)
    surf.write_to_png('chibi_sheet.png'); print('chibi_sheet.png')
