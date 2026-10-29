import cairocffi as cairo, math, random, numpy as np
W,H,FPS=1920,1080,30
FONT='Noto Serif CJK SC'
_hc={}
def hx(h,a=1.0):
    if h not in _hc:
        s=h.lstrip('#');_hc[h]=(int(s[:2],16)/255,int(s[2:4],16)/255,int(s[4:],16)/255)
    r,g,b=_hc[h];return (r,g,b,a)
GOLD='#d9b56a';RED='#c0392b';CREAM='#efe2c4';GREY='#8a7d68';INK='#120c08'
def cl(x,a=0,b=1):return max(a,min(b,x))
def ease(x):x=cl(x);return x*x*(3-2*x)
def eio(x):x=cl(x);return 4*x*x*x if x<.5 else 1-(-2*x+2)**3/2
def eo(x):x=cl(x);return 1-(1-x)**3
def ei(x):x=cl(x);return x*x*x
def eback(x,s=1.7):x=cl(x);x-=1;return x*x*((s+1)*x+s)+1
def lerp(a,b,k):return a+(b-a)*k
def seg(t,keys):
    """keys: [(t,val),...] piecewise eased interpolation"""
    if t<=keys[0][0]:return keys[0][1]
    for (t0,v0),(t1,v1) in zip(keys,keys[1:]):
        if t<=t1:
            k=eio((t-t0)/(t1-t0)) if t1>t0 else 1
            if isinstance(v0,tuple):return tuple(lerp(a,b,k) for a,b in zip(v0,v1))
            return lerp(v0,v1,k)
    return keys[-1][1]
def col(c,h,a=1):c.set_source_rgba(*hx(h,a))
def rect(c,x,y,w,h,f,a=1):col(c,f,a);c.rectangle(x,y,w,h);c.fill()
def circ(c,x,y,r,f,a=1):col(c,f,a);c.arc(x,y,max(r,0.01),0,2*math.pi);c.fill()
def ell(c,x,y,rx,ry,f,a=1):
    c.save();c.translate(x,y);c.scale(max(rx,.01),max(ry,.01));c.arc(0,0,1,0,2*math.pi);c.restore();col(c,f,a);c.fill()
def path(c,pts,close=True):
    c.move_to(*pts[0])
    for p in pts[1:]:c.line_to(*p)
    if close:c.close_path()
def poly(c,pts,f=None,a=1,s=None,lw=2,sa=1):
    path(c,pts)
    if f:col(c,f,a)
    if f and s:c.fill_preserve()
    elif f:c.fill()
    if s:col(c,s,sa);c.set_line_width(lw);c.stroke()
def line(c,x0,y0,x1,y1,h,lw=2,a=1,cap=1):
    col(c,h,a);c.set_line_width(lw);c.set_line_cap(cap);c.move_to(x0,y0);c.line_to(x1,y1);c.stroke()
def lgrad(c,x0,y0,x1,y1,stops):
    g=cairo.LinearGradient(x0,y0,x1,y1)
    for o,h,a in stops:g.add_color_stop_rgba(o,*hx(h,a))
    return g
def glow(c,x,y,r,h,a=.6):
    if r<=0 or a<=0:return
    g=cairo.RadialGradient(x,y,0,x,y,r);g.add_color_stop_rgba(0,*hx(h,a));g.add_color_stop_rgba(1,*hx(h,0))
    c.set_source(g);c.arc(x,y,r,0,2*math.pi);c.fill()
def text(c,s,x,y,size,h=CREAM,a=1,align='c',bold=True,sp=0,shadow=0):
    c.select_font_face(FONT,0,1 if bold else 0);c.set_font_size(size)
    ws=[c.text_extents(ch)[4] for ch in s];tw=sum(ws)+sp*(len(s)-1)
    x0=x-tw/2 if align=='c' else (x-tw if align=='r' else x)
    for pas in ([1,0] if shadow else [0]):
        xx=x0
        if pas:col(c,'#000000',a*.6*shadow)
        else:col(c,h,a)
        for ch,w in zip(s,ws):
            c.move_to(xx+(2 if pas else 0),y+(2 if pas else 0));c.show_text(ch);xx+=w+sp
    return tw
def vtext(c,s,x,y,size,h=CREAM,a=1,lh=1.18,shadow=0):
    c.select_font_face(FONT,0,1);c.set_font_size(size)
    for i,ch in enumerate(s):
        if ch==' ':continue
        e=c.text_extents(ch)
        if shadow:col(c,'#000000',a*.6);c.move_to(x-e[4]/2+3,y+i*size*lh+3);c.show_text(ch)
        col(c,h,a);c.move_to(x-e[4]/2,y+i*size*lh);c.show_text(ch)
def rich(c,s,x,y,size,a=1):
    segs=[];cur='';g=False
    for ch in s:
        if ch=='{':segs.append((cur,g));cur='';g=True
        elif ch=='}':segs.append((cur,g));cur='';g=False
        else:cur+=ch
    segs.append((cur,g))
    c.select_font_face(FONT,0,1);c.set_font_size(size)
    tw=sum(c.text_extents(t)[4] for t,_ in segs);x0=x-tw/2
    for t,gg in segs:
        if not t:continue
        col(c,'#000000',.7*a);c.move_to(x0+2,y+3);c.show_text(t)
        col(c,GOLD if gg else '#efe6d2',a);c.move_to(x0,y);c.show_text(t);x0+=c.text_extents(t)[4]
    return tw
def surf(w=W,h=H):return cairo.ImageSurface(cairo.FORMAT_ARGB32,int(w),int(h))
def make_overlay():
    rng=np.random.default_rng(3)
    n=(rng.random((H,W))*255).astype(np.uint8)
    arr=np.zeros((H,W,4),np.uint8);a=(np.abs(n.astype(int)-128)>120)*16
    yy,xx=np.mgrid[0:H,0:W];d=np.sqrt(((xx-W/2)/(W*.62))**2+((yy-H/2)/(H*.62))**2)
    v=np.clip((d-.5)/.65,0,1)**1.5*225
    arr[...,3]=np.clip(a+v.astype(int),0,255).astype(np.uint8)
    s=surf();np.frombuffer(s.get_data(),np.uint8).reshape(H,s.get_stride()//4,4)[:,:W]=arr
    s.mark_dirty();return s
def make_paper(seed=7):
    rng=np.random.default_rng(seed)
    base=rng.random((H//8,W//8));
    from PIL import Image
    im=np.array(Image.fromarray((base*255).astype(np.uint8)).resize((W,H),Image.BICUBIC)).astype(float)/255
    fine=rng.random((H,W))
    v=(im*0.6+fine*0.4)
    arr=np.zeros((H,W,4),np.uint8)
    al=(np.abs(v-.5)*60).astype(np.uint8)
    lightm=v>.5
    arr[...,0]=np.where(lightm,int(0xd9*0.25),0);arr[...,1]=np.where(lightm,int(0xb5*0.25),0);arr[...,2]=np.where(lightm,int(0x6a*0.25),0)
    arr[...,3]=al
    # premultiply
    for k in range(3):arr[...,k]=(arr[...,k].astype(int)*al//255).astype(np.uint8)
    s=surf();np.frombuffer(s.get_data(),np.uint8).reshape(H,s.get_stride()//4,4)[:,:W]=arr[...,[2,1,0,3]]
    s.mark_dirty();return s
