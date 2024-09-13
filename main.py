import difflib

# 1 针对语料路径进行配置
path = "../CheckRepeat/database/OrigCorpus/datas.txt"  # 训练语料库
flagpath = "../CheckRepeat/database/OrigCorpus/flagdatas.txt"  # 语料标记

# 2 对原始语料进行标记和简单清洗
listset = ""  # 标记后的语料集合
i, j = 1, 1
with open(path, 'r', encoding='utf-8') as f:
    for rline in f.readlines():
        line = rline.strip().replace(" ", "")
        if "summary" in line:
            listset += "\n" + str(i) + "_" + line
            i += 1  # 简介打标签
        elif "subject" not in line:
            listset += line
        elif "subject" in line:
            listset += "\n" + str(j) + "_" + line
            j += 1  # 项目题目打标签

# 3 保存标记后语料并统计标记结果
with open(flagpath, 'w', encoding='utf-8') as f1:
    f1.write(listset.strip())
print("=" * 70)
print("项目共计标题:" + str(len(listset.split("subject")) - 1))
print("项目共计简介:" + str(len(listset.split("summary")) - 1))
print("-" * 70)
# 4 对标记数据进行分词处理
cutpath = "../CheckRepeat/database/OrigCorpus/cutdatas.txt"  # 保存分词后的结果
cutword(flagpath, cutpath)


def checkfun(namestr):
    subject = {}  # 记录查重结果，键值对，原句+重复率
    summary = {}
    # 1 找到对比库的历史数据
    checkpath = "../CheckRepeat/database/OrigCorpus/cutdatas.txt"  # 数据库中对比项目语料库
    with open(checkpath, "r", encoding="utf-8") as f:
        checklist = [line[:] for line in f.readlines()]
    subjectname = [sub for sub in checklist if "subject" in sub]  # 项目名称
    summaryname = [summ for summ in checklist if "summary" in summ]  # 项目简介

    if "subject" in namestr:
        # 2 进行项目名称验证操作
        for rline in subjectname:
            line = ''.join(str(rline).split(' ')[2:])
            subp = difflib.SequenceMatcher(None, namestr.split('\n')[0].replace('subject', ''), line).ratio()
            subject[line] = float('%.4f' % (subp))
    if "summary" in namestr:
        # 3 进行项目简介验证操作
        for rline in summaryname:
            line = ''.join(str(rline).split(' ')[2:])
            sump = difflib.SequenceMatcher(None, namestr.split('\n')[1].replace('summary', ''), line).ratio()
            summary[line] = float('%.4f' % (sump))

    # 4 打印检测结果
    outreslut = ""
    sort1 = sorted(subject.items(), key=lambda e: e[1], reverse=True)  # 排序
    outreslut += "项目名称：" + "*" * 5 + "[" + namestr.split('\n')[0].replace('subject', '') + "]" + "*" * 5 + "的查重结果如下:\n\n"
    for item in sort1[:1]:
        if item[1] >= 0.5:
            outreslut += ("与项目库中\t[<span style=\"color:red\">" + item[0].replace("\n", '') +
                          "</span>]\t的相似率最高：<span style=\"color:red\">" + str(item[1]) + "</span>\n")
        else:
            outreslut += "<span style=\"color:green\">没有查出重复的项目简介</span>\n"

    sort2 = sorted(summary.items(), key=lambda e: e[1], reverse=True)  # 排序
    outreslut += "\n\n项目简介：" + "*" * 5 + "[" + namestr.split('\n')[1].replace('summary', '') + "]" + "*" * 5 + "的查重结果如下：\n\n"
    for item in sort2[:1]:
        if item[1] >= 0.5:
            outreslut += ("与项目库中\t[<span style=\"color:red\">" + item[0].replace("\n", '') +
                          "</span>]\t的相似率最高：<span style=\"color:red\">" + str(item[1]) + "</span>\n")
        else:
            outreslut += "<span style=\"color:green\">没有查出重复的项目简介</span>\n"

    # 5 写到文件里面
    with open("../CheckRepeat/database/DealCorpus/checkout.txt", 'w', encoding='utf-8') as f:
        f.write(outreslut)
    print(outreslut)
