# encoding=utf-8
'''
工具类
'''
from snownlp.sentiment import classify
import jieba


def get_sentence_sentiment(sentence):
    '''
    用于情感分析
    :param word_list:list形式，分词后的结果
    :return: [0,1]之间的极性结果
    '''
    return classify(sentence)


def word_segment(sentence):
    '''
    分词
    :param sentence:带分词句子
    :return: 分词结果，list形式
    '''
    words = jieba.cut(sentence, cut_all=True)
    list = []
    for i in words:
        if len(i) > 0:
            list.append(i)
    return list




if __name__ == '__main__':
    s = "这个软件非常好用。"
    l = word_segment(s)
    print(l)
    a= get_sentence_sentiment(s)
    print(a)