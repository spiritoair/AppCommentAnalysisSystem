import csv
from app import util

app_word = {}


def run():
    filename = 'c.csv'
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)
        for x in data:
            # print(x)
            s = x[5]
            appid = x[1]
            if appid not in app_word.keys():
                app_word[appid] = {}
            l = util.word_segment(s)
            for word in l:
                if len(word) <2:
                    continue
                if word in app_word[appid].keys():
                    app_word[appid][word] += 1
                else:
                    app_word[appid][word] = 1
            like = util.get_sentence_sentiment(l)
            x[6] = like
        f.close()
        with open('word_segment.csv','w+',encoding='utf-8') as f:
            writer = csv.writer(f)
            for aw in app_word:
                for word in app_word[aw]:
                    writer.writerow([aw,word,app_word[aw][word]])
            f.close()
        with open(filename,'w+',encoding='utf-8') as f:
            writer = csv.writer(f)
            for r in data:
                writer.writerow(r)
            f.close()


if __name__ == '__main__':
    run()
