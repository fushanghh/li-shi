import numpy as np, math
from scipy import ndimage
LAND = np.array([[18, 15, 12], [40, 34, 27], [72, 62, 49], [112, 98, 78], [158, 142, 116], [205, 192, 168]], float)
STOPS = np.array([0, .18, .38, .6, .82, 1.05])
def hillshade(d, px_m, exag):
    gy, gx = np.gradient(d * exag / px_m)
    nx, ny, nz = -gx, -gy, np.ones_like(gx)
    n = np.sqrt(nx**2+ny**2+nz**2); nx/=n; ny/=n; nz/=n
    def L(az, al):
        az, al = math.radians(az), math.radians(al)
        return np.clip(nx*math.cos(al)*math.sin(az) - ny*math.cos(al)*math.cos(az) + nz*math.sin(al), 0, 1)
    h = 0.55*L(315, 40) + 0.25*L(270, 50) + 0.20*L(0, 55)
    return h, 1-nz
def colorize(d, water, px_m, exag, elev_span):
    h, slope = hillshade(d, px_m, exag)
    flat = h[slope < 0.002].mean() if (slope < 0.002).any() else h.mean()
    v = 0.30 + (h - flat)*1.6 + 0.12*np.clip((d - np.percentile(d, 5))/elev_span, 0, 1)
    v = np.clip(v, 0, 1.05)
    rgb = np.stack([np.interp(v, STOPS, LAND[:, k]) for k in range(3)], -1)
    # water: blue with lighter rim glow
    dist = ndimage.distance_transform_edt(water)
    deep = np.clip(dist/40, 0, 1)[..., None]
    wcol = np.array([52, 112, 178])*(1-deep) + np.array([30, 72, 128])*deep
    rgb = np.where(water[..., None], wcol, rgb)
    edge = water ^ ndimage.binary_erosion(water, iterations=1)
    g = ndimage.gaussian_filter(edge.astype(np.float32), 2.0)*2.5 + edge*0.5
    rgb = rgb + np.clip(g, 0, 1)[..., None]*np.array([110, 180, 240])*0.6
    return np.clip(rgb, 0, 255).astype(np.uint8)
