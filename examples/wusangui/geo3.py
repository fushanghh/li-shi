# 暗金古地图：清初全国（三藩之乱）
from lib import *
K=88.0
def P(lon,lat):return ((lon-111)*K,-(lat-30)*K*1.15)
COAST=[(126,40.5),(124,40.2),(122.2,40.6),(121.2,40.9),(121.6,39.6),(121.2,38.8),(122.1,39.3),(121.4,39.8),(120.3,40.2),(119.2,39.6),(118,39.2),(117.7,38.5),(118.8,37.5),(119.5,37.1),(120.7,37.8),(122.5,37.4),(121,36.5),(120,35.8),(119.4,35),(120.3,34.3),(121,32.5),(121.9,31.0),(121.5,30.3),(122,29.8),(121.6,28.5),(120.8,27.8),(120.2,27),(119.6,26),(119.5,25.4),(118.6,24.6),(117.6,23.8),(116.5,23),(115.4,22.8),(114.2,22.3),(113.5,22.2),(112.5,21.8),(111,21.5),(110.4,21.2),(109.8,21.5),(108.5,21.7),(107.5,21.5),(107,18),(130,18),(130,40.5)]
TAIWAN=[(121,25.3),(122,25),(121.6,23.5),(120.9,22),(120.2,22.8),(120.1,23.8),(120.7,24.8)]
HAINAN=[(108.6,19.2),(109.5,18.2),(110.5,18.7),(111,19.8),(110.3,20.1),(109.2,19.9)]
YANGTZE=[(99.5,27.5),(100.2,26.6),(102,26.2),(103.6,28.6),(104.6,28.8),(106.5,29.6),(108,30.5),(110,30.9),(111.3,30.7),(112.2,30.3),(113.1,29.45),(114.3,30.6),(115.9,29.7),(117,30.5),(118.4,31.5),(118.8,32.05),(119.4,32.2),(120.5,32),(121.6,31.5)]
HUANGHE=[(101,35.8),(103.6,36.1),(104.8,37.4),(106.4,39.2),(107.8,40.8),(110,40.6),(111,39.6),(110.6,37.8),(110.4,36.2),(110.3,34.6),(111.2,34.8),(112.4,34.9),(113.6,34.9),(114.5,35.0),(116,34.6),(117.5,34.2),(118.8,33.8),(119.8,34.0)]
XIANG=[(110.6,25.5),(111.6,26.4),(112.6,26.9),(112.9,28.2),(112.9,29.0)]
CANAL=[(116.4,39.9),(116.8,38.4),(116.3,37),(116.6,35.4),(117.2,34.2),(118.6,33.5),(119.0,32.6),(119.4,32.2),(119.6,31.6),(120.2,30.3)]
PEARL=[(104.5,24.8),(107,23.8),(109.4,23.4),(111.5,23.4),(113.2,23.1)]
DONGTING=[(112.1,29.2),(112.6,29.45),(113.1,29.35),(113.0,28.85),(112.4,28.8)]
CITIES={'北京':(116.4,39.9),'山海关':(119.75,40.0),'昆明':(102.7,25.04),'贵阳':(106.7,26.6),'成都':(104.07,30.67),'长沙':(112.94,28.23),
'岳州':(113.13,29.37),'衡阳':(112.57,26.9),'常德':(111.7,29.03),'武昌':(114.3,30.55),'江宁':(118.8,32.05),'杭州':(120.15,30.27),
'福州':(119.3,26.08),'广州':(113.26,23.13),'西安':(108.94,34.27),'平凉':(106.67,35.54),'台湾':(120.2,23.0),'桂林':(110.3,25.27),'荆州':(112.2,30.33)}
PROV={
'云南':[(98,28.5),(99.5,28),(101,26.5),(103,27.5),(104.5,26),(106,24.5),(105,23),(102,22.5),(100,21.6),(98,23.5)],
'贵州':[(104.5,26),(103.7,27.6),(106.5,29),(109,28.5),(109.5,26.4),(108.5,25.3),(106,24.8)],
'四川':[(98.5,33),(102,34),(105.5,32.8),(108.5,32),(110,31),(109,29),(106.5,29),(103.7,27.6),(101,26.5),(99.5,28)],
'湖南':[(109,28.5),(109.6,29.6),(111,30),(113.5,29.8),(114,28),(113.8,26),(112.5,25),(110,25.5),(109.5,26.4)],
'广西':[(104.5,23.5),(106,24.6),(108.5,25.3),(109.5,26.4),(110,25.5),(111.5,25),(112,24),(111,22),(109,21.6),(106.5,22.4)],
'福建':[(116.5,24),(117.5,26),(118.3,28.2),(120.5,27.3),(119.6,25.4),(118.5,24.5)],
'广东':[(110,21.3),(111,22),(112,24),(113.8,25.5),(115.5,24.9),(116.5,24),(117.2,23.5),(115.5,22.8),(113.5,22.2),(112,21.7)],
'陕甘':[(104,34),(104.5,36.5),(107.5,38),(110.5,37.5),(110.4,34.5),(108,33),(105.5,32.8)],
}
QING=[(107,41.5),(124,41.5),(122,31),(121,28.4),(118.3,28.2),(116,28.8),(114,29.8),(111,30.6),(110.4,34.5),(110.5,37.5),(107.5,38)]
JIANGNAN=[(116,34.5),(119.5,35),(121.8,31.5),(121,28.5),(118.3,28.2),(116.5,29.5),(115,30.5),(115.5,32.5)]
_r=random.Random(9);MTS=[]
for (lo0,lo1,la0,la1,n) in [(98.5,104,23.5,28,60),(104,108.5,25,28.2,45),(99,103,28.5,33,40),(108,111,31,33.4,26),(106,110,33.2,34.2,26),
    (110,116,24.6,25.8,40),(113.2,114.5,35.5,40,34),(116.5,119,25.5,28,26),(108.5,110.5,27.5,30,20),(103,106,34.5,37,18),(115,118.5,30.2,31.2,14)]:
    for i in range(n):MTS.append((_r.uniform(lo0,lo1),_r.uniform(la0,la1),_r.uniform(.7,1.3)))
MTS.sort(key=lambda m:-m[1])
def pl(c,pts):
    c.move_to(*P(*pts[0]))
    for p in pts[1:]:c.line_to(*P(*p))
def basemap(c,cx,cy,zoom,t,regions=(),dim=0):
    g=cairo.RadialGradient(W/2,H/2,100,W/2,H/2,1250);g.add_color_stop_rgb(0,*hx('#3e2f1d')[:3]);g.add_color_stop_rgb(1,*hx('#150f09')[:3]);c.set_source(g);c.paint()
    c.save();c.translate(W/2,H/2);c.scale(zoom,zoom);x0,y0=P(cx,cy);c.translate(-x0,-y0)
    s=1/zoom
    col(c,'#d9b56a',.05);c.set_line_width(1*s)
    for lo in range(94,130,2):c.move_to(*P(lo,16));c.line_to(*P(lo,44))
    for la in range(16,45,2):c.move_to(*P(94,la));c.line_to(*P(130,la))
    c.stroke()
    for name,(lo,la),a in regions:
        x,y=P(lo,la);text(c,name,x,y,46*s,'#c9a86a',a*.5,sp=40*s)
    for sh in (COAST,TAIWAN,HAINAN):
        pl(c,sh);c.close_path();col(c,'#0f191b') if sh is COAST else col(c,'#3a2c1c');c.fill_preserve();col(c,'#6a8a80',.35);c.set_line_width(3*s);c.stroke()
    pl(c,DONGTING);c.close_path();col(c,'#1a2a2c');c.fill_preserve();col(c,'#9cc0b2',.4);c.set_line_width(2*s);c.stroke()
    for r,w in ((HUANGHE,3),(YANGTZE,3.6),(XIANG,2),(PEARL,2.2)):
        pl(c,r);col(c,'#7fa79a',.18);c.set_line_width((w+5)*s);c.stroke_preserve();col(c,'#9cc0b2',.5);c.set_line_width(w*s);c.stroke()
    pl(c,CANAL);c.set_dash([8*s,6*s]);col(c,'#9cc0b2',.35);c.set_line_width(2*s);c.stroke();c.set_dash([])
    for lo,la,sz in MTS:
        x,y=P(lo,la);hh=20*sz;ww=15*sz
        poly(c,[(x-ww,y),(x,y-hh),(x,y)],'#8a6a3e',.8)
        poly(c,[(x,y-hh),(x+ww,y),(x,y)],'#4a3822',.85)
        col(c,'#d9b56a',.25);c.set_line_width(1*s);c.move_to(x-ww,y);c.line_to(x,y-hh);c.line_to(x+ww,y);c.stroke()
    if dim:rect(c,-5000,-5000,10000,10000,'#000000',dim)
    return s
def endmap(c):c.restore()
def city(c,name,s,t,state='gold',pulse=0,a=1,label=True,lx=16,ly=-12,size=30,big=1.0):
    x,y=P(*CITIES[name]);h=GOLD if state=='gold' else RED
    glow(c,x,y,40*s*big,h,.55*a)
    if pulse:
        for kk in (0,.5):
            k=(t*.7+kk)%1;col(c,h,(1-k)*.8*a);c.set_line_width(3*s);c.new_sub_path();c.arc(x,y,(12+70*k)*s*big,0,2*math.pi);c.stroke()
    circ(c,x,y,8*s*big,h,a);circ(c,x,y,3.4*s*big,'#fff4d8',a)
    if label:
        text(c,name,x+lx*s+2*s,y+ly*s+2*s,size*s,'#000000',.6*a,align='l' if lx>=0 else 'r')
        text(c,name,x+lx*s,y+ly*s,size*s,'#f3e6c8',a,align='l' if lx>=0 else 'r')
def route(c,pts,k,s,h=GOLD,lw=4,dash=False,head=True,a=1,arrow=False):
    xy=[P(*p) for p in pts];L=[0]
    for i in range(1,len(xy)):L.append(L[-1]+math.dist(xy[i-1],xy[i]))
    tot=L[-1];target=tot*cl(k)
    if target<=0:return None
    c.move_to(*xy[0]);end=xy[0];prev=xy[0]
    for i in range(1,len(xy)):
        if L[i]<=target:c.line_to(*xy[i]);prev=xy[i-1];end=xy[i]
        else:
            r=(target-L[i-1])/(L[i]-L[i-1]);prev=xy[i-1];end=(lerp(xy[i-1][0],xy[i][0],r),lerp(xy[i-1][1],xy[i][1],r));c.line_to(*end);break
    if dash:c.set_dash([14*s,10*s])
    col(c,h,.3*a);c.set_line_width((lw+8)*s);c.stroke_preserve();col(c,h,a);c.set_line_width(lw*s);c.stroke();c.set_dash([])
    if arrow:
        an=math.atan2(end[1]-prev[1],end[0]-prev[0]);L2=30*s
        poly(c,[(end[0]+math.cos(an)*L2,end[1]+math.sin(an)*L2),(end[0]+math.cos(an+2.4)*L2,end[1]+math.sin(an+2.4)*L2),(end[0]+math.cos(an-2.4)*L2,end[1]+math.sin(an-2.4)*L2)],h,a)
    elif head and k<1:glow(c,end[0],end[1],36*s,h,.85*a);circ(c,end[0],end[1],6*s,'#fff4d8',a)
    return end
def flag(c,lon,lat,s,txt='清',a=1,h=GOLD,tc='#7a1f1a',t=0):
    x,y=P(lon,lat);wv=math.sin(t*4+lon)*3*s
    col(c,'#15100c',a);c.set_line_width(2.5*s);c.move_to(x,y);c.line_to(x,y-54*s);c.stroke()
    poly(c,[(x,y-54*s),(x+36*s,y-52*s+wv),(x+36*s,y-24*s+wv),(x,y-26*s)],h,a,'#15100c',1.5*s,a)
    text(c,txt,x+18*s,y-30*s+wv,21*s,tc,a)
def zone(c,pts,h,a,s,dash=True):
    if a<=0:return
    pl(c,pts);c.close_path();col(c,h,.24*a);c.fill_preserve()
    if dash:c.set_dash([14*s,10*s])
    col(c,h,.75*a);c.set_line_width(3*s);c.stroke();c.set_dash([])
def plabel(c,name,s,a=1,h='#f3e6c8',size=34):
    pts=PROV[name];lo=sum(p[0] for p in pts)/len(pts);la=sum(p[1] for p in pts)/len(pts);x,y=P(lo,la)
    text(c,name,x,y,size*s,h,a,sp=8*s)
