from pyhanlp import *

CustomDictionary.add('并行计算机')
CustomDictionary.add('数值分析与计算')

# 依存句法分析
str = '本课程旨在引导帮助学生了解并行计算机的初步知识'
print(HanLP.parseDependency(str))
