#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动GUI考试系统的简单脚本
"""

import sys
import os

def main():
    """启动GUI考试系统"""
    print("正在启动人工智能考试练习系统GUI版本...")

    # 检查Python版本
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本")
        return

    # 检查必要文件
    required_files = [
        'exam_system_gui.py',
        'single_choice.json',
        'multiple_choice.json',
        'judgment.json'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"错误: 缺少必要文件: {', '.join(missing_files)}")
        return

    # 导入并运行GUI
    try:
        from exam_system_gui import ExamSystemGUI
        print("GUI界面启动中...")
        app = ExamSystemGUI()
        app.run()
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保tkinter库已安装")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == "__main__":
    main()