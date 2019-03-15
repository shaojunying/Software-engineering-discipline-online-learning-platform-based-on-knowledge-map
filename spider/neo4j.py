# -*- coding: utf-8 -*-
from py2neo import *
from xml.dom import minidom as minidom
from setting import *
import py2neo


def get_xml_text_node_value(node, name):
    """
    获取xml中文本节点的值
    :param name:
    :param node: 一个xml.dom.minidom类型的节点
    :return: node中的text值
    """
    return node.getElementsByTagName(name)[0].childNodes[0].data


def get_all_sub_element_node(node):
    """
    获取node的所有子元素(非文本)
    :param node:
    :return:
    """
    for sub_node in node.childNodes:
        if sub_node.nodeType == minidom.Node.TEXT_NODE:
            continue
        yield sub_node


def save_all_course_info():
    """
    将所有课程信息保存进neo4j中
    :return:
    """
    dom = minidom.parse("data.xml")
    root = dom.documentElement
    # 获得所有课程节点的父节点
    courses_nodes = root.getElementsByTagName('courses')
    courses = []
    graph = Graph(neo4j_url, password=neo4j_password)
    graph.delete_all()
    # 创建所有课程节点
    for course_node in get_all_sub_element_node(courses_nodes[0]):
        # 获取课程名字
        course = {
            'name': get_xml_text_node_value(course_node, 'name'),
            'details': get_xml_text_node_value(course_node, 'details'),
            'id': get_xml_text_node_value(course_node, 'id'),
            'english_name': get_xml_text_node_value(course_node, 'english_name'),
            'credit': get_xml_text_node_value(course_node, 'credit'),
            'credit_hour': get_xml_text_node_value(course_node, 'credit_hour'),
            'optional': get_xml_text_node_value(course_node, 'optional'),
            'semester': get_xml_text_node_value(course_node, 'semester'),
        }

        # 判断教室节点是否存在,不存在需要创建
        teacher_name = get_xml_text_node_value(course_node, 'teacher')
        matcher = NodeMatcher(graph)
        teacher_node = matcher.match('Teacher', name=teacher_name).first()
        if not teacher_node:
            teacher_node = Node('Teacher')
            teacher_node.update({'name': teacher_name})
            graph.create(teacher_node)

        # 创建课程节点
        course_node = Node('Course')
        course_node.update(course)
        courses.append(course_node)
        graph.create(course_node)

        # 创建课程与教室的关系
        relationship = Relationship(teacher_node, 'Teach', course_node)
        graph.create(relationship)

    # 根据xml中的关系创建Relationship对象
    adv_course_node = root.getElementsByTagName('adv-course')[0]
    for item_node in get_all_sub_element_node(adv_course_node):
        adv = get_xml_text_node_value(item_node, 'adv')
        pre = get_xml_text_node_value(item_node, 'pre')
        # pre是adv的先修课程
        relationship = Relationship(courses[int(adv)], "StartWith", courses[int(pre)])
        graph.create(relationship)


def main():
    """
    找到所有的课程,并返回课程的详细信息
    """
    graph = Graph(neo4j_url, password=neo4j_password)
    # 找到算法分析与设计的所有先修课程
    data1 = graph.run('match (cc:Course)-[StartWith]-(c:Course) where cc.name="算法分析与设计" return c').data()
    print(len(data1))
    print(data1[1]['c']['name'],
          # help(data1[0]['c'])
          )
    # df = DataFrame(data1)
    # print(df)


if __name__ == '__main__':
    save_all_course_info()
    # # main()
    # courses_name, courses_details = get_all_courses_name_and_details()
    # for i in range(len(courses_name)):
    #     print(courses_name[i])
    # print('\n'+courses_name[i]+'\n')
    # data = courses_details[i].replace(' ', '')
    # pattern = r'\.|。'
    # result = re.split(pattern, data)
    # [print(i) for i in result[:-1]]
