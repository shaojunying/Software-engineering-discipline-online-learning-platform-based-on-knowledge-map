from ExceptionMsg import ExceptionMsg
from ResponseData import ResponseData
from neo4j import Neo4j


class Service:
    def __init__(self):
        """初始化一个模型,初始化之后可以直接调用question进行查询"""
        self.neo4j = Neo4j()

    def get_adv_courses(self, course_name):
        """
        获取一门课程的所有先修课程
        :return:
        """
        # 判断课程是否存在
        course = self.neo4j.get_course_node(course_name)
        if not course:
            return ResponseData(ExceptionMsg.NONEXISTENT_COURSE).encode()

        # 获取课程的先修课程
        data = self.neo4j.get_course_adv(course_name)
        response_data = ResponseData(ExceptionMsg.SUCCESS, data=data).encode()
        return response_data

    def get_course_info(self, course_name):
        """
        获取课程详细信息
        :return:
        """
        # 获取课程节点
        course = self.neo4j.get_course_node(course_name)
        if not course:
            return ResponseData(ExceptionMsg.NONEXISTENT_COURSE).encode()
        return ResponseData(data=course).encode()

    def get_course_teacher(self,course_name):
        """
        获取课程的教师信息
        :return:
        """
        # 获取课程节点
        course = self.neo4j.get_course_node(course_name)
        if not course:
            return ResponseData(ExceptionMsg.NONEXISTENT_COURSE).encode()

        # 获取课程的教师信息
        teacher = self.neo4j.get_course_teacher(course_name)
        if not teacher:
            return ResponseData(ExceptionMsg.NO_INFO_ABOUT_THIS_COURSE).encode()
        return ResponseData(data=teacher).encode()

    def get_teacher_all_courses(self,teacher_name):
        """
        获取教师教的所有课程
        :return:
        """
        # 获取该教师教授的课程
        courses = self.neo4j.get_teacher_all_course(teacher_name)
        if not courses:
            return ResponseData(ExceptionMsg.NONEXISTENT_TEACHER).encode()
        return ResponseData(data=courses).encode()
