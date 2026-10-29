# 战争风 · 学习包

- SKILL.md：完整画风与制作规则（含 2026-10-29 新规：每片重写配乐、剧本结构随内容变）。导入为自定义技能“zhanzheng”。
- 参考截图（参考样片的10秒片段在仓库 reference-clips/zhanzheng_安史之乱.mp4）：画风来源，只学方法不照抄。
- 引擎/：最新代码（南梁侯景版）。Python + cairocffi + numpy + pillow + ffmpeg。
  - 安装：pip install cairocffi numpy pillow；把仓库根目录 fonts/ 里的字体拷进 ~/.fonts 后 fc-cache -f
  - 镜头写在 shots1.py / shots2.py（@nx(拍数,'年份·地点','字幕{重点}','出处')）
  - 抽帧：python3 render.py still <秒...>，再 python3 sheet.py s.jpg <秒...>
  - 分段渲染：python3 render.py seg 起帧 止帧 segN.mp4；配乐：python3 scan.py && python3 score_t.py
  - 注意：score_t.py 是上一片的配乐，新片必须按 SKILL.md 重写音乐。
- 示例剧本/：三份已按史实修订的剧本。
