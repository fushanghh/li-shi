"""Gold relief terrain maps (reference style: TikMate 7692097776751383194).
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
    def relief(self, scale=2, exag=3.0, sun_az=315, sun_alt=35, warm=1.0):
        d = ndimage.zoom(self.dem, scale, order=1)
        land = d > 0
        d = ndimage.gaussian_filter(d, 0.8)
        gy, gx = np.gradient(d * exag / (scale * 1.0) / 600.0)
        nx, ny, nz = -gx, -gy, np.ones_like(gx)
        n = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2); nx /= n; ny /= n; nz /= n
        az, al = math.radians(sun_az), math.radians(sun_alt)
        lx, ly, lz = math.cos(al) * math.sin(az), -math.cos(al) * math.cos(az), math.sin(al)
        lam = np.clip(nx * lx + ny * ly + nz * lz, 0, 1)
        hx, hy, hz = lx, ly, lz + 1; hn = math.sqrt(hx * hx + hy * hy + hz * hz)
        spec = np.clip((nx * hx + ny * hy + nz * hz) / hn, 0, 1) ** 40
        slope = 1 - nz
        v = 0.04 + 0.35 * lam ** 3 + 1.0 * spec + 0.7 * np.clip(slope * 3, 0, 1) * lam ** 2
        flat = np.clip(1 - slope * 25, 0, 1)
        v = v * (1 - 0.65 * flat)  # plains darker, like reference
        # elevation contours (thin gold iso-lines)
        c = np.zeros_like(d)
        for lvl in (1500, 3000, 4500):
            m = (d > lvl).astype(np.float32)
            e = np.abs(ndimage.sobel(ndimage.gaussian_filter(m, 0.6)))
            c = np.maximum(c, np.clip(e, 0, 1))
        v = v + 0.12 * c
        v = np.where(land, v, 0)
        # palette
        stops = np.array([0, .12, .35, .65, 1.0, 1.6])
        cols = np.array([[8, 6, 3], [38, 26, 10], [105, 72, 28], [196, 146, 62], [250, 214, 140], [255, 246, 220]], float)
        rgb = np.stack([np.interp(v, stops, cols[:, k]) for k in range(3)], -1)
        # sea: near black + wave stripes near coast
        dist = ndimage.distance_transform_edt(~land)
        Y, X = np.mgrid[0:d.shape[0], 0:d.shape[1]]
        waves = np.clip((np.sin(dist / (4.0 * scale) + np.sin(X / 140.0) * 1.5) - 0.85) / 0.15, 0, 1) * np.exp(-dist / (90 * scale)) * 40
        sea = np.stack([10 + waves, 8 + waves * 0.75, 5 + waves * 0.4], -1)
        rgb = np.where(land[..., None], rgb, sea)
        # coast glow
        edge = land ^ ndimage.binary_erosion(land, iterations=1, border_value=1)
        edge = ndimage.binary_opening(land, iterations=1) ^ ndimage.binary_erosion(ndimage.binary_opening(land, iterations=1), iterations=1, border_value=1)
        g = ndimage.gaussian_filter(edge.astype(np.float32), 1.5 * scale) * 3.0 + edge * 0.75
        rgb += np.clip(g, 0, 1)[..., None] * np.array([255, 205, 120])
        self.scale = scale
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
FONT = '/workspace/work/fonts/NotoSerifSC-Bold.otf'


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
