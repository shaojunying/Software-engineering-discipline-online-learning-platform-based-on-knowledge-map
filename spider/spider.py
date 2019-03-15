# coding=gbk
import os
import re
import xml.dom.minidom
from setting import data_xml_dir_path

from pyquery import PyQuery as pq

doc = xml.dom.minidom.Document()


def init_xml():
    """
    初始化一个xml文件对象，返回两个节点
    :return: 课程详细信息的xml对象 先修课程的xml对象
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


def convert_adv_course(courses_info, course_name_to_index):
    """
    将文字版的先修课程信息转为数字表示的字典
    :param courses_info: 课程信息
    :param course_name_to_index: 课程名到下标的对应关系
    :return: 先修课程字典(用一门课的下标指代该门课程)
    """
    adv_courses_dict = {}
    for i, course_info in enumerate(courses_info):
        # 获得当前课程的先修课程
        course_adv = course_info['advance']
        if course_adv == "无":
            continue
        # 遍历所有的课程名称,如果先修课程中包含该名字,就加进去
        for course_name in course_name_to_index.keys():
            if course_name not in course_adv:
                continue
            if i not in adv_courses_dict.keys():
                adv_courses_dict[i] = [course_name_to_index[course_name]]
            else:
                adv_courses_dict[i].append(course_name_to_index[course_name])
    print(adv_courses_dict)
    return adv_courses_dict


def save_course_adv_to_xml(courses_info, course_name_to_index, courses_adv_xml):
    """
    # 将先修课程信息存入xml中
    :param courses_info: 课程信息
    :param course_name_to_index:课程名与下标的对应关系
    :param courses_adv_xml: 先修课程的xml对象
    :return: None
    """
    # 将文字版的课程先修信息转化为字典
    adv_course_dict = convert_adv_course(courses_info=courses_info, course_name_to_index=course_name_to_index)
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
    print("成功为先修课程创建为xml节点")


def create_node(node_parent, node_name, node_content=None):
    """
    # 创建一个节点,节点的父节点为node_parent,新结点名字为node_name,节点内容为node_content
    :param node_parent: 新节点的父节点
    :param node_name: 新节点的名称
    :param node_content: 节点内容
    :return: 新创建的节点对象
    """
    global doc
    node_adv = doc.createElement(node_name)
    if node_content is not None:
        node_adv.appendChild(doc.createTextNode(str(node_content)))
    node_parent.appendChild(node_adv)
    return node_adv


def save_xml_to_file():
    """
    将xml信息写入文件中
    :return:
    """
    global doc
    path = os.path.join('../', data_xml_dir_path)
    fp = open(path, 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="gbk")
    print('成功将xml节点存入'+path+'中')


def parse_html(html_name):
    """
    解析html_name中的内容,将读取出的课程信息返回
    :param html_name: html文件名
    :return: [{"name":,"id":...}...]
    """
    pyquery_html = pq(filename=html_name)
    # 提取课程标题和先修课程
    li = pyquery_html('body > div.WordSection2 > table,p')
    print(li.text())
    courses_temp = re.findall("课程名称\n(.*?)"  # 课程名称
                              "\n课程编号\n(.*?)"  # 课程编号
                              "\n(.*?)"  # 英文名称 
                              "\n学分/学时\n(.*?)/(.*?)"
                              "\n(.*?)"
                              "\n开课学期\n(.*?)\n.*?"
                              "\n先修课程\n(.*?)课程名称.*?二、课程教学目标(.*?)三、课程与支撑的毕业要求.*?执笔人:(.*?)审核人", li.text(),
                              flags=re.DOTALL)
    courses_info = []
    for item in courses_temp:
        courses_info.append({
            # 课程名称
            "name": "".join(item[0].strip('中文：').split()),
            # 课程编号
            "id": "".join(item[1].strip("").split()),
            # 英文名称
            "english_name": item[2].strip("英文：").replace(u'\xa0', u' '),
            # 学分
            "credit": "".join(item[3].strip("").split()),
            # 学时
            "credit_hour": "".join(item[4].strip("").split()),
            # # 选修/必修
            "optional": 'y' if '必修（）' in "".join(item[5].strip("").split())
                .replace(u'\u2a57', u'').replace(u'\uf0fc', u'') else 'n',
            # 开课学期
            "semester": "".join(item[6].strip("").split()),
            # 先修课程
            "advance": "".join(item[7].strip("").split()),
            # 课程详细信息
            "details": "".join(item[8].strip("").split()),
            # 课程老师
            "teacher": "".join(item[9].strip("").split())
        })
    print("成功解析html中的课程信息,课程总数为:", len(courses_info))
    return courses_info


def save_courses_info_to_xml(courses_info):
    """
    将课程信息存入xml中
    :param courses_info: 课程信息
    :return: None
    """
    courses_info_xml, adv_courses_xml = init_xml()
    course_name_to_index = {}
    for i, course_info in enumerate(courses_info):
        course_node_xml = create_node(node_parent=courses_info_xml, node_name="course")
        for key, value in course_info.items():
            if key == 'advance':
                continue
            create_node(node_parent=course_node_xml, node_name=str(key), node_content=str(value))
        # 将课程名称和对应的下标存储成一个dict
        course_name_to_index[course_info['name']] = i
    print("成功为课程的信息(除先修课程)创建为xml节点")
    save_course_adv_to_xml(courses_info, course_name_to_index, adv_courses_xml)
    save_xml_to_file()


def main():
    # 解析xml
    courses_info = parse_html("hello.htm")
    # 将解析出的课程信息存入xml中
    save_courses_info_to_xml(courses_info)


if __name__ == '__main__':
    main()
