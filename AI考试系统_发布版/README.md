# AI考试系统发布版（完美版 v2.0）

## 发布简介
- 面向人工智能知识练习的桌面考试系统，题库内置可离线使用
- PyInstaller 打包的独立 exe，解压后即可在 Windows 上双击运行
- 适配单选、多选、判断三种题型，支持实时统计与智能反馈
- 本次发布整合所有修复内容，推荐使用 `AI考试系统_完美版.exe`

## 文件结构
- `AI考试系统_完美版.exe`：最新稳定版本，内置全部资源（推荐使用）
- `使用说明.md`：详细的上手指南与操作流程
- `GUI使用说明.md`：界面区域说明及交互细节
- Web 版本源码位于项目根目录：`web_exam_system.py` 与 `templates/index.html`

## 快速上手（桌面版）
1. 将整个 `AI考试系统_发布版` 文件夹解压/复制到本地
2. 双击 `AI考试系统_完美版.exe` 启动程序（首次启动可能略有延迟）
3. 点击界面中的“开始考试”，根据题型选择答案并提交
4. 查看即时反馈与统计信息，点击“下一题”继续练习

## Web 版本（Flask）
- Web 端位于源码根目录，适用于 PC 浏览器或手机浏览器访问
- 依赖：Python 3.8+、Flask (`pip install flask`)
- 启动方式：
  ```bash
  cd 项目根目录
  pip install flask
  python web_exam_system.py
  ```
- 访问地址：`http://localhost:5000`（手机可使用同一局域网下的电脑 IP）
- 特性亮点：移动端自适应界面、实时正确率统计、REST API 交互 (`/get_question`、`/submit_answer` 等)

## 功能亮点
- ✅ **480 道精选题目**：单选 300、多选 60、判断 120，全量题库内置
- ✅ **智能颜色反馈**：正确选项自动标绿，错误选项标红
- ✅ **实时正确率**：仅基于已答题目计算，更贴近真实水平
- ✅ **现代化界面**：按钮状态自动管理，长题目支持滚动查看
- ✅ **完全离线运行**：无需安装 Python 或额外依赖

## 更新与修复
- 修复题库路径问题，确保 exe 可独立运行且资源自动加载
- 新增 `answered_questions` 计数逻辑，正确率只统计已作答题目
- 切换到下一题时自动清理上一题的结果提示，界面信息更清晰
- 优化 PyInstaller 打包资源，减少首次启动异常与缺失提示

## PyInstaller 打包说明
1. 确认已安装 PyInstaller：`pip install pyinstaller`
2. 打包所需脚本与题库文件需放在同一目录（`exam_system_gui.py`、`single_choice.json`、`multiple_choice.json`、`judgment.json`）
3. 推荐使用现成的 `AI考试系统_完美版.spec`：
   ```bash
   pyinstaller AI考试系统_完美版.spec
   ```
   - 或手动执行：
     ```bash
     pyinstaller -w -F exam_system_gui.py \
       --name "AI考试系统_完美版" \
       --add-data "single_choice.json;." \
       --add-data "multiple_choice.json;." \
       --add-data "judgment.json;."
     ```
4. 生成文件位于 `dist/AI考试系统_完美版.exe`，`build`、`dist` 及 `.spec` 文件可按需保留或清理
5. 若需要包含 Web 资源，请额外打包 `templates` 目录并调整 `--add-data` 路径

## 分享与部署
- 保持文件夹结构不变，直接压缩后分享给同学或朋友
- 朋友只需解压并双击 exe 即可使用，无需额外配置

## 常见问题
- **需要联网吗？** 不需要，可完全离线练习
- **可以继续使用旧版本 exe 吗？** 建议删除旧版，使用当前完美版以获得全部修复
- **程序报杀毒提示？** exe 由 PyInstaller 打包，若被误报请添加到信任列表
- **如何切换至 Web 版？** 在源码目录运行 `python web_exam_system.py`，使用浏览器访问即可

祝你学习顺利，也欢迎反馈更多建议！