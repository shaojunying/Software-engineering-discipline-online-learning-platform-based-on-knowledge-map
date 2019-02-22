from pyhanlp import *

CustomDictionary.add("星期机")
result = HanLP.segment("今天星期机")
print(result)
