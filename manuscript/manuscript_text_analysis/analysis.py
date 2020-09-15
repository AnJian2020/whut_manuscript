from enum import Enum
from multiprocessing import Process
import jieba
reviewStatus=Enum("reviewStatus",('preliminary','external_audit','review','final_judgment'))
print(reviewStatus.review)
for name, member in reviewStatus.__members__.items():
    print(name, '=>', member, ',', member.value)

# class Analysis(object):
#
#     def __init__(self,text=None):
#         self._text=text
#
#     def participle(self):
#         return ' '.join(jieba.cut(self._text))
#
#     def analysis(self):
#         textParticipe=self.participle()
#         print(textParticipe)
#
#
# if __name__=="__main__":
#     text="随着互联网的迅速发展,大数据时代的来临,数据挖掘在从海量数据中探查潜在的价值信息起到了重要的作用,成为当下热" \
#          "门的研究和实践方向之一。python作为数据挖掘领域中较为热门的程序语言,其丰富的技术库和强大的科学计算能力成为数据挖" \
#          "掘过程中不可或缺的工具。本次研究主要是基于python语言对智联招聘网的数据进行数据挖掘分析和建模,进而得出招聘信息薪资" \
#          "待遇预测分类模型。本次研究主要分为如下步骤:数据源选择、数据采集、数据存储、数据预处理、数据建模和模型评估,通过算法构" \
#          "建了近邻和决策树两种分类模型,其次对两种模型的混淆矩阵数据进行计算,比较模型的预测准确率,最终得出准确率较高的数据模型。" \
#          "本次研究所得的分类模型,可以帮助被招聘者在浏览网站招聘信息时预测薪资待遇水平,有效的评估招聘内容是否合适,以及对招聘岗位提" \
#          "供的薪资待遇是否感到满意,进而有效的提高求职者在寻求招聘岗位时的效率。同时,该模型对于企业优化招聘信息也起到反馈性作用。"
#     Analysis(text).analysis()
