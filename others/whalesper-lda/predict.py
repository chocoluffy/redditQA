# -*- coding: utf-8 -*-

import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import json
from pprint import pprint
from pymongo import MongoClient
import pickle
from collections import defaultdict
import os.path
import urllib
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
import requests
import jieba
import gensim
from gensim import corpora
import os.path
import numpy

stopwords = []
for line in open('stopwords.dat', 'r'):
    word = line.rstrip().decode('utf8') # strip off newline and any other trailing whitespace
    stopwords.append(word)
    
blackword_lst = [
    "约克", 
    "论坛",
    "月",
    "日",
    "超级", 
    "生活",
    "多伦多",
    "吃喝",
    "玩乐",
    "http",
    "ca",
    "征稿",
    "小编",
    "微博",
    "转发理由",
    "编"
]

for bad_word in blackword_lst:
    stopwords.append(bad_word.decode('utf8'))

def clean(doc):
    """
    Use chinese stopword and tokenizer to obtain clean doc array. 
    Output, array of string, join by tokens.
    """
    token_lst = jieba.cut(doc, cut_all=True)
    token_lst = filter(lambda x: x not in stopwords, token_lst)
    # print("Full Mode: " + "/ ".join(token_lst))
    return " ".join(token_lst)

if not os.path.exists('models/tokens.dict'):
    # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)
    # Filter out words that occur less than 20 documents, or more than 50% of the documents.
    dictionary.filter_extremes(no_below=20, no_above=0.5)
    dictionary.save('models/tokens.dict')
else:
    dictionary = corpora.Dictionary.load('models/tokens.dict')
    print("preprocessed dictionary loaded...")


# Save LDA model
if not os.path.exists('models/model.lda'):
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel
    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=15, id2word = dictionary, passes=50)
    ldamodel.save('models/model.lda')
else:
    ldamodel = gensim.models.ldamodel.LdaModel.load('models/model.lda')
    print("lda model loaded...")


def get_topic_from_query(question):
    important_words = clean(question).split(" ")

    dictionary = corpora.Dictionary.load('models/tokens.dict')

    ques_vec = []
    ques_vec = dictionary.doc2bow(important_words)

    topic_vec = []
    topic_vec = ldamodel[ques_vec]

    word_count_array = numpy.empty((len(topic_vec), 2), dtype = numpy.object)
    for i in range(len(topic_vec)):
        word_count_array[i, 0] = topic_vec[i][0]
        word_count_array[i, 1] = topic_vec[i][1]

    idx = numpy.argsort(word_count_array[:, 1])
    idx = idx[::-1]
    word_count_array = word_count_array[idx]

    final = []
    final = ldamodel.print_topic(word_count_array[0, 0], 10)

    question_topic = final.split('*') ## as format is like "probability * topic"

    print "==="
    print question
    print ' '.join(question_topic)
    print "==="


test_titles = [
{
    "title_short" : " 想吃美食,懒得出门? 这家外卖速度比你男友快,服务好过你太太!更多多伦多吃喝玩乐的消息，可关注:weibo.com/lifeinca，或是微信:lifeintoronto，ins: "
},
{
    "title_short" : "转发理由：一家年 收 入 抵一个海底捞！ 国内超火第1佳大鸡排空袭多伦多。超厚超大的秘制鸡排，有芝士爆浆、藤椒、孜然等口味。还有关八会长最爱的爆浆鸡排。喜欢吃M记的麦辣鸡翅的朋友，绝对不能错过这个脆辣对翅。香辣可口，鲜嫩多汁。多伦多吃喝玩乐的秒拍视频#torontodiary# #多伦多哪里吃# #多伦多美食推荐# ​​​"
},
{
    "title_short" : " 十月双“喜喜”即将到来：黑帮经典 与 热血喜剧 相遇 大鹏和娜扎来了？！更多多伦多吃喝玩乐的消息，可关注:weibo.com/lifeinca，或是微信:lifeintoronto，ins: "
},
{
    "title_short" : "没有看到三文鱼洄游的Morningside Park三文鱼醉氧日，天气太好了 结果鱼先走了，尽管如此，这样的自然环境也足以让人陶醉了#带着微博去旅行#加拿大·多伦多 @多伦多吃喝玩乐 加拿大·多伦多 ​​​转发理由：周末好去处之一~Morningside Park"
},
{
    "title_short" : "【长假long weekend推荐】在long point eco-advantures 租个胶囊屋享受（图二外）露天洗澡房的乐趣白天玩个zip line 再来个hiking在winery品个酒 在酒庄里面逛逛看看葡萄周六晚上去sandbar on the beach吃饭去跟当地歌手上台一展歌喉吧或者选择在营地篝火旁谈天说地看流星????走之前还可以去tu ​​​...转发理由：周末好去处~在lo"
},
{
    "title_short" : " 找试题、笔记、书本答案 在加拿大读书的你们应该有的学霸修炼秘籍更多多伦多吃喝玩乐的消息，可关注:weibo.com/lifeinca，或是微信:lifeintoronto，ins: "
},
{
    "title_short" : " 十月份多伦多的十大免费活动更多多伦多吃喝玩乐的消息，可关注:weibo.com/lifeinca，或是微信:lifeintoronto，ins: "
},
{
    "title_short" : " 【觅迷】多伦多一周活动快报点击蓝字关注我们又不知道玩啥了吧！又在纠结去哪耍？想看帅哥和美女？必然要看觅迷周报的啊！2017 - 10 月 -周报 "
},
{
    "title_short" : " 不差钱！UBC亲身诠释啥叫真土豪！造价3900万的游泳馆长这样！说到加拿大哪些学校最土豪，最不差钱，那UBC要算数一数二的。最近UBC的Point Grey campus造价3900万"
},
{
    "title_short" : " 揭秘！在加拿大养一个孩子需要多少钱？学生已经开学了，家长又开始围着上学的孩子转圈了。忙着接送孩子，给孩子准备午餐，督促孩子学习，安排娱乐活动……仔细想想，在"
}

]

for obj in test_titles:
    get_topic_from_query(obj["title_short"])