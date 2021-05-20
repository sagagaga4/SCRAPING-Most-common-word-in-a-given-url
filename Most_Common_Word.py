
from urllib.request import urlopen
from html.parser import HTMLParser
import json
import collections


class WordsParser(HTMLParser):
    # מחסן תגיות לחיפוש

    search_tags = ['p', 'div', 'span', 'a', 'h1', 'h2', 'h2', 'h3', 'h4']
    current_tag = ''
    # רשימה של המילים הכי נפוצות

    common_words = {}

    def handle_starttag(self, tag, attr):
        self.current_tag = tag

    def handle_data(self, data):
        # התאמה בין תגית נוכחית לתגית חיפוש

        if self.current_tag in self.search_tags:
            # לולאה של חיפוש מילה

            for word in data.strip().split():
                # פילטר לתוצאה של אותיות בלבד

                common_word = word.lower()
                common_word = common_word.replace('.', '')
                common_word = common_word.replace(':', '')
                common_word = common_word.replace(',', '')
                common_word = common_word.replace('"', '')

                # פילטר למילים עד שתי אותיות

                if (
                    len(common_word) > 2 and
                    common_word not in ['the', 'and', 'all'] and
                    common_word[0].isalpha()
                ):

                    try:
                        # ספירת חזרתיות של מילה נפוצה

                        self.common_words[common_word] += 1

                    except:
                        # אחסון מילה נפוצה

                        self.common_words.update({common_word: 1})


url_enter = input(
    "Enter URL adress you would like to scrape most common word out of:")

if __name__ == '__main__':
    url = url_enter
    response = urlopen(url)
    html = response.read().decode('utf-8', errors='ignore')
    words_parser = WordsParser()
    words_parser.feed(html)
    words_count = collections.Counter(words_parser.common_words)
    most_common = words_count.most_common(25)

    for word, count in most_common:
        print(word, str(count) + ' times', sep=": ")
