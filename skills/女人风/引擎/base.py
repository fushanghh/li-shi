# 随份子从哪儿来 —— 画布、外框、字幕、镜头工具
from ppl import *
import re, random

FW, FH = 1440, 1080          # 成片 4:3
SW, SH = 1920, 1080          # 场景画布
SC = 0.75; SY = 44           # 场景缩放与放置（1440×810 放在 y=44）
FPS = 24
BEAT = 60.0 / BPM; BAR = BEAT * 4; HALF = BEAT * 2
BLUE = (49 / 255, 82 / 255, 135 / 255); RED = (157 / 255, 64 / 255, 39 / 255); GREEN = (60 / 255, 110 / 255, 70 / 255); INK = (34 / 255, 19 / 255, 5 / 255)
NAMES = ['刘邦', '吕公', '萧何', '柴家娘', '尼功德进', '功德进', '贾母', '王熙凤', '凤姐', '薛姨妈', '邢夫人', '王夫人', '荀子']
SERIF = 'Noto Serif CJK SC'

def rect(c, x0, y0, x1, y1, fill, lw=2.4): shape(c, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, lw, n=1)
def surf(w=SW, h=SH): s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); return s, cairo.Context(s)

_bgc = {}
def bg_cached(key, fn):
    if key not in _bgc:
        s, c = surf(); fn(c); s.flush(); _bgc[key] = s
    return _bgc[key]

# ---------- 环境动态 ----------
def clouds(c, t, y=120, n=4, col=hx('f6efe0'), sp=14, seed=1):
    r = random.Random(seed)
    for i in range(n):
        x = (r.uniform(0, 2200) + t * sp * (0.6 + 0.4 * r.random())) % 2300 - 200; yy = y + r.uniform(-50, 60); w = r.uniform(120, 220)
        for k in range(4): ell(c, x + k * w * 0.28, yy - (k % 2) * 16, w * 0.3, w * 0.16, col, 2)
        ink(c, [(x - 10, yy + 18), (x + w * 0.9, yy + 18)], 2, LINE, 1, 2)

def birds(c, t, y=180, n=4, seed=2):
    r = random.Random(seed)
    for i in range(n):
        x = (r.uniform(0, 1920) + t * 60) % 2100 - 100; yy = y + r.uniform(-40, 40) + math.sin(t * 2 + i) * 8; f = math.sin(t * 10 + i * 2) * 8
        ink(c, [(x - 16, yy - f), (x, yy), (x + 16, yy - f)], 3, LINE, 1.2, 4)

def dust(c, t, n=30, seed=3, box=(0, 0, 1920, 900), col=hx('fff6dc'), a=0.5):
    r = random.Random(seed)
    for i in range(n):
        x = box[0] + (r.uniform(0, box[2]) + t * r.uniform(5, 20)) % box[2]; y = box[1] + (r.uniform(0, box[3]) - t * r.uniform(3, 12)) % box[3]
        c.set_source_rgba(*col, a * (0.5 + 0.5 * math.sin(t * 2 + i))); c.arc(x, y, r.uniform(2, 4), 0, TAU); c.fill()

def flame(c, x, y, t, s=1.0, ph=0):
    f = 1 + 0.12 * math.sin(t * 17 + ph) + 0.08 * math.sin(t * 29 + ph * 2)
    rg = cairo.RadialGradient(x, y - 10 * s, 2, x, y - 10 * s, 70 * s); rg.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.45); rg.add_color_stop_rgba(1, 1, 0.8, 0.4, 0)
    c.set_source(rg); c.arc(x, y - 10 * s, 70 * s, 0, TAU); c.fill()
    shape(c, [(x, y - 34 * s * f), (x + 9 * s, y - 8 * s), (x, y + 2 * s), (x - 9 * s, y - 8 * s)], hx('f2b13c'), 1.4)
    shape(c, [(x, y - 20 * s * f), (x + 4 * s, y - 6 * s), (x - 4 * s, y - 6 * s)], hx('fff0b0'), 0)

def glow(c, x, y, r, col=(1, .9, .6), a=0.5):
    rg = cairo.RadialGradient(x, y, 1, x, y, r); rg.add_color_stop_rgba(0, *col, a); rg.add_color_stop_rgba(1, *col, 0); c.set_source(rg); c.arc(x, y, r, 0, TAU); c.fill()

def sparks(c, x, y, k, n=14, col=hx('f2c14e'), R=160, seed=4):
    if k <= 0 or k >= 1: return
    r = random.Random(seed)
    for i in range(n):
        a = r.uniform(0, TAU); d = R * ease(k) * r.uniform(0.5, 1.1)
        c.save(); c.translate(x + math.cos(a) * d, y + math.sin(a) * d); c.rotate(a)
        c.set_source_rgba(*col, 1 - k); c.move_to(-10, 0); c.line_to(0, -4); c.line_to(10, 0); c.line_to(0, 4); c.close_path(); c.fill(); c.restore()

def beams(c, x, y, t, n=10, R=900, col=(1, .93, .7), a=0.18):
    for i in range(n):
        ang = i / n * TAU + t * 0.2
        c.move_to(x, y); c.line_to(x + math.cos(ang - 0.08) * R, y + math.sin(ang - 0.08) * R); c.line_to(x + math.cos(ang + 0.08) * R, y + math.sin(ang + 0.08) * R); c.close_path()
        c.set_source_rgba(*col, a); c.fill()

# ---------- 标记 ----------
def tag(name, xy, side='R'): return ('tag', name, xy, side)
def num(text, x, y, size=120, a=1, col=RED, pop=1.0): return ('num', text, x, y, size, a, col, pop)
def shake(v): return ('shake', v)
def flash(v): return ('flash', v)

# ---------- 外框 ----------
def top_band(c):
    c.set_source_rgb(*hx('2e2016')); c.rectangle(0, 0, FW, SY); c.fill()
    tiles = [hx(t) for t in ('f1ead6', '8fb08a', 'c9a24a', 'f1ead6', 'a9c39a', 'd98c8c', 'c9a24a', 'f1ead6', '6f9a80')]
    k = 0
    for x in range(6, FW, 22):
        c.set_source_rgb(*tiles[(k * 7 + (k >> 2)) % 9]); c.rectangle(x, 9, 18, 26); c.fill(); k += 1
    # 中央徽记
    ell(c, FW / 2, SY / 2 + 6, 46, 34, hx('c9a24a'), 3, col=hx('2e2016')); ell(c, FW / 2, SY / 2 + 6, 36, 26, hx('f6eedb'), 2, col=hx('2e2016'))
    font(c, 'LXGW WenKai', 30, True); tw = c.text_extents('份')[4]; c.set_source_rgb(*hx('8e2c26')); c.move_to(FW / 2 - tw / 2, SY / 2 + 17); c.show_text('份')

def board(c):
    y0, y1 = 856, FH
    c.set_source_rgb(*hx('2e2016')); c.rectangle(0, y0 - 4, FW, y1 - y0 + 4); c.fill()
    tiles = [hx(t) for t in ('c9a24a', '8fb08a', 'f1ead6', 'd98c8c')]
    for k, x in enumerate(range(6, FW, 22)):
        c.set_source_rgb(*tiles[k % 4]); c.rectangle(x, 1052, 18, 20); c.fill()
    shape(c, [(30, y0 + 10), (FW - 30, y0 + 10), (FW - 30, 1040), (30, 1040)], hx('f6ecd0'), 3, col=hx('c9a24a'), n=1)
    c.set_source_rgb(*LINE); c.set_line_width(1.6); c.rectangle(40, y0 + 20, FW - 80, 1030 - y0 - 20); c.stroke()
    for sd in (1, -1):   # 两端鞭线卷草
        c.save()
        if sd < 0: c.translate(FW, 0); c.scale(-1, 1)
        pts = [(52, 1010), (70, 960), (110, 930), (150, 950)] + spiral(140, 952, 16, 0, 1.0, 1, 10)[1:]
        c.set_source_rgb(*hx('c9a24a')); ribbon_path(c, dense(pts, 4), lambda q: 8 * (1 - q) + 1.5); c.fill()
        pts2 = [(58, 900), (84, 930), (90, 980)]
        c.set_source_rgb(*hx('8fb08a')); ribbon_path(c, dense(pts2, 6), swellW(7, 1)); c.fill()
        ell(c, 66, 892, 8, 8, hx('d07a86'), 1.6)
        c.restore()

_frame = {}
def frame_base():
    if 'f' not in _frame:
        s, c = surf(FW, FH); top_band(c); board(c); s.flush(); _frame['f'] = s
    return _frame['f']

# ---------- 字幕 ----------
def parse(line):
    segs = []; col = None
    for part in re.split(r'(\[/?[rgb]\])', line):
        if part in ('[r]', '[g]', '[b]'): col = {'[r]': RED, '[g]': GREEN, '[b]': BLUE}[part]; continue
        if part in ('[/r]', '[/g]', '[/b]'): col = None; continue
        if not part: continue
        if col: segs.append((part, col)); continue
        # 人名自动蓝
        pat = '(' + '|'.join(sorted(NAMES, key=len, reverse=True)) + ')'
        for q in re.split(pat, part):
            if q: segs.append((q, BLUE if q in NAMES else INK))
    return segs

def draw_line(c, line, y, size, a):
    segs = parse(line); font(c, SERIF, size, True)
    tw = sum(c.text_extents(s)[4] for s, _ in segs); x = FW / 2 - tw / 2
    for s, col in segs:
        c.move_to(x, y); c.set_source_rgba(*col, a); c.show_text(s); x += c.text_extents(s)[4]

def subtitle(c, l1, l2, a):
    if a <= 0: return
    if l2: draw_line(c, l1, 938, 56, a); draw_line(c, l2, 1010, 56, a)
    else: draw_line(c, l1, 972, 60, a)

def plain_len(s): return len(re.sub(r'\[/?[rgb]\]', '', s).replace(' ', '').replace('、', '').replace('，', ''))

def name_tag(c, name, x, y, side, a=1):
    font(c, SERIF, 30, True); tw = c.text_extents(name)[4]
    bx = x + (60 if side == 'R' else -60 - tw - 36); by = y - 70
    c.set_source_rgba(*LINE, a); c.set_line_width(2); c.move_to(x, y); c.line_to(bx + (0 if side == 'R' else tw + 36), by + 22); c.stroke()
    c.save(); c.push_group()
    shape(c, [(bx, by), (bx + tw + 36, by), (bx + tw + 36, by + 46), (bx, by + 46)], hx('f6ecd0'), 2.4, n=1)
    c.set_source_rgb(*hx('c9a24a')); c.set_line_width(2); c.rectangle(bx + 5, by + 5, tw + 26, 36); c.stroke()
    c.move_to(bx + 18, by + 34); c.set_source_rgb(*BLUE); c.show_text(name)
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()

def big_num(c, text, x, y, size, a, col, pop):
    c.save(); c.translate(x, y); c.scale(pop, pop)
    font(c, SERIF, size, True); tw = c.text_extents(text)[4]
    c.move_to(-tw / 2, size * 0.36); c.text_path(text)
    c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_source_rgba(*hx('f6ecd0'), a); c.set_line_width(size * 0.16); c.stroke_preserve(); c.set_source_rgba(*col, a); c.fill()
    c.restore()

def pop_at(lt, t0, dur=0.35):
    """t0 时刻弹出：返回缩放（0→1.25→1）"""
    if lt < t0: return 0
    x = (lt - t0) / dur
    return back_out(x) if x < 1 else 1.0
