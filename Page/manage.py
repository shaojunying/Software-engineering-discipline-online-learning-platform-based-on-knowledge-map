#!/usr/bin/env python
import os
import sys


def load_course_name_dict(course_name_dict_path):
    """
    将课程名字添加至自定义字典中
    :param course_name_dict_path: 存放课程名字文件的路径
    :return: None
    """
    for line in helper.read_file(course_name_dict_path):
        CustomDictionary.insert(line, 'cn 99999999')


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoftwareEngineeringLearningPlatform.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
