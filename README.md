# Software-engineering-discipline-online-learning-platform-based-on-knowledge-map
##### 基于知识图谱的软件工程学科在线学习平台
北邮大创项目,项目链接https://win.bupt.edu.cn/program.do?id=180

### 项目目前大致思路
用户进入网站注册之后,将让用户选择几个感兴趣的标签,之后将根据用户选择标签给用户推荐课程,待有一定用户量之后,再根据用户的相似度进行推荐

### 项目文件夹说明

- [pages](pages)下存放了两个文件,分别是
    - [main](pages/main)一个简陋的主页面的源代码
        - [test.html](pages/main/test.html)这个网页实现了箭头的功能,但是箭头眼色不能随连线颜色的改变而改变,且界面需要进一步美化
        - [show.html](pages/main/show.html)这个网页是最初的课程信息展示
    - [signup](pages/signup)一个用jquery实现的注册页面(登录界面的代码应该是类似的,只需要修改少量代码即可)
- [spider](spider)一个用于爬取课程数据的简单爬虫

    - 已完成的工作:
        - 解析出hello.htm中的课程标题, 先修课程, 课程教学目标信息
        - 将上述信息存储进data.xml文件中
        - 找到所有的可以学习的课程(没有先修课程或者用户已经修完该课的先修课程的所有课程)
        - 统计所有课程的课程目标信息中用户选择的标签分别在每个课程中出现的次数(为以后的推荐做准备)
        - 将用户可以学习的课程按照用户选择的标签进行排序
    - 待完成的工作:
        - 待有一定的用户数据之后根据用户的相似度进行更加个性化的推荐
- [other_file](other_file)则保存了一些项目相关的非代码文件
