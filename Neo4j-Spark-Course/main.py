#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask

from ModelProcess import *
from neo4j import Neo4j


def load_course_name_dict(course_name_dict_path):
    """
    将课程名字添加至自定义字典中
    :param course_name_dict_path: 存放课程名字文件的路径
    :return: None
    """
    for line in helper.read_file(course_name_dict_path):
        CustomDictionary.insert(line, 'cn 99999999')


def main():
    """读取课程名字对应的词典"""
    load_course_name_dict(course_dict_dir_path)
    """初始化一个模型,初始化之后可以直接调用question进行查询"""
    query_process = ModelProcess()
    neo4j = Neo4j()

    app = Flask(__name__)

    @app.route('/query/<question>')
    def query(question):
        """分词问题question,返回模型的下标,以及对应的问题模板"""
        index, pattern = query_process.analysis_query(question)
        if index == 0:
            # 需要课程的详细信息
            result = neo4j.get_course_details(pattern[0])
            if result is None:
                print("没有要查询的课程")
                return "没有要查询的课程"
            else:
                return pattern[0] + "的详细信息为:" + result
        elif index == 1:
            # 需要课程的先修课程
            result = neo4j.get_course_adv(pattern[0])
            if result is None:
                return "没有要查询的课程"
            elif len(result) == 0:
                return "查询的课程没有先修课程"
            else:
                result_str = ""
                for i in result.keys():
                    result_str += i+', '
                return "" + pattern[0] + "的先修课程为" + result_str
        else:
            result = ""
            for i in pattern:
                result += i + " "
            return result

    app.run()


if __name__ == '__main__':
    main()