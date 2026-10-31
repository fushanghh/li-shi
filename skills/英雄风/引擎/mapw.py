# 战争风暗金古地图：世界坐标=经纬度投影，缓存大底图，镜头 cam(lon, lat, zoom)
import math, random
import numpy as np
import cairocffi as cairo
from kit import W, H, FONT, text, glow, GOLD, RED, ease, eout, cl, lerp

K = 260.0; LON0, LAT0 = 106.5, 37.8
MW, MH = int(10 * K), int(8.5 * K)
def wp(lon, lat): return ((lon - LON0) * K, (LAT0 - lat) * K)

PLACES = {
    '咸阳': (108.7, 34.35), '杜邮': (108.45, 34.42), '函谷关': (110.9, 34.62), '伊阙': (112.47, 34.56), '新城': (112.2, 34.25),
    '新郑': (113.73, 34.4), '大梁': (114.35, 34.8), '华阳': (113.6, 34.7), '陉城': (111.5, 35.68), '长平': (112.9, 35.83),
    '光狼城': (112.6, 35.62), '邯郸': (114.48, 36.6), '鄢': (112.3, 31.72), '郢': (112.2, 30.4), '陈': (114.88, 33.73),
    '夷陵': (111.3, 30.75), '洛阳': (112.45, 34.68), '阴密': (107.6, 35.4), '宛': (112.53, 33.0), '上党': (113.1, 36.2),
}
YELLOW = [(110.6, 37.8), (110.5, 36.6), (110.55, 35.6), (110.3, 34.62), (111.2, 34.78), (112.3, 34.85), (113.4, 34.92), (114.2, 35.1), (114.9, 35.6), (115.5, 36.3), (116.3, 37.2)]
RIVERS = [
    [(106.5, 34.45), (107.6, 34.35), (108.7, 34.35), (109.6, 34.5), (110.3, 34.62)],               # 渭
    [(112.6, 37.8), (112.3, 36.9), (111.6, 36.0), (111.2, 35.6), (110.6, 35.45)],                 # 汾
    [(106.5, 33.1), (108.5, 32.9), (110.4, 32.7), (111.3, 32.4), (112.1, 32.05), (112.3, 31.5), (113.0, 30.9), (114.1, 30.6)],  # 汉
    [(108.5, 30.4), (110.0, 30.9), (111.3, 30.7), (112.2, 30.3), (113.1, 29.9), (114.3, 30.5), (115.6, 29.9), (116.5, 30.2)],  # 长江
    [(110.4, 34.1), (111.2, 34.3), (112.0, 34.6), (112.9, 34.75)],                                   # 洛
    [(111.3, 33.8), (112.0, 34.3), (112.47, 34.56)],                                                 # 伊
    [(112.9, 32.6), (112.3, 32.0), (112.3, 31.72)],                                                  # 夷水（白起渠引水）
]
MOUNTS = [  # (起lon,lat, 止lon,lat, 数量)
    (107.0, 33.75, 110.6, 33.9, 46), (110.9, 33.6, 113.0, 33.4, 26), (113.3, 35.3, 114.1, 37.4, 38),
    (110.9, 35.1, 112.0, 35.2, 16), (111.4, 36.2, 112.3, 37.6, 22), (108.0, 31.6, 110.5, 31.9, 28),
    (112.0, 35.4, 113.0, 35.95, 14), (107.0, 35.6, 108.2, 36.8, 18),
]
REGIONS = [('秦', 108.6, 35.2, 150), ('韩', 113.0, 34.05, 110), ('魏', 114.6, 35.25, 110), ('赵', 114.3, 37.25, 120),
           ('楚', 113.3, 31.4, 150), ('关 中', 108.0, 34.8, 60), ('河 东', 111.2, 36.3, 60), ('南 阳', 112.0, 32.9, 56), ('上 党', 112.6, 36.6, 56)]

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
    river(YELLOW, 7, 0.75)
    for rv in RIVERS: river(rv, 3.2, 0.5)
    # 山：一簇簇小三角，两面明暗
    for lo0, la0, lo1, la1, n in MOUNTS:
        for i in range(n):
            k = i / max(1, n - 1)
            x, y = wp(lerp(lo0, lo1, k) + r.uniform(-0.25, 0.25), lerp(la0, la1, k) + r.uniform(-0.25, 0.25))
            s = r.uniform(26, 48)
            c.set_source_rgba(0.45, 0.33, 0.18, 0.9); c.move_to(x - s, y); c.line_to(x, y - s * 1.1); c.line_to(x, y); c.close_path(); c.fill()
            c.set_source_rgba(0.20, 0.14, 0.08, 0.95); c.move_to(x, y); c.line_to(x, y - s * 1.1); c.line_to(x + s * 0.9, y); c.close_path(); c.fill()
    _MAP = sf
    return sf

class Cam:
    lon = 112.0; lat = 34.0; z = 0.6
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
