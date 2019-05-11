# Neo4j配置
import os

neo4j_password = "shao1999"
# neo4j_url = "http://localhost:11005/db/data/"
neo4j_url = "http://119.3.208.1:7474/db/data"
neo4j_user = "neo4j"

# HanLP分词词典及自定义问题模板根目录
root_dir_path = "..\\data"
custom_data_dir_path = os.path.join(root_dir_path, 'custom_data')
dict_dir_path = os.path.join(custom_data_dir_path, 'dictionary')
course_dict_dir_path = os.path.join(dict_dir_path, 'course_dict.txt')
question_dir_path = os.path.join(custom_data_dir_path, 'question')
question_classification_dir_path = os.path.join(question_dir_path, 'question_classification.txt')
vocabulary_dir_path = os.path.join(question_dir_path, 'vocabulary.txt')
detailed_questions_dir_path = os.path.join(question_dir_path, 'detailed_questions')
stop_words_dir_path = os.path.join(root_dir_path, 'stopwords.txt')

data_xml_dir_path = 'spider/data.xml'
