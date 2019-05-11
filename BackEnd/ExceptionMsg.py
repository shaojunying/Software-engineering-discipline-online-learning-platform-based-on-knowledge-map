from enum import Enum


class ExceptionMsg(Enum):
    SUCCESS = ("0000", "操作成功")
    NONEXISTENT_COURSE = ("0001", "课程不存在")
    REQUIRE_COURSE_NAME = ("0002", "需要课程名(course_name)")
    NO_INFO_ABOUT_THIS_COURSE = ("0003", "没有这门课程的教师信息")
    REQUIRE_TEACHER_NAME = ("0004", "需要教师姓名(teacher_name)")
    NONEXISTENT_TEACHER = ("0005", "该教师不存在")
    REQUIRE_QUESTION = ("0006", "需要问题参数(question)")
    QUESTION_IDENTIFICATION_WRONG = ("0007", "识别问题出错")

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message
