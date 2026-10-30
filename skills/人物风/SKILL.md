---
name: renwu
description: 人物风（玉溪风·近现代人物版，学自《杨振宁》样片）。暗色电影感背景+纯黑剪影人物+单件发光主体，左上打字机字幕、右上年份地点、左下年龄计数器；高潮段加速切镜+红闪+震屏+碎裂特效。不配乐，只用 numpy 合成音效。用户说“人物风”“杨振宁那种”“玉溪风现代人物”“科学家/人物传记”时使用。
---

# 人物风（玉溪风·近现代人物版，杨振宁样片）

样片：《杨振宁》，约 3 分 20 秒，1920×1080，30fps，约 24MB，**无背景音乐，只有音效**。高潮：宇称实验 → 镜子碎了 → 诺贝尔奖。
参考帧：`参考帧/sheet0~2.jpg`（全片抽帧）、`c.jpg`、`fix.jpg`。史料核对：`剧本/research.md`（每条都附出处链接）。
本技能是 yuxi（玉溪风）的近现代分支，基础画风规则同 yuxi；区别是**这一版加音效**，并新增现代人物与道具库。

## 环境
`pip install numpy cairocffi pillow`，需要 ffmpeg；`mkdir -p ~/.fonts && cp 字体/*.otf ~/.fonts/ && fc-cache -f`。把 `代码/` 复制成新工程目录运行，无绝对路径。

## 代码结构
| 文件 | 作用 |
|---|---|
| kit.py | 玉溪风基础库：古风剪影 sil()、环境（stars/moon/mountains/water/palace/citywall/fires/banner/crowd/horse）、字幕 subs（左上打字机、【红】〖金〗| 换行）、tag 右上年份、counter 计数、redflash、vignette |
| modern.py | **近现代库**：man()/woman() 西装、长衫、眼镜剪影；crowd_m 鼓掌人群；mirror 镜子（可裂、碎片飞散）；rays 光芒、sparks 火花；auditorium 礼堂、chandelier 吊灯；ship 轮船、plane/bomber 飞机；blackboard+chalk 黑板写公式；mushroom 蘑菇云；letter 书信；bouquet 花束；window 窗；tinroof 铁皮屋顶下雨；nametag 人名牌 |
| script.py | 稿子 L=(场景key, "年份 · 地点", 出处小字, 计数(岁), 字幕, [时长覆盖])；CLIMAX 集合里的镜头切换间隙缩短到 0.08 秒；durs() 按字数算时长 |
| scenes.py | 每镜一个函数 S_<key>(c, lt, d, p)；CAM 字典配推镜；FX 设置 shake/flash/white |
| render.py | `python3 render.py still 秒…` 抽帧；`info` 看总时长；`python3 render.py 段号 段数` 分段渲染 |
| sfx.py | 音效轨（numpy 合成）：打字 tick、转场 whoosh、低频冲击、玻璃碎裂、掌声、轮船汽笛、飞机/轰炸、雨声、心跳、钟声等，按镜头起点和 CLIMAX 自动对齐，输出 sfx.wav |
| go.sh | 2 路并行渲染 + 音效 → concat → mux 成片 |

## 工作流
1. 史料核查写 research.md（权威来源：清华讣告、校史馆、诺奖官网等），存疑处标“示意/存疑”。
2. 写 script.py：钩子 3 句（结局/名言先行）→ 标题 → 按年份一事一镜（左下计数器=主角年龄）→ 高潮快切 → 回归与收尾。结构按题材变，不照抄。
3. scenes.py 每镜写函数，用 modern.py 道具；只让一件主体发光（本片是镜子、奖章、书信）。
4. 抽帧检查：字幕区 y<260 不放道具、人名 ≥40px、计数器在推镜外、红闪位置对、亮度够。
5. `bash go.sh` 出片，控制在 60MB 内。

## 高潮做“燃”的方法
- CLIMAX 镜头时长 2.0–3.4 秒，间隙 0.08 秒，字幕短句加感叹号。
- 镜子碎裂：crack 渐增 → shards 飞散 + 白闪 + 震屏 + 玻璃碎裂声 + 低频冲击。
- 颁奖：rays 光芒旋转 + sparks + 掌声渐强 + 钟声；数字（35岁/31岁）金色大字。
- 高潮后回落：节奏放慢、音效变稀，留白收尾。

## 文字
- 全白话，古文（如《吊古战场文》）紧跟白话翻译；名言标出处。
- 【红】= 灾难/死亡/沦陷，〖金〗= 重点人名数字。
