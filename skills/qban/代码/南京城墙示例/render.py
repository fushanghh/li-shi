import sys, os, subprocess, time
from scenes import *

STARTS = []; acc = 0.0
for s in SCENES:
    STARTS.append(acc); acc += s['D']
TOTAL = acc; NF = int(round(TOTAL * FPS))
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); C = cairo.Context(surf)
surfB = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); CB = cairo.Context(surfB)
surfA = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); CA = cairo.Context(surfA)
vig = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
vc = cairo.Context(vig)
pat = cairo.RadialGradient(W/2, H/2, H*0.45, W/2, H/2, H*1.1)
pat.add_color_stop_rgba(0, 0, 0, 0, 0); pat.add_color_stop_rgba(1, 0, 0, 0, 0.28)
vc.set_source(pat); vc.paint()
TR = 0.55


def smooth(u):
    u = clamp(u); return u * u * (3 - 2 * u)


def draw_scene(ctx, i, t):
    sc = SCENES[i]
    ctx.identity_matrix(); ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    sx, sy, sr = sc['spot']
    if sc['bg'] == 'dark': bg_dark2(ctx, t, sx, sy, sr)
    cam = sc.get('cam') or (960, 540, 1.0, 1.05)
    if len(cam) == 4: cam = (cam[0], cam[1], cam[0], cam[1], cam[2], cam[3])
    cx0, cy0, cx1, cy1, z0, z1 = cam
    u = smooth(t / sc['D'])
    z = lerp(z0, z1, u); cx = lerp(cx0, cx1, u); cy = lerp(cy0, cy1, u)
    hw, hh = W / 2 / z, H / 2 / z
    cx = min(max(cx, hw), W - hw) if z >= 1 else cx
    cy = min(max(cy, hh), H - hh) if z >= 1 else cy
    ctx.save()
    ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-cx, -cy)
    sc['fn'](ctx, t)
    ctx.restore()
    ctx.identity_matrix()
    ctx.set_source_surface(vig, 0, 0); ctx.paint()
    if sc['caps']:
        g = cairo.RadialGradient(300, 150, 50, 300, 150, 1100)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.30); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(g); ctx.paint()
    caps2(ctx, t, sc['caps'], sc.get('cx', 90), sc.get('cy', 80))
    if sc.get('counter'):
        lab, num, unit, t0 = sc['counter']
        if callable(num): num = num(t)
        counter(ctx, lab, num, unit, fin(t, t0))
    footer(ctx, sc['src'], fin(t, 0.6))


def render(T):
    i = 0
    while i + 1 < len(SCENES) and T >= STARTS[i+1]: i += 1
    t = T - STARTS[i]
    draw_scene(C, i, t)
    if i > 0 and t < TR:
        u = smooth(t / TR)
        draw_scene(CB, i - 1, SCENES[i - 1]['D'] - 0.001)
        surfA_ctx = CA; surfA_ctx.identity_matrix()
        surfA_ctx.set_source_surface(surf, 0, 0); surfA_ctx.paint()   # copy current
        C.identity_matrix()
        kind = i % 3
        if kind == 0:   # zoom-through crossfade
            C.set_source_surface(surfA, 0, 0); C.paint()
            C.save(); C.translate(W / 2, H / 2); C.scale(1 + 0.18 * u, 1 + 0.18 * u); C.translate(-W / 2, -H / 2)
            C.set_source_surface(surfB, 0, 0); C.paint_with_alpha(1 - u); C.restore()
        elif kind == 1:  # push slide
            C.set_source_surface(surfB, -W * 0.35 * u, 0); C.paint()
            C.set_source_rgba(0, 0, 0, 0.5 * u); C.paint()
            xx = W * (1 - u)
            C.save(); C.rectangle(xx, 0, W, H); C.clip()
            C.set_source_surface(surfA, xx * 0.25, 0); C.paint(); C.restore()
            rgba(C, GOLDL, 0.9 * (1 - abs(2 * u - 1))); C.rectangle(xx - 4, 0, 8, H); C.fill()
        else:            # iris
            C.set_source_surface(surfB, 0, 0); C.paint()
            r = 1150 * u
            C.save(); C.arc(W / 2, H / 2, max(1, r), 0, 6.283); C.clip()
            C.set_source_surface(surfA, 0, 0); C.paint(); C.restore()
            rgba(C, GOLDL, 0.8 * (1 - u)); C.set_line_width(6); C.arc(W / 2, H / 2, max(1, r), 0, 6.283); C.stroke()
    if T > TOTAL - 1.2:
        C.identity_matrix(); C.set_source_rgba(0, 0, 0, clamp((T - (TOTAL - 1.2)) / 1.2)); C.paint()
    surf.flush()


def still(ts, d='stills'):
    os.makedirs(d, exist_ok=True)
    for T in ts:
        t0 = time.time(); render(T); surf.write_to_png('%s/f_%06.2f.png' % (d, T)); print(T, '%.2fs' % (time.time()-t0))


def segment(f0, f1, out):
    cmd = ['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgra','-s','%dx%d'%(W,H),'-r',str(FPS),'-i','-',
           '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-threads','1',out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); t0 = time.time()
    for f in range(f0, f1):
        render(f / FPS); p.stdin.write(bytes(surf.get_data()))
        if (f-f0) % 300 == 0: print(out, f-f0, f1-f0, '%.0fs' % (time.time()-t0), flush=True)
    p.stdin.close(); p.wait(); print('DONE', out, time.time()-t0, flush=True)


if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'info':
        print('TOTAL', TOTAL, 'NF', NF)
        for k,(s,st) in enumerate(zip(SCENES, STARTS)): print(k+1, '%.1f' % st, s['fn'].__name__)
    elif m == 'still': still([float(x) for x in sys.argv[2:]])
    elif m == 'mid':
        still([st + s['D'] * 0.8 for s, st in zip(SCENES, STARTS)])
    elif m == 'seg': segment(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
