import os
import jieba
from collections import Counter
from wordcloud import WordCloud
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType

def generate_HTML_wordcloud(title, n_top=100):

    def get_words(filepath):
        words = []
        with open(filepath, 'r', encoding='utf-8') as file:
            for each_line in file:
                _, comment, _ = each_line.split(',')
                seg_list = jieba.cut(comment, cut_all=False)
                words.extend(seg_list)
        return words

    def get_term_frequency_pair(words, n_top):
        c = Counter()
        for x in words:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1
        return c.most_common(n_top)

    def generate(tfp):
        c = (
            WordCloud().add("", tfp, word_size_range=[20, 100], shape=SymbolType.ROUND_RECT).set_global_opts(
                title_opts=opts.TitleOpts(title=title))
        ).render(os.path.join('../html/', title + '词云.html'))

    file_path = os.path.join('../doc/', title + '.csv')
    words = get_words(file_path)
    tfp = get_term_frequency_pair(words, n_top)
    generate(tfp)


def main():
    title=input('输入要统计词云的文件名:')
    generate_HTML_wordcloud(title)
    #print(wc)

if __name__ == '__main__':
    main()
