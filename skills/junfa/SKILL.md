---
name: junfa
description: 军阀风（战争风·民国军阀版）（学自《吴佩孚：四年封神，一夜崩塌》）。暗金华北民国地图+铁路线+金线行军、民国军装纸偶人物、火车/双翼机/大炮/兵舰/电报/银元道具、红印章大字、顶部年份进度条、底部字幕+出处小字。全片不配乐，只用 numpy 合成音效逐镜对齐。用户说“军阀风”“吴佩孚那种”“民国战争风”“军阀混战”“北洋”时使用。
---

# 军阀风（战争风·民国军阀版，吴佩孚样片）

样片：《吴佩孚：四年封神，一夜崩塌》，204.7 秒，1920×1080，30fps，约 52MB，**无背景音乐，只有音效**。
参考帧：`参考帧/抽帧总图.jpg`、`sheet_a~d.jpg`。剧本与音效方案：`剧本/script_v1.md`、`剧本/sfx_plan.md`。
本技能是 zhanzheng（战争风）的民国分支，通用画风规则（暗金底、金/朱红两色强调、印章、字幕、电影感）同 zhanzheng 与 li-shi-preferences。

## 环境
1. `pip install cairocffi numpy pillow pyshp scipy`，需要 ffmpeg。
2. `mkdir -p ~/.fonts && cp ../../fonts/NotoSerif*.otf ~/.fonts/ && fc-cache -f`（字体在仓库根目录 fonts/）（Noto Serif SC Bold / CJK SC Black）。
3. 把 `代码/` 整个复制成新工程目录，在里面运行。代码里没有绝对路径。

## 代码结构
| 文件 | 作用 |
|---|---|
| lib.py / clib.py | cairo 基础绘图、中文排版、`rich()` 带 {金色重点} 的字幕 |
| hud.py | 印章 stamp、大字 slam/bigword、计数器 counter、人物徽章 badge、冲突锯齿线 vs_line |
| geo3.py + map.png | 地理投影与底图（Natural Earth 风格化） |
| nmap.py | **华北民国地图**：nmap() 底图（区域名、铁路、长城），cities() 发光城点/红点陷落，railname() 铁路名，arrow() 红色进攻箭头，ring() 小旗包围圈 |
| figq.py | **民国纸偶人物** person(kind, pose, …)：军官/士兵/大帅/文官等，姿势含站立、行军、举枪、跪、倒地、被押、说话；horse() 战马与骑手 |
| props.py | **民国道具**：train+rails 火车、biplane+bomb 双翼机投弹、explosion、cannon 火炮、mg 机枪、sandbags 沙袋、gunboat 兵舰+sea+pier 码头、telepole/wires/telekey/morse_tape 电报、yuan/coinstack/notes 银元钞票（贿选）、wu_bust 吴佩孚半身像、time_cover《时代》封面、couplet 竖排寿联、hall 中式殿堂、lantern、westbldg 西式楼、whiteflag、rifle_pile 缴械枪堆、searchlight 探照灯 |
| wscene.py | 场景组装：army() 成片军队布阵、draw_army、flags 旗海、nightsky、far_fires 远处营火、bjskyline 北京城天际线、vign 暗角、infocard 人物卡 |
| common.py | `@nx(拍数,'年份·地点','字幕{重点}','出处')` 顺序排镜；card() 章节卡 |
| shots1.py / shots2.py | 本片全部镜头（新片照这个写法重写镜头） |
| render.py | 合成：转场（punch/whip/flash/iris/slide）、震屏、字幕、顶部 1920—1925 进度条（新片改起止年份 frac_of） |
| sfx.py | **音效轨**，numpy 合成，按镜头切点和 stamp 自动对齐，输出 sfx.wav |
| scan.py / sheet.py | 扫描镜头时长、拼抽帧表 |

## 工作流
1. 改写剧本（规则同 zhanzheng：逐句核史实、删无出处细节、多因素、野史标注），存 `script_v1.md`，修订记录写文末。用户说“直接做”就不等确认。
2. 结构按内容定，本片是**倒叙**：塘沽登舰残局开场 → 《时代》封面 → 直皖 → 第一次直奉 → 洛阳巅峰 → 两颗雷 → 四照堂点将 → 山海关 → **高潮：北京政变之夜** → 崩塌 → 回到塘沽 → 多因素复盘。新片不要照抄这个结构。
3. 写 `sfx_plan.md`：音色库 + 每段音效密度，高潮段最密。
4. 在 shots1/shots2 写镜头；抽帧 `python3 render.py still 秒…` → `python3 sheet.py s.jpg 秒…` 检查。
5. 分段渲染 `python3 render.py seg 起帧 止帧 segN.mp4`，ffmpeg concat。
6. `python3 sfx.py` 生成 sfx.wav（软限幅，峰值约 −1.5 dBFS，RMS 约 −20 dBFS），与视频 mux 成片，控制在 60MB 内。
7. 出抽帧总图检查：地图字不糊、城名不重叠、字幕不压出处、印章不挡人物、暗底人物看得清。

## 音效（不配乐）
全片不用 score*/synth。音色库：海浪、兵舰汽笛、风、雨、电报嘀嗒、炮声/爆炸、机枪、步枪、飞机/炸弹哨音、火车与汽笛、军号、马蹄、行军脚步、盖印“咚”、纸张、银元叮当、心跳、重锣/低频冲击、转场 whoosh、鞭炮、人声、城门吱呀、快门闪光。每个切点轻 whoosh，印章自动配“咚”，转折点重锣+冲击，政变夜段落最密（雨、脚步、电报、心跳、门撞击）。

## 民国画面要点
- 地图：华北为主（北京、天津、保定、洛阳、山海关、古北口、秦皇岛、石家庄、塘沽），铁路线（京汉、京奉、津浦）用细金线并标名；长城用锯齿线。
- 人物：北洋军装（灰蓝/土黄呢军服、大檐帽、肩章、马靴、披风），大帅放大中景，士兵成排列队；表情克制。
- 道具镜头：火车开进、双翼机投弹、火炮齐射、兵舰离岸、电报机嘀嗒+纸带、银元堆（贿选“每票五千元”）、《时代》封面闪光、寿联竖排。
- 年份标签用公历“1924年10月·北京”，顶部进度条起止年按本片改。
