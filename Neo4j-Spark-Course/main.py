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

    @app.route('/')
    def index():
        return "index"

    @app.route('/query/<question>')
    def query(question):
        print(question)
        """分词问题question,返回模型的下标,以及对应的问题模板"""
        index, pattern = query_process.analysis_query(question)
        print(index, pattern)
        # if index == 0:
        if True:
            # 需要课程的详细信息
            print("获取之前")
            result = neo4j.get_course_details(pattern[0])
            print("获取之后")
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
                    result_str += i + ', '
                return "" + pattern[0] + "的先修课程为" + result_str
        elif index == 2:
            # 需要课程的开课学期
            result = neo4j.get_course_semester(pattern[0])
            if result is None:
                return "没有要查询的课程"
            else:
                return "" + pattern[0] + "的开课学期为" + result
        elif index == 3:
            # 需要课程的必修选修
            result = neo4j.get_course_optional(pattern[0])
            if result is None:
                return "没有要查询的课程"
            else:
                return "" + pattern[0] + "为" + ("选修" if result == 'y' else "必修")
        elif index == 4:
            # 需要课程的学分
            result = neo4j.get_course_credit(pattern[0])
            if result is None:
                return "没有要查询的课程"
            else:
                return "" + pattern[0] + "的学分为" + result
        elif index == 5:
            # 需要课程的学时
            result = neo4j.get_course_credit_hour(pattern[0])
            if result is None:
                return "没有要查询的课程"
            else:
                return "" + pattern[0] + "的学时为" + result
        elif index == 6:
            # 需要课程的课程编号
            result = neo4j.get_course_id(pattern[0])
            if result is None:
                return "没有要查询的课程"
            else:
                return "" + pattern[0] + "的课程编号为" + result
        elif index == 7:
            # 需要课程的英文名称
            result = neo4j.get_course_english_name(pattern[0])
            if result is None:
                return "没有要查询的课程"
            else:
                return "" + pattern[0] + "的英文名称为" + result
        elif index == 8:
            pass
        elif index == 9:
            # 需要课程的老师姓名
            result = neo4j.get_course_teacher(pattern[0])
            if result is None:
                return "没有要查询的课程"
            else:
                return "" + pattern[0] + "的老师姓名为" + result
        elif index == 10:
            pass
        elif index == 11:
            pass
        elif index == 12:
            pass
        else:
            result = ""
            for i in pattern:
                result += i + " "
            return result

    app.run()


if __name__ == '__main__':
    main()
