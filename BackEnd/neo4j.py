from py2neo import Graph

from setting import *


class Neo4j:
    def __init__(self):
        self.graph = Graph(neo4j_url, password=neo4j_password)

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

    def get_course_adv(self, course_name):
        """
        获取课程的先修课程
        :param course_name:
        :return:
        """
        if not self.get_course_node(course_name):
            # 没有要查询的课程
            return None
        query_sentence = 'match(cc:Course)-[relationship:StartWith *1..]->(advCourse:Course) ' \
                         'where cc.name="%s" return relationship' % course_name
        query_result = self.graph.run(query_sentence).data()
        courses = [course_name]
        index_relationships = []
        for item in query_result:
            relationships = item['relationship']
            for sub_relationship in relationships:
                start_node_name = sub_relationship.start_node['name']
                if start_node_name not in courses:
                    courses.append(start_node_name)
                end_node_name = sub_relationship.end_node['name']
                if end_node_name not in courses:
                    courses.append(end_node_name)
                index_relationship = (
                    courses.index(start_node_name),
                    courses.index(end_node_name))
                if index_relationship not in index_relationships:
                    index_relationships.append(index_relationship)
        return {"courses": courses, "index_relationships": index_relationships}

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
        return data1[0]['t']

    def get_teacher_all_course(self, teacher_name):
        """
        获取某老师教的所有课程
        :return:
        """
        query_sentence = 'match(t:Teacher)-[r:Teach]->(c:Course) where t.name="%s" return c' % teacher_name
        data1 = self.graph.run(query_sentence).data()
        result = [data['c']['name'] for data in data1]
        return result


def main():
    neo4j = Neo4j()
    course_name = "算法分析与设计"
    print(neo4j.get_course_adv(course_name))
    print(neo4j.get_course_teacher(course_name))
    print(neo4j.get_teacher_all_course("韩万江"))


if __name__ == '__main__':
    main()
