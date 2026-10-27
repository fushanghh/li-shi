import sys,subprocess
from lib import *
import shots1 as A
SH=[
dict(f=A.s_hook1,T=4.5,subs=[(0,'同样是{造反}：一个流传千古，一个骂名千年')],src='',bar=None,lab='秦末  ·  唐末',tr='fade'),
dict(f=A.s_hook2,T=4.5,subs=[(0,'司马迁把陈胜写进{《世家》}，与诸侯同列'),(2.3,'黄巢却被写进了{《逆臣传》}')],src='《史记·陈涉世家》  ·  《新唐书·逆臣传》',bar=None,lab='史书里的两个人',tr='push'),
dict(f=A.s_hook3,T=3,subs=[(0,'都是举兵反朝廷，差别到底在哪？')],src='',bar=None,lab='一个问题',tr='flash'),
]
import shots2 as B
BQ=('前209','前206')
SH+=[
dict(f=B.s_qinmap,T=6.5,subs=[(0,'前209年秋，秦廷征发{900}名戍卒，北上{渔阳}戍边'),(3.0,'走到{大泽乡}，天降大雨，路断了')],src='《史记·陈涉世家》：发闾左適戍渔阳，九百人屯大泽乡',bar=BQ+((0,.05),),lab='前209年7月 · 大泽乡',tr='dive'),
dict(f=B.s_rainwide,T=3.5,subs=[(0,'暴雨连天，九百人困在泥泽里')],src='《史记》：会天大雨，道不通',bar=BQ+(.06,),lab='前209年7月 · 大泽乡',tr='dive'),
dict(f=B.s_mudfeet,T=3,subs=[(0,'掐指一算：{已经误期}')],src='《史记》：度已失期',bar=BQ+(.07,),lab='前209年7月 · 大泽乡',tr='cut'),
dict(f=B.s_law,T=3.5,subs=[(0,'按秦法——{失期，法皆斩}')],src='《史记》：失期，法皆斩（出土秦简所载徭律罚则较轻，此说存疑）',bar=BQ+(.08,),lab='前209年7月 · 大泽乡',tr='cut'),
dict(f=B.s_fish,T=3.2,subs=[(0,'鱼腹里藏帛书{“陈胜王”}'),(1.6,'夜里篝火，学狐狸叫')],src='《史记》：丹书帛曰“陈胜王”……篝火，狐鸣呼曰“大楚兴，陈胜王”',bar=BQ+(.09,),lab='前209年7月 · 大泽乡',tr='ink'),
dict(f=B.s_kill,T=3.2,subs=[(0,'军尉醉酒鞭打吴广，吴广{夺剑杀尉}')],src='《史记》：尉剑挺，广起，夺而杀尉。陈胜佐之，并杀两尉',bar=BQ+(.1,),lab='前209年7月 · 大泽乡',tr='cut'),
dict(f=B.s_shout,T=4.6,subs=[(0,'陈胜登台一呼：{“王侯将相，宁有种乎！”}')],src='《史记·陈涉世家》',bar=BQ+(.11,),lab='前209年7月 · 大泽乡',tr='flash'),
dict(f=B.s_poles,T=3.6,subs=[(0,'{斩木为兵，揭竿为旗}，天下云集响应')],src='贾谊《过秦论》：斩木为兵，揭竿为旗，天下云会响应',bar=BQ+(.13,),lab='前209年 · 蕲县',tr='fire'),
]
import shots3 as C
SH+=[
dict(f=C.s_chenmap,T=7,subs=[(0,'攻下蕲县、陈县，在陈称王，国号{张楚}'),(3.6,'各地郡县纷纷{杀秦吏响应}')],src='《史记》：诸郡县苦秦吏者，皆刑其长吏，杀之以应陈涉',bar=BQ+((.15,.3),),lab='前209年 · 陈县',tr='flag'),
dict(f=C.s_chenfall,T=4.6,subs=[(0,'可仅仅{六个月}后，陈胜兵败'),(2.0,'被自己的车夫{庄贾}杀害')],src='《史记》：陈胜王凡六月……其御庄贾杀以降秦',bar=BQ+(.4,),lab='前208年 · 下城父',tr='smoke'),
dict(f=C.s_qinfall,T=5,subs=[(0,'但他点燃的火没有灭，三年内{秦朝灭亡}')],src='《史记》：其所置遣侯王将相竟亡秦，由涉首事也',bar=BQ+((.5,1),),lab='前207年 · 咸阳',tr='ink'),
dict(f=C.s_matchA,T=1.6,subs=[(0,'他举起的，是一把{锄头}')],src='',bar=None,lab='秦末',tr='fade'),
]
HQ=('875','884')
SH+=[
dict(f=C.s_matchB,T=2.4,subs=[(0,'一千多年后，唐末，又一个人举起了{刀}')],src='',bar=None,lab='唐末',tr='match'),
]
import shots4 as D
SH+=[
dict(f=D.s_salt,T=4.4,subs=[(0,'{黄巢}，曹州冤句人，贩私盐起家'),(2.1,'相传他屡考进士，{屡试不第}')],src='《新唐书》：世鬻盐，富于赀（科举落第一说，新旧唐书未载）',bar=HQ+(0,),lab='唐 · 曹州冤句',tr='ink'),
dict(f=D.s_poem,T=5,subs=[(0,'相传落第后，他写下：{满城尽带黄金甲}')],src='《不第后赋菊》最早见于明代《七修类稿》，作者归属存疑',bar=HQ+(0,),lab='唐 · 长安',tr='smoke'),
dict(f=D.s_famine,T=4.6,subs=[(0,'那时关东大旱，穷人磨{蓬草籽}当面'),(2.4,'官府照样{鞭打催税}')],src='《资治通鉴》卢携上言：贫者硙蓬实为面，蓄槐叶为齑……督趣甚急',bar=HQ+(0,),lab='874年 · 关东',tr='push'),
dict(f=D.s_huangmap,T=9,subs=[(0,'875年他起兵，从山东一路{南下}'),(3.9,'879年攻破{广州}，掉头北上'),(6.6,'880年末，破洛阳、过潼关，直入{长安}')],src='广州破城时史载屠杀胡商，人数诸说不一（存疑）',bar=HQ+((0,.7),),lab='875 — 881 · 转战南北',tr='dive'),
dict(f=D.s_changan,T=4.6,subs=[(0,'{金甲}涌入长安'),(2.3,'唐僖宗仓皇逃往{成都}')],src='史载：宦官田令孜护送僖宗奔蜀',bar=HQ+(.7,),lab='881年1月 · 长安',tr='fire'),
dict(f=D.s_throne,T=3.6,subs=[(0,'黄巢在含元殿称帝，国号{大齐}')],src='史载：即位于含元殿，国号大齐，年号金统',bar=HQ+(.72,),lab='881年1月 · 含元殿',tr='flash'),
dict(f=D.s_wash,T=4.6,subs=[(0,'长安百姓曾迎接唐军，他回城后下令{“洗城”}')],src='《旧唐书·黄巢传》：贼怒坊市百姓迎王师，乃下令洗城',bar=HQ+(.75,),lab='881年4月 · 长安',tr='cut'),
dict(f=D.s_mill,T=4.2,subs=[(0,'围陈州时，史书更有骇人的{“舂磨寨”}')],src='《旧唐书》《资治通鉴》均载；规模与做法，后世多疑夸大',bar=HQ+(.85,),lab='883年 · 陈州',tr='smoke'),
dict(f=D.s_wolf,T=4.6,subs=[(0,'884年，部下纷纷投降，他败走{狼虎谷}'),(2.2,'死于外甥林言刀下（一说自刎）')],src='《旧唐书》：至狼虎谷，巢将林言斩巢……',bar=HQ+(1,),lab='884年6月 · 狼虎谷',tr='ink'),
dict(f=D.s_tang,T=3.4,subs=[(0,'又过23年，他的降将{朱温}篡唐')],src='',bar=HQ+(1,),lab='907年 · 汴州',tr='fade'),
]
import shots5 as E
SH+=[
dict(f=E.s_card,T=2.6,subs=[(0,'把两个人放进同一张表，逐项对比')],src='',bar=None,lab='对照 · 五个问题',tr='push',yi=False),
dict(f=E.mkrow(0),T=4.6,subs=[(0,'起兵原因：两人都是{被逼}的')],src='',bar=None,lab='对照 · 1/5',tr='cut',yi=False),
dict(f=E.mkrow(1),T=4.6,subs=[(0,'反的是谁：秦被后世公认{暴政}；唐却是后人怀念的盛世王朝')],src='《史记》：天下苦秦久矣',bar=None,lab='对照 · 2/5',tr='cut',yi=False),
dict(f=E.mkrow(2),T=4.8,subs=[(0,'对待百姓：黄巢军屠城的记载{一再出现}')],src='《旧唐书》《新唐书》《资治通鉴》（部分记载存疑）',bar=None,lab='对照 · 3/5',tr='cut',yi=False),
dict(f=E.mkrow(3),T=4.6,subs=[(0,'留下什么：陈胜{首事}，后来者灭秦建汉；黄巢之后是{乱世}')],src='《史记》：其所置遣侯王将相竟亡秦，由涉首事也',bar=None,lab='对照 · 4/5',tr='cut',yi=False),
dict(f=E.mkrow(4),T=4.8,subs=[(0,'谁写历史：汉朝本就{反秦起家}；宋朝最怕的就是{造反}')],src='',bar=None,lab='对照 · 5/5',tr='cut',yi=False),
dict(f=E.s_hgaozu,T=3.8,subs=[(0,'所以汉高祖为陈胜{置守冢三十家}，至今血食')],src='《史记》：高祖时为陈涉置守冢三十家砀，至今血食',bar=None,lab='汉初 · 砀',tr='ink'),
dict(f=E.s_flaws,T=5,subs=[(0,'公平地说，陈胜也有短板：称王后{杀故人、用苛吏}'),(2.6,'诸将不再亲附，这正是他{败亡}的原因')],src='《史记》：诸将以其故不亲附，此其所以败也',bar=None,lab='前209年 · 陈县',tr='smoke'),
dict(f=E.s_answer,T=7.4,subs=[(0,'黄巢同样是被逼上路，可评价的分量不在“反不反”'),(2.0,'而在：{反的是谁、伤了多少百姓、留下了什么、谁来写历史}')],src='',bar=None,lab='答案',tr='dive'),
dict(f=E.s_end,T=5.6,subs=[(0,'同样是造反，差别在于：{刀口，朝向了谁}')],src='',bar=None,lab='陈胜 · 黄巢',tr='fade'),
]
