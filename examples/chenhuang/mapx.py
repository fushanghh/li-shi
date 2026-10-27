from lib import *
K=46.0
def P(lon,lat):return ((lon-110)*K,-(lat-31)*K*1.18)
COAST=[(124,40.2),(122.2,40.6),(121.2,40.9),(121.6,39.6),(121.2,38.8),(122.1,39.3),(121.4,39.8),(120.3,40.2),(119.2,39.6),(118,39.2),(117.7,38.5),(118.8,37.5),(119.5,37.1),(120.7,37.8),(122.5,37.4),(121,36.5),(120,35.8),(119.4,35),(120.3,34.3),(121,32.5),(121.9,31.0),(121.9,30),(122,29.5),(121.5,28.5),(120.5,27.5),(119.6,26),(118.6,24.6),(117,23.5),(115,22.8),(113.6,22.2),(112,21.7),(110.4,21.2),(110,20.3),(109.6,21.5),(108.2,21.6),(106.8,20.6),(106,19.4),(105.6,18.2),(106.6,17.0),(108.8,15.4),(109.3,13),(170,13),(170,40.2)]
KOREA=[(124,40.2),(125.5,39.5),(125.2,38),(126.5,37.4),(126.3,35),(127.5,34.6),(129.3,35.3),(129.5,36.8),(128.5,38.6),(127.5,39.8),(129.8,41),(170,41),(170,40.2)]
HAINAN=[(108.6,19.2),(109.6,20.0),(110.6,20.1),(111.0,19.6),(110.4,18.6),(109.5,18.2),(108.7,18.5)]
TAIWAN=[(120.1,23.0),(120.7,22.0),(121.0,22.6),(121.9,24.6),(121.5,25.3),(120.8,24.6)]
YELLOW=[(96,35),(100,36),(103.6,36.1),(104.8,37.4),(106.4,39.2),(107.8,40.8),(110,40.6),(111,39.6),(110.5,37),(110.4,34.6),(112.4,34.9),(114.5,35),(116.5,36.2),(118.5,37.7)]
YANGTZE=[(91,33),(97,33),(99.5,28.5),(101.8,26.6),(104.6,28.8),(106.5,29.6),(109.5,31),(111.3,30.7),(113,29.5),(114.3,30.6),(116,29.8),(117.5,31),(119.5,32.2),(121.5,31.5)]
HUAI=[(113.2,32.4),(114.5,32.4),(115.6,32.5),(116.6,32.8),(117.6,33.0),(118.6,33.3),(119.3,33.6),(120.2,34.0)]
PEARL=[(104,24.5),(107,23.5),(109.5,23.4),(111.5,23.2),(113.2,23.1)]
XIANG=[(110.3,25.5),(111.5,26.4),(112.6,27.5),(112.9,28.3),(112.9,29.3)]
GAN=[(115.0,25.8),(115.0,27),(115.8,28.6),(116.2,29.3)]
CITIES={'大泽乡':(117.4,33.4),'渔阳':(116.85,40.37),'咸阳':(108.7,34.33),'陈':(114.88,33.73),'蕲':(117.05,33.6),'荥阳':(113.4,34.8),'邯郸':(114.5,36.6),'戏':(109.25,34.4),'下城父':(116.2,33.4),'砀':(116.35,34.1),
'冤句':(115.3,35.1),'郓州':(116.3,35.9),'汝州':(112.8,34.2),'洛阳':(112.45,34.62),'潼关':(110.25,34.55),'长安':(108.94,34.27),'成都':(104.07,30.67),'广州':(113.26,23.13),'福州':(119.3,26.08),
'桂州':(110.29,25.27),'潭州':(112.94,28.23),'江陵':(112.2,30.35),'宣州':(118.75,30.95),'越州':(120.58,30.0),'洪州':(115.9,28.68),'泗州':(118.0,33.0),'陈州':(114.88,33.73),'狼虎谷':(117.68,36.2),'蔡州':(114.36,33.0),'汴州':(114.35,34.8),'泉州':(118.6,24.9)}
rng=random.Random(5);MTS=[]
for (lo0,lo1,la0,la1,n) in [(105.5,111,33.2,34.0,30),(112.6,114.2,35.5,38.8,24),(95,103,37.7,39.2,26),(86,101,30,35.5,80),(99,103,26,31,30),(103.5,106.5,36,37.2,10),(108,111.5,24.6,27,20),(115,119,25.5,28.6,24),(110.5,112.5,37,40,12),(117,118.5,35.8,36.6,10),(109,111,28.5,31.5,14),(113,116,30.5,31.6,10),(112,114.5,24.4,25.6,10),(104,108,31.6,33,14)]:
    for i in range(n):MTS.append((rng.uniform(lo0,lo1),rng.uniform(la0,la1),rng.uniform(.7,1.3)))
MTS.sort(key=lambda m:-m[1])
def pl(c,pts):
    c.move_to(*P(*pts[0]))
    for p in pts[1:]:c.line_to(*P(*p))
def basemap(c,cx,cy,zoom,t,regions=(),tone='#3a2c1c',mt=1.0):
    g=cairo.RadialGradient(W/2,H/2,100,W/2,H/2,1200);g.add_color_stop_rgb(0,*hx(tone)[:3]);g.add_color_stop_rgb(1,*hx('#17110b')[:3]);c.set_source(g);c.paint()
    c.save();c.translate(W/2,H/2);c.scale(zoom,zoom);x0,y0=P(cx,cy);c.translate(-x0,-y0)
    s=1/zoom
    for name,(lo,la,a) in regions:
        x,y=P(lo,la);text(c,name,x,y,44*s,'#b89a62',a*.42,sp=44*s)
    for poly_ in (COAST,KOREA):
        pl(c,poly_);c.close_path();col(c,'#0f191b');c.fill_preserve();col(c,'#6a8a80',.35);c.set_line_width(2.5*s);c.stroke()
    for pp in (HAINAN,TAIWAN):
        pl(c,pp);c.close_path();col(c,'#3a2c1c');c.fill_preserve();col(c,'#6a8a80',.4);c.stroke()
    for r in (YELLOW,YANGTZE,HUAI,PEARL,XIANG,GAN):
        pl(c,r);col(c,'#d9b56a',.3);c.set_line_width(2.2*s);c.stroke()
    for lo,la,sz in MTS:
        x,y=P(lo,la);hh=15*sz*mt;ww=11*sz*mt
        poly(c,[(x-ww,y),(x,y-hh),(x,y)],'#8a6a3e',.72);poly(c,[(x,y-hh),(x+ww,y),(x,y)],'#4a3822',.78)
    return s
def endmap(c):c.restore()
def city(c,name,s,t,state='gold',pulse=0,a=1,label=True,lx=14,ly=-10,size=24):
    x,y=P(*CITIES[name]);h=GOLD if state=='gold' else RED
    glow(c,x,y,32*s,h,.5*a)
    if pulse:
        k=(t*.8)%1;col(c,h,(1-k)*.8*a);c.set_line_width(2.5*s);c.arc(x,y,(10+55*k)*s,0,2*math.pi);c.stroke()
    circ(c,x,y,6.5*s,h,a);circ(c,x,y,2.6*s,'#fff4d8',a)
    if label:
        text(c,name,x+lx*s,y+ly*s,size*s,'#efe2c4',a,align='l' if lx>=0 else 'r',shadow=1)
def route(c,pts,k,s,h=GOLD,lw=3,dash=False,head=True,a=1):
    xy=[P(*p) for p in pts];L=[0]
    for i in range(1,len(xy)):L.append(L[-1]+math.dist(xy[i-1],xy[i]))
    tot=L[-1];target=tot*cl(k)
    if target<=0:return None
    c.move_to(*xy[0]);end=xy[0]
    for i in range(1,len(xy)):
        if L[i]<=target:c.line_to(*xy[i]);end=xy[i]
        else:
            r=(target-L[i-1])/(L[i]-L[i-1]);end=(lerp(xy[i-1][0],xy[i][0],r),lerp(xy[i-1][1],xy[i][1],r));c.line_to(*end);break
    if dash:c.set_dash([12*s,8*s])
    col(c,h,.3*a);c.set_line_width((lw+7)*s);c.stroke_preserve();col(c,h,a);c.set_line_width(lw*s);c.stroke();c.set_dash([])
    if head and k<1:glow(c,end[0],end[1],30*s,h,.8*a);circ(c,end[0],end[1],5*s,'#fff4d8',a)
    return end
def smooth(pts,n=8):
    """catmull-rom through lon/lat points"""
    out=[]
    P_=[pts[0]]+pts+[pts[-1]]
    for i in range(1,len(P_)-2):
        p0,p1,p2,p3=P_[i-1],P_[i],P_[i+1],P_[i+2]
        for k in range(n):
            t=k/n;t2=t*t;t3=t2*t
            out.append(tuple(.5*((2*p1[j])+(-p0[j]+p2[j])*t+(2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*t2+(-p0[j]+3*p1[j]-3*p2[j]+p3[j])*t3) for j in range(2)))
    out.append(pts[-1]);return out
def badge(c,x,y,r,name,sub,colr,s,a=1,draw_fig=None):
    glow(c,x,y,r*1.8,colr,.35*a)
    circ(c,x,y,r+3*s,colr,a);circ(c,x,y,r,'#2a2016',a)
    if draw_fig:
        c.save();c.arc(x,y,r,0,6.3);c.clip();draw_fig(c,x,y,r);c.restore()
    text(c,name,x,y+r+30*s,24*s,'#efe2c4',a,shadow=1);text(c,sub,x,y+r+54*s,16*s,colr,a*.9)
