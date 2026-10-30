import sys,subprocess,math,random,re
from base import *
import shots1,shots2,common
NB=common.CUR[0];TOTAL=NB*B
SH.sort(key=lambda s:s[0])
CUTS=sorted(set(round(a,4) for a,b_,f,p in SH if a>0))
TYPES=['punch','whip','flash','iris','punch','slide','whip','punch']
OV=None
HITS=[]
def subt(c,T):
    for t0,t1,s,src in SUBS:
        if t0<=T<t1:
            a=cl((T-t0)/.12)*cl((t1-T)/.1)
            g=cairo.LinearGradient(0,H-230,0,H);g.add_color_stop_rgba(0,0,0,0,0);g.add_color_stop_rgba(1,0,0,0,.82);c.set_source(g);c.rectangle(0,H-230,W,230);c.fill()
            n=len(s.replace('{','').replace('}',''));size=min(60,int(1720/max(n,1)))
            u=T-t0;sc=1+.1*math.exp(-u*14)*(u<.5)
            c.save();c.translate(W/2,H-96);c.scale(sc,sc);c.translate(-W/2,-(H-96));clib.rich(c,s,W/2,H-100 if src else H-80,size,a)
            c.restore()
            if src:text(c,src,W/2,H-40,24,'#b8a888',a*.9)
def shake(T,hits,amp=14):
    ox=oy=0
    for h in hits:
        u=T-h
        if 0<=u<.3:k=(1-u/.3)**2;ox+=math.sin(u*90)*amp*k;oy+=math.cos(u*71)*amp*k
    return ox,oy
def frac_of(place,T):
    m=re.match(r'(\d{4})年(?:(\d{1,2})月)?',place or '')
    if not m:return None
    y=int(m.group(1));mo=int(m.group(2) or 6)
    return cl((y+(mo-1)/12-1920)/5)
LASTF=[0.98]
def frame(T):
    s1=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c1=cairo.Context(s1)
    pl_=''
    for t0,t1,fn,place in SH:
        if t0<=T<t1:fn(c1,T-t0,T);pl_=place;break
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c=cairo.Context(s)
    rect(c,0,0,W,H,'#000000')
    ox,oy=shake(T,HITS+CUTS,10)
    ci=None
    for i,ct in enumerate(CUTS):
        if 0<=T-ct<.3:ci=i;u=T-ct
    c.save();c.translate(ox,oy)
    ty=TYPES[ci%len(TYPES)] if ci is not None else None
    if ty=='punch':
        k=1-(1-min(1,u/.22))**3;z=lerp(1.15,1,k);c.translate(W/2,H/2);c.scale(z,z);c.translate(-W/2,-H/2)
    if ty=='whip' and u<.2:
        k=1-(1-u/.2)**3;c.translate((1-k)*W*.5,0)
        for j in range(5):c.save();c.set_source_surface(s1,-j*28*(1-k),0);c.paint_with_alpha(.18*(1-k));c.restore()
    if ty=='slide' and u<.25:
        k=1-(1-u/.25)**3;c.translate(0,(1-k)*H*.35)
    if ty=='iris' and u<.3:
        k=eo(u/.3);c.new_sub_path();c.arc(W/2,H/2,60+1150*k,0,2*math.pi);c.clip()
    c.set_source_surface(s1,0,0);c.paint();c.restore()
    if ty=='flash':rect(c,0,0,W,H,'#fff6e0',.8*max(0,1-u/.18))
    elif ty=='punch':rect(c,0,0,W,H,'#ffffff',.25*max(0,1-u/.1))
    elif ty=='whip' and u<.2:
        r=random.Random(ci)
        for j in range(30):y=r.uniform(0,H);col(c,'#f3e6c8',.5*(1-u/.2));c.set_line_width(r.uniform(1,4));c.move_to(0,y);c.line_to(W,y);c.stroke()
    c.set_source_surface(OV,0,0);c.paint()
    f=frac_of(pl_,T)
    if f is None:f=LASTF[0]
    else:LASTF[0]=f
    topbar(c,T,f,pl_,('1920','1924'))
    subt(c,T)
    return s
if __name__=='__main__':
    OV=make_overlay()
    if sys.argv[1]=='still':
        for b in sys.argv[2:]:frame(float(b)).write_to_png(f'h_{b}.png')
    elif sys.argv[1]=='info':
        print('beats',NB,'sec',TOTAL,'shots',len(SH))
        for t0,t1,fn,p in SH:print(f'{fn.__name__} {t0:.2f}-{t1:.2f} {(t0+t1)/2:.2f}')
    else:
        i0,i1,out=int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r','30','-i','-','-c:v','libx264','-preset','medium','-crf','21','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        for i in range(i0,i1):p.stdin.write(bytes(frame(i/30).get_data()))
        p.stdin.close();p.wait()
