"""Gray-brown / blue-gray relief terrain maps (2026-10-25: gold palette removed per user) (reference style: TikMate 7692097776751383194).
Real DEM (AWS terrarium tiles) -> metallic gold hillshade, dark sea with wave lines,
glowing coast and rivers (Natural Earth 10m). Web-mercator projection.
"""
import os, math, io, urllib.request
import numpy as np
from PIL import Image
from scipy import ndimage
import cairocffi as cairo
import shapefile

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cache'); os.makedirs(CACHE, exist_ok=True)


def lon2x(lon, z): return (lon + 180) / 360 * 2 ** z * 256


def lat2y(lat, z):
    r = math.radians(lat)
    return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2 ** z * 256


class Map:
    def __init__(self, lon0, lon1, lat0, lat1, z=6):
        self.z = z
        self.px0, self.px1 = lon2x(lon0, z), lon2x(lon1, z)
        self.py0, self.py1 = lat2y(lat1, z), lat2y(lat0, z)
        tx0, tx1 = int(self.px0 // 256), int(self.px1 // 256)
        ty0, ty1 = int(self.py0 // 256), int(self.py1 // 256)
        key = f'{CACHE}/dem_{z}_{tx0}_{tx1}_{ty0}_{ty1}.npy'
        if os.path.exists(key):
            big = np.load(key)
        else:
            big = np.zeros(((ty1 - ty0 + 1) * 256, (tx1 - tx0 + 1) * 256), np.float32)
            for tx in range(tx0, tx1 + 1):
                for ty in range(ty0, ty1 + 1):
                    u = f'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{tx}/{ty}.png'
                    a = np.asarray(Image.open(io.BytesIO(urllib.request.urlopen(u, timeout=30).read())).convert('RGB')).astype(np.float32)
                    big[(ty - ty0) * 256:(ty - ty0 + 1) * 256, (tx - tx0) * 256:(tx - tx0 + 1) * 256] = a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
            np.save(key, big)
        ox, oy = tx0 * 256, ty0 * 256
        self.dem = big[int(self.py0 - oy):int(self.py1 - oy), int(self.px0 - ox):int(self.px1 - ox)]
        self.H, self.W = self.dem.shape

    def xy(self, lon, lat):
        return lon2x(lon, self.z) - self.px0, lat2y(lat, self.z) - self.py0

    # ---------- base relief ----------
    def relief(self, scale=2, exag=3.0, water_below=None, **kw):
        """multi-directional hillshade, gray-brown -> blue-gray hypsometric tint, lifted plains, clear blue water."""
        d = ndimage.zoom(self.dem, scale, order=1)
        d = np.where(d < -500, np.nan, d)
        d = np.where(np.isnan(d), np.nanmedian(d), d)
        land = d > 0
        self.scale = scale
        mpp = 156543.0 * math.cos(math.radians(30)) / 2 ** self.z / scale
        rgb, _ = shade_rgb(d, mpp, exag)
        if water_below is not None:
            rgb = paint_water(rgb, d, water_below)
        sea = np.array([34, 52, 74], float)
        rgb = np.where(land[..., None], rgb, sea)
        return np.clip(rgb, 0, 255).astype(np.uint8)

    # ---------- vector overlays ----------
    def rivers(self, minrank=None, names=None):
        sf = shapefile.Reader(f'{HERE}/rivers/ne_10m_rivers_lake_centerlines.shp')
        flds = [f[0] for f in sf.fields[1:]]
        out = []
        for sr in sf.iterShapeRecords():
            rec = dict(zip(flds, sr.record))
            if minrank is not None and rec.get('scalerank', 99) > minrank: continue
            if names and not any(nm.lower() in (str(rec.get('name'))+'|'+str(rec.get('name_en'))+'|'+str(rec.get('name_zh'))).lower() for nm in names): continue
            pts = sr.shape.points; parts = list(sr.shape.parts) + [len(pts)]
            for a, b in zip(parts[:-1], parts[1:]):
                seg = [self.xy(*p) for p in pts[a:b]]
                if any(0 <= x <= self.W and 0 <= y <= self.H for x, y in seg):
                    out.append((rec.get('scalerank', 9), seg))
        return out


# ---------- shading helpers (new palette) ----------
def shade_rgb(d, mpp, exag=2.0, sm=0.8):
    d = ndimage.gaussian_filter(d, sm)
    gy, gx = np.gradient(d, mpp)
    gx = gx * exag; gy = gy * exag
    nz = 1 / np.sqrt(1 + gx ** 2 + gy ** 2); nx = -gx * nz; ny = -gy * nz
    sh = np.zeros_like(d); wsum = 0
    for az, w in ((315, 0.40), (270, 0.20), (360, 0.20), (225, 0.20)):
        a_, al = math.radians(az), math.radians(42)
        lx, ly, lz = math.cos(al) * math.sin(a_), -math.cos(al) * math.cos(a_), math.sin(al)
        sh += w * np.clip(nx * lx + ny * ly + nz * lz, 0, 1); wsum += w
    sh /= wsum
    # normalise so flat ground = ~1
    flat = math.sin(math.radians(42))
    s_ = sh / flat
    lo, hi = np.percentile(d, 3), np.percentile(d, 99.5)
    h = np.clip((d - lo) / max(hi - lo, 1), 0, 1)
    stops = np.array([0, .18, .45, .75, 1.0])
    cols = np.array([[182, 172, 150], [150, 138, 116], [120, 110, 98], [104, 112, 120], [160, 168, 176]], float)
    tint = np.stack([np.interp(h, stops, cols[:, k]) for k in range(3)], -1)
    slope = 1 - nz
    plain = np.clip(1 - slope * 18, 0, 1)
    k = 0.18 + 0.92 * np.clip(s_, 0, 1.4) ** 1.3
    k = k * (1 - 0.18 * np.clip(slope * 4, 0, 1)) + 0.10 * plain
    return tint * k[..., None], h


def paint_water(rgb, d, level, blur=1.4):
    w = ndimage.gaussian_filter((d < level).astype(np.float32), blur)
    wm = np.clip((w - 0.35) * 3, 0, 1)
    wb = ndimage.binary_closing(wm > 0.5, iterations=6)
    wb = ndimage.binary_opening(wb, iterations=2)
    lab, n = ndimage.label(wb)
    if n:
        sz = ndimage.sum(wb, lab, range(1, n + 1)); keep = np.isin(lab, 1 + np.where(sz > 4000)[0])
        wb = keep
    lab, n = ndimage.label(~wb)
    if n:
        sz = ndimage.sum(~wb, lab, range(1, n + 1)); wb = wb | np.isin(lab, 1 + np.where(sz < 6000)[0])
    wm = wb.astype(np.float32)
    wm = ndimage.gaussian_filter(wm, 0.9)
    edge = np.clip(ndimage.gaussian_filter(wm, 2.5) - wm, 0, 1)
    blue = np.array([44, 118, 196], np.float32)
    rgb = rgb * (1 - wm[..., None]) + blue * wm[..., None]
    rgb = rgb * (1 - 0.6 * edge[..., None]) + np.array([150, 205, 245]) * 0.6 * edge[..., None]
    return rgb


def glow_lines(size, lines, scale, width=1.6, color=(1, .84, .5), glow=8, alpha=1.0, progress=1.0):
    """Return RGBA float layer with glowing polylines. progress<1 draws partial length."""
    W, H = size
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cr = cairo.Context(surf)
    cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_join(cairo.LINE_JOIN_ROUND)
    for w, seg in lines:
        pts = [(x * scale, y * scale) for x, y in seg]
        if progress < 1:
            L = np.cumsum([0] + [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)])
            pts = [p for p, l in zip(pts, L) if l <= L[-1] * progress]
        if len(pts) < 2: continue
        cr.move_to(*pts[0])
        for p in pts[1:]: cr.line_to(*p)
        cr.set_line_width(w); cr.set_source_rgba(1, 1, 1, 1); cr.stroke()
    a = np.ndarray((H, W, 4), np.uint8, surf.get_data())[..., 3].astype(np.float32) / 255
    halo = ndimage.gaussian_filter(a, glow) * 2.2 + ndimage.gaussian_filter(a, glow / 3) * 0.8
    core = np.clip(a * 1.3, 0, 1)
    col = np.array(color)
    rgb = core[..., None] * np.array([1, .97, .88]) + np.clip(halo, 0, 1.2)[..., None] * col
    return np.clip(rgb * alpha, 0, 1.5)


def compose(base, *layers):
    out = base.astype(np.float32) / 255
    for l in layers:
        out = 1 - (1 - out) * (1 - np.clip(l, 0, 1))  # screen
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)


# ---------- animation helpers ----------
FONT = os.path.expanduser('~/.fonts/NotoSerifSC-Bold.otf')


def camera(img, cx, cy, view_w, out=(1920, 1080)):
    """crop img (HxWx3 uint8) centred at pixel (cx,cy) with width view_w, resize to out."""
    from PIL import Image as _I
    H, W = img.shape[:2]
    vw = view_w; vh = vw * out[1] / out[0]
    x0 = min(max(cx - vw / 2, 0), W - vw); y0 = min(max(cy - vh / 2, 0), H - vh)
    return _I.fromarray(img).transform(out, _I.AFFINE, (vw / out[0], 0, x0, 0, vh / out[1], y0), resample=_I.BICUBIC)


def route_layer(size, pts, progress, width=7, t=0.0):
    """Glowing rope-like marching route (reference: white braided line). pts in output pixels."""
    W, H = size
    L = np.cumsum([0] + [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)])
    cut = L[-1] * progress
    keep = [p for p, l in zip(pts, L) if l <= cut]
    if len(keep) < len(pts) and len(keep) >= 1:
        i = len(keep); f = (cut - L[i - 1]) / max(L[i] - L[i - 1], 1e-6)
        keep.append((pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f))
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cr = cairo.Context(surf)
    cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_join(cairo.LINE_JOIN_ROUND)
    if len(keep) >= 2:
        cr.move_to(*keep[0]); [cr.line_to(*p) for p in keep[1:]]
        cr.set_line_width(width); cr.set_source_rgba(1, 1, 1, .75); cr.stroke_preserve()
        cr.set_dash([width * 0.9, width * 0.9], -t * 40); cr.set_line_width(width * 0.55); cr.set_source_rgba(1, 1, 1, 1); cr.stroke()
    a = np.ndarray((H, W, 4), np.uint8, surf.get_data())[..., 3].astype(np.float32) / 255
    halo = ndimage.gaussian_filter(a, 12) * 1.6
    rgb = a[..., None] * np.array([1, .98, .92]) + np.clip(halo, 0, 1)[..., None] * np.array([1, .8, .45])
    return rgb, (keep[-1] if keep else None)


def gold_label(img, text, x, y, size=46, alpha=1.0, bar=260):
    """Label with two gold glowing bars above/below (reference '秦军')."""
    from PIL import ImageDraw, ImageFont, ImageFilter, Image as _I
    lay = _I.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(FONT, size)
    for dy in (-size * 0.75, size * 0.75):
        d.line([(x - bar, y + dy), (x + bar, y + dy)], fill=(255, 205, 110, int(255 * alpha)), width=3)
    glow = lay.filter(ImageFilter.GaussianBlur(6))
    d.text((x, y), text, font=f, fill=(255, 238, 200, int(255 * alpha)), anchor='mm')
    img.alpha_composite(glow) if img.mode == 'RGBA' else None
    out = img.convert('RGBA'); out.alpha_composite(glow); out.alpha_composite(glow); out.alpha_composite(lay)
    return out.convert('RGB')
