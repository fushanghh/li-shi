import sys,subprocess,math,random
from base import *
import shots1,shots2,common,re
NB=common.CUR[0];TOTAL=NB*B
SH.sort(key=lambda s:s[0])
CUTS=sorted(set(round(a,4) for a,b_,f,p in SH if a>0))
TYPES=['punch','flash','whip']
OV=None;YR=[736]
def subt(c,T):
    for t0,t1,s,src in SUBS:
        if t0<=T<t1:
            a=cl((T-t0)/.12)*cl((t1-T)/.1)
            g=cairo.LinearGradient(0,H-220,0,H);g.add_color_stop_rgba(0,0,0,0,0);g.add_color_stop_rgba(1,0,0,0,.8);c.set_source(g);c.rectangle(0,H-220,W,220);c.fill()
            n=len(s.replace('{','').replace('}',''));size=min(62,int(1700/max(n,1)))
            u=T-t0;sc=1+.12*math.exp(-u*14)*(u<.5)
            c.save();c.translate(W/2,H-92);c.scale(sc,sc);c.translate(-W/2,-(H-92));clib.rich(c,s,W/2,H-96,size,a)
            if src:text(c,src,W/2,H-34,24,'#b8a888',a*.9)
            c.restore()
HITS=[]
def shake(T,hits,amp=14):
    ox=oy=0
    for h in hits:
        u=T-h
        if 0<=u<.4:k=(1-u/.4)**2;ox+=math.sin(u*90)*amp*k;oy+=math.cos(u*71)*amp*k
    return ox,oy
def frame(T):
    s1=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c1=cairo.Context(s1)
    pl_=''
    for t0,t1,fn,place in SH:
        if t0<=T<t1:fn(c1,T-t0,T);pl_=place;break
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c=cairo.Context(s)
    rect(c,0,0,W,H,'#000000')
    ox,oy=shake(T,HITS+CUTS,16)
    ci=None
    for i,ct in enumerate(CUTS):
        if 0<=T-ct<.3:ci=i;u=T-ct
    c.save();c.translate(ox,oy)
    ty=TYPES[ci%3] if ci is not None else None
    if ty=='punch':
        k=1-(1-min(1,u/.22))**3;z=lerp(1.18,1,k);c.translate(W/2,H/2);c.scale(z,z);c.translate(-W/2,-H/2)
    if ty=='whip' and u<.2:
        k=1-(1-u/.2)**3;c.translate((1-k)*W*.6,0)
        for j in range(5):c.save();c.set_source_surface(s1,-j*28*(1-k),0);c.paint_with_alpha(.18*(1-k));c.restore()
    c.set_source_surface(s1,0,0);c.paint();c.restore()
    if ty=='flash':rect(c,0,0,W,H,'#fff6e0',.85*max(0,1-u/.18))
    elif ty=='punch':rect(c,0,0,W,H,'#ffffff',.35*max(0,1-u/.1))
    elif ty=='whip' and u<.2:
        r=random.Random(ci)
        for j in range(30):y=r.uniform(0,H);col(c,'#f3e6c8',.5*(1-u/.2));c.set_line_width(r.uniform(1,4));c.move_to(0,y);c.line_to(W,y);c.stroke()
    for h in HITS:
        if 0<=T-h<.08:rect(c,0,0,W,H,'#ffffff',.5*(1-(T-h)/.08))
    c.set_source_surface(OV,0,0);c.paint()
    topbar(c,T,cl(T/TOTAL),pl_,('507','549'))
    subt(c,T)
    return s
if __name__=='__main__':
    OV=make_overlay()
    if sys.argv[1]=='still':
        for b in sys.argv[2:]:frame(float(b)*B).write_to_png(f'h_{b}.png')
    else:
        i0,i1,out=int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r','30','-i','-','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
        for i in range(i0,i1):p.stdin.write(bytes(frame(i/30).get_data()))
        p.stdin.close();p.wait()
