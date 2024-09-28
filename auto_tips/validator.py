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
        if '/' in exercise:
            correct_answer = calculate_answer_2(exercise)
        else:
            correct_answer = calculate_answer_1(exercise)

        if correct_answer == answer.strip().split('. ')[1]:
            correct.append(i)
        else:
            wrong.append(i)

    with open('Grade.txt', 'w', encoding='utf-8') as f:
        f.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        f.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")


def calculate_answer_1(exercise):
    exercise = exercise.strip().split('. ')[1]  # 移除题号
    numbers = re.findall(r'\d+', exercise)
    operator = re.findall(r'[+\-*]', exercise)[0]

    a = int(numbers[0])
    b = int(numbers[1])

    if operator == '+':
        return str(format_fraction(a + b))
    elif operator == '-':
        return str(format_fraction(a - b))
    elif operator == '*':
        return str(format_fraction(a * b))


def calculate_answer_2(exercise):
    # 计算题目的正确答案
    exercise = exercise.strip().split('. ')[1]  # 移除题号
    exercise = re.sub(r'÷', '/', exercise)  # 替换运算符为Python可识别的形式
    exercise = re.sub(r'×', '*', exercise)

    # 匹配分数或整数
    elements = re.findall(r'\d+/\d+|\d+', exercise)  # 匹配分数或整数
    operators = re.findall(r'\s[/*+-]\s', exercise)  # 匹配运算符

    # 将匹配的数字或分数转换为 Fraction 对象
    fractions = [Fraction(e) for e in elements]

    # 依次处理运算符
    result = fractions[0]
    for i, operator in enumerate(operators):
        if operator == '+':
            result += fractions[i + 1]
        elif operator == '-':
            result -= fractions[i + 1]
        elif operator == '*':
            result *= fractions[i + 1]
        elif operator == '/':
            result /= fractions[i + 1]

    return str(format_fraction(result))  # 返回格式化后的结果
