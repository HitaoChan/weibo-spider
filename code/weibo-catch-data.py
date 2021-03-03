import requests
import pprint
from bs4 import BeautifulSoup
import re


# pprint.pprint(response.json()) #格式化输出 只有接口爬虫能用


# 接受json 提取键值内容
def CatchData(url):
    # 得到评论区
    try:
        response = requests.get(url, timeout=30)
        # 如果不是200，引发HTTPEroor异常
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        data = response.json()
    except:
        print("产生异常")
    cards = data['data']['data']
    for card in cards:
        # 加上一个楼中楼爬取
        # pprint.pprint(card) card是每一条回复
        if card:
            text = card.get('text')  # 评论
            like_count = card.get('like_count')  # 点赞
            user = card.get('user')  # 评论用户表信息
            # cid = card.get('mid')
            # url = url + "?cid=" + cid
            # try:
            #     response=requests.get(url,timeout=30)
            #     response.raise_for_status()
            #     response.encoding=response.apparent_encoding
            #     data
            name = user.get('screen_name')  # 用户名
            profile = user.get('profile_url')  # 用户主页
            print("用户名:" + name, "评论:" + text, "点赞数量:" + str(like_count))
            # print(user)
            # print(name,text,like_count)


def getTopic(id):
    # 打印话题热点
    url = "https://m.weibo.cn/statuses/extend?id="+id
    try:
        response = requests.get(url, timeout=30)
        # 如果不是200，引发HTTPEroor异常
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        data = response.json()
        pprint.pprint(data)
    except:
        print("产生异常")
    topic=data['data']
    text=topic.get('longTextContent')
    #print(type(text)) #text是str类型
    # 提取#开头结尾的的字符串
    pattern=re.compile(r'#.*#')
    print(text)
    str=pattern.search(text)
    print(str.group(0))
    # print(card.get('longTextContent'))


if __name__ == "__main__":
    url = "https://m.weibo.cn/comments/hotflow?id=4610404497493299&mid=4610404497493299&max_id_type=0"
    CatchData(url) #评论爬取 通过，楼中楼爬取未通过
    id=4610404497493299 #话题id
    #getTopic(str(id)) #爬取话题通过