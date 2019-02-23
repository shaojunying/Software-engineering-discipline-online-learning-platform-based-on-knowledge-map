from pyhanlp import HanLP

terms = HanLP.segment("算法分析与设计")
abstract_query = ""

for term in terms:
    print(term)
    word = term.word
    term_str = str(term)
    print(word,term_str)