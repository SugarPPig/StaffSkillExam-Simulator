#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人工智能考试练习系统 - GUI优化版本
解决问题：
1. 判断题默认选项应该是未选中状态
2. 统计信息和答题结果显示优化
使用tkinter图形界面
"""

import json
import random
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Any, Tuple
import os


class ExamSystemGUI:
    def __init__(self):
        # 初始化数据
        self.questions = {
            'single_choice': [],
            'multiple_choice': [],
            'judgment': []
        }
        self.current_question = None
        self.current_question_type = None
        self.total_questions = 0
        self.correct_answers = 0
        self.answered_questions = 0  # 新增：已回答的题目数量
        self.selected_answers = []

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("人工智能考试练习系统")

        # 获取屏幕尺寸并设置固定窗口大小
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 设置窗口为屏幕的85%高度，最小900像素，最大1100像素
        window_height = max(900, min(1100, int(screen_height * 0.85)))
        window_width = 950

        # 居中显示
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)  # 禁止调整大小，固定高度

        # 设置样式
        self.setup_styles()

        # 创建界面
        self.create_widgets()

        # 加载题库
        self.load_questions()

    def setup_styles(self):
        """设置界面样式"""
        # 配置主题色彩
        self.colors = {
            'primary': '#2196F3',      # 蓝色
            'success': '#4CAF50',      # 绿色
            'error': '#F44336',        # 红色
            'warning': '#FF9800',      # 橙色
            'background': '#F5F5F5',   # 浅灰色背景
            'white': '#FFFFFF',        # 白色
            'text': '#333333',         # 深灰色文字
            'light_text': '#666666',   # 浅灰色文字
            'light_bg': '#F8F9FA'      # 浅色背景
        }

        # 配置字体
        self.fonts = {
            'title': ('微软雅黑', 16, 'bold'),
            'subtitle': ('微软雅黑', 12, 'bold'),
            'normal': ('微软雅黑', 10),
            'button': ('微软雅黑', 10, 'bold'),
            'large': ('微软雅黑', 11)
        }

    def create_widgets(self):
        """创建界面组件"""
        # 主框架 - 直接使用Frame，不使用滚动
        main_frame = tk.Frame(self.root, bg=self.colors['white'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 标题区域
        self.create_header(main_frame)

        # 题目区域
        self.create_question_area(main_frame)

        # 选项区域
        self.create_options_area(main_frame)

        # 按钮区域
        self.create_buttons_area(main_frame)

        # 统计区域 - 优化显示
        self.create_stats_area(main_frame)

        # 结果显示区域 - 优化显示
        self.create_result_area(main_frame)

    def create_header(self, parent):
        """创建标题区域"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], relief=tk.RAISED, bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # 主标题
        title_label = tk.Label(
            header_frame,
            text="人工智能考试练习系统",
            font=self.fonts['title'],
            fg=self.colors['white'],
            bg=self.colors['primary']
        )
        title_label.pack(pady=10)

        # 副标题
        subtitle_label = tk.Label(
            header_frame,
            text="支持单选题、多选题、判断题练习",
            font=self.fonts['normal'],
            fg=self.colors['white'],
            bg=self.colors['primary']
        )
        subtitle_label.pack(pady=(0, 10))

    def create_question_area(self, parent):
        """创建题目显示区域"""
        question_frame = tk.LabelFrame(
            parent,
            text="题目内容",
            font=self.fonts['subtitle'],
            fg=self.colors['text'],
            bg=self.colors['white'],
            relief=tk.RAISED,
            bd=2
        )
        question_frame.pack(fill=tk.X, pady=(0, 10))  # 不使用expand

        # 题目类型和序号标签框架
        type_frame = tk.Frame(question_frame, bg=self.colors['white'])
        type_frame.pack(fill=tk.X, padx=10, pady=5)

        # 题目类型标签
        self.question_type_label = tk.Label(
            type_frame,
            text="",
            font=self.fonts['subtitle'],
            fg=self.colors['primary'],
            bg=self.colors['light_bg'],
            relief=tk.RAISED,
            bd=1,
            padx=10,
            pady=5
        )
        self.question_type_label.pack(side=tk.LEFT)

        # 题目序号标签
        self.question_number_label = tk.Label(
            type_frame,
            text="",
            font=self.fonts['subtitle'],
            fg=self.colors['warning'],
            bg=self.colors['light_bg'],
            relief=tk.RAISED,
            bd=1,
            padx=10,
            pady=5
        )
        self.question_number_label.pack(side=tk.RIGHT)

        # 题目内容显示区域
        self.question_text = scrolledtext.ScrolledText(
            question_frame,
            height=3,  # 减少高度
            wrap=tk.WORD,
            font=self.fonts['large'],
            state=tk.DISABLED,
            bg=self.colors['white'],
            relief=tk.SUNKEN,
            bd=2
        )
        self.question_text.pack(fill=tk.X, padx=10, pady=5)  # 不使用expand

    def create_options_area(self, parent):
        """创建选项区域"""
        self.options_frame = tk.LabelFrame(
            parent,
            text="选项",
            font=self.fonts['subtitle'],
            fg=self.colors['text'],
            bg=self.colors['white'],
            relief=tk.RAISED,
            bd=2
        )
        self.options_frame.pack(fill=tk.X, pady=(0, 10))

        # 用于存储选项变量
        self.option_vars = []
        self.option_widgets = []

    def create_buttons_area(self, parent):
        """创建按钮区域"""
        buttons_frame = tk.Frame(parent, bg=self.colors['white'])
        buttons_frame.pack(fill=tk.X, pady=(0, 15))

        # 第一行按钮
        top_buttons = tk.Frame(buttons_frame, bg=self.colors['white'])
        top_buttons.pack(fill=tk.X, pady=(0, 5))

        # 开始考试按钮
        self.start_btn = tk.Button(
            top_buttons,
            text="开始考试",
            font=self.fonts['button'],
            bg=self.colors['primary'],
            fg=self.colors['white'],
            command=self.start_exam,
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))

        # 提交答案按钮
        self.submit_btn = tk.Button(
            top_buttons,
            text="提交答案",
            font=self.fonts['button'],
            bg=self.colors['warning'],
            fg=self.colors['white'],
            command=self.submit_answer,
            width=12,
            height=2,
            state=tk.DISABLED,
            relief=tk.RAISED,
            bd=3
        )
        self.submit_btn.pack(side=tk.LEFT, padx=(0, 10))

        # 下一题按钮
        self.next_btn = tk.Button(
            top_buttons,
            text="下一题",
            font=self.fonts['button'],
            bg=self.colors['success'],
            fg=self.colors['white'],
            command=self.next_question,
            width=12,
            height=2,
            state=tk.DISABLED,
            relief=tk.RAISED,
            bd=3
        )
        self.next_btn.pack(side=tk.LEFT, padx=(0, 10))

        # 重新开始按钮
        self.restart_btn = tk.Button(
            top_buttons,
            text="重新开始",
            font=self.fonts['button'],
            bg=self.colors['text'],
            fg=self.colors['white'],
            command=self.restart_exam,
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        self.restart_btn.pack(side=tk.RIGHT)

    def create_stats_area(self, parent):
        """创建统计信息区域 - 优化显示"""
        stats_frame = tk.LabelFrame(
            parent,
            text="统计信息",
            font=self.fonts['subtitle'],
            fg=self.colors['text'],
            bg=self.colors['white'],
            relief=tk.RAISED,
            bd=2
        )
        stats_frame.pack(fill=tk.X, pady=(0, 10))  # 减少pady

        # 统计信息容器
        stats_container = tk.Frame(stats_frame, bg=self.colors['light_bg'], relief=tk.SUNKEN, bd=2)
        stats_container.pack(fill=tk.X, padx=10, pady=5)  # 减少pady

        # 题库信息
        self.library_stats_label = tk.Label(
            stats_container,
            text="题库加载中...",
            font=self.fonts['normal'],
            fg=self.colors['text'],
            bg=self.colors['light_bg'],
            pady=5
        )
        self.library_stats_label.pack()

        # 答题进度
        self.progress_stats_label = tk.Label(
            stats_container,
            text="等待开始考试...",
            font=self.fonts['large'],
            fg=self.colors['primary'],
            bg=self.colors['light_bg'],
            pady=5
        )
        self.progress_stats_label.pack()

    def create_result_area(self, parent):
        """创建结果显示区域 - 优化显示"""
        self.result_frame = tk.LabelFrame(
            parent,
            text="答题结果",
            font=self.fonts['subtitle'],
            fg=self.colors['text'],
            bg=self.colors['white'],
            relief=tk.RAISED,
            bd=2
        )
        self.result_frame.pack(fill=tk.X)

        # 结果容器
        result_container = tk.Frame(self.result_frame, bg=self.colors['light_bg'], relief=tk.SUNKEN, bd=2)
        result_container.pack(fill=tk.X, padx=10, pady=5)  # 减少pady

        self.result_label = tk.Label(
            result_container,
            text="请点击开始考试按钮开始练习",
            font=self.fonts['large'],
            fg=self.colors['light_text'],
            bg=self.colors['light_bg'],
            pady=10,
            wraplength=800,
            justify=tk.LEFT
        )
        self.result_label.pack()

    def load_questions(self):
        """加载题库文件"""
        try:
            # 加载单选题
            single_choice_path = get_resource_path('single_choice.json')
            with open(single_choice_path, 'r', encoding='utf-8') as f:
                self.questions['single_choice'] = json.load(f)

            # 加载多选题
            multiple_choice_path = get_resource_path('multiple_choice.json')
            with open(multiple_choice_path, 'r', encoding='utf-8') as f:
                self.questions['multiple_choice'] = json.load(f)

            # 加载判断题
            judgment_path = get_resource_path('judgment.json')
            with open(judgment_path, 'r', encoding='utf-8') as f:
                self.questions['judgment'] = json.load(f)

            # 更新统计信息
            single_count = len(self.questions['single_choice'])
            multiple_count = len(self.questions['multiple_choice'])
            judgment_count = len(self.questions['judgment'])
            total_count = single_count + multiple_count + judgment_count

            stats_text = f"📚 题库加载成功！单选题: {single_count}道 | 多选题: {multiple_count}道 | 判断题: {judgment_count}道 | 总计: {total_count}道"
            self.library_stats_label.config(text=stats_text, fg=self.colors['success'])

            return True

        except FileNotFoundError as e:
            messagebox.showerror("错误", f"题库文件未找到: {e}")
            self.library_stats_label.config(text="❌ 题库加载失败", fg=self.colors['error'])
            return False
        except json.JSONDecodeError as e:
            messagebox.showerror("错误", f"题库文件格式错误: {e}")
            self.library_stats_label.config(text="❌ 题库加载失败", fg=self.colors['error'])
            return False

    def get_random_question(self) -> Tuple[str, Dict[str, Any]]:
        """随机获取一道题目"""
        # 随机选择题型
        question_types = ['single_choice', 'multiple_choice', 'judgment']
        question_type = random.choice(question_types)

        # 随机选择题目
        questions = self.questions[question_type]
        if not questions:
            return None, None

        question = random.choice(questions)
        return question_type, question

    def display_question(self, question_type: str, question: Dict[str, Any]):
        """显示题目"""
        # 清空之前的选项
        self.clear_options()

        # 重置选项颜色（为新题目准备）
        self.reset_option_colors()

        # 设置题目类型标签
        type_names = {
            'single_choice': '【单选题】',
            'multiple_choice': '【多选题】',
            'judgment': '【判断题】'
        }
        self.question_type_label.config(text=type_names[question_type])

        # 设置题目序号
        self.question_number_label.config(text=f"第 {self.total_questions} 题")

        # 显示题目内容
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(1.0, question['Unnamed: 1'])
        self.question_text.config(state=tk.DISABLED)

        # 显示选项
        self.create_question_options(question_type, question)

    def clear_options(self):
        """清空选项区域"""
        for widget in self.option_widgets:
            widget.destroy()
        self.option_widgets.clear()
        self.option_vars.clear()

    def create_question_options(self, question_type: str, question: Dict[str, Any]):
        """创建题目选项"""
        # 选项容器
        options_container = tk.Frame(self.options_frame, bg=self.colors['white'])
        options_container.pack(fill=tk.X, padx=10, pady=10)
        self.option_widgets.append(options_container)  # 将容器也加入到widget列表中

        if question_type == 'single_choice':
            # 单选题选项 - 确保默认未选中
            self.selected_answer = tk.StringVar()
            self.selected_answer.set(None)  # 设置为None确保未选中

            options = [
                ('A', question['Unnamed: 2']),
                ('B', question['Unnamed: 3']),
                ('C', question['Unnamed: 4']),
                ('D', question['Unnamed: 5'])
            ]

            for value, text in options:
                option_frame = tk.Frame(options_container, bg=self.colors['white'], relief=tk.RIDGE, bd=1)
                option_frame.pack(fill=tk.X, pady=2)

                rb = tk.Radiobutton(
                    option_frame,
                    text=f"{value}. {text}",
                    variable=self.selected_answer,
                    value=value,
                    font=self.fonts['normal'],
                    bg=self.colors['white'],
                    wraplength=700,
                    justify=tk.LEFT,
                    padx=10,
                    pady=5,
                    indicatoron=1  # 确保显示单选按钮
                )
                rb.pack(anchor=tk.W)
                self.option_widgets.append(rb)
                self.option_widgets.append(option_frame)

        elif question_type == 'multiple_choice':
            # 多选题选项
            self.selected_answers = {}
            options = [
                ('A', question['Unnamed: 2']),
                ('B', question['Unnamed: 3']),
                ('C', question['Unnamed: 4']),
                ('D', question['Unnamed: 5']),
                ('E', question['Unnamed: 6'])
            ]

            for value, text in options:
                var = tk.BooleanVar()
                var.set(False)  # 确保默认未选中
                self.selected_answers[value] = var

                option_frame = tk.Frame(options_container, bg=self.colors['white'], relief=tk.RIDGE, bd=1)
                option_frame.pack(fill=tk.X, pady=2)

                cb = tk.Checkbutton(
                    option_frame,
                    text=f"{value}. {text}",
                    variable=var,
                    font=self.fonts['normal'],
                    bg=self.colors['white'],
                    wraplength=700,
                    justify=tk.LEFT,
                    padx=10,
                    pady=5
                )
                # 为了颜色标记功能，给checkbutton添加一个自定义属性
                cb.option_value = value
                cb.pack(anchor=tk.W)
                self.option_widgets.append(cb)
                self.option_widgets.append(option_frame)

        elif question_type == 'judgment':
            # 判断题选项 - 重点修复默认选中问题
            self.selected_answer = tk.StringVar()
            self.selected_answer.set(None)  # 设置为None确保未选中

            options = [
                ('A', '正确'),
                ('B', '错误')
            ]

            for value, text in options:
                option_frame = tk.Frame(options_container, bg=self.colors['white'], relief=tk.RIDGE, bd=1)
                option_frame.pack(fill=tk.X, pady=2)

                rb = tk.Radiobutton(
                    option_frame,
                    text=f"{value}. {text}",
                    variable=self.selected_answer,
                    value=value,
                    font=self.fonts['large'],
                    bg=self.colors['white'],
                    padx=20,
                    pady=8,
                    indicatoron=1  # 确保显示为圆形按钮
                )
                rb.pack(anchor=tk.W)
                self.option_widgets.append(rb)
                self.option_widgets.append(option_frame)

    def start_exam(self):
        """开始考试"""
        if not any(self.questions.values()):
            messagebox.showerror("错误", "题库为空，无法开始考试")
            return

        # 重置统计
        self.total_questions = 0
        self.correct_answers = 0
        self.answered_questions = 0  # 重置已回答题目计数

        # 更新按钮状态
        self.start_btn.config(state=tk.DISABLED)
        self.submit_btn.config(state=tk.NORMAL)

        # 显示第一题
        self.next_question()

        # 更新结果显示
        self.result_label.config(text="🎯 考试已开始，请选择答案后点击提交", fg=self.colors['text'])

    def next_question(self):
        """显示下一题"""
        question_type, question = self.get_random_question()

        if not question:
            messagebox.showwarning("提示", "没有可用的题目")
            return

        self.current_question = question
        self.current_question_type = question_type
        self.total_questions += 1

        # 显示题目
        self.display_question(question_type, question)

        # 更新按钮状态
        self.submit_btn.config(state=tk.NORMAL)
        self.next_btn.config(state=tk.DISABLED)

        # 重置答题结果显示
        self.result_label.config(text="🎯 请选择答案后点击提交", fg=self.colors['text'])

        # 更新统计信息（但此时还没有提交答案，所以正确率基于已完成的题目计算）
        self.update_stats()

    def submit_answer(self):
        """提交答案"""
        if not self.current_question:
            return

        # 获取用户答案
        user_answer = self.get_user_answer()
        if not user_answer:
            messagebox.showwarning("提示", "请先选择答案再提交")
            return

        # 获取正确答案
        correct_answer = self.current_question['Unnamed: 7']

        # 检查答案
        is_correct = self.check_answer(user_answer, correct_answer)

        if is_correct:
            self.correct_answers += 1

        # 增加已回答题目计数
        self.answered_questions += 1

        # 显示结果
        self.show_answer_result(user_answer, correct_answer, is_correct)

        # 更新按钮状态
        self.submit_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL)

        # 更新统计
        self.update_stats()

    def get_user_answer(self) -> str:
        """获取用户答案"""
        if self.current_question_type in ['single_choice', 'judgment']:
            answer = self.selected_answer.get()
            return answer if answer else ""
        elif self.current_question_type == 'multiple_choice':
            selected = []
            for key, var in self.selected_answers.items():
                if var.get():
                    selected.append(key)
            return ''.join(sorted(selected))
        return ""

    def check_answer(self, user_answer: str, correct_answer: str) -> bool:
        """检查答案是否正确"""
        user_answer = user_answer.upper().strip()
        correct_answer = correct_answer.upper().strip()

        if self.current_question_type == 'multiple_choice':
            # 多选题需要所有选项都正确
            user_set = set(user_answer.replace(' ', ''))
            correct_set = set(correct_answer.replace(' ', ''))
            return user_set == correct_set
        else:
            return user_answer == correct_answer

    def show_answer_result(self, user_answer: str, correct_answer: str, is_correct: bool):
        """显示答题结果并标识选项颜色"""
        # 显示结果文本
        if is_correct:
            result_text = f"✅ 恭喜！回答正确！\n\n📝 你的答案: {user_answer}\n✔️ 正确答案: {correct_answer}"
            color = self.colors['success']
        else:
            result_text = f"❌ 很遗憾，回答错误！\n\n📝 你的答案: {user_answer}\n✔️ 正确答案: {correct_answer}"
            color = self.colors['error']

        self.result_label.config(text=result_text, fg=color)

        # 对选项进行颜色标识
        self.highlight_answer_options(user_answer, correct_answer)

    def highlight_answer_options(self, user_answer: str, correct_answer: str):
        """高亮显示答案选项：正确答案标绿，错误答案标红"""
        user_answer_set = set(user_answer.upper().replace(' ', ''))
        correct_answer_set = set(correct_answer.upper().replace(' ', ''))

        # 遍历所有选项widget，找到RadioButton和Checkbutton进行颜色标识
        for widget in self.option_widgets:
            if isinstance(widget, (tk.Radiobutton, tk.Checkbutton)):
                try:
                    # 获取选项的值
                    if isinstance(widget, tk.Radiobutton):
                        # RadioButton使用value属性
                        option_value = widget['value']
                    elif isinstance(widget, tk.Checkbutton):
                        # Checkbutton使用自定义的option_value属性
                        option_value = getattr(widget, 'option_value', None)

                    if option_value:
                        option_value = option_value.upper()

                        # 判断是否是正确答案
                        if option_value in correct_answer_set:
                            # 正确答案标绿
                            widget.config(bg='#E8F5E8', fg=self.colors['success'])
                            # 如果父框架存在，也改变背景色
                            parent = widget.master
                            if parent and isinstance(parent, tk.Frame):
                                parent.config(bg='#E8F5E8', relief=tk.RIDGE, bd=2)
                        elif option_value in user_answer_set:
                            # 用户选择的错误答案标红
                            widget.config(bg='#FFE8E8', fg=self.colors['error'])
                            # 如果父框架存在，也改变背景色
                            parent = widget.master
                            if parent and isinstance(parent, tk.Frame):
                                parent.config(bg='#FFE8E8', relief=tk.RIDGE, bd=2)
                except (tk.TclError, KeyError, AttributeError):
                    # 如果widget没有相应属性，跳过
                    continue

    def reset_option_colors(self):
        """重置选项颜色为默认状态"""
        for widget in self.option_widgets:
            if isinstance(widget, (tk.Radiobutton, tk.Checkbutton)):
                try:
                    widget.config(bg=self.colors['white'], fg=self.colors['text'])
                    # 重置父框架颜色
                    parent = widget.master
                    if parent and isinstance(parent, tk.Frame):
                        parent.config(bg=self.colors['white'], relief=tk.RIDGE, bd=1)
                except tk.TclError:
                    # 如果widget已被销毁，跳过
                    continue

    def update_stats(self):
        """更新统计信息"""
        if self.answered_questions > 0:
            accuracy = (self.correct_answers / self.answered_questions) * 100
            stats_text = f"📊 进度: 第 {self.total_questions} 题 | ✅ 正确: {self.correct_answers} 题 | 📈 正确率: {accuracy:.1f}%"
            color = self.colors['success'] if accuracy >= 60 else self.colors['warning'] if accuracy >= 40 else self.colors['error']
        else:
            stats_text = f"📊 进度: 第 {self.total_questions} 题 | 🚀 准备答题..."
            color = self.colors['text']

        self.progress_stats_label.config(text=stats_text, fg=color)

    def restart_exam(self):
        """重新开始考试"""
        # 重置所有状态
        self.total_questions = 0
        self.correct_answers = 0
        self.answered_questions = 0  # 重置已回答题目计数
        self.current_question = None
        self.current_question_type = None

        # 清空显示
        self.clear_options()
        self.question_type_label.config(text="")
        self.question_number_label.config(text="")
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END)
        self.question_text.config(state=tk.DISABLED)

        # 重置按钮状态
        self.start_btn.config(state=tk.NORMAL)
        self.submit_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)

        # 重置显示
        self.result_label.config(text="🎯 请点击开始考试按钮开始练习", fg=self.colors['light_text'])
        self.progress_stats_label.config(text="🚀 等待开始考试...", fg=self.colors['text'])

    def run(self):
        """运行GUI应用"""
        self.root.mainloop()


def get_resource_path(relative_path):
    """获取资源文件的正确路径（支持打包后的exe）"""
    try:
        # PyInstaller会创建临时文件夹并存储路径在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境下使用当前目录
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    """主函数"""
    # 检查题库文件是否存在（使用资源路径）
    required_files = ['single_choice.json', 'multiple_choice.json', 'judgment.json']
    missing_files = []

    for filename in required_files:
        file_path = get_resource_path(filename)
        if not os.path.exists(file_path):
            missing_files.append(filename)

    if missing_files:
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        messagebox.showerror("错误", f"缺少题库文件: {', '.join(missing_files)}")
        return

    # 创建并运行GUI应用
    app = ExamSystemGUI()
    app.run()


if __name__ == "__main__":
    main()