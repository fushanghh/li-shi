import sys,subprocess
from lib import *
import shots as S
SH=[
(S.s_title,7,[(0,'装疯卖傻{36年}，一朝登基，却成了晚唐最后的“{顶梁柱}”')],'',810,'唐 · 大中年间'),
(S.s_prince,6,[(0,'他叫{李忱}，唐宪宗第十三子，母亲郑氏原是宫女')],'《旧唐书·宣宗纪》：宪宗第十三子，母曰孝明皇后郑氏',815,'元和年间 · 长安'),
(S.s_banquet,6,[(0,'宫中都以为他“{不慧}”，皇族宴会上常拿他逗乐取笑')],'《资治通鉴》：宫中或以为不慧……强诱其言以为戏笑',830,'文宗年间 · 十六宅'),
(S.s_wuzong,7,[(0,'侄子武宗即位后，对这位皇叔{尤不为礼}'),(3.6,'他只能继续装傻，一句话都不多说')],'《资治通鉴》：武宗气豪，尤不为礼',841,'会昌年间 · 大明宫'),
(S.s_legend,7,[(0,'野史还说，他曾被扔进{宫厕}，靠宦官仇公武偷偷救出')],'《中朝故事》（野史，未必可信）',843,'会昌年间 · 长安'),
(S.s_tl1,8,[(0,'36年里，龙椅换了{5}位主人：父亲、哥哥、三个侄子')],'',846,'810 — 846'),
(S.s_eunuch,7,[(0,'846年，武宗服丹暴亡，宦官们想立一个{好控制}的“傻王爷”')],'《资治通鉴》：诸宦官密于禁中定策……立光王为皇太叔',846,'846年3月 · 大明宫'),
(S.s_rise,8,[(0,'谁知登基后，他{哀毁满容，接待群僚，决断庶务}'),(4,'人们这才发现：这位“傻王爷”，{一点都不傻}')],'《资治通鉴》：哀毁满容，接待群僚，决断庶务',846,'846年 · 即位'),
(S.s_lideyu,8,[(0,'他上台就罢免权相{李德裕}，一贬再贬，直到海南{崖州}')],'《资治通鉴》：贬李德裕为崖州司户',848,'846 — 848'),
(S.s_study,8,[(0,'他勤政节俭，{用法无私，从谏如流}，刺史赴任都要亲自召见')],'《资治通鉴》：宣宗性明察沉断，用法无私，从谏如流',849,'大中年间 · 大明宫'),
(S.s_hexi,9,[(0,'可安史之乱后，{河西、陇右}被吐蕃占了八十多年'),(4.5,'吐蕃兵锋，离长安不过数百里')],'',849,'763 — 849 · 河陇'),
(S.s_849,9,[(0,'849年，吐蕃内乱，唐军收复秦、原、安乐{三州七关}')],'《资治通鉴》：以秦、原、安乐三州及石门等七关来降',849,'849年 · 陇右'),
(S.s_gate,9,[(0,'河陇父老千余人来到长安，城楼下{脱去胡服，换回唐装}')],'《资治通鉴》：上御延喜门楼见之，欢呼舞跃，解胡服，袭冠带',849,'849年8月 · 延喜门'),
(S.s_851,11,[(0,'851年，沙州{张议潮}起兵，赶走吐蕃守将'),(4.5,'派人千里奔赴长安，献上{十一州}图籍')],'《资治通鉴》：张义潮……奉十一州图籍入见',851,'851年 · 沙州'),
(S.s_dan,7,[(0,'可宦官和藩镇的病根他没能拔掉，晚年也迷上了{丹药}')],'《资治通鉴》：上饵医官李玄伯所治丹剂，疽发于背',858,'大中末年 · 大明宫'),
(S.s_death,6,[(0,'859年，宣宗服丹中毒，背生毒疮而死，终年{五十}岁')],'',859,'859年8月 · 长安'),
(S.s_tl2,9,[(0,'他走后，再没人撑得住这个摇摇欲坠的大唐'),(4.5,'{48年}后，唐朝灭亡')],'',859,'859 — 907'),
(S.s_end,10,[(0,'后人称他“{小太宗}”：大中之政，讫于唐亡，人思咏之'),(5.5,'他撑住的，是晚唐倒下前的{最后一根梁}')],'《资治通鉴》：故大中之政，讫于唐亡，人思咏之，谓之小太宗',859,'唐宣宗 李忱 · 810 — 859'),
]
DIS=0.4
starts=[];acc=0
for sh in SH:starts.append(acc);acc+=sh[1]
TOTAL=acc
OV=make_overlay()
def ui(c,i,t):
    fn,T,subs,src,yr,lab=SH[i]
    a=cl(t/.35)*cl((T-t)/.25+0.0001) if True else 1
    # progress bar
    x0,x1=60,380;text(c,'810',x0,40,16,GREY,.8,align='l');text(c,'859',x1,40,16,GREY,.8,align='r')
    col(c,GREY,.5);c.set_line_width(1.5);c.move_to(x0,52);c.line_to(x1,52);c.stroke()
    k=(yr-810)/49;col(c,RED,.9);c.set_line_width(3);c.move_to(x0,52);c.line_to(lerp(x0,x1,k),52);c.stroke();circ(c,lerp(x0,x1,k),52,4,RED)
    rect(c,W-60-3,26,3,30,RED);text(c,lab,W-75,50,24,'#c9b88e',.9,align='r')
    text(c,'（示意）',60,1060,16,GREY,.5,align='l')
    cur=None
    for st,s in subs:
        if t>=st:cur=(st,s)
    if cur:
        aa=cl((t-cur[0])/.25)
        g=cairo.LinearGradient(0,880,0,H);g.add_color_stop_rgba(0,0,0,0,0);g.add_color_stop_rgba(1,0,0,0,.75);c.set_source(g);c.rectangle(0,880,W,200);c.paint() if False else c.fill()
        rich(c,cur[1],W/2,990,46,aa)
        if src:text(c,src,W/2,1036,22,GREY,aa*.85,bold=False)
def draw_shot(i,t):
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c=cairo.Context(s)
    fn,T=SH[i][0],SH[i][1]
    c.save();fn(c,t,T);c.restore()
    c.set_source_surface(OV);c.paint()
    ui(c,i,t);return s
def frame(fi):
    tt=fi/FPS
    i=max(j for j in range(len(SH)) if starts[j]<=tt);t=tt-starts[i]
    s=draw_shot(i,t)
    T=SH[i][1]
    if i+1<len(SH) and t>T-DIS:
        s2=draw_shot(i+1,0.0);c=cairo.Context(s);c.set_source_surface(s2);c.paint_with_alpha(ease((t-(T-DIS))/DIS))
    if i==0 and t<.6:c=cairo.Context(s);c.set_source_rgba(0,0,0,1-t/.6);c.paint()
    if tt>TOTAL-1:c=cairo.Context(s);c.set_source_rgba(0,0,0,cl(tt-(TOTAL-1)));c.paint()
    return s
def rgb(s):
    a=np.frombuffer(s.get_data(),np.uint8).reshape(H,s.get_stride()//4,4)[:,:W,:3]
    return a[:,:,::-1].tobytes()
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='sheet':
        from PIL import Image
        ts=[float(x) for x in sys.argv[2].split(',')]
        ims=[Image.frombytes('RGB',(W,H),rgb(frame(int(x*FPS)))).resize((640,360)) for x in ts]
        cols=3;rows=(len(ims)+2)//3;sh=Image.new('RGB',(640*cols,360*rows))
        for k,im in enumerate(ims):sh.paste(im,((k%cols)*640,(k//cols)*360))
        sh.save(sys.argv[3]);print('ok',TOTAL)
    else:
        part,n=int(sys.argv[2]),int(sys.argv[3]);N=int(TOTAL*FPS);a=N*part//n;b=N*(part+1)//n
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',f'part{part}.mp4'],stdin=subprocess.PIPE)
        for f in range(a,b):
            p.stdin.write(rgb(frame(f)))
            if f%300==0:print(part,f,flush=True)
        p.stdin.close();p.wait();print('done',part,flush=True)
