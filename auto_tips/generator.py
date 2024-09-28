# 生成题目和答案
import re
import random
import operator
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


# 将表达式转换为 Fraction 对象的函数
def problem_eval(expression):
    # 匹配分数或整数
    elements = []
    pattern = r'\d+/\d+|\d+'  # 匹配分数或整数
    elements.append(re.findall(pattern, expression))
    
    # 解析运算符
    operators = re.findall(r'\s[*/+-]\s', expression)  # 匹配运算符
    # print(operators)
    # 将匹配的数字或分数转换为 Fraction 对象
    fractions = [Fraction(e) for e in elements[0]]
    # print(fractions)
    
    # 使用两个栈来处理运算符优先级
    values = []
    ops = []

    for i in range(len(fractions)):
        values.append(fractions[i])
        
        if i < len(operators):
            op = operators[i].strip()
            while (ops and precedence(op) <= precedence(ops[-1])):
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

    return values[0]


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


def generate_problem(r):
    # 确保不产生负数和符合真分数要求
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    # 随机生成运算符个数（1到3个）
    num_operators = random.randint(1, 3)
    terms = []

    for _ in range(num_operators + 1):  # 生成操作数
        if random.choice([True, False]):  # 50%概率选择自然数
            term = random.randint(1, r)
        else:  # 50%概率选择分数
            numerator = random.randint(1, r)
            denominator = random.randint(1, r) + 1  # 确保分母不为0
            term = Fraction(numerator, denominator)
        terms.append(term)

    # 随机选择运算符
    expression = str(terms[0])
    for i in range(num_operators):
        op = random.choice(list(operators.keys()))
        expression += f" {op} {terms[i + 1]}"

    # 计算结果
    try:
        result = problem_eval(expression) 
    except ZeroDivisionError:
        return generate_problem(r)  # 重新生成题目以避免除以零

    # 检查结果
    if result < 0 or (result.denominator != 1 and result.numerator < 0):
        return generate_problem(r)  # 重新生成题目以避免负数

    # 格式化结果为真分数形式
    formatted_result = format_fraction(result)
    expression = expression.replace('*', '×')
    if re.search(r'\s/\s', expression):
        expression = re.sub(r'\s/\s', ' ÷ ', expression)

    return expression, formatted_result


def generate_problems_and_answers(n, r):
    problems = []
    answers = []
    for _ in range(n):
        problem, answer = generate_problem(r)
        problems.append(problem)
        answers.append(answer)
    with open('Exercises.txt', 'w', encoding='utf-8') as f:
        for i, problem in enumerate(problems, 1):
            f.write(f"{i}. {problem}\n")
    with open('Answers.txt', 'w', encoding='utf-8') as f:
        for i, answer in enumerate(answers, 1):
            f.write(f"{i}. {answer}\n")
