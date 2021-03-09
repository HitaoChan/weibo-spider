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


def start_crawl(cookie_dict,id):
	base_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'
	next_url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type={}'
	page = 1
	id_type = 0
	comment_count = 0
	requests_count = 1
	res = requests.get(url=base_url.format(id,id), headers=headers,cookies=cookie_dict)
	while True:
		print('parse page {}'.format(page))
		page += 1
		try:
			data = res.json()['data']
			wdata = []
			max_id = data['max_id']
			for c in data['data']:
				comment_count += 1
				row = info_parser(c)
				wdata.append(info_parser(c))
				if c.get('comments', None):
					temp = []
					for cc in c.get('comments'):
						temp.append(info_parser(cc))
						wdata.append(info_parser(cc))
						comment_count += 1
					row['comments'] = temp
				print(row)
			with open('{}/{}.csv'.format(comment_path, id), mode='a+', encoding='utf-8-sig', newline='') as f:
				writer = csv.writer(f)
				for d in wdata:
					writer.writerow([d['wid'],d['time'],d['text'],d['uid'],d['username'],d['following'],d['followed'],d['gender']])

			time.sleep(5)
		except:
			print(res.text)
			id_type += 1
			print('评论总数: {}'.format(comment_count))

		res = requests.get(url=next_url.format(id, id, max_id,id_type), headers=headers,cookies=cookie_dict)
		requests_count += 1
		if requests_count%50==0:
			print(id_type)
		print(res.status_code)


def info_parser(data):
	id,time,text =  data['id'],data['created_at'],data['text']
	user = data['user']
	uid,username,following,followed,gender = \
		user['id'],user['screen_name'],user['follow_count'],user['followers_count'],user['gender']
	return {
		'wid':id,
		'time':time,
		'text':text,
		'uid':uid,
		'username':username,
		'following':following,
		'followed':followed,
		'gender':gender
	}


if __name__ == "__main__":
    url = "https://m.weibo.cn/comments/hotflow?id=4610404497493299&mid=4610404497493299&max_id_type=0"
    CatchData(url) #评论爬取 通过，楼中楼爬取未通过
    id=4610404497493299 #话题id
    #getTopic(str(id)) #爬取话题通过