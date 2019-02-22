from .ModelProcess import *


def main():
    question = "算法分析与设计是谁教的"
    query_process = ModelProcess()

    """
    Todo:此处需要给添加自定义词典
    （课程名，知识点，老师名字。。。）
    """

    model_index, _ = query_process.analysis_query(question)
