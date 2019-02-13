from flask import Flask, url_for, render_template
from pandas import DataFrame
from py2neo import Graph

app = Flask(__name__)
graph = Graph("http://localhost:11005", password="shao1999")


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return "He!"


@app.route('/user/<username>')
def show_user_profile(username):
    return "User %s" % username


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)


@app.route('/adv_course/<course_name>')
def adv_course(course_name):
    # 找到算法分析与设计的所有先修课程
    data1 = graph.run('match (cc:Course)-[StartWith]-(c:Course) where cc.name="%s" return c'
                      % course_name).data()

    return render_template('index.html', data=data1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # with app.test_request_context():
    # print(url_for('static',filename='neo4j.py'))
    # print(url_for('show_user_profile', username="shao"))
