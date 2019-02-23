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
        query_sentence = 'match (c:Course) where c.name="%s" return c' % course_name
        data1 = self.graph.run(query_sentence).data()
        if len(data1) == 0:
            return None
        return data1[0]['c']['details']

    def get_course_adv(self, course_name):
        """
        获取课程的先修课程
        :param course_name:
        :return:
        """
        if not self.get_course_details(course_name):
            # 没有要查询的课程
            return None
        query_sentence = 'match(cc:Course)-[r:StartWith]->(c:Course) where cc.name="%s" return c' % course_name
        data1 = self.graph.run(query_sentence).data()
        data_dict = {}
        for data in data1:
            data_dict[data['c']['name']] = data['c']['details']
        return data_dict


def main():
    neo4j = Neo4j()
    neo4j.get_course_adv("算法分析与设计")


if __name__ == '__main__':
    main()
