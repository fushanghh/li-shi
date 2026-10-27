# 历史动画技能库（li-shi）

纯代码做历史/水浒短视频的画风技能：Python + cairocffi 逐帧绘制 + ffmpeg 合成，不用 AI 生图。

## 技能列表（skills/ 下每个文件夹一个技能，读 SKILL.md）
| 文件夹 | 叫法 | 一句话 | 画幅 |
|---|---|---|---|
| zhanzheng | 战争风 | 暗金古地图+金线行军+红印章，电影感镜头 | 横屏 1920×1080 |
| shihai | 史海风 | 瘦长扁平古风人物+木格窗暖光 | 横屏 |
| qq-lishi | qq历史 | 暖棕舞台Q版+左上逐字显影字幕 | 横屏 |
| qban | q版 | 大头Q版+写实地图+两层字幕（含完整代码库） | 横屏 |
| yuxi / heiying | 玉溪 / 黑影 | 暗色剪影+单个发光主体+纯字幕 | 横屏 |
| shenhua | 神话风 | 陶土橙舞台+黑剪影+计数器卡点+音乐主导（水浒传系列用这个） | 竖屏 / 3:4 |
| zhidiao | 纸雕山河 | 自创层叠宣纸画风 | 都可 |

- `PREFERENCES.md`：所有片子都要遵守的制作偏好 + 水浒传系列设定（必读）。
- `examples/`：示例工程代码与抽帧（xuanzong、chenhuang=战争风；sz2=黑影；shuihu=水浒林冲，含彩色英雄卡 v2/cardstill.py；zhidiao=纸雕；shipin=qq历史特效库）。
- `fonts/`：Noto Serif SC 字体。
- 参考样片视频因体积太大没有放进仓库。

## 给 agent 的安装说明
1. 克隆本仓库。把 `skills/<名字>/` 放到你的 `/workspace/skills/<名字>/`，`examples/<名字>/` 放到 `/workspace/work/<名字>/`（SKILL.md 里写的路径就是这些位置；qq-lishi 的素材在原路径叫 `/workspace/skills/qq历史/`）。
2. 读每个 `skills/*/SKILL.md`，按开头的 name / description 创建同名技能，正文作为技能内容。
3. 把 `PREFERENCES.md` 记进记忆，做任何一部片都遵守。
4. 环境：`pip install cairocffi numpy pillow`；把 `fonts/` 里的字体拷到 `~/.fonts` 后运行 `fc-cache -f`；需要 ffmpeg。
