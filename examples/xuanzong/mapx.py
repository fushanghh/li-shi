from lib import *
K=46.0
def P(lon,lat):return ((lon-105)*K,-(lat-31)*K*1.18)
COAST=[(124,40.2),(122.2,40.6),(121.2,40.9),(121.6,39.6),(121.2,38.8),(122.1,39.3),(121.4,39.8),(120.3,40.2),(119.2,39.6),(118,39.2),(117.7,38.5),(118.8,37.5),(119.5,37.1),(120.7,37.8),(122.5,37.4),(121,36.5),(120,35.8),(119.4,35),(120.3,34.3),(121,32.5),(121.9,31.0),(121.9,30),(122,29.5),(121.5,28.5),(120.5,27.5),(119.6,26),(118.6,24.6),(117,23.5),(115,22.8),(113.6,22.2),(112,21.7),(110.4,21.2),(110,20.3),(109.6,21.5),(108.2,21.6),(106.8,20.6),(106,19.4),(105.6,18.2),(106.6,17.0),(108.8,15.4),(109.3,13),(130,13),(130,40.2)]
HAINAN=[(108.6,19.2),(109.6,20.0),(110.6,20.1),(111.0,19.6),(110.4,18.6),(109.5,18.2),(108.7,18.5)]
YELLOW=[(96,35),(100,36),(103.6,36.1),(104.8,37.4),(106.4,39.2),(107.8,40.8),(110,40.6),(111,39.6),(110.5,37),(110.4,34.6),(112.4,34.9),(114.5,35),(116.5,36.2),(118.5,37.7)]
YANGTZE=[(91,33),(97,33),(99.5,28.5),(101.8,26.6),(104.6,28.8),(106.5,29.6),(109.5,31),(111.3,30.7),(113,29.5),(114.3,30.6),(116,29.8),(117.5,31),(119.5,32.2),(121.5,31.5)]
CITIES={'长安':(108.9,34.3),'洛阳':(112.4,34.6),'沙州':(94.7,40.1),'瓜州':(95.8,40.5),'凉州':(102.6,37.9),'甘州':(100.4,38.9),'肃州':(98.5,39.7),
'鄯州':(101.8,36.6),'原州':(106.3,36.0),'秦州':(105.7,34.6),'安乐州':(105.7,37.5),'崖州':(109.5,18.4),'荆南':(112.2,30.3),'潮州':(116.6,23.7),
'逻些':(91.1,29.6),'河州':(103.2,35.6),'兰州':(103.8,36.1),'伊州':(93.5,42.8),'西州':(89.2,42.9),'扬州':(119.4,32.4),'成都':(104.1,30.7),'幽州':(116.4,39.9)}
rng=random.Random(5);MTS=[]
for (lo0,lo1,la0,la1,n) in [(105.5,111,33.4,34.0,26),(112.6,114.2,35.5,38.8,22),(95,103,37.7,39.2,30),(86,101,30,35.5,90),(99,103,26,31,30),(103.5,106.5,36,37.2,10),(108,111,25,27,14),(115,119,26,29,16),(110.5,112.5,37,40,12)]:
    for i in range(n):MTS.append((rng.uniform(lo0,lo1),rng.uniform(la0,la1),rng.uniform(.7,1.3)))
MTS.sort(key=lambda m:-m[1])
def pl(c,pts):
    c.move_to(*P(*pts[0]))
    for p in pts[1:]:c.line_to(*P(*p))
def basemap(c,cx,cy,zoom,t,tibet=0.0,regions=()):
    # cx,cy lon/lat center
    g=cairo.RadialGradient(W/2,H/2,100,W/2,H/2,1200);g.add_color_stop_rgb(0,*hx('#3a2c1c')[:3]);g.add_color_stop_rgb(1,*hx('#17110b')[:3]);c.set_source(g);c.paint()
    c.save();c.translate(W/2,H/2);c.scale(zoom,zoom);x0,y0=P(cx,cy);c.translate(-x0,-y0)
    s=1/zoom
    if tibet>0:
        # tubo-controlled zone (red wash) west of tang
        zone=[(78,28),(78,44),(96,44),(99,42),(103,39.6),(104.6,37.4),(106.5,36.4),(106.6,35.2),(104.5,34),(103,32),(100,29),(92,27)]
        pl(c,zone);c.close_path();col(c,'#8a2a1c',.28*tibet);c.fill_preserve();col(c,'#c0392b',.5*tibet);c.set_line_width(2.5*s);c.set_dash([10*s,8*s]);c.stroke();c.set_dash([])
    for name,(lo,la,a) in regions:
        x,y=P(lo,la);text(c,name,x,y,40*s,'#b89a62',a*.45,sp=40*s)
    # sea
    pl(c,COAST);c.close_path();col(c,'#101a1c');c.fill_preserve();col(c,'#6a8a80',.35);c.set_line_width(2.5*s);c.stroke()
    pl(c,HAINAN);c.close_path();g2='#3a2c1c';col(c,g2);c.fill_preserve();col(c,'#6a8a80',.4);c.stroke()
    for r in (YELLOW,YANGTZE):
        pl(c,r);col(c,'#d9b56a',.35);c.set_line_width(2.2*s);c.stroke()
    for lo,la,sz in MTS:
        x,y=P(lo,la);hh=14*sz;ww=11*sz
        poly(c,[(x-ww,y),(x,y-hh),(x,y)],'#8a6a3e',.75)
        poly(c,[(x,y-hh),(x+ww,y),(x,y)],'#4a3822',.8)
    return s
def endmap(c):c.restore()
def city(c,name,s,t,state='gold',pulse=0,a=1,label=True,lx=14,ly=-10,size=24):
    x,y=P(*CITIES[name])
    h=GOLD if state=='gold' else RED
    glow(c,x,y,30*s,h,.5*a)
    if pulse:
        k=(t*.8)%1;col(c,h,(1-k)*.8*a);c.set_line_width(2.5*s);c.arc(x,y,(10+50*k)*s,0,2*math.pi);c.stroke()
    circ(c,x,y,6*s,h,a);circ(c,x,y,2.5*s,'#fff4d8',a)
    if label:text(c,name,x+lx*s,y+ly*s,size*s,'#efe2c4',a,align='l' if lx>=0 else 'r')
def route(c,pts,k,s,h=GOLD,lw=3,dash=False,head=True,a=1):
    # pts lon/lat polyline, draw first k fraction
    xy=[P(*p) for p in pts];L=[0]
    for i in range(1,len(xy)):L.append(L[-1]+math.dist(xy[i-1],xy[i]))
    tot=L[-1];target=tot*cl(k)
    if target<=0:return
    c.move_to(*xy[0]);end=xy[0]
    for i in range(1,len(xy)):
        if L[i]<=target:c.line_to(*xy[i]);end=xy[i]
        else:
            r=(target-L[i-1])/(L[i]-L[i-1]);end=(lerp(xy[i-1][0],xy[i][0],r),lerp(xy[i-1][1],xy[i][1],r));c.line_to(*end);break
    if dash:c.set_dash([12*s,8*s])
    col(c,h,.35*a);c.set_line_width((lw+6)*s);c.stroke_preserve();col(c,h,a);c.set_line_width(lw*s);c.stroke();c.set_dash([])
    if head and k<1:glow(c,end[0],end[1],28*s,h,.8*a);circ(c,end[0],end[1],5*s,'#fff4d8',a)
def flag(c,lon,lat,s,txt='唐',a=1,h='#d9b56a'):
    x,y=P(lon,lat)
    col(c,'#15100c',a);c.set_line_width(2*s);c.move_to(x,y);c.line_to(x,y-40*s);c.stroke()
    poly(c,[(x,y-40*s),(x+26*s,y-38*s),(x+26*s,y-16*s),(x,y-18*s)],h,a,'#15100c',1.5*s,a)
    text(c,txt,x+13*s,y-21*s,15*s,'#7a1f1a' if h=='#d9b56a' else '#efe2c4',a)
