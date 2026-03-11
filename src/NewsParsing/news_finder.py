import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from configuration.config import NAVER_API_CLIENT_ID, NAVER_API_CLIENT_SECRET, OPENAI_API_KEY, NAVER_NEW_SEARCH_URL

import requests
import json

# 크롤링 제외 도메인 (에러 페이지 반환 확인됨)
SKIP_DOMAINS = [
    "byline.network",
    "heraldcorp.com",
    "dt.co.kr",
    "nytimes.com",
    "breaknews.com",
]

# 뉴스 사이트별 기사 본문 CSS 선택자
# selector: BeautifulSoup select() 메서드에 전달할 CSS 선택자 문자열
SITE_SELECTORS = {
    "mk.co.kr":             {"selector": "div.article_txt"},
    "hankooki.com":         {"selector": "article#article-view-content-div"},
    "etnews.com":           {"selector": "div#articleBody"},
    "newspim.com":          {"selector": "section.contents"},
    "newdaily.co.kr":       {"selector": "div#article_conent"},  # 원본 HTML의 오타 그대로
    "ddaily.co.kr":         {"selector": "div.article_content"},
    "inews24.com":          {"selector": "article#articleBody"},
    "edaily.co.kr":         {"selector": "div.news_body"},
    "sportschosun.com":     {"selector": "div#articleBody"},
    "newstown.co.kr":       {"selector": "article.grid.body"},
    "financialpost.co.kr":  {"selector": "article#article-view-content-div"},
    "enewstoday.co.kr":     {"selector": "article#article-view-content-div"},
    "yna.co.kr":            {"selector": "article.story-news"},
    "thefirstmedia.net":    {"selector": "article#article-view-content-div"},
    "smedaily.co.kr":       {"selector": "article#article-view-content-div"},
    "ftoday.co.kr":         {"selector": "article#article-view-content-div"},
    "itdaily.kr":           {"selector": "article#article-view-content-div"},
    "ebn.co.kr":            {"selector": "article#article-view-content-div"},
    "seoulwire.com":        {"selector": "div#article-view-content-div"},
    "hansbiz.co.kr":        {"selector": "article#article-view-content-div"},
    "wowtv.co.kr":          {"selector": "div#divNewsContent"},
    "aitimes.com":          {"selector": "article"},
    "sidae.com":            {"selector": "div.article-body"},
    "pinpointnews.co.kr":   {"selector": "article#article-view-content-div"},
    "hellot.net":           {"selector": "div#news_body_area"},
    "ziksir.com":           {"selector": "article#article-view-content-div"},
    "megaeconomy.co.kr":    {"selector": "div#viewConts"},
    "koit.co.kr":           {"selector": "article#article-view-content-div"},
    "kdpress.co.kr":        {"selector": "article#article-view-content-div"},
    "kbs.co.kr":            {"selector": "div#cont_newstext"},
    "cstimes.com":          {"selector": "article.grid.body"},
    "swtvnews.com":         {"selector": "div#viewConts"},
    "fnnews.com":           {"selector": "div#article_content"},
    "epnc.co.kr":           {"selector": "article#article-view-content-div"},
    "newswell.co.kr":       {"selector": "article"},
    "tvchosun.com":         {"selector": "article#ui_contents"},
    "venturesquare.net":    {"selector": "div.entry-content"},
    "fetv.co.kr":           {"selector": "div#news_body_area"},
    "dailysecu.com":        {"selector": "div#article-view-content-div"},
    "financialreview.co.kr":{"selector": "article.grid.body"},
    "popcornnews.net":      {"selector": "article#article-view-content-div"},
    "sisacast.kr":          {"selector": "article"},
    "datanet.co.kr":        {"selector": "div#article-view-content-div"},
    "gamemeca.com":         {"selector": "div.article"},
    "seoul.co.kr":          {"selector": "div#cont_newstext"},
    "inven.co.kr":          {"selector": "div.contentBody"},
    "bizwnews.com":         {"selector": "article#article-view-content-div"},
    "hbnpress.com":         {"selector": "div#viewConts"},
    "efnews.co.kr":         {"selector": "article.grid.body"},
    "donga.com":            {"selector": "div.view_body"},
    "socialvalue.kr":       {"selector": "div#viewConts"},
    "ggilbo.com":           {"selector": "article#article-view-content-div"},
    "hellodd.com":          {"selector": "article#article-view-content-div"},
    "news2day.co.kr":       {"selector": "div.article_view_sec"},
    "mt.co.kr":             {"selector": "article#articleBody"},
    "metroseoul.co.kr":     {"selector": "div.left-article-txt"},
    "kado.net":             {"selector": "div.article-body"},
    "aving.net":            {"selector": "article#article-view-content-div"},
    "asiatoday.co.kr":      {"selector": "div.article_body"},
    "busan.com":            {"selector": "div.article_content"},
    "bloter.net":           {"selector": "article#article-view-content-div"},
    "dailian.co.kr":        {"selector": "div.article"},
    "newsis.com":           {"selector": "div.articleView"},
    "economist.co.kr":      {"selector": "div#articleBody"},
    "gamefocus.co.kr":      {"selector": "div#view_content"},
}

class NewsFinder :
    def __init__(self, display_size, sort_criteria = 'sim') :
        self.display_size = display_size
        if(sort_criteria not in ('sim', 'date')) :
            raise ValueError('invalid sorting criteria. expect -> [\'sim\' or \'date\']')
        
        self.criteria = sort_criteria
    
    def search_news(self, topic, page) :
        response = requests.get(url=NAVER_NEW_SEARCH_URL,
            params= {
                "query" : topic,
                "display" : self.display_size,
                "start" : (page - 1) * self.display_size + 1,
                "sort" : self.criteria
            },
            headers= {
                "X-Naver-Client-Id" : NAVER_API_CLIENT_ID,
                "X-Naver-Client-Secret" : NAVER_API_CLIENT_SECRET
            })
        self.parse_and_crawl(response_text= response.text)

    def parse_and_crawl(self, response_text) :
        article_list = list(map(lambda i : i['originallink'], json.loads(response_text)['items']))
        with open("./candidates.txt", "+a") as f :
            for article in article_list :
                f.write(article + "\n")
            f.flush()
        return
        result = []
        for article_sh in article_list :
            article = dict()
            article['title'] = article_sh['title']
            article['pubDate'] = article_sh['pubDate']
            article['content'] = self.crawl(article_sh['originallink'])
            result.append()
    
    
    def crawl(self, url) :
        from bs4 import BeautifulSoup
        html = requests.get(url=url).text
        print(html)
        crawler = BeautifulSoup()

if __name__ == '__main__' :
    # from bs4 import BeautifulSoup
    # # "https://www.news2day.co.kr/article/20260311500226"
    # # response = requests.get(url="http://www.edaily.co.kr/news/newspath.asp?newsid=04608406645382336")
    
    # response = requests.get(url="https://www.news2day.co.kr/article/20260311500226")
    # soup = BeautifulSoup(response.text, "html.parser")
    # news_body = soup.select(".news_body")

    # print(news_body)
    finder = NewsFinder(display_size=100)
    for page in range(2) :
        finder.search_news(topic="AI Agent", page=1)
    