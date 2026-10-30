import cairocffi as cairo, math, random, numpy as np
W,H,FPS=1920,1080,30
FONT='Noto Serif CJK SC'
def hx(h,a=1.0):
    h=h.lstrip('#');return (int(h[:2],16)/255,int(h[2:4],16)/255,int(h[4:],16)/255,a)
GOLD='#d9b56a';RED='#c0392b';CREAM='#efe2c4';GREY='#8a7d68'
def cl(x,a=0,b=1):return max(a,min(b,x))
def ease(x):x=cl(x);return x*x*(3-2*x)
def eo(x):x=cl(x);return 1-(1-x)**3
def eback(x,s=1.7):x=cl(x);x-=1;return x*x*((s+1)*x+s)+1
def lerp(a,b,k):return a+(b-a)*k
def col(c,h,a=1):c.set_source_rgba(*hx(h,a))
def rect(c,x,y,w,h,f,a=1):col(c,f,a);c.rectangle(x,y,w,h);c.fill()
def circ(c,x,y,r,f,a=1):col(c,f,a);c.arc(x,y,r,0,2*math.pi);c.fill()
def poly(c,pts,f=None,a=1,s=None,lw=2,sa=1):
    c.move_to(*pts[0])
    for p in pts[1:]:c.line_to(*p)
    c.close_path()
    if f:col(c,f,a)
    if f and s:c.fill_preserve()
    elif f:c.fill()
    if s:col(c,s,sa);c.set_line_width(lw);c.stroke()
def glow(c,x,y,r,h,a=.6):
    g=cairo.RadialGradient(x,y,0,x,y,r);g.add_color_stop_rgba(0,*hx(h,a));g.add_color_stop_rgba(1,*hx(h,0))
    c.set_source(g);c.arc(x,y,r,0,2*math.pi);c.fill()
def text(c,s,x,y,size,h=CREAM,a=1,align='c',bold=True,sp=0):
    c.select_font_face(FONT,0,1 if bold else 0);c.set_font_size(size)
    if sp:
        ws=[c.text_extents(ch)[4] for ch in s];tw=sum(ws)+sp*(len(s)-1)
        x0=x-tw/2 if align=='c' else (x-tw if align=='r' else x)
        col(c,h,a)
        for ch,w in zip(s,ws):c.move_to(x0,y);c.show_text(ch);x0+=w+sp
        return tw
    e=c.text_extents(s);tw=e[4]
    x0=x-tw/2 if align=='c' else (x-tw if align=='r' else x)
    col(c,h,a);c.move_to(x0,y);c.show_text(s);return tw
def vtext(c,s,x,y,size,h=CREAM,a=1):
    c.select_font_face(FONT,0,1);c.set_font_size(size);col(c,h,a)
    for i,ch in enumerate(s):
        e=c.text_extents(ch);c.move_to(x-e[4]/2,y+i*size*1.15);c.show_text(ch)
def rich(c,s,x,y,size,a=1):
    # {gold} segments
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
        # shadow
        col(c,'#000000',.6*a);c.move_to(x0+2,y+2);c.show_text(t)
        col(c,GOLD if gg else '#efe6d2',a);c.move_to(x0,y);c.show_text(t);x0+=c.text_extents(t)[4]
# precomputed textures
def make_overlay():
    rng=np.random.default_rng(3)
    n=(rng.random((H,W))*255).astype(np.uint8)
    arr=np.zeros((H,W,4),np.uint8);a=(np.abs(n.astype(int)-128)>118)*14
    arr[...,3]=a.astype(np.uint8)
    yy,xx=np.mgrid[0:H,0:W];d=np.sqrt(((xx-W/2)/(W*.62))**2+((yy-H/2)/(H*.62))**2)
    v=np.clip((d-.55)/.6,0,1)**1.6*215
    arr[...,3]=np.clip(arr[...,3].astype(int)+v.astype(int),0,255).astype(np.uint8)
    # premultiplied black: rgb 0
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H)
    buf=s.get_data();np.frombuffer(buf,np.uint8).reshape(H,s.get_stride()//4,4)[:, :W]=arr
    s.mark_dirty();return s
