from pyhanlp import *
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint

from helper import *
from setting import *


class ModelProcess:

    def __init__(self):
        # 问题模板，记录每个下标对应问题模板
        self.questions_pattern = self.load_vocabulary()
        # 词典，存储每个特征词对应的下标
        self.vocabulary = self.load_vocabulary()
        self.nb_model = self.load_classifier_model()
        self.abstract_map = {}

    def load_questions_pattern(self):
        """
        加载问题模板 == 分类器标签
        从文件中读取所有问题模板，存入字典中
        :return:
        """
        questions_pattern = {}
        path = os.path.join(root_dir_path, 'question\\question_classification.txt')
        for line in helper.read_file(path):
            tokens = line.split(':')
            index, pattern = tokens[0], tokens[1]
            questions_pattern[int(index)] = pattern
        return questions_pattern

    def load_vocabulary(self):
        """
        加载词汇表 == 关键特征 == 与HanLP分词后的单词进行匹配
        从文件中读取词汇表，存入字典中
        :return:
        """
        vocabulary = {}
        path = os.path.join(root_dir_path, 'question\\vocabulary.txt')
        for line in helper.read_file(path):
            tokens = line.split(':')
            index, word = tokens[0], tokens[1]
            vocabulary[word] = int(index)
        return vocabulary

    def sentence_to_array(self, line):
        vector = [0] * len(self.vocabulary)
        terms = HanLP.segment(line)
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
        conf = SparkConf().setAppName("NaiveBayesTest").setMaster('local[*]')
        sc = SparkContext.getOrCreate(conf)

        """
        生成训练集
        """
        train_list = []

        path = os.path.join(root_dir_path, 'question\\detailed_questions')
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                continue
            for line in helper.read_file(file_path):
                index = file_path.split('】')[0].split('【')[1]
                array = self.sentence_to_array(line)
                train_one = LabeledPoint(float(index), Vectors.dense(array))
                train_list.append(train_one)
        print(train_list)
        trainingRDD = sc.parallelize(train_list)
        nb_model = NaiveBayes.train(trainingRDD)
        sc.stop()
        return nb_model

    def analysis_query(self, question):
        """
        分析句子
        :param question:
        :return:
        """
        print("原始句子:", question)
        print("========HanLP开始分词========")

        """
        利用HanLp分词.将关键词进行词性抽象
        """
        ab_str = self.queryAbstract(question)
        print("句子抽象化的结果:", ab_str)

        """
        将抽象的句子与spark训练集中的模板进行匹配,得到句子对应的模板
        """
        index, str_pattern = self.queryClassify(ab_str)
        print("句子套用模板之后的结果:", str_pattern)

        """
        将模板还原成句子
        """
        final_pattern = self.query_extension(str_pattern)
        print("原始句子替换成系统可识别的结果:", final_pattern)

        final_pattern_array = final_pattern.split(' ')
        return index, final_pattern_array

    def queryAbstract(self, question):
        """
        将句子抽象化
        算法分析与设计的学分 --> co 的 学分
        :param question:
        :return: 句子中抽象化之后的结果
        """
        terms = HanLP.segment(question)
        abstract_query = ""

        """
        此处需要加对于不同词性的词做不同的处理
        """

        print("========HanLP分词结束========")
        return abstract_query

    def queryClassify(self, ab_str):

        # 将抽象化后的句子转化为数组
        test_array = self.sentence_to_array(ab_str)
        vector = Vectors.dense(test_array)

        """
        对数据进行预测
        句子模板在Spark贝叶斯分类器中的索引[位置]
        根据词汇使用频率判断句子对应哪一个模板
        """
        index = self.nb_model.predict(vector)
        model_index = int(index)
        print("模型的下标是:", model_index)
        return model_index, self.questions_pattern[model_index]

    def query_extension(self, str_pattern):
        for key in self.abstract_map:
            if key in str_pattern:
                value = self.abstract_map[key]
                str_pattern = str_pattern.replace(key,value)
        self.abstract_map.clear()
        return str_pattern


ModelProcess()
