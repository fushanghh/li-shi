"""v2 框架：镜头表、转场、字幕、事件"""
import math, random
import cairocffi as cairo
from engine import *
from chars import *
from bgs import *

def kb(lst):  # 拍 → 秒
    return [(a * B,) + tuple(r) for a, *r in lst]

class Shot:
    def __init__(s, beats, fn, cam=None, trans='cut', caps=(), ev=(), name=''):
        s.beats = beats; s.dur = beats * B; s.fn = fn; s.cam = cam or (lambda t: (SCX, SCY, 1.0))
        s.trans = trans; s.caps = list(caps); s.ev = list(ev); s.name = name

SHOTS = []
def shot(beats, trans='cut', cam=None, caps=(), ev=(), name=''):
    def deco(fn):
        SHOTS.append(Shot(beats, fn, cam, trans, caps, ev, name)); return fn
    return deco

def camk(keys, fn=eio):
    """镜头关键帧 [(beat, (cx, cy, z))]"""
    ks = [(b * B, v) for b, v in keys]
    return lambda t: track(t, ks, fn)

def ragdoll(p, g, kind, face, sc, x0, t, t0, vx=500, vy=-700, spin=400, land=GY, pose0='guard', slide=80, extra=None, lie_dir=1):
    """被击飞：抛物线 + 旋转 → 落地躺倒滑行，留在地上"""
    if t < t0:
        return figure(p, g, x0, land, sc, face, pose0, kind, t=t, extra=extra)
    k = t - t0
    G = 2600.0
    # 落地时间：vy*k + G k^2/2 = 0 → k = -2vy/G
    tl = max(0.15, -2 * vy / G)
    if k < tl:
        x = x0 + vx * k; y = land + vy * k + G * k * k / 2
        sg = 1 if vx >= 0 else -1
        ang = (90 + 360 * round(spin / 500)) * eo(k / tl)
        return figure(p, g, x, y + 118 * sc * (k / tl) ** 2, sc, face, 'hurt', kind, rot=ang * sg * face, t=t, extra=extra)
    kk = k - tl
    sg = 1 if vx >= 0 else -1
    x = x0 + vx * tl + sg * slide * eo(kk / 0.4)
    figure(p, g, x, land + 118 * sc, sc, face, 'lie', kind, rot=90 * sg * face, t=t, extra=extra)
    return None

def landed(t, t0, vy=-700):
    return t >= t0 + max(0.15, -2 * vy / 2600.0)

def tipfn(x, gy, sc, face, keys, kind='lin', extra=None, xk=None, yk=None):
    def f(q, tt):
        xx = track(tt, xk) if xk else x; yy = track(tt, yk) if yk else gy
        return figure(q, None, xx, yy, sc, face, anim(tt, keys), kind, t=tt, extra=extra)
    return f

def draw_trail(g, fn, t, n=7, dt=1 / 50, col='CREAM', w=24, minspeed=600):
    pts = fig_tip_path(fn, t, n, dt)
    sp = math.hypot(pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]) / dt
    if sp > minspeed: trail(g, pts, col, w, min(1, (sp - minspeed) / 1500 + 0.3))

def footstep(p, g, x, t, t0):
    if t < t0: return
    a = clamp(1 - (t - t0) / 3)
    p.poly([(x - 30, GY + 12), (x + 30, GY + 12), (x + 26, GY + 26), (x - 26, GY + 26)], 'GOLD', a=a)
    g.poly([(x - 30, GY + 12), (x + 30, GY + 12), (x + 26, GY + 26), (x - 26, GY + 26)], 'GOLD', a=a * 0.6)
    p.poly([(x + 60, GY + 19), (x + 90, GY + 8), (x + 90, GY + 30)], 'GOLD', a=a); p.line([(x + 90, GY + 19), (x + 150, GY + 19)], 'GOLD', 5, a)

def mini_soldier(p, x, y, s, ph=0.0, face=-1, thrust=0.0):
    """远景小兵（快速）"""
    h = 120 * s
    p.poly([(x - 12 * s, y), (x - 6 * s, y - h * .5), (x - 14 * s, y - h * .85), (x + 14 * s, y - h * .85), (x + 6 * s, y - h * .5), (x + 12 * s, y)], 'BLK')
    p.ell(x, y - h * .95, 9 * s, 10 * s, 'CREAM'); p.poly([(x - 10 * s, y - h), (x + 10 * s, y - h), (x, y - h * 1.18)], 'BLK')
    a = math.radians(lerp(10, 80, thrust))
    hx_, hy_ = x + face * 18 * s, y - h * .62
    p.line([(hx_ - face * math.sin(a) * 60 * s, hy_ + math.cos(a) * 60 * s), (hx_ + face * math.sin(a) * 90 * s, hy_ - math.cos(a) * 90 * s)], 'BLK', 3 * s + 1)
    p.ell(hx_ + face * math.sin(a) * 92 * s, hy_ - math.cos(a) * 92 * s, 3 * s + 1, 3 * s + 1, 'CREAM')

def seal_stamp(p, g, txt, x, y, t, t0, s0=3.0, w_=600, h_=240, rot=-0.06):
    if t < t0 - 0.25: return
    k = clamp((t - (t0 - 0.25)) / 0.25)
    sc = lerp(s0, 1.0, ei(k)) * (punch(t, t0, 0.25, 0.12) if t >= t0 else 1)
    a = k
    for q in (p,):
        q.c.save(); q.c.translate(x, y); q.c.rotate(rot); q.c.scale(sc, sc)
        q.poly([(-w_ / 2, -h_ / 2), (w_ / 2, -h_ / 2), (w_ / 2, h_ / 2), (-w_ / 2, h_ / 2)], 'RED', 'BLK', 10, a=a)
        q.poly([(-w_ / 2 + 20, -h_ / 2 + 20), (w_ / 2 - 20, -h_ / 2 + 20), (w_ / 2 - 20, h_ / 2 - 20), (-w_ / 2 + 20, h_ / 2 - 20)], 'RED', 'CREAM', 5, a=a)
        q.text(txt, 0, h_ * 0.2, h_ * 0.52, 'CREAM', a=a)
        q.c.restore()

def sync_ctx(p, g, fnc):
    fnc(p.c); fnc(g.c)
