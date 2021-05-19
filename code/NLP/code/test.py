from snownlp import sentiment
import codecs
import random

class Model(object):
    def __init__(self):
        self.sentiment = sentiment
    
    def fit(self, X, Y):
        print(f'Training on the specified data (with size {len(X)})...')
        data = zip(X, Y)
        neg, pos = [sent for sent, label in data if label == 'pos'], [sent for sent, label in data if label == 'neg']
        self.sentiment.classifier.train(neg, pos)
    
    def save(self, file_name = 'sentiment.marshal', iszip=True):
        # 持久化
        print(f'Saving model with file name {file_name}')
        self.sentiment.save(file_name, iszip)
    
    def load(self, file_name = 'sentiment.marshal', iszip=True):
        # 读取模型
        print(f'Loading model {file_name}')
        self.sentiment.load(file_name, iszip)
    
    def predict(self, X):
        print('Commencing prediction procedure...')
        # 内部分类器
        classifier = self.sentiment.classifier.classifier
        # 句子处理器
        handle = self.sentiment.classifier.handle
        Y = []
        for line in X:
            # 介于API, 对每一个句子单独预测
            line = line.rstrip("\r\n")
            handled_sent = handle(line)
            result, _ = classifier.classify(handled_sent)
            Y.append(result)
        return Y
    
    def score(self, X, Y):
        print('Commencing scoring procedure...')
        pred_Y = self.predict(X) # 获得预测的Y
        data_size = len(X) # 数据集大小
        
        # 统计正确预测的数量
        correct_cnt = 0
        for idx in range(data_size):
            true_y, pred_y = Y[idx], pred_Y[idx]
            if true_y == pred_y:
                correct_cnt += 1
            else:
                print(X[idx], true_y, pred_y)
        
        # 返回准确率
        return correct_cnt / data_size

def read_test_data():
    print("Loading test data...")
    X = [line.rstrip("\r\n") for line in codecs.open('test.txt', 'r', 'utf-8').readlines()]
    Y = ['neg'] * len(X)
    return X, Y

def read_data(shuffle = True):
    print("Loading data...")
    neg_X = [line.rstrip("\r\n") for line in codecs.open('neg.txt', 'r', 'utf-8').readlines()]
    pos_X = [line.rstrip("\r\n") for line in codecs.open('pos.txt', 'r', 'utf-8').readlines()]
    neg_Y = ['neg'] * len(neg_X)
    pos_Y = ['pos'] * len(pos_X)
    X = neg_X + pos_X
    Y = neg_Y + pos_Y
    if shuffle: 
        temp = list(zip(X, Y))
        random.shuffle(temp)
        X, Y = list(zip(*temp))
    return X, Y


def main():
    # 读取数据
    X, Y = read_data()
    # 三七分数据集
    splitter = int(len(X) * 0.7)
    train_X, test_X = X[:splitter], X[splitter:]
    train_Y, test_Y = Y[:splitter], Y[splitter:]
    # 实例化Model
    model = Model()
    try:
        model.load()
    except Exception as e:
        # 训练
        model.fit(train_X, train_Y)
        # 持久化
        model.save()
    # 测试精度
    #precision = model.score(test_X, test_Y)
    #print('PRECISION:', round(precision, 3))

    # 如果想用自己的测试，则解开下面的注释
    test_X, test_Y = read_test_data()
    precision = model.score(test_X, test_Y)
    print('PRECISION FROM CUSTOMIZED DATA:', round(precision, 3))


if __name__ == '__main__':
    main()