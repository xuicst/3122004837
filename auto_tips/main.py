import argparse
from generator import generate_problems_and_answers
from validator import validate_answers


def main():
    parser = argparse.ArgumentParser(description="自动生成小学四则运算题目")
    parser.add_argument('-n', type=int, help='生成题目的个数')
    parser.add_argument('-r', type=int, help='题目中数值的范围')
    parser.add_argument('-e', type=str, help='题目文件')
    parser.add_argument('-a', type=str, help='答案文件')
    args = parser.parse_args()

    if args.n and args.r:
        generate_problems_and_answers(args.n, args.r)
    elif args.e and args.a:
        validate_answers(args.e, args.a)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
