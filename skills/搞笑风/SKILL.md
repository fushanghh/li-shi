---
name: gaoxiao
description: 搞笑风（社恐小人·“在看我”风）：粗黑描边大头人物（女主苏糖，配角长相各不相同、按剧情换装）、青色视线虚线、左上角“在看我”计数 HUD、彩色关键词字幕，加喜怒哀乐夸张表情和鬼畜复读、猛推镜、RGB 错位闪。适合生活小事、社恐尴尬、反转段子类短片。用户说“搞笑风”“社恐风”“在看我那种”“鬼畜风”时使用。
---
# 搞笑风（学自抖音“在看我”社恐小人样片，2026-10-29 样片已获用户认可）

素材包位置：/workspace/skills/搞笑风/
- 引擎/：lib.py（描边绘图底层）、rig.py（角色骨架+表情库）、scenes.py（场景/HUD/特效）、render.py（样片时间线，新片复制它改）、audio.py（BGM+音效+配音混音）、tts.py（edge-tts 配音，已处理代理）
- 字体：仓库根目录 fonts/ 下的 NotoSansSC-Black.otf、NotoSansSC-Bold.otf（字幕和 HUD 用黑体，装到 ~/.fonts 后 fc-cache）
- 参考/：原片.mov、原片联系表、原片高清帧
- 角色/：角色表.png（8 个预设人物）、女主苏糖_定妆.png、王大美_定妆.png
- 引擎/juese.py：新版人物引擎（画风、换脸、换装、表情、动作全在这里）
- 样片/：20 岁女生超市+地铁 10 秒样片及联系表

## 开工
1. 依赖：pip install numpy cairocffi edge-tts；字体拷到 ~/.fonts 并 fc-cache -f。
2. 复制整个“引擎”到新工程，改 render.py 的镜头函数、LOOPS、字幕、HUD 数字；改 audio.py 的配音时间点和音效。
3. 配音：python3 tts.py "台词" vo/N.mp3 zh-CN-XiaoyiNeural "+18%"，再用 ffmpeg silenceremove 去掉首尾静音，转 44.1k 单声道 wav。audio.py 用环境变量 VO_DIR 找配音。
4. 预览：python3 render.py out/p 0.3 1.3 …（单帧 PNG），先拼联系表自己检查，再整片渲染：python3 render.py silent.mp4 → python3 audio.py → ffmpeg 合成。

## 角色画风（2026-10-29 新定稿，所有人物必须用这个）
- 用 引擎/juese.py 画人，旧的 rig.py 卫衣小人不再用于新片（只留作兼容）。
- 画风：粗黑描边 #1c1a1f（1080p 约 6px×缩放）、大头身（约 2.6 头身）、杏仁斜眼带眼线小勾、红色厚唇或嘟嘴、圆形大腮红、单线勾鼻。参考 参考/画风参考_东北大姐.png 的感觉，但造型全部原创。
- 女主固定为“苏糖”25岁：浅棕及下巴层次短发+空气刘海+两侧修颜碎发，日常表情嘟嘴斜眼，默认穿奶白针织 polo+四叶草项链+浅蓝直筒牛仔裤+小白鞋（CAST['sutang']，定妆图 角色/女主苏糖_定妆.png）。
- 其他人物全部同一画风，长相不能重样：每个角色至少在 脸型 face / 发型 hair / 眼型 eye / 嘴型 mouth / 特征 extras 里有三项和别人不同。CAST 里有现成的：王大美（东北大姐）、闺蜜小鹿、同事阿杰、王总、超市阿姨、地铁小哥、精致姐姐；新角色用 mk(...) 组合新参数，别直接复制别人。
- 换装按剧情来：同一个人在不同场景可以换 top/bottom/shoes/颜色和道具（上班穿衬衫、逛超市穿开衫、下雨穿羽绒服），但脸和发型不变，观众要一眼认得出来。
- 可选参数：face 脸型 oval/round/square/long/v；hair 发型 bob/long/clipbun/ponytail/curly/buns/crop/side_part/buzz/bald；eye 眼型 side/round/dot/sleepy/fox；glasses 眼镜 round/square/sun；mouth 嘴型 pout/thick/line/smirk/frown/grin；extras 特征 folds/mole/stubble/mustache/freckles/eyebags/pearl/hoop/necklace；top 上衣 polo/cardigan/hoodie/tshirt/shirt/suit/apron/puffer/vest/dress/uniform；bottom 下装 jeans/pants/skirt/shorts/pajama；shoes 鞋 sneaker/boot/leather/heels/slipper；bw 体宽。
- 动作：arms=(左手,右手) 可用 down/hip/hold/up/point/cover/both_up/shrug/phone_ear，也可以直接给 ((肘dx,dy),(手dx,dy))；props 道具 phone/cup/bag/basket/thermos/briefcase/scanner；legs=(左脚偏移,右脚偏移) 走路；lean 身体倾斜、squash 挤压拉伸、head_tilt 歪头；person() 返回 head 坐标，拿去连视线虚线。
- 表情 e：neutral 日常 / side 斜眼瞟（围观路人用）/ happy 喜 / angry 怒（红脸+怒筋）/ cry 哀（喷泉泪+鼻涕泡）/ laugh 乐（眯眼大笑+“哈”字）/ shock 惊。传 t 让泪水、星星、“哈”字动起来。
- 预览：python3 juese.py 角色表.png 会出 8 人角色表。

## 场景与原片画风（场景、HUD、字幕照原片）
- 扁平矢量、纯色填充；场景描边可以继续用深藏青 #232842，人物用黑色描边。
- （旧版卫衣小人造型已停用，人物一律见上一节。）
- 路人布置：中景站立的人抓吊环/扶杆，远处坐着的半身，前景左右下角放大半身斜眼看主角，三层制造纵深。
- 场景两种：① 侧面平铺（货架、街景、收银台：顶/墙/主体/地砖四层，可横向平移）；② 一点透视对称（地铁车厢、办公室，主角站正中）。
- 色彩：明亮暖白室内或黄昏紫粉渐变；车厢是深蓝墙配亮黄扶杆和白色顶灯条。

## 招牌元素
- 视线线：每个围观者眼睛发青光，青色虚线弧（#4fd8e0，外加深色阴影线，虚线流动）连到主角头上，依次画出来。
- “在看我”HUD：左上角深色圆角框，眼睛图标、“在看我”小字、大数字；数字逐段升级（0/3→30→300），每次切换弹跳放大；反转时归零，眼睛加斜杠，数字变青色。
- 字幕：底部居中，Noto Sans SC Black 66px，白字深描边加投影，底部暗色渐变；前半句白字先出，后半句关键词换彩色（橙/红/蓝/青）卡拍弹出。
- 结构：同一个尴尬梗逐段加码，最后一句反转收尾（比如“原来根本没人在看我”）。每段约 2.5 秒，切镜时白闪 2 帧。
- 不照搬原片的抖音水印。

## 喜怒哀乐表情库（rig.face 的 e 参数）
- 喜 star：星星眼旋转、张大嘴露舌、腮红；配爆炸光芒、闪光星、跳起来（挤压拉伸）、双手举高。
- 怒 angry：整张脸红色渐变、V 字眉、咬牙方嘴；配头顶冒蒸汽、💢 怒筋跳动、握拳、震屏、红闪。
- 哀 cry：八字眉、闭眼弯线、嘴巴发抖；配两道泪喷泉抛物线、头顶乌云下雨、悲伤长号 wah-wah-wah-waaah。
- 乐 laugh：眯眼、超大嘴上下开合、头后仰摇晃、双手挥舞；配彩色“哈”字弹出、彩纸。
- 过渡：shock（大眼、O 嘴）、smile、side（斜眼，围观用）、down（低头看手机）。

## 鬼畜手法
- 时间重映射 LOOPS：(起, 止, 循环窗口起, 窗口长, 效果)，把 0.22–0.3 秒的动作循环复读 3–5 次。
- 每次循环开头：猛推镜（zoom）后回弹，或抖动（shake）、拉远（zoomout）、镜像翻转（mirror）；头 2 帧 RGB 通道左右错位 18px，怒段加红，乐段奇数次反色。
- 配音同步复读：单字 TTS 循环（冲！冲！冲！、网…网…网卡了？！、哈哈）。每次循环配一个 glitch 咔嗒音。

## 声音
- BGM 程序合成：130BPM C 大调 oompah（低音+和弦拨弦+旋律+鼓）；怒段升半音并加速 1.12 倍；哀段 BGM 断掉，换悲伤长号；乐段恢复。
- 音效：叮（价签）、boing（跳）、whoosh（冲刺）、唱片刮擦（切镜）、扫码哔、错误蜂鸣、蒸汽嘶嘶、啵啵（东西掉地上）、ta-da（反转）。
- 配音用 edge-tts zh-CN-XiaoyiNeural，语速 +18%，活泼女声；有配音时 BGM 压低 55%。

## 已知可改进
- 10 秒样片还是旧版卫衣小人，下一部片要用新角色重做。
- 侧面镜头的人物比例偏小，脚下地面留空较多，可以把人物加大或把机位压低。
