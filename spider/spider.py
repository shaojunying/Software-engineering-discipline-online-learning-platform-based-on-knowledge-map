# coding=gbk
import re
import xml.dom.minidom
from pyquery import PyQuery as pq
from jieba.analyse import *

doc = xml.dom.minidom.Document()


def init_xml():
    """
    :return: 课程名称的xml对象 先修课程的xml对象
    """
    # 初始化一个xml对象
    global doc
    root = doc.createElement("root")
    doc.appendChild(root)

    # 课程名字对应的标签
    courses_name_xml = doc.createElement("courses")
    root.appendChild(courses_name_xml)

    # 先修课程对应的标签
    adv_courses_xml = doc.createElement("adv-course")
    root.appendChild(adv_courses_xml)

    return courses_name_xml, adv_courses_xml


def save_course_name_and_detail_to_xml(courses, courses_name_xml):
    """
    存储课程名称和详细介绍信息
    :param courses: 所有课程组成的list
    :param courses_name_xml: xml对象(课程信息将会保存到这里)
    :return: 课程名称和对应下标组成的字典
    """
    global doc
    course_index = 0
    course_name_to_index = {}
    courses_name = courses["name"]
    courses_detail = courses["detail"]
    for i in range(len(courses_name)):
        # 将课程名称存进xml结点中
        create_node(node_parent=courses_name_xml, node_name="name", node_content=courses_name[i])
        create_node(node_parent=courses_name_xml, node_name="details", node_content=courses_detail[i])

        # 将课程名称和对应的下标存储成一个dict
        course_name_to_index[courses_name[i]] = course_index
        course_index += 1

    return course_name_to_index


def convert_adv_course(courses_advance, course_name_to_index):
    """
    :param courses_advance: 先修课程
    :param course_name_to_index: 课程名到下标的对应关系
    :return: 先修课程字典
    """
    pre_course_index = 0
    adv_course_dict = {}
    for course_adv in courses_advance:
        # 取出课程的先修课信息
        if course_adv != "无":
            for course_adv_item in course_name_to_index.keys():
                # 找出在本门课程的先修课中的课程名称
                if course_adv_item in course_adv:
                    if pre_course_index not in adv_course_dict.keys():
                        adv_course_dict[pre_course_index] = [course_name_to_index[course_adv_item]]
                    else:
                        adv_course_dict[pre_course_index].append(course_name_to_index[course_adv_item])
            # 此处考虑"计算机程序设计语言"这种情况
            if "计算机程序设计语言" in course_adv:
                if pre_course_index not in adv_course_dict.keys():
                    adv_course_dict[pre_course_index] = [-1]
                else:
                    adv_course_dict[pre_course_index].append(-1)

        pre_course_index += 1
    return adv_course_dict


def save_course_adv_to_xml(adv_course_dict, courses_adv_xml):
    """
    :param adv_course_dict: 先修课程字典
    :param courses_adv_xml: 先修课程的xml对象
    :return: none
    """
    for pre_course, adv_courses in adv_course_dict.items():
        for adv_course in adv_courses:
            # 创建一个先修课节点
            node = doc.createElement("item")
            # 将该先修课节点添加到整个先修课节点中
            courses_adv_xml.appendChild(node)
            # 创建先修课中当前课程的节点
            create_node(node_parent=node, node_name="adv", node_content=pre_course)
            # 创建先修课中先修课程的信息
            create_node(node_parent=node, node_name="pre", node_content=adv_course)


def create_node(node_parent, node_name, node_content):
    """
    :param node_parent: 被添加元素的父节点
    :param node_name: 要添加的节点名称
    :param node_content: 节点内容
    :return:
    """
    global doc
    node_adv = doc.createElement(node_name)
    node_adv.appendChild(doc.createTextNode(str(node_content)))
    node_parent.appendChild(node_adv)


def save_xml_to_file():
    global doc
    fp = open('data.xml', 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="gbk")


def parse_html(filename):
    """
    :param filename: html文件名
    :return: 课程信息list
    """
    pyquery_html = pq(filename=filename)
    # 提取课程标题和先修课程
    li = pyquery_html('body > div.WordSection2 > table,p')
    courses_temp = re.findall("课程名称\n(.*?)\n课程编号.*?先修课程\n(.*?)课程名称.*?二、课程教学目标(.*?)三、课程与支撑的毕业要求", li.text(),
                              flags=re.DOTALL)

    return {"name": [item[0].strip('中文：') for item in courses_temp],
            "advance": [item[1].strip('序号课程名称 ') for item in courses_temp],
            "detail": [item[2].strip() for item in courses_temp]}


def find_all_course_can_study(courses_name, adv_course_dict, learned_courses=[]):
    """
    遍历寻找所有的当前可以上的课程
    :param courses_name: 课程名字对应的数组
    :param adv_course_dict: 课程与先修课的对应字典
    :param learned_courses: 已经学过的课程
    :return: 可以选择的课程
    """
    can_be_selected_courses = []
    for course_index in range(len(courses_name)):
        # 当前课程没有学过
        if course_index not in learned_courses:
            # 当前课程有先修课程
            if course_index in adv_course_dict:
                # 判断是否所有先修课程都已经学过了
                all_adv_courses_has_been_learned = True
                for adv_course in adv_course_dict[course_index]:
                    if adv_course not in learned_courses:
                        all_adv_courses_has_been_learned = False
                        break
                if all_adv_courses_has_been_learned:
                    can_be_selected_courses.append(course_index)
            else:
                can_be_selected_courses.append(course_index)
    return can_be_selected_courses


tags = ["数据库", "数据结构", "c语言", "Java", "Linux", "XML", "汇编语言", "软件测试", "C++", "计算机网络"]


def count_tags_occurrences_in_every_courses_details(courses_details, favorite_tags_index):
    tags_occurrences = []
    for course_index in range(len(courses_details)):
        tags_occurrences.append(0)
        for favorite_tag_index in favorite_tags_index:
            # 统计一个标签在课程介绍中出现的次数
            tag_occurrences_in_one_class = courses_details[course_index].count(tags[favorite_tag_index])
            tags_occurrences[course_index] += tag_occurrences_in_one_class
    return tags_occurrences


def main():
    courses = parse_html("hello.htm")
    courses_name_xml, adv_courses_xml = init_xml()
    course_name_to_index = save_course_name_and_detail_to_xml(courses, courses_name_xml)
    adv_course_dict = convert_adv_course(courses["advance"], course_name_to_index)
    save_course_adv_to_xml(adv_course_dict, adv_courses_xml)
    save_xml_to_file()

    can_be_selected_courses = find_all_course_can_study(courses_name=courses["name"], adv_course_dict=adv_course_dict,
                                                        learned_courses=[])
    tags_occurrences = count_tags_occurrences_in_every_courses_details(courses_details=courses["detail"], favorite_tags_index=[0, 1, 2])
    print(tags_occurrences)


if __name__ == '__main__':
    main()
