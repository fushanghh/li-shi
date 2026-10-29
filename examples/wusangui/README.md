# 三藩之乱：吴三桂五大致命盲区（战争风·激情版）

横屏 1920×1080，约 207.6 秒，100 BPM 配乐。风格参考《玄武门 B计划》，镜头手法沿用 chenhuang（陈胜吴广）：关键道具特写、多层视差运镜、大远景推近景、动作与道具的象征表现。

## 文件
- `clib.py` / `lib.py`：基础绘制库（cairocffi）。
- `scene3.py`：多层视差相机、天空、山、火、烟尘、城墙等场景工具。
- `base.py`：镜头注册、字幕、人群精灵缓存、视差图层、卷轴、旗帜。
- `figq.py`（`fig2.py` 旧版）：吴三桂、康熙、清军、吴军、绿营人物造型。
- `geo3.py`：全国地图、路线、省区、城市、战区高亮。
- `hud.py` / `kinetic.py`：大字砸屏、印章、徽章、计数器、开场钩子动态字。
- `shotsA.py`：钩子、片名、盲区一（信用破产）。
- `shotsB.py`：盲区二（岳州停兵）、盲区三（塑料同盟）。
- `shotsC.py`：盲区四（代际差距/汉将绿营）、盲区五（国力悬殊）、结尾推演。
- `render.py`：渲染、转场、镜头抖动、字幕顶栏；分段输出 p0–p5.mp4。
- `scan.py`：扫描动态事件 → `events.json`。
- `synth.py` + `score4.py`：按事件卡点合成 100 BPM 配乐 `wsg.wav`。
- `l.txt`：ffmpeg concat 列表。
- `a.jpg` `b.jpg` `c.jpg` `fin.jpg`：分段联系表和成片抽帧；`ref_ch.jpg`：陈胜吴广参考联系表。

## 流程
1. `python render.py v <起始帧> <结束帧> p0.mp4` 按帧区间分段渲染（30fps，共约 6228 帧，分 6 段可并行）；`python render.py still <拍号…>` 出静帧检查。
2. `python scan.py` 生成 `events.json`，再 `python score4.py`（会读取同目录 `score.py` 的合成段，`score.py` 已附）生成 `wsg.wav`。
3. `ffmpeg -f concat -i l.txt -i wsg.wav -c:v copy -c:a aac -shortest out.mp4`。

## 史实约束（做同题材时遵守）
- 吴应熊 1674 年被处置；吴三桂 1678 年衡阳称帝（大周），同年病死；吴世璠接班，昆明 1681 年失守。
- 岳州停兵是 1674—1678 长期僵持，不是几个月。
- 第四盲区汉将用赵良栋、王进宝、张勇；施琅属台湾战事，不放这里。
- “若直接北伐能否改写历史”必须标明是历史推演。

成片 10 秒片段见 `reference-clips/zhanzheng_三藩之乱吴三桂.mp4`。
