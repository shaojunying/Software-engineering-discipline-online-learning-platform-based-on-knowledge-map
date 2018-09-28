# coding=utf-8
import re

from pyquery import PyQuery as pq

doc = pq(filename='hello.htm')
li = doc('body > div.WordSection2 > table')
# print(li.text())
result = re.findall("课程名称\n(.*?)\n.*?先修课程\n(.*?)\n", li.text(),flags=re.DOTALL)
print(len(result))
for item in re.findall("课程名称\n(.*?)\n.*?先修课程\n(.*?)\n", li.text(),flags=re.DOTALL):
    if item[0][:3] == "中文：":
        print("课程名称",item[0][3:])
    else:
        print("课程名称",item[0])
    # if item[1][-2:] == "序号":
    #     print("先修课程",item[1][:-3])
    # else:
    print("先修课程",item[1])
