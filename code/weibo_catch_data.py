import requests
import pprint
from bs4 import BeautifulSoup
import re
import time
import json
import pandas as pd

# 设置头部和cookie
header = {'Content-Type':'text/html; charset=utf-8','User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
Cookie = {'Cookie':'SCF=AjlxfU4Kv0l4jCsBl3iOr4H2dem0yfdqb1ES5foMJrsqfNmUM4hfBKVZ9st6PqzYQSnYZ4FSPks_dDpc8ChK8KY.; SUB=_2A25NQo1BDeRhGeFK71UY8ynEzzyIHXVuzBMJrDV6PUJbktAfLVLtkW1NQ0Hmr20Kb2pJUy_PGi8oLceZQj3SEaTW; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW9ZY.B8i9iYw7wv9WKvDFa5NHD95QNShBN1KeN1hB7Ws4DqcjiIrSuIcf_9GyQ; _T_WM=93953758161; XSRF-TOKEN=d19bbb; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=lfid=102803&luicode=20000174&uicode=20000174'}

# 得到榜单
def get_topics():
    """
    得到榜单的json数据
    """
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=231583&page_type=searchall'
    response = requests.get(url,headers=header,cookies=Cookie)
    datas=response.json()
    topics=datas['data']['cards'][0]['group']
    return topics


def get_titles_schemes(topics):
    """
    返回榜单的标题和链接schemes
    """
    titles = []
    schemes = []
    for topic in topics:
        if (topic['item_log'].get('key') != None):
            text = re.sub("[#]", '', topic['item_log'].get('key'))
            titles.append(text)
            schemes.append(topic['scheme'])

    return titles, schemes


def get_urls(schemes):
    """
    得到榜单对应的urls，为得到事件ID做准备
    """
    urls = []
    for url in schemes:
        # 将scheme转换为需要的url
        url = re.sub('(search\?)', 'api/container/getIndex?', url) + '&page_type=searchall'
        urls.append(url)
        # response=requests.get(url,headers=header,cookies=Cookie)
        # json = response.json()
        # jsons.append(response.json())
    return urls

class GetKeyValue(object):
    """
    从json中找到key的值
    """
    def __init__(self, o, mode='j'):
        self.json_object = None
        if mode == 'j':
            self.json_object = o
        elif mode == 's':
            self.json_object = json.loads(o)
        else:
            raise Exception('Unexpected mode argument.Choose "j" or "s".')

        self.result_list = []

    def search_key(self, key):
        self.result_list = []
        self.__search(self.json_object, key)
        return self.result_list

    def __search(self, json_object, key):

        for k in json_object:
            if k == key:
                self.result_list.append(json_object[k])
            if isinstance(json_object[k], dict):
                self.__search(json_object[k], key)
            if isinstance(json_object[k], list):
                for item in json_object[k]:
                    if isinstance(item, dict):
                        self.__search(item, key)
        return


def get_ids(urls):
    """
    得到榜单事件对应的ID
    """
    ids = []
    for url in urls:
        response = requests.get(url, headers=header, cookies=Cookie)
        json = response.json()
        gkv = GetKeyValue(o=json, mode='j')
        id = gkv.search_key('mid')[0]
        ids.append(id)
        time.sleep(1)
    return ids


count = 0
target = 1000
#评论爬取模块
# 接受json 提取键值内容
def CatchData(id,max_id=0):
    global count
    global target
    # 得到评论区 爬取第一页
    try:
        time.sleep(0.25)
        url="https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0&max_id={}".format(str(id),str(id),str(max_id))
        print(url)
        response = requests.get(url,headers=header,cookies=Cookie)
        # 如果不是200，引发HTTPEroor异常
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except:
        print("产生异常")
    data = response.json()
    cards = data['data']['data']
    max_id_from_data = data['data']['max_id']
    for card in cards:
        # 加上一个楼中楼爬取
        # pprint.pprint(card) card是每一条回复
        if card:
            text = card.get('text')  # 评论
            like_count = card.get('like_count')  # 点赞
            user = card.get('user')  # 评论用户表信息
            max_id = max_id_from_data #下一页的id

            name = user.get('screen_name')  # 用户名
            profile = user.get('profile_url')  # 用户主页
            fileName=titles[index]
            if(count <= target):
                with open("../doc/" + fileName + ".csv", mode='a', encoding='utf-8-sig') as f:
                    text = re.sub(r'<.*>', ' ', text)  # 过滤标签
                    f.write(",".join([name, text, str(like_count)]))
                    f.write('\n')
                    count = count + 1
                print("catch {} comment".format(count))

            # print(user)
            # print(name,text,like_count)
    getComments(id,max_id) #开始爬取下一页


def getComments(id,max_id):
    # 如果不是最后一页就爬取下一页
    if max_id != None:
        #url=url+"&max_id={}&max_id_type=0".format(str(max_id))
        CatchData(id,max_id)


def getTopic(id: int)->str:
    # 打印话题热点
    url = "https://m.weibo.cn/statuses/extend?id="+str(id)
    try:
        response = requests.get(url, timeout=30)
        # 如果不是200，引发HTTPEroor异常
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        data = response.json()
        # pprint.pprint(data)
    except:
        print("产生异常")
    topic=data['data']
    text=topic.get('longTextContent')
    #print(type(text)) #text是str类型
    # 提取#开头结尾的的字符串
    pattern=re.compile(r'#.*#')
    # print(text)
    str1=pattern.search(text)
    #print(str1.group(0))
    # print(card.get('longTextContent'))
    return str1.group(0)


def get_index(titles):
    print("select a index of topic to catch comment:")
    count = 0
    for title in titles:
        print('\t' + str(count) + title)
        count = count + 1
    index = input("input the index:")
    return int(index)



if __name__ == "__main__":
    # 准备工作 topics是帮当的json，titles是榜单事件标题，schemes是各榜单转换url的原材料，urls是各事件的url，ids是爬取评论的id关键词
    topics = get_topics()
    titles, schemes = get_titles_schemes(topics)
    urls = get_urls(schemes)
    ids = get_ids(urls)
    index = get_index(titles)
    title = titles[index]
    # 爬取评论
    CatchData(ids[index],0)