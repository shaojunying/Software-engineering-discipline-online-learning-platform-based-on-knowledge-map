from py2neo import *

graph = Graph("http://localhost:7474", username="zzq", password='zam123456')

data = graph.run('match (cc:Course)-[StartWith]-(c:Course) where cc.name="算法分析与设计" return c')
data = graph.run('match (cc:Course) return cc')
n = 0
for item in data:
    print(item['cc']['name'])
    n = n + 1
print(n)
