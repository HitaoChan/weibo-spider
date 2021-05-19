import re
import time
import requests
import json
# 设置头部和cookie
header = {'Content-Type':'text/html; charset=utf-8','User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
Cookie = {'Cookie':'SCF=AjlxfU4Kv0l4jCsBl3iOr4H2dem0yfdqb1ES5foMJrsqfNmUM4hfBKVZ9st6PqzYQSnYZ4FSPks_dDpc8ChK8KY.; SUB=_2A25NQo1BDeRhGeFK71UY8ynEzzyIHXVuzBMJrDV6PUJbktAfLVLtkW1NQ0Hmr20Kb2pJUy_PGi8oLceZQj3SEaTW; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW9ZY.B8i9iYw7wv9WKvDFa5NHD95QNShBN1KeN1hB7Ws4DqcjiIrSuIcf_9GyQ; _T_WM=93953758161; XSRF-TOKEN=d19bbb; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=lfid=102803&luicode=20000174&uicode=20000174'}

count=0
target=999
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
            fileName="爱奇艺道歉"
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

if __name__ == '__main__':
    CatchData(4634172041730479,0)