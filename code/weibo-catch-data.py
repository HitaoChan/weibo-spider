import requests
import pprint
from bs4 import BeautifulSoup
import re
import time
import time

# pprint.pprint(response.json()) #格式化输出 只有接口爬虫能用


# 接受json 提取键值内容
def CatchData(id,max_id):
    # 得到评论区 爬取第一页
    try:
        time.sleep(0.25)
        url="https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(str(id),str(id))
        response = requests.get(url, timeout=30)
        # 如果不是200，引发HTTPEroor异常
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except:
        print("产生异常")
    data = response.json()
    cards = data['data']['data']
    for card in cards:
        # 加上一个楼中楼爬取
        # pprint.pprint(card) card是每一条回复
        if card:
            text = card.get('text')  # 评论
            like_count = card.get('like_count')  # 点赞
            user = card.get('user')  # 评论用户表信息
            max_id = card.get('max_id') #下一页的id
            name = user.get('screen_name')  # 用户名
            profile = user.get('profile_url')  # 用户主页
            fileName=getTopic(id)
            with open("../doc/"+fileName+".csv",mode='a',encoding='utf-8-sig') as f:
                f.write(",".join([name,text,str(like_count)]))
                f.write('\n')
            print("catch one comment")
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


                                                                                                                                                                                                    

if __name__ == "__main__":
    url = "https://m.weibo.cn/comments/hotflow?id=4610404497493299&mid=4610404497493299&max_id_type=0"
    # 话题id,https://m.weibo.cn/detail/4610404497493299
    # 用户提供detail之后的id即可
    id=4610404497493299
    # 第一页的max_id为0
    CatchData(id,0) #评论爬取 通过，楼中楼爬取未通过
    #getTopic(str(id)) #爬取话题通过
