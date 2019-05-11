from py2neo import Graph

from setting import *


class Neo4j:
    def __init__(self):
        self.graph = Graph(neo4j_url, password=neo4j_password)

    def get_course_details(self, course_name):
        """
        获取course_name的详细信息
        :param course_name:
        :return:
        """
        course_node = self.get_course_node(course_name)
        print(course_node)
        return course_node['details'] if course_node else None

    def get_course_adv(self, course_name):
        """
        获取课程的先修课程
        :param course_name:
        :return:
        """
        if not self.get_course_node(course_name):
            # 没有要查询的课程
            return None
        query_sentence = 'match(cc:Course)-[r:StartWith]->(c:Course) where cc.name="%s" return c' % course_name
        data1 = self.graph.run(query_sentence).data()
        data_dict = {}
        for data in data1:
            data_dict[data['c']['name']] = data['c']['details']
        return data_dict

    def get_course_teacher(self, course_name):
        """
        获取课程的教师姓名
        :param course_name:
        :return:
        """
        if not self.get_course_node(course_name):
            # 没有要查询的课程
            return None
        query_sentence = 'match(t:Teacher)-[r:Teach]->(c:Course) where c.name="%s" return t' % course_name
        data1 = self.graph.run(query_sentence).data()
        if not data1:
            return None
        return data1[0]['t']['name']

    def get_course_node(self, course_name):
        """
        获取课程名为course_name的课程节点
        :param course_name:
        :return:
        """
        query_sentence = 'match (c:Course) where c.name="%s" return c' % course_name
        data1 = self.graph.run(query_sentence).data()
        if len(data1) == 0:
            return None
        return data1[0]['c']

    def get_course_semester(self, course_name):
        """
        获取课程的开课学期
        :param course_name:
        :return:
        """
        course_node = self.get_course_node(course_name)
        return course_node['semester'] if course_node else None

    def get_course_optional(self, course_name):
        """
        获取课程的选修或必修
        :param course_name:
        :return:
        """
        course_node = self.get_course_node(course_name)
        return course_node['optional'] if course_node else None

    def get_course_credit(self, course_name):
        """
        获取课程的学分
        :param course_name:
        :return:
        """
        course_node = self.get_course_node(course_name)
        return course_node['credit'] if course_node else None

    def get_course_credit_hour(self, course_name):
        """
        获取课程的学时
        :param course_name:
        :return:
        """
        course_node = self.get_course_node(course_name)
        return course_node['credit_hour'] if course_node else None

    def get_course_id(self, course_name):
        """
        获取课程的课程编号
        :param course_name:
        :return:
        """
        course_node = self.get_course_node(course_name)
        return course_node['id'] if course_node else None

    def get_course_english_name(self, course_name):
        """
        获取课程的英文名称
        :param course_name:
        :return:
        """
        course_node = self.get_course_node(course_name)
        return course_node['english_name'] if course_node else None


def main():
    neo4j = Neo4j()
    neo4j.get_course_adv("算法分析与设计")


if __name__ == '__main__':
    main()
