import os
import re
import sys
import jieba
import cProfile
import test_module

from os import path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def preprocess_text(text):
    # 使用结巴分词对文本进行分词
    words = jieba.cut(text)
    return ' '.join(words)


def calculate_similarity(orig_text, plag_text):
    # 处理文本
    orig_text = preprocess_text(orig_text)
    plag_text = preprocess_text(plag_text)

    # 使用TF-IDF向量化
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([orig_text, plag_text])

    # 计算余弦相似度
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim[0][0]


def save_file_to_folder(folder, duplicate_rate, plag_file_path):
    # 被检测文件
    plag_files = re.search(r'/([^/]+)$', plag_file_path).group(1)

    # 创建文件夹（如果不存在）
    folder0 = re.search(r'^(.+)/([^/]+)$', folder).group(1)
    folder1 = re.search(r'/([^/]+)$', folder).group(1)
    if not path.exists(folder0):
        os.makedirs(folder0)
        path.join(folder0, folder1)
    elif not path.exists(folder1):
        filepath = folder
        # 打开文件并写入内容
        with open(filepath, 'a', encoding='utf-8') as file:
            file.write(f"{plag_files}的重复率为: {duplicate_rate:.2f}%\n")


def main(orig_file_path, plag_file_path, output_file_path):
    orig_text = read_file(orig_file_path)
    plag_text = read_file(plag_file_path)

    similarity = calculate_similarity(orig_text, plag_text)
    duplicate_rate = similarity * 100  # 转换为百分比

    save_file_to_folder(output_file_path, duplicate_rate, plag_file_path)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python main.py <原文文件路径> <抄袭文件路径> <输出文件路径>")
# python main.py ./text_dataset/orig.txt ./text_dataset/orig_0.8_add.txt ./text_dataset/output_file.txt
        sys.exit(1)

    orig_file = sys.argv[1]
    plag_file = sys.argv[2]
    output_file = sys.argv[3]

    main(orig_file, plag_file, output_file)

cProfile.run('calculate_similarity(orig_file, plag_file)')
