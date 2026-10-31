# 历史动画技能库（li-shi）

纯代码做历史/水浒/搞笑短视频的画风技能：Python + cairocffi 逐帧绘制 + ffmpeg 合成，不用 AI 生图。

## 技能列表（skills/ 下每个文件夹一个技能，读 SKILL.md）
| 文件夹 | 叫法 | 一句话 | 画幅 |
|---|---|---|---|
| zhanzheng | 战争风 | 暗金古地图+金线行军+红印章，电影感镜头（含最新引擎与示例剧本） | 横屏 1920×1080 |
| junfa | 军阀风 | 战争风民国军阀版：华北民国地图+铁路金线、北洋军装纸偶、火车/双翼机/兵舰/电报/银元道具、红印章、年份进度条，只配音效（吴佩孚样片） | 横屏 |
| tangchao | 唐朝风 | 瘦长扁平古风人物+木格窗暖光（原名史海风；含人物库示例 examples/tangchao） | 横屏 1920×1080 |
| qq-lishi | qq历史 | 暖棕舞台Q版+左上逐字显影字幕 | 横屏 |
| qban | q版 | 大头Q版+写实地图+两层字幕（含完整代码库） | 横屏 |
| yuxi / heiying | 玉玺黑影风 | 暗色剪影+单个发光主体+纯字幕 | 横屏 |
| shenhua | 神话风 | 壁画剪纸木偶讲世界神话（希腊/埃及/北欧），无旁白中文大字幕+异域配乐，含北欧范例 | 横屏 4:3 |
| jiangziya | 姜子牙风 | 竖屏彩陶边框+陶土橙舞台+黑剪影，计数器弹跳打击+95.7BPM 卡点+音乐主导（水浒传系列用这个） | 竖屏 / 3:4 |
| zhidiao | 纸雕山河 | 自创层叠宣纸画风 | 都可 |
| 搞笑风 | 搞笑风 | 粗黑描边大头人物（女主苏糖+7个配角，可换装）+青色视线虚线+“在看我”计数，喜怒哀乐夸张表情+鬼畜复读（含引擎、样片、原片） | 横屏 1920×1080 |

| 女人风 | 女人风 | 慕夏新艺术海报画风+全身关节木偶，真实历史现场、侧脸互动，两行中文字幕+自写五声古风曲卡拍（随份子样片，含引擎） | 横屏 4:3 1440×1080 |

- `PREFERENCES.md`：所有片子都要遵守的制作偏好 + 水浒传系列设定（必读）。
- `examples/`：示例工程代码与抽帧（xuanzong、chenhuang、wusangui=战争风；sz2=黑影；shuihu=水浒林冲，含彩色英雄卡 v2/cardstill.py；zhidiao=纸雕；shipin=qq历史特效库）。
- `fonts/`：Noto Serif SC 等字体；搞笑风用 Noto Sans SC Black/Bold。
- `reference-clips/`：各画风参考样片的 10 秒片段（第 20–30 秒），只用来看画风，不照抄构图和台词。yuxi/黑影、纸雕没有外部参考片。

## 给 agent 的安装说明
1. 克隆本仓库。把 `skills/<名字>/` 放到你的 `/workspace/skills/<名字>/`，`examples/<名字>/` 放到 `/workspace/work/<名字>/`（SKILL.md 里写的路径就是这些位置；qq-lishi 的素材在原路径叫 `/workspace/skills/qq历史/`）。
2. 读每个 `skills/*/SKILL.md`，按开头的 name / description 创建同名技能，正文作为技能内容。
3. 把 `PREFERENCES.md` 记进记忆，做任何一部片都遵守。
4. 环境：`pip install cairocffi numpy pillow`（搞笑风另需 `edge-tts` 配音）；把 `fonts/` 里的字体拷到 `~/.fonts` 后运行 `fc-cache -f`；需要 ffmpeg。


## 人物风（`skills/人物风/`）
玉溪黑影风的近现代人物传记分支，学自《杨振宁》样片：西装/长衫剪影、年龄计数器、高潮快切+镜子碎裂+红闪震屏，无背景音乐只配合成音效。说明见 [`skills/人物风/SKILL.md`](skills/人物风/SKILL.md)。
