# validator.py
import re

def validate_answers(exercise_file, answer_file):
    with open(exercise_file, 'r') as ef, open(answer_file, 'r') as af:
        exercises = ef.readlines()
        answers = af.readlines()

    correct = []
    wrong = []
    for i, (exercise, answer) in enumerate(zip(exercises, answers), 1):
        correct_answer = calculate_answer(exercise)
        if correct_answer == answer.strip().split('. ')[1]:
            correct.append(i)
        else:
            wrong.append(i)

    with open('Grade.txt', 'w') as f:
        f.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        f.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")


def calculate_answer(exercise):
    # 计算题目的正确答案
    exercise = exercise.strip().split('. ')[1]  # 移除题号
    numbers = re.findall(r'\d+', exercise)
    operator = re.findall(r'[+\-*/]', exercise)[0]
    
    a = int(numbers[0])
    b = int(numbers[1])
    
    if operator == '+':
        return str(a + b)
    elif operator == '-':
        return str(a - b)
    elif operator == '*':
        return str(a * b)
    elif operator == '/':
        return str(a // b)  # 使用整数除法
