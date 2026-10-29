"""社恐小人风 引擎底层：cairo 扁平描边绘图工具"""
import cairocffi as cairo, math, random
W, H, FPS = 1920, 1080, 30
OL = '#232842'          # 统一描边色（深藏青）
FONT = 'Noto Sans SC'   # 字幕/HUD 用黑体 Black
_hc = {}
def hx(h, a=1.0):
    if h not in _hc:
        s = h.lstrip('#'); s = ''.join(ch*2 for ch in s) if len(s) == 3 else s; _hc[h] = (int(s[:2], 16)/255, int(s[2:4], 16)/255, int(s[4:], 16)/255)
    r, g, b = _hc[h]; return (r, g, b, a)
def col(c, h, a=1): c.set_source_rgba(*hx(h, a))
def cl(x, a=0., b=1.): return max(a, min(b, x))
def lerp(a, b, k): return a+(b-a)*k
def ease(x): x = cl(x); return x*x*(3-2*x)
def eo(x): x = cl(x); return 1-(1-x)**3
def eback(x, s=2.2): x = cl(x)-1; return x*x*((s+1)*x+s)+1
def ramp(t, t0, t1): return ease((t-t0)/(t1-t0)) if t1 > t0 else float(t >= t1)
def pop(t, t0, d=.25): return max(.02, eback((t-t0)/d)) if t >= t0 else 0.
def mix(h1, h2, k):
    a, b = hx(h1), hx(h2)
    return '#%02x%02x%02x' % tuple(int(255*lerp(a[i], b[i], k)) for i in range(3))

def fill_stroke(c, f, a=1, lw=5, oc=OL):
    if f: col(c, f, a); c.fill_preserve()
    if lw: col(c, oc, a); c.set_line_width(lw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    else: c.new_path()
def rrect(c, x, y, w, h, r):
    r = min(r, w/2, h/2)
    c.new_sub_path()
    c.arc(x+w-r, y+r, r, -math.pi/2, 0); c.arc(x+w-r, y+h-r, r, 0, math.pi/2)
    c.arc(x+r, y+h-r, r, math.pi/2, math.pi); c.arc(x+r, y+r, r, math.pi, 1.5*math.pi); c.close_path()
def box(c, x, y, w, h, f, r=0, lw=5, a=1):
    if r: rrect(c, x, y, w, h, r)
    else: c.rectangle(x, y, w, h)
    fill_stroke(c, f, a, lw)
def ellipse(c, x, y, rx, ry):
    c.save(); c.translate(x, y); c.scale(max(rx, .01), max(ry, .01)); c.arc(0, 0, 1, 0, 2*math.pi); c.restore()
def ell(c, x, y, rx, ry, f, lw=5, a=1): c.new_path(); ellipse(c, x, y, rx, ry); fill_stroke(c, f, a, lw)
def poly(c, pts, f, lw=5, a=1, close=True):
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    if close: c.close_path()
    fill_stroke(c, f, a, lw)
def tube(c, pts, w, f, lw=5):
    """橡皮管肢体：先粗描边色再细填色，圆头圆角"""
    for ww, cc in ((w+2*lw, OL), (w, f)):
        c.new_path(); c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        col(c, cc); c.set_line_width(ww); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
def stroke_line(c, pts, w, h, a=1, dash=None, off=0, cap=True):
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    col(c, h, a); c.set_line_width(w)
    c.set_line_cap(cairo.LINE_CAP_ROUND if cap else cairo.LINE_CAP_BUTT)
    if dash: c.set_dash(dash, off)
    c.stroke(); c.set_dash([])
def text(c, s, x, y, size, h='#ffffff', weight='Black', anchor='c', a=1, stroke=None, sw=0, font=FONT):
    c.select_font_face(font+(' '+weight if weight == 'Black' else ''), cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size)
    ext = c.text_extents(s); w = ext[4]
    xx = x-w/2 if anchor == 'c' else (x if anchor == 'l' else x-w)
    c.new_path(); c.move_to(xx, y+size*.36); c.text_path(s)
    if stroke: col(c, stroke, a); c.set_line_width(sw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    col(c, h, a); c.fill()
    return w
def text_w(c, s, size, weight='Black'):
    c.select_font_face(FONT+(' '+weight if weight == 'Black' else ''), cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size); return c.text_extents(s)[4]
def star(c, x, y, r, f, lw=4, n=5, inner=.45, rot=0):
    pts = []
    for i in range(2*n):
        rr = r if i % 2 == 0 else r*inner; a = rot-math.pi/2+i*math.pi/n
        pts.append((x+rr*math.cos(a), y+rr*math.sin(a)))
    poly(c, pts, f, lw)
def qcurve(p0, p1, p2, n=40):
    return [((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0], (1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1])
            for t in [i/n for i in range(n+1)]]
