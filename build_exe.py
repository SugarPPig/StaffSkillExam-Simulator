#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考试系统打包脚本
自动将考试系统打包为独立的exe程序
"""

import os
import sys
import subprocess
import shutil

def create_spec_file():
    """创建PyInstaller规格文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['exam_system_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('single_choice.json', '.'),
        ('multiple_choice.json', '.'),
        ('judgment.json', '.'),
        ('README.md', '.'),
        ('GUI使用说明.md', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='人工智能考试练习系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''

    with open('exam_system.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print("已创建PyInstaller规格文件")

def check_files():
    """检查必要文件是否存在"""
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
        print(f"缺少必要文件: {', '.join(missing_files)}")
        return False

    print("所有必要文件都存在")
    return True

def build_exe():
    """构建exe程序"""
    print("开始打包程序...")

    try:
        # 使用spec文件打包
        result = subprocess.run([
            'pyinstaller',
            '--clean',  # 清理缓存
            'exam_system.spec'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("程序打包成功！")
            print(f"exe文件位置: {os.path.abspath('dist')}")
            return True
        else:
            print("打包失败:")
            print(result.stderr)
            return False

    except FileNotFoundError:
        print("未找到pyinstaller命令，请确保已正确安装")
        return False

def create_release_folder():
    """创建发布文件夹"""
    release_folder = "AI考试系统_发布版"

    if os.path.exists(release_folder):
        shutil.rmtree(release_folder)

    os.makedirs(release_folder)

    # 复制exe文件
    exe_path = os.path.join('dist', '人工智能考试练习系统.exe')
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, release_folder)
        print(f"已复制exe文件到 {release_folder}")

    # 复制说明文档
    docs = ['README.md', 'GUI使用说明.md']
    for doc in docs:
        if os.path.exists(doc):
            shutil.copy2(doc, release_folder)

    print(f"发布包已准备完毕: {release_folder}/")

def main():
    """主函数"""
    print("人工智能考试练习系统 - 打包工具")
    print("=" * 50)

    # 检查文件
    if not check_files():
        return

    # 创建规格文件
    create_spec_file()

    # 构建exe
    if build_exe():
        create_release_folder()
        print("\n打包完成！")
        print(f"发布文件夹: {os.path.abspath('AI考试系统_发布版')}")
        print("使用说明:")
        print("   1. 将整个发布文件夹复制给朋友")
        print("   2. 双击'人工智能考试练习系统.exe'运行")
        print("   3. 无需安装Python环境即可使用")
    else:
        print("\n打包失败，请检查错误信息")

if __name__ == "__main__":
    main()