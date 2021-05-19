from snownlp import SnowNLP
import codecs
import os
import numpy as np
import matplotlib.pyplot as plt

def generate_HTML_sentiment(title):
    def get_sentiments(filePath):
        sentiments=[]
        with open(filePath, 'r', encoding='utf-8') as file:
            for each_line in file:
                _,comment,_ = each_line.split(',')
                s=SnowNLP(comment)
                sentiments.append(s.sentiments)

        return sentiments

    def get_PNG(sentiments):
        #print(sentiments)
        plt.hist(sentiments, bins=np.arange(0, 1, 0.01), facecolor='g')
        plt.xlabel('Sentiments Probability')
        plt.ylabel('Quantity')
        plt.title('Analysis of Sentiments')
        plt.savefig(os.path.join('../img/') + title + '情感分析.jpg')
        plt.show()

    filePath=os.path.join('../doc', title+'.csv')
    sentiments=get_sentiments(filePath)
    get_PNG(sentiments)

def main():
    title=input("输入要情感分析的文件:")
    generate_HTML_sentiment(title)

if __name__ == '__main__':
    main()