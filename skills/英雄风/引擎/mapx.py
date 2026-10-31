# 战争风暗金古地图：世界坐标=经纬度投影，缓存大底图，镜头 cam(lon, lat, zoom)
import math, random
import numpy as np
import cairocffi as cairo
from kit import W, H, FONT, text, glow, GOLD, RED, ease, eout, cl, lerp

K = 110.0; LON0, LAT0 = 71.0, 50.5
MW, MH = int(36 * K), int(18 * K)
def wp(lon, lat): return ((lon - LON0) * K, (LAT0 - lat) * K)

PLACES = {
 '兰州': (103.83, 36.06), '肃州': (98.5, 39.75), '嘉峪关': (98.29, 39.80), '安西': (95.8, 40.5), '玉门关': (93.9, 40.35),
 '哈密': (93.5, 42.83), '巴里坤': (93.0, 43.6), '古城': (89.6, 44.0), '阜康': (87.98, 44.15), '古牧地': (87.62, 44.0),
 '乌鲁木齐': (87.6, 43.8), '昌吉': (87.3, 44.0), '玛纳斯': (86.2, 44.3), '达坂城': (88.3, 43.36), '吐鲁番': (89.18, 42.95),
 '托克逊': (88.65, 42.79), '喀喇沙尔': (86.57, 42.06), '库尔勒': (86.15, 41.73), '库车': (82.96, 41.72), '阿克苏': (80.26, 41.17),
 '喀什噶尔': (75.99, 39.47), '叶尔羌': (77.24, 38.41), '英吉沙': (76.17, 38.93), '和田': (79.92, 37.11), '伊犁': (81.0, 43.9),
 '塔城': (82.98, 46.75), '西宁': (101.78, 36.62),
}
YELLOW = [(100.5, 35.6), (101.8, 36.0), (103.8, 36.1), (104.5, 37.0), (105.8, 37.6), (106.2, 38.8), (106.6, 40.2)]
RIVERS = [
 [(75.8, 39.6), (77.5, 40.2), (79.3, 40.7), (81.5, 41.1), (84.0, 41.05), (86.4, 40.6), (88.0, 39.9), (89.0, 39.6)],   # 塔里木河
 [(83.0, 43.4), (81.6, 43.85), (80.2, 44.0), (78.5, 44.3), (77.0, 44.9)],                                           # 伊犁河
 [(76.0, 39.47), (76.8, 39.4), (77.3, 38.5), (78.3, 38.9), (79.3, 40.0)],                                           # 喀什噶尔/叶尔羌河
 [(80.0, 37.0), (80.6, 38.5), (81.0, 40.0), (81.5, 41.0)],                                                           # 和田河
 [(99.0, 39.2), (98.5, 39.75), (99.0, 40.6), (100.2, 41.8)],                                                         # 黑河
]
LAKES = [(86.95, 42.0, 0.5, 0.18), (90.2, 40.3, 0.45, 0.3), (75.5, 46.6, 3.5, 0.45), (99.9, 36.9, 0.8, 0.35), (81.3, 45.0, 0.25, 0.15)]
MOUNTS = [
 (74.5, 40.0, 80.0, 42.0, 40), (80.0, 42.0, 84.5, 43.2, 40), (84.5, 43.2, 88.0, 43.3, 34), (88.0, 43.1, 94.8, 43.0, 46),
 (74.5, 37.3, 80.0, 36.3, 36), (80.0, 36.3, 90.0, 36.1, 56), (90.0, 36.3, 96.0, 36.0, 30),
 (85.5, 48.6, 90.8, 46.8, 38), (73.6, 37.8, 75.3, 39.2, 20), (94.0, 39.2, 102.5, 37.4, 50), (80.5, 45.2, 83.5, 45.4, 14),
]
DESERTS = [(83.0, 39.0, 7.0, 1.6), (87.6, 45.2, 2.2, 0.55), (92.5, 41.6, 2.0, 0.5)]
REGIONS = [('北  疆', 86.0, 46.2, 120), ('南  疆', 82.5, 38.0, 130), ('天    山', 84.6, 42.5, 70), ('河 西', 99.6, 39.4, 70),
           ('俄 国', 78.0, 48.6, 120), ('塔 克 拉 玛 干', 83.0, 39.2, 56), ('准 噶 尔', 87.6, 45.4, 52), ('中 亚', 72.6, 41.8, 70)]

_MAP = None
def build():
    global _MAP
    if _MAP is not None: return _MAP
    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, MW, MH); c = cairo.Context(sf)
    g = cairo.RadialGradient(MW * 0.55, MH * 0.5, 100, MW * 0.55, MH * 0.5, MW * 0.8)
    g.add_color_stop_rgb(0, 0.23, 0.17, 0.10); g.add_color_stop_rgb(1, 0.10, 0.075, 0.05)
    c.set_source(g); c.paint()
    # 纸纹颗粒
    rnd = np.random.default_rng(3)
    a = np.ndarray((MH, MW, 4), np.uint8, sf.get_data())
    n = rnd.normal(0, 7, (MH, MW)).astype(np.int16)
    for ch in range(3): a[..., ch] = np.clip(a[..., ch].astype(np.int16) + n, 0, 255).astype(np.uint8)
    sf.mark_dirty()
    r = random.Random(5)
    # 区域大字
    for name, lo, la, sz in REGIONS:
        x, y = wp(lo, la)
        c.select_font_face(FONT, 0, 1); c.set_font_size(sz)
        ext = c.text_extents(name)
        c.set_source_rgba(0.85, 0.68, 0.40, 0.13); c.move_to(x - ext[4] / 2, y + sz * 0.35); c.show_text(name)
    # 河流
    def river(pts, w, a_):
        c.set_line_cap(1); c.set_line_join(1)
        for ww, aa in ((w * 4, a_ * 0.12), (w, a_)):
            c.set_source_rgba(0.85, 0.70, 0.42, aa); c.set_line_width(ww)
            q = [wp(*p) for p in pts]; c.move_to(*q[0])
            for i in range(1, len(q) - 1):
                mx, my = (q[i][0] + q[i + 1][0]) / 2, (q[i][1] + q[i + 1][1]) / 2
                c.curve_to(q[i][0], q[i][1], q[i][0], q[i][1], mx, my)
            c.line_to(*q[-1]); c.stroke()
    for lo, la, rx, ry in DESERTS:
        for i in range(int(rx * ry * 320)):
            ang = r.uniform(0, 6.283); rr_ = math.sqrt(r.random())
            x, y = wp(lo + math.cos(ang) * rx * rr_, la + math.sin(ang) * ry * rr_)
            c.set_source_rgba(0.80, 0.62, 0.35, r.uniform(0.05, 0.18)); c.arc(x, y, r.uniform(1.5, 3.0), 0, 6.28); c.fill()
    for lo, la, rx, ry in LAKES:
        x, y = wp(lo, la)
        c.save(); c.translate(x, y); c.scale(rx * K, ry * K); c.arc(0, 0, 1, 0, 6.28); c.restore()
        c.set_source_rgba(0.06, 0.10, 0.11, 0.95); c.fill_preserve(); c.set_source_rgba(0.85, 0.70, 0.42, 0.5); c.set_line_width(2.5); c.stroke()
    river(YELLOW, 7, 0.75)
    for rv in RIVERS: river(rv, 3.2, 0.5)
    # 山：一簇簇小三角，两面明暗
    for lo0, la0, lo1, la1, n in MOUNTS:
        for i in range(n):
            k = i / max(1, n - 1)
            x, y = wp(lerp(lo0, lo1, k) + r.uniform(-0.25, 0.25), lerp(la0, la1, k) + r.uniform(-0.25, 0.25))
            s = r.uniform(30, 56)
            c.set_source_rgba(0.45, 0.33, 0.18, 0.9); c.move_to(x - s, y); c.line_to(x, y - s * 1.1); c.line_to(x, y); c.close_path(); c.fill()
            c.set_source_rgba(0.20, 0.14, 0.08, 0.95); c.move_to(x, y); c.line_to(x, y - s * 1.1); c.line_to(x + s * 0.9, y); c.close_path(); c.fill()
    _MAP = sf
    return sf

class Cam:
    lon = 86.0; lat = 42.0; z = 1.0
CAM = Cam()

def set_cam(lon, lat, z):
    CAM.lon, CAM.lat, CAM.z = lon, lat, z

def sp(lon, lat):
    x, y = wp(lon, lat); cx, cy = wp(CAM.lon, CAM.lat)
    return (W / 2 + (x - cx) * CAM.z, H / 2 + (y - cy) * CAM.z)

def P(name): return sp(*PLACES[name])

def draw(c):
    sf = build()
    cx, cy = wp(CAM.lon, CAM.lat)
    c.save(); c.set_source_rgb(0.08, 0.06, 0.04); c.paint()
    c.translate(W / 2, H / 2); c.scale(CAM.z, CAM.z); c.translate(-cx, -cy)
    c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
    c.restore()

def city(c, name, state='gold', t=0, a=1, label=True, dx=18, dy=-14, size=34, ring=0):
    x, y = P(name)
    col = (1.0, 0.82, 0.45) if state == 'gold' else ((0.95, 0.22, 0.15) if state == 'red' else (0.6, 0.75, 0.95))
    glow(c, x, y, 46, col, 0.55 * a)
    c.set_source_rgba(*col, a); c.arc(x, y, 8, 0, 6.28); c.fill()
    c.set_source_rgba(1, 1, 1, 0.9 * a); c.arc(x, y, 3.5, 0, 6.28); c.fill()
    if ring:
        rr = 20 + (t * 60) % 70
        c.set_source_rgba(*col, a * (1 - ((t * 60) % 70) / 70)); c.set_line_width(3); c.arc(x, y, rr, 0, 6.28); c.stroke()
    if label: text(c, name, x + dx, y + dy, size, (0.95, 0.88, 0.72), a, 'l' if dx >= 0 else 'r')

def path_pts(names_or_pts):
    return [P(n) if isinstance(n, str) else sp(*n) for n in names_or_pts]

def march(c, pts, k, col=(1.0, 0.82, 0.45), w=5, a=1, head=True):
    """金色行军线：沿折线按 k(0→1) 画出，线头光点"""
    if k <= 0: return
    seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    tot = sum(seg); L = tot * cl(k)
    c.set_line_cap(1); c.set_line_join(1)
    for ww, aa in ((w * 4, 0.18), (w, 1)):
        c.set_source_rgba(*col, aa * a); c.set_line_width(ww); c.move_to(*pts[0]); acc = 0; hx, hy = pts[0]
        for i, sl in enumerate(seg):
            if acc + sl >= L:
                f = (L - acc) / sl if sl else 0
                hx = lerp(pts[i][0], pts[i + 1][0], f); hy = lerp(pts[i][1], pts[i + 1][1], f); c.line_to(hx, hy); break
            c.line_to(*pts[i + 1]); acc += sl; hx, hy = pts[i + 1]
        c.stroke()
    if head and k < 1:
        glow(c, hx, hy, 40, col, 0.9 * a); c.set_source_rgba(1, 1, 1, a); c.arc(hx, hy, 6, 0, 6.28); c.fill()
    return hx, hy

def arrow(c, x0, y0, x1, y1, k, col=RED, w=26, a=1, dash=False):
    if k <= 0: return
    x = lerp(x0, x1, cl(k)); y = lerp(y0, y1, cl(k))
    ang = math.atan2(y - y0, x - x0)
    c.set_line_cap(1)
    if dash: c.set_dash([w * 0.9, w * 0.7])
    c.set_source_rgba(*col, 0.25 * a); c.set_line_width(w * 2.2); c.move_to(x0, y0); c.line_to(x - math.cos(ang) * w, y - math.sin(ang) * w); c.stroke()
    c.set_source_rgba(*col, a); c.set_line_width(w); c.move_to(x0, y0); c.line_to(x - math.cos(ang) * w, y - math.sin(ang) * w); c.stroke()
    c.set_dash([])
    hw = w * 1.6; hl = w * 2.2
    c.move_to(x + math.cos(ang) * hl * 0.3, y + math.sin(ang) * hl * 0.3)
    c.line_to(x - math.cos(ang) * hl + math.cos(ang + 1.57) * hw, y - math.sin(ang) * hl + math.sin(ang + 1.57) * hw)
    c.line_to(x - math.cos(ang) * hl - math.cos(ang + 1.57) * hw, y - math.sin(ang) * hl - math.sin(ang + 1.57) * hw)
    c.close_path(); c.set_source_rgba(*col, a); c.fill()

def flagpin(c, x, y, ch, col=(0.75, 0.10, 0.07), a=1, s=1.0):
    c.set_source_rgba(0.9, 0.8, 0.6, a); c.set_line_width(3 * s); c.move_to(x, y); c.line_to(x, y - 60 * s); c.stroke()
    c.set_source_rgba(*col, a); c.rectangle(x, y - 60 * s, 40 * s, 30 * s); c.fill()
    c.set_source_rgba(0.95, 0.85, 0.6, a); c.set_line_width(1.5); c.rectangle(x, y - 60 * s, 40 * s, 30 * s); c.stroke()
    text(c, ch, x + 20 * s, y - 36 * s, 22 * s, (1, 0.92, 0.75), a, 'c', shadow=False)

def jag(c, x0, y0, x1, y1, t, a=1, col=RED):
    n = 14; c.set_source_rgba(*col, a); c.set_line_width(5); c.move_to(x0, y0)
    for i in range(1, n + 1):
        k = i / n; x = lerp(x0, x1, k); y = lerp(y0, y1, k)
        off = (14 if i % 2 else -14) * (1 + 0.3 * math.sin(t * 20 + i))
        nx, ny = -(y1 - y0), (x1 - x0); L = math.hypot(nx, ny) or 1
        c.line_to(x + nx / L * off, y + ny / L * off)
    c.stroke()

def army_block(c, x, y, w, h, col, label, a=1, sub=None):
    c.set_source_rgba(*col, 0.85 * a)
    c.rectangle(x - w / 2, y - h / 2, w, h); c.fill()
    c.set_source_rgba(1, 0.9, 0.7, 0.8 * a); c.set_line_width(2.5); c.rectangle(x - w / 2, y - h / 2, w, h); c.stroke()
    # 方阵小格
    c.set_source_rgba(1, 0.9, 0.7, 0.25 * a); c.set_line_width(1)
    for i in range(1, int(w / 22)): c.move_to(x - w / 2 + i * 22, y - h / 2); c.line_to(x - w / 2 + i * 22, y + h / 2)
    c.stroke()
    text(c, label, x, y + 14, 40, (1, 0.96, 0.88), a, 'c')
    if sub: text(c, sub, x, y + h / 2 + 40, 28, (0.9, 0.82, 0.65), a, 'c', shadow=False)
