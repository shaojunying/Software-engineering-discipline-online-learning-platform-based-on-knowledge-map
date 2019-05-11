import jieba
import numpy as np
from jieba import posseg
from pyhanlp import *
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from sklearn.naive_bayes import GaussianNB

from helper import *
from data_setting import *


class ModelProcess:

    def __init__(self):
        self.segment = HanLP.newSegment()
        jieba.load_userdict(course_dict_dir_path)
        # 将句子中的关键词虚拟化时存储代词与原词的对应关系
        self.abstract_map = {}
        # 存储停用词
        self.stopwords = []
        # 问题模板，记录每个下标对应问题模板
        self.questions_pattern = self.load_questions_pattern()
        # 词典，存储每个特征词对应的下标
        self.vocabulary = self.load_vocabulary()
        # 模型,训练之后可直接用于预测
        self.model = self.load_classifier_model()

    def load_questions_pattern(self):
        """
        加载问题模板 == 分类器标签
        从文件中读取所有问题模板，存入字典中
        :return:
        """
        questions_pattern = {}
        for line in helper.read_file(question_classification_dir_path):
            tokens = line.split(':')
            index, pattern = tokens[0], tokens[1]
            questions_pattern[int(index)] = pattern
        return questions_pattern

    def save_vocabulary_to_file(self):
        """
        将详细问题的各个问题进行分词,将所有词都存入文件中,作为词典
        :return: None
        """
        # 读取所有无意义词
        self.load_stop_words()
        train_list = []
        with open(vocabulary_dir_path, 'a', encoding='utf-8') as f:
            for file in os.listdir(detailed_questions_dir_path):
                file_path = os.path.join(detailed_questions_dir_path, file)
                if os.path.isdir(file_path):
                    continue
                for line in helper.read_file(file_path):
                    terms = posseg.cut(line)
                    for term in terms:
                        if term.word in train_list or term.word in self.stopwords:
                            continue
                        train_list.append(term.word)
                        f.write(term.word + '\n')

    def load_vocabulary(self):
        """prin
        加载词汇表 == 关键特征 == 与HanLP分词后的单词进行匹配
        从文件中读取词汇表，存入字典中
        :return:
        """
        vocabulary = {}
        if os.path.getsize(vocabulary_dir_path) == 0:
            self.save_vocabulary_to_file()

        index = 0
        for line in helper.read_file(vocabulary_dir_path):
            vocabulary[line] = index
            index += 1
        return vocabulary

    def sentence_to_array(self, line):
        """
        将句子分词成数组
        :param line: 要被分割的句子
        :return: 生成的数组
        """
        vector = [0] * len(self.vocabulary)
        terms = self.segment.seg(line)
        for term in terms:
            word = term.word
            if word in self.vocabulary:
                index = self.vocabulary[word]
                vector[index] = 1
        return vector

    def load_classifier_model(self):
        """
        对特定的模板进行加载并分类
        :return:
        """
        model = GaussianNB()
        # 生成训练集
        train_list = []
        data = np.array([])
        target = np.array([])
        for file in os.listdir(detailed_questions_dir_path):
            file_path = os.path.join(detailed_questions_dir_path, file)
            if os.path.isdir(file_path):
                continue
            for line in helper.read_file(file_path):
                index = file_path.split('】')[0].split('【')[1]
                array = self.sentence_to_array(line.strip())
                if len(data) == 0:
                    data = np.array(np.array([array]))
                    target = np.array(int(index))
                else:
                    data = np.append(data, np.array([array]), axis=0)
                    target = np.append(target, np.array([int(index)]))
                train_one = LabeledPoint(float(index), Vectors.dense(array))
                train_list.append(train_one)
        model.fit(data, target)
        return model

    def analysis_query(self, question):
        """
        分析句子
        :param question:
        :return:
        """
        print("原始句子:", question)

        """
        利用HanLp分词.将关键词进行词性抽象
        """
        ab_str = self.query_abstract(question)
        print("替换关键词之后:", ab_str)

        """
        将抽象的句子与spark训练集中的模板进行匹配,得到句子对应的模板
        """
        index, str_pattern = self.query_classify(ab_str)
        print("句子套用对应的问题模板后:", str_pattern)

        """
        将模板还原成句子
        """
        final_pattern = self.query_extension(str_pattern)
        print("原始句子替换成系统可识别的结果:", final_pattern)

        final_pattern_array = final_pattern.split(' ')
        return index, final_pattern_array

    def query_abstract(self, question):
        """
        将句子抽象化
        算法分析与设计的学分 --> co 的 学分
        :param question:
        :return: 句子中抽象化之后的结果
        """
        terms = posseg.cut(question)
        # 用来存储问题抽象之后的结果
        abstract_query = ""

        for term in terms:
            word = term.word
            print(term.word, term.flag)
            term_str = str(term)
            if term.flag == 'cn':
                abstract_query += "cn "
                self.abstract_map['cn'] = word
            else:
                abstract_query += word + " "
        return abstract_query

    def query_classify(self, ab_str):
        """
        将虚拟化之后的句子根据词典转化成向量,向量中保存词典中每个词在句子中是否出现.
        将向量带入模型中进行预测,得到目标的问题模板
        :param ab_str:虚拟化之后的句子
        :return:问题模型的下标,问题模板
        """
        # 将抽象化后的句子转化为数组
        test_array = self.sentence_to_array(ab_str)

        """
        对数据进行预测
        句子模板在Spark贝叶斯分类器中的索引[位置]
        根据词汇使用频率判断句子对应哪一个模板
        """
        index = self.model.predict([test_array])
        model_index = int(index)
        print("模型的下标是:", model_index)
        return model_index, self.questions_pattern[model_index]

    def query_extension(self, str_pattern):
        """
        将问题模板与虚拟化的词典对应的词进行替换,将模板中的代词换成原始的名词
        :param str_pattern:问题模板
        :return:模板中代词替换回名词得到的结果
        """
        for key in self.abstract_map:
            if key in str_pattern:
                value = self.abstract_map[key]
                str_pattern = str_pattern.replace(key, value)
        self.abstract_map.clear()
        return str_pattern

    def load_stop_words(self):
        for word in helper.read_file(stop_words_dir_path):
            self.stopwords.append(word)


def main():
    """初始化一个模型,初始化之后可以直接调用question进行查询"""
    query_process = ModelProcess()
    query_process.analysis_query("离散数学好学吗")


if __name__ == '__main__':
    main()
