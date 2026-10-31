---
name: nvren
description: 女人风——慕夏新艺术海报画风 × 全身关节木偶的历史动画（真实历史现场、侧脸互动、两行中文字幕、自写古风配乐卡拍、4:3 1440×1080、结尾回开场可循环）。用户说“女人风”“随份子那种”“慕夏木偶风”或要做这类民俗/社会史题材时使用。
---

# 女人风（nvren）

样片：《随份子从哪儿来》（154 秒、27 镜头）。得名于片中敦煌“女人社”。

## 包内结构
- `引擎/`：完整工程。`nv.py` 慕夏底层（线条、色板、标题字）；`ppl.py` 全身关节木偶 `fig()`；`base.py` 外框、字幕、名牌、大数字；`bgs.py` 各时代真实场景（静态层缓存 + 动态层）；`scenes.py` 镜头函数；`film.py` 镜头表 + 渲染；`audio.py` 自写配乐 + 音效；`build.sh` 一键重建；`FACTS.md` 史实依据；`TREATMENT.md` 制作说明。
- `字体/`：NotoSerifSC-Bold（字幕、囍字）、LXGW WenKai（标题、牌匾）。开工先 `mkdir -p ~/.fonts && cp 字体/* ~/.fonts && fc-cache -f`。
- `参考视频/样片_随份子_前10秒.mp4`、`样片截图/`。

## 快速开始
```bash
pip install numpy scipy cairocffi pillow soundfile     # 另需 ffmpeg
cp -r 引擎 /workspace/work/新片 && cd /workspace/work/新片
# 改 scenes.py（镜头函数）、bgs.py（场景）、film.py 的 SHOTS 镜头表和 WIPE_AT、base.py 的 NAMES
python3 film.py --sheet                 # 每镜 70% 处一帧联系表 → out/sheet.jpg，先自己审
python3 film.py --still 26              # 单帧 → out/still.png
bash build.sh                           # 2 进程渲染 + 配乐 + iPhone 兼容转码 → out/*.mp4
```
单帧约 0.05–0.15 秒，154 秒片 2 核约 6 分钟。命令超过 120 秒会被转后台，渲染用后台 `&` 起，再分次查 log。

## 用户的硬性要求
- 背景必须是真实历史现场：真实房屋、院落、人物、器物、道具。不要抽象背景、装饰光环、拱门拱窗、纯神话式构图。慕夏味只留在线条、配色、外框纹样里。
- 人物用侧脸或三分之二侧脸互动，不要一直正面看镜头。
- 全部代码画，不用 AI 生图；只要中文字幕，无旁白、无英文。
- 群像真画人群（后排小人 `outline=False`、错相位小动作）。
- 拿到题材直接开做，自己出联系表把关，直接交成片；交付时一句话说明对原文的改动和演绎处。
- 配乐：本风格要自写古风曲，有特点、节奏不要太慢（约 110–116 BPM），剪辑和动作跟着节拍走（用户 2026-10-31 定）。
- 史实严谨：不把多源演变说成单线起源；演绎处在 FACTS.md 标明。

## 画风
- 慕夏剪影描边：人物离屏绘制后错位垫深棕 #4e3320 粗外轮廓（`layer()`），内线细；暖色低饱和平涂。
- 木偶约 8 头身，朝右为默认，`flip=True` 朝左。头侧面、杏仁眼。
- 外框恒定：顶部马赛克色带 + 中央“份”字徽记（换题材换徽记字）；底部米色字幕牌，两端金色鞭线卷草 + 绿叶 + 粉花，最底再一条色带。
- 场景 1920×1080 画，缩放 0.75 放进 1440×810（y=44 起），下方是字幕牌。每个场景至少三层：远景天空/山/云鸟，中景建筑，近景地面器物；加动态（云、鸟、灯笼摆、烛火、香烟、光尘、驼队）。

## 木偶 `fig(c, x, yfeet, h, pose, t, outline=True, **o)`
- pose：`nsh nel fsh fel`（近/远肩、肘，0 下垂、正值向前）、`nhip nkn fhip fkn`、`head`、`body`（只转上身，鞠躬用）、`bob`。`walk_pose(ph, stride)` 走路，`wph(lt)` 一拍一步。
- 服饰 `body`：`skirt`（唐高腰裙+披帛 pibo）、`robe`（交领袍）、`mourn`（丧服）、`aoqun`（明清袄裙）、`changshan`（长衫，可加 `magua` 马褂）、`suit`（西装）、`dress`（现代裙）。
- 发型 `hair`：`gaoji` 高髻、`nun` 尼、`wanji` 低髻、`grey` 白发抹额（老太太）、`bob` 短发、`guan` 周汉冠、`fangjin` 明方巾、`guapi` 瓜皮帽、`short` 现代短发、`mourn` 首绖。
- 其他：`male beard age mouth('open'/'smile'/'closed') eyes('wide'/'closed') brow blink sit('chair'/'kneel') top bot bot2 belt trim shoe jacket tie kasaya flower wind`。
- 道具 `near=/far=` 传函数（手坐标系）：`p_hongbao p_brush p_bolt p_coins p_ye p_bowl p_silver p_phone p_book`，及 scenes.py 里的 `jar_p basket_p`。
- 返回 `{'head','top','mouth','hand_n','hand_f'}` 世界坐标，给名牌、落物、倒油对位。

## 讲故事
- 字幕两行、每行 4–12 字，口语说书腔；镜头时长 = 字数/4.5+1.5 秒，向上取整到半小节（2 拍），保证切点在拍上。
- 标记：`[r]红[/r]` 结果/数字/情绪，`[g]绿[/g]` 地名、专有物，人名按 `NAMES` 自动蓝。
- 镜头函数返回：`tag(名, 坐标, 'L'/'R')` 名牌、`num(文字,x,y,字号,透明度,颜色,弹出)` 大字/计数、`shake(强度)`。`pop_at(lt, t0)` 做弹出，计数在拍点上跳（如 ¥200→¥800、二十两→十六两）。
- 结构：钩子（今天的场景）→ 椭圆标题牌 → 各时代依次展开（每段换真实场景，段首翻纸转场 WIPE_AT）→ 今天 → 回到本意 → 结尾回开场构图可循环。
- 文书、典籍用真实形态出镜：竹简（`bamboo_card`）、手卷（`scroll_card`）、礼簿（`ledger_card` 竖排右起）、份子单（`fenzi_list`）、牌匾（`plaque`），并标出处小字。

## 配乐与音效（audio.py）
- D 宫五声（D E F# A B），112 BPM。笛子主旋律（颤音、倚音、气声），古筝分解和弦（拨弦带按音滑音），低音拨弦，笙式长音垫底；打击：堂鼓、梆子、小镲、大锣、手鼓。
- 主题 TA/TB 两句 + 俏皮断奏 TC + 西域味 TD（以 B 为中心）。每段换律动：庄重段半速鼓、诙谐段梆子八分、西域段手鼓+十六分古筝、热闹段密鼓轮指、民国段唢呐、结尾笛子独奏→全编制收锣。
- 音效按镜头和拍点放（`at(i, beats)`）：嘈杂人声、脚步、红包窸窣、落箱、铜钱、毛笔、竹简、风、驼铃、倒油、翻碗、银锭、鞭炮、算盘、扫码“叮”、心跳、翻纸 whoosh。最后 loudnorm -15 LUFS。

## 交付（iPhone 兼容）
`-vf fps=24 -c:v libx264 -profile:v high -level 4.1 -crf 21 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart`；ffprobe 查 level=41、24/1、视音频时长一致。

## 踩过的坑
- `fig()` 在离屏层里画，返回坐标必须加回层偏移（已修好）。
- LXGW WenKai 没有“囍”“赗”“襚”等字，这些字用 `SERIF`（Noto Serif CJK SC）。
- `body` 旋转只作用上身，否则鞠躬像整块木板倒下。
- 坐姿要在人物前画椅子（`chair()`），不要画进静态背景，否则对不上。
