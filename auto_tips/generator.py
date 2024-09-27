# 生成题目和答案
import random
import operator


def generate_problem(r):
    # 确保不产生负数和符合真分数要求
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }
    
    while True:
        a = random.randint(1, r)
        b = random.randint(1, r)
        op = random.choice(list(operators.keys()))
        
        if op == '/' and b == 0:
            continue
        
        result = operators[op](a, b)
        
        if op == '-' and result < 0:
            continue
        if op == '/' and not result.is_integer():
            continue
        
        problem = f"{a} {op} {b}"
        answer = str(int(result))
        return problem, answer

def generate_problems_and_answers(n, r):
    problems = []
    answers = []
    for _ in range(n):
        problem, answer = generate_problem(r)
        problems.append(problem)
        answers.append(answer)
    with open('Exercises.txt', 'w') as f:
        for i, problem in enumerate(problems, 1):
            f.write(f"{i}. {problem}\n")
    with open('Answers.txt', 'w') as f:
        for i, answer in enumerate(answers, 1):
            f.write(f"{i}. {answer}\n")
