# 测试正误
import re
from fractions import Fraction


def format_fraction(frac):
    """将分数格式化为真分数形式"""
    if frac.denominator == 1:
        return str(frac.numerator)  # 如果是整数，直接返回
    whole = frac.numerator // frac.denominator
    remainder = frac.numerator % frac.denominator
    if whole > 0:
        return f"{whole}'{remainder}/{frac.denominator}"  # 返回真分数形式
    return f"{remainder}/{frac.denominator}"  # 返回分数形式


def validate_answers(exercise_file, answer_file):
    with open(exercise_file, 'r+', encoding='utf-8') as ef, open(answer_file, 'r+', encoding='utf-8') as af:
        exercises = ef.readlines()
        answers = af.readlines()

    correct = []
    wrong = []
    for i, (exercise, answer) in enumerate(zip(exercises, answers), 1):
        exercise = re.sub(r'÷', '/', exercise)  # 将除号替换为Python可识别的除号
        exercise = re.sub(r'×', '*', exercise)
        correct_answer = format_fraction(calculate_answer(exercise))

        if correct_answer == answer.strip().split('. ')[1]:
            correct.append(i)
        else:
            wrong.append(i)

    with open('Grade.txt', 'w', encoding='utf-8') as f:
        f.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        f.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")


def calculate_answer(exercise):
    exercise = exercise.strip().split('. ')[1]  # 移除题号

    # 匹配分数或整数
    elements = re.findall(r'\d+/\d+|\d+', exercise)  # 匹配分数或整数
    operators = re.findall(r'\s[+\-*/]\s', exercise)  # 匹配运算符

    # 将匹配的数字或分数转换为 Fraction 对象
    fractions = [Fraction(e) for e in elements]

    # 使用两个栈来处理运算符优先级
    values = []
    ops = []

    for i in range(len(fractions)):
        values.append(fractions[i])

        if i < len(operators):
            op = operators[i].strip()
            while ops and precedence(op) <= precedence(ops[-1]):
                # if len(values) < 2:  # 确保有足够的值进行运算
                #     break
                right = values.pop()
                left = values.pop()
                operator = ops.pop()
                values.append(apply_operator(left, right, operator))
            ops.append(op)

    # 处理剩余的运算符
    while ops:
        right = values.pop()
        left = values.pop()
        operator = ops.pop()
        values.append(apply_operator(left, right, operator))

    return values[0]  # 返回格式化后的结果


def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def apply_operator(left, right, operator):
    if operator == '+':
        return left + right
    elif operator == '-':
        return left - right
    elif operator == '*':
        return left * right
    elif operator == '/':
        return left / right
