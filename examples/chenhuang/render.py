import sys,subprocess,os
from lib import *
from timeline import SH
TRD={'fade':.6,'push':.55,'dive':.6,'ink':.8,'fire':.8,'smoke':.9,'flash':.3,'flag':.7,'cut':0,'match':0}
starts=[];acc=0
for sh in SH:starts.append(acc);acc+=sh['T']
TOTAL=acc
OV=None;PAPER=None
def ui(c,i,t,a=1):
    sh=SH[i];T=sh['T']
    bar=sh.get('bar')
    if bar:
        l0,l1,k=bar;x0,x1=60,380
        text(c,l0,x0,42,16,GREY,.85,align='l');text(c,l1,x1,42,16,GREY,.85,align='r')
        line(c,x0,54,x1,54,GREY,1.5,.5,0)
        kk=k if not isinstance(k,tuple) else lerp(k[0],k[1],ease(t/T))
        line(c,x0,54,lerp(x0,x1,kk),54,RED,3,.95,0);circ(c,lerp(x0,x1,kk),54,4.5,RED)
    if sh.get('lab'):
        rect(c,W-63,28,3,30,RED);text(c,sh['lab'],W-78,52,24,'#c9b88e',.92,align='r')
    if sh.get('yi',True):text(c,'（示意）',60,1058,16,GREY,.45,align='l')
    cur=None
    for st,s in sh['subs']:
        if t>=st:cur=(st,s)
    if cur:
        aa=cl((t-cur[0])/.2)*a
        g=lgrad(c,0,870,0,H,[(0,'#000000',0),(1,'#000000',.72)]);c.set_source(g);c.rectangle(0,870,W,210);c.fill()
        rich(c,cur[1],W/2,988,46,aa)
        if sh.get('src'):text(c,sh['src'],W/2,1036,21,GREY,aa*.9,bold=False)
def draw_shot(i,t):
    s=surf();c=cairo.Context(s)
    col(c,'#120c08');c.paint()
    c.save();SH[i]['f'](c,t,SH[i]['T']);c.restore()
    return s
def ink_mask(c,k,seed=3):
    r=random.Random(seed)
    for j in range(14):
        x=r.uniform(0,W);y=r.uniform(0,H);st=r.uniform(0,.45);kk=cl((k-st)/(.55))
        R=eo(kk)*r.uniform(500,900)
        if R<=1:continue
        n=40
        for q in range(n+1):
            an=q/n*6.283;rr=R*(1+.18*math.sin(an*5+j)+.08*math.sin(an*13+j*2))
            (c.move_to if q==0 else c.line_to)(x+math.cos(an)*rr,y+math.sin(an)*rr)
        c.close_path()
def compose(i,t):
    """i shot index, t local time"""
    sh=SH[i];T=sh['T']
    # incoming transition of this shot
    tr=sh.get('tr','cut');d=TRD.get(tr,0)
    nxt=SH[i+1] if i+1<len(SH) else None
    ntr=nxt.get('tr','cut') if nxt else 'cut';nd=TRD.get(ntr,0)
    if nxt and t>T-nd/2:   # in outgoing half of next transition
        return mix(i,t,i+1,t-T,ntr,nd)
    if t<d/2 and i>0:
        return mix(i-1,SH[i-1]['T']+t,i,t,tr,d)
    s=draw_shot(i,t);c=cairo.Context(s);finish(c,i,t);return s
def mix(ia,ta,ib,tb,tr,d):
    k=cl((tb+d/2)/d) if d>0 else 1
    A=draw_shot(ia,ta);B=draw_shot(ib,max(tb,0))
    out=surf();c=cairo.Context(out)
    if tr=='fade':
        c.set_source_surface(A);c.paint_with_alpha(cl(1-k*2));
        if k>.5:c.set_source_surface(B);c.paint_with_alpha(cl(k*2-1))
    elif tr=='push':
        e=eio(k);c.set_source_surface(A,-e*W,0);c.paint();c.set_source_surface(B,W*(1-e),0);c.paint()
        for j in range(6):line(c,lerp(W,0,e)+j*30-90,0,lerp(W,0,e)+j*30-90,H,'#f2d48a',2,.15*math.sin(k*math.pi))
    elif tr=='dive':
        e=ei(k)
        c.save();c.translate(W/2,H/2);c.scale(1+e*2.2,1+e*2.2);c.translate(-W/2,-H/2);c.set_source_surface(A);c.paint();c.restore()
        c.save();c.translate(W/2,H/2);sc=lerp(1.25,1,eo(k));c.scale(sc,sc);c.translate(-W/2,-H/2);c.set_source_surface(B);c.paint_with_alpha(eio(k));c.restore()
        col(c,'#ffffff',.25*math.sin(k*math.pi));c.paint()
    elif tr=='ink':
        c.set_source_surface(A);c.paint()
        c.save();ink_mask(c,k);c.clip();c.set_source_surface(B);c.paint();c.restore()
        c.save();ink_mask(c,k);col(c,'#000000',.6*(1-k));c.set_line_width(14);c.stroke();c.restore()
    elif tr=='fire':
        c.set_source_surface(A);c.paint()
        xe=lerp(-300,W+300,eio(k))
        def edge():
            c.move_to(-10,-10)
            for y in range(0,H+41,40):c.line_to(xe+math.sin(y*.02+k*20)*80+math.sin(y*.07)*30,y)
            c.line_to(-10,H+10);c.close_path()
        c.save();edge();c.clip();c.set_source_surface(B);c.paint();c.restore()
        c.save()
        for y in range(0,H+1,12):
            x=xe+math.sin(y*.02+k*20)*80+math.sin(y*.07)*30
            glow(c,x,y,70,'#ff7a20',.35);circ(c,x,y,6,'#ffd27a',.8)
        r=random.Random(2)
        for j in range(80):
            y=r.uniform(0,H);x=xe+r.uniform(-60,200);circ(c,x+math.sin(k*30+j)*20,y-k*200*r.random(),r.uniform(1.5,4),'#ffb04a',.8)
        c.restore()
    elif tr=='smoke':
        c.set_source_surface(A if k<.5 else B);c.paint()
        dens=math.sin(k*math.pi)
        r=random.Random(5)
        for j in range(40):
            x=r.uniform(-200,W+200)+k*r.uniform(-300,300);y=r.uniform(-100,H+100)-k*200
            R=r.uniform(200,420)*(.5+dens)
            ell(c,x,y,R,R*.7,'#0e0a08',.55*dens)
        col(c,'#0e0a08',cl(dens*1.3-.3));c.paint()
    elif tr=='flash':
        c.set_source_surface(A if k<.5 else B);c.paint()
        col(c,'#fff8ec',math.sin(k*math.pi)**.6);c.paint()
    elif tr=='flag':
        xc=lerp(W+700,-700,eio(k))
        c.set_source_surface(A);c.paint()
        c.save();c.rectangle(xc,0,W,H);c.clip();c.set_source_surface(B);c.paint();c.restore()
        # cloth
        pts=[(xc-480,-50)]
        for y in range(-50,H+60,30):pts.append((xc-480+math.sin(y*.012+k*12)*50,y))
        for y in range(H+50,-60,-30):pts.append((xc+260+math.sin(y*.01+k*10)*70,y))
        poly(c,pts,'#a8261c',1)
        for y in range(-50,H+60,90):line(c,xc-480+math.sin(y*.012+k*12)*50,y,xc+260,y+40,'#7a1a12',8,.35)
        c.select_font_face(FONT,0,1);text(c,'楚',xc-110,H/2+150,420,'#e8c97a',.9)
    else:
        c.set_source_surface(B);c.paint()
    i_ui,t_ui=(ia,ta) if k<.5 else (ib,max(tb,0))
    finish(c,i_ui,t_ui)
    return out
def finish(c,i,t):
    c.set_source_surface(PAPER);c.paint()
    c.set_source_surface(OV);c.paint()
    ui(c,i,t)
def frame(fi):
    global OV,PAPER
    if OV is None:OV=make_overlay();PAPER=make_paper()
    tt=fi/FPS
    i=max(j for j in range(len(SH)) if starts[j]<=tt+1e-9);t=tt-starts[i]
    s=compose(i,t)
    c=cairo.Context(s)
    if tt<.6:col(c,'#000000',1-tt/.6);c.paint()
    if tt>TOTAL-1.2:col(c,'#000000',cl((tt-(TOTAL-1.2))/1.2));c.paint()
    return s
def rgb(s):
    a=np.frombuffer(s.get_data(),np.uint8).reshape(H,s.get_stride()//4,4)[:,:W,:3]
    return a[:,:,::-1].tobytes()
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='sheet':
        from PIL import Image
        ts=[float(x) for x in sys.argv[2].split(',')]
        ims=[]
        for x in ts:
            im=Image.frombytes('RGB',(W,H),rgb(frame(int(x*FPS)))).resize((640,360))
            from PIL import ImageDraw
            ImageDraw.Draw(im).text((6,4),f'{x:.1f}',fill=(0,255,0))
            ims.append(im)
        cols=3;rows=(len(ims)+2)//3;sh=Image.new('RGB',(640*cols,360*rows))
        for k,im in enumerate(ims):sh.paste(im,((k%cols)*640,(k//cols)*360))
        sh.save(sys.argv[3]);print('ok',TOTAL)
    elif mode=='one':
        frame(int(float(sys.argv[2])*FPS)).write_to_png(sys.argv[3])
    elif mode=='info':
        for i,sh in enumerate(SH):print(i,round(starts[i],2),sh['T'],sh['f'].__name__,sh.get('tr'))
        print('TOTAL',TOTAL)
    else:
        part,n=int(sys.argv[2]),int(sys.argv[3]);N=int(TOTAL*FPS);a=N*part//n;b=N*(part+1)//n
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',f'part{part}.mp4'],stdin=subprocess.PIPE)
        for f in range(a,b):
            p.stdin.write(rgb(frame(f)))
            if f%150==0:print(part,f,flush=True)
        p.stdin.close();p.wait();print('done',part,flush=True)
