#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI考试系统 - Web版本
使用Flask创建Web界面，支持手机浏览器访问
"""

from flask import Flask, render_template, request, jsonify, session
import json
import random
import os

app = Flask(__name__)
app.secret_key = 'ai_exam_system_2024'  # 用于session管理

class WebExamSystem:
    def __init__(self):
        self.questions = {
            'single_choice': [],
            'multiple_choice': [],
            'judgment': []
        }
        self.load_questions()

    def load_questions(self):
        """加载题库文件"""
        try:
            # 加载单选题
            with open('single_choice.json', 'r', encoding='utf-8') as f:
                self.questions['single_choice'] = json.load(f)

            # 加载多选题
            with open('multiple_choice.json', 'r', encoding='utf-8') as f:
                self.questions['multiple_choice'] = json.load(f)

            # 加载判断题
            with open('judgment.json', 'r', encoding='utf-8') as f:
                self.questions['judgment'] = json.load(f)

            return True
        except Exception as e:
            print(f"加载题库失败: {e}")
            return False

    def get_random_question(self):
        """随机获取一道题目"""
        question_types = ['single_choice', 'multiple_choice', 'judgment']
        question_type = random.choice(question_types)

        questions = self.questions[question_type]
        if not questions:
            return None, None

        question = random.choice(questions)
        return question_type, question

    def check_answer(self, question_type, user_answer, correct_answer):
        """检查答案是否正确"""
        user_answer = user_answer.upper().strip()
        correct_answer = correct_answer.upper().strip()

        if question_type == 'multiple_choice':
            # 多选题需要所有选项都正确
            user_set = set(user_answer.replace(' ', ''))
            correct_set = set(correct_answer.replace(' ', ''))
            return user_set == correct_set
        else:
            return user_answer == correct_answer

# 创建全局考试系统实例
exam_system = WebExamSystem()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/start_exam', methods=['POST'])
def start_exam():
    """开始考试"""
    session['total_questions'] = 0
    session['correct_answers'] = 0
    session['answered_questions'] = 0
    return jsonify({'status': 'success', 'message': '考试开始！'})

@app.route('/get_question', methods=['GET'])
def get_question():
    """获取下一题"""
    question_type, question = exam_system.get_random_question()

    if not question:
        return jsonify({'status': 'error', 'message': '没有可用的题目'})

    # 增加题目计数
    session['total_questions'] = session.get('total_questions', 0) + 1

    # 准备选项数据
    options = []
    if question_type == 'single_choice':
        options = [
            {'value': 'A', 'text': question['Unnamed: 2']},
            {'value': 'B', 'text': question['Unnamed: 3']},
            {'value': 'C', 'text': question['Unnamed: 4']},
            {'value': 'D', 'text': question['Unnamed: 5']}
        ]
    elif question_type == 'multiple_choice':
        options = [
            {'value': 'A', 'text': question['Unnamed: 2']},
            {'value': 'B', 'text': question['Unnamed: 3']},
            {'value': 'C', 'text': question['Unnamed: 4']},
            {'value': 'D', 'text': question['Unnamed: 5']},
            {'value': 'E', 'text': question['Unnamed: 6']}
        ]
    elif question_type == 'judgment':
        options = [
            {'value': 'A', 'text': '正确'},
            {'value': 'B', 'text': '错误'}
        ]

    # 保存当前题目到session
    session['current_question'] = question
    session['current_question_type'] = question_type

    return jsonify({
        'status': 'success',
        'question_type': question_type,
        'question_text': question['Unnamed: 1'],
        'options': options,
        'question_number': session['total_questions'],
        'correct_answer': question['Unnamed: 7']  # 暂时返回，实际应该隐藏
    })

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """提交答案"""
    user_answer = request.json.get('answer', '')

    if not user_answer:
        return jsonify({'status': 'error', 'message': '请先选择答案'})

    current_question = session.get('current_question')
    current_question_type = session.get('current_question_type')

    if not current_question:
        return jsonify({'status': 'error', 'message': '没有当前题目'})

    correct_answer = current_question['Unnamed: 7']
    is_correct = exam_system.check_answer(current_question_type, user_answer, correct_answer)

    # 更新统计
    session['answered_questions'] = session.get('answered_questions', 0) + 1
    if is_correct:
        session['correct_answers'] = session.get('correct_answers', 0) + 1

    # 计算正确率
    accuracy = (session['correct_answers'] / session['answered_questions']) * 100 if session['answered_questions'] > 0 else 0

    return jsonify({
        'status': 'success',
        'is_correct': is_correct,
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'total_questions': session['total_questions'],
        'correct_answers': session['correct_answers'],
        'answered_questions': session['answered_questions'],
        'accuracy': round(accuracy, 1)
    })

@app.route('/get_stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    answered_questions = session.get('answered_questions', 0)
    accuracy = (session.get('correct_answers', 0) / answered_questions) * 100 if answered_questions > 0 else 0

    return jsonify({
        'total_questions': session.get('total_questions', 0),
        'correct_answers': session.get('correct_answers', 0),
        'answered_questions': answered_questions,
        'accuracy': round(accuracy, 1)
    })

if __name__ == '__main__':
    print("🚀 AI考试系统Web版本启动中...")
    print("📱 支持手机浏览器访问")
    print("🌐 访问地址: http://localhost:5000")
    print("📶 手机访问: http://[电脑IP]:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)