---
name: yuxi
description: 玉玺黑影风：暗色电影感背景 + 黑剪影人物 + 单件发光主体的“假如你是X”纯文字讲解历史视频（无配音、无音效、无音轨）。用户说“玉玺黑影”“玉玺黑影风”或要做这种剪影视角历史片时使用。
---

# 玉玺黑影风 历史短视频

用纯代码做动画：Python + cairo 逐帧画，再用 ffmpeg 编码。1920x1080，30fps。
**不配音，不加音效，成片没有音轨。**参考样片只学形式（节奏、字幕样式、讲解方式），文案、构图、角色和美术都要原创。

## 文件
- 示例_张元/：最新模板（推荐复制它开新题）。示例_和氏璧/：第一条成片。
  - kit.py：工具库。剪影人物 `sil(c,x,y,s,hat,pose,face,a,col,p,robe)`
    - hat：mian冕旒 / guan冠 / helm盔 / bun发髻 / lady / futou唐幞头 / song宋直脚幞头 / xia西夏毡冠
    - pose：stand offer raise throw drink point sword kneel bow cry sit lie
    - 环境：palace mountains stars moon water reeds citywall roofhall fires banner crowd horse
    - 道具：stone（可裂开） / bi玉璧 / seal玉玺；hand 画外伸手
    - UI：subs字幕 / tag右上年份 / counter计数器 / redflash红闪 / vignette暗角
  - script.py：稿子列表 L=(场景key, "年份 · 地点", 出处小字, 计数, 字幕)。字幕里【红】表示死亡或惩罚，〖金〗表示重点，| 换行
  - scenes.py：每个镜头写一个函数 `S_<key>(c, lt, d, p)`（lt=本镜秒数，p=进度0→1），CAM 字典配推镜
  - render.py：`python3 render.py still 12.5 30` 抽帧检查；`bash go.sh` 四路并行渲染并拼成 out.mp4
  - dur.json：每句时长，改稿后重新生成：max(2.6, 1.0 + 字数×0.15) 秒
- 字体/：Noto Serif CJK SC Bold

## 环境
pip install numpy cairocffi pillow；装 ffmpeg；mkdir -p ~/.fonts && cp 字体/*.otf ~/.fonts/ && fc-cache -f

## 画面
- 背景是暗色电影感（宫殿暗红、夜蓝、火光橙、黄昏金、雪灰）。人物是纯黑剪影，靠帽冠区分身份。
- 全片只让主角物件发光；重点人物最多给一抹颜色。
- 每个镜头慢推镜，开头 0.18 秒从黑场淡入；死亡或惩罚的瞬间红闪。

## 文字
- 用第二人称“假如你是X”，从物件或人物的视角讲（不一定非用这个句式）。
- 结构：3 句钩子 → 大标题问句（问全片核心问题）→ 按年份一事一镜 → 计数总结 → 反转 → 向观众提问。
- 左上字幕：粗衬线白字，打字机效果逐字淡入，每秒 15 字，最多两行。**按字数自动调字号**：size = clamp(1150 / 最长一行的字数, 60, 96) px，字少时就放大。
- 右上：红短线 +“年份 · 地点”42px，下面一行 30px 灰字写出处。
- 左下：贯穿全片的累积计数器，按题目来定（如“宋军阵亡 N 人”）。计数器要画在推镜之外，不然会被裁掉。
- 人名标注不小于 40px。字幕区（大约 y<260）不要放道具或文字板。
- 史实先核查；传说标“相传”，野史标“据《××》”；引古文要紧跟白话翻译。

## 交付前检查
每个镜头至少抽一帧拼成总图，检查文字重叠、文字被裁、画面过暗，然后交付。
