# -*- coding: utf-8 -*-
from py2neo import *
from xml.dom import minidom as minidom


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


def get_all_courses_name_and_details():
    dom = minidom.parse("data.xml")
    root = dom.documentElement
    # 获得所有课程节点的父节点
    courses_nodes = root.getElementsByTagName('courses')
    courses_name = []
    courses_details = []
    # 获取所有课程节点
    for course_node in get_all_sub_element_node(courses_nodes[0]):
        courses_name.append(get_xml_text_node_value(course_node, 'name'))
        courses_details.append(get_xml_text_node_value(course_node, 'details'))
    return courses_name, courses_details


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
    graph = Graph("http://localhost:11005", password="shao1999")
    graph.delete_all()
    # 获取所有课程节点
    for course_node in get_all_sub_element_node(courses_nodes[0]):
        # 获取课程名字
        course = {
            'name': get_xml_text_node_value(course_node, 'name'),
            'details': get_xml_text_node_value(course_node, 'details')
        }
        node = Node('Course')
        node.update(course)
        courses.append(node)
        graph.create(node)
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
    graph = Graph("http://localhost:11005", password="shao1999")
    # 找到算法分析与设计的所有先修课程
    data1 = graph.run('match (cc:Course)-[StartWith]-(c:Course) where cc.name="算法分析与设计" return c').data()
    print(len(data1))
    print(data1[1]['c']['name'],
          # help(data1[0]['c'])
          )
    # df = DataFrame(data1)
    # print(df)


if __name__ == '__main__':
    # main()
    pass
    courses_name, courses_details = get_all_courses_name_and_details()
    for i in range(len(courses_name)):
        print('\n'+courses_name[i]+'\n')
        data = courses_details[i].replace(' ', '')
        pattern = r'\.|。'
        result = re.split(pattern, data)
        [print(i) for i in result[:-1]]
