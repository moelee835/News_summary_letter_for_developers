import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from configuration.config import NAVER_API_CLIENT_ID, NAVER_API_CLIENT_SECRET, OPENAI_API_KEY, NAVER_NEW_SEARCH_URL

import requests
import json

SITE_SELECTORS = {
    "4th.kr": "#article-view-content-div",
    "aflnews.co.kr": "div.article-body",
    "aitimes.com": "#article-view-content-div",
    "aitimes.kr": "#article-view-content-div",
    "ajunews.com": "#articleBody",
    "akomnews.com": "#news_body_area",
    "apnews.kr": "#article-view-content-div",
    "asiaa.co.kr": "#article-view-content-div",
    "asiatoday.co.kr": "#font",
    "beyondpost.co.kr": "#articleBody",
    "biotimes.co.kr": "#article-view-content-div",
    "biz.newdaily.co.kr": "#article_conent",
    "bizwnews.com": "#article-view-content-div",
    "bloter.net": "#article-view-content-div",
    "bokuennews.com": "#news_body_area",
    "bosa.co.kr": "#article-view-content-div",
    "busan.com": "div.article_content",
    "ccdn.co.kr": "#article-view-content-div",
    "ccnnews.co.kr": "div.auto-article.auto-dl04",
    "cfnews.kr": "div.con",
    "cn.asiatoday.co.kr": "div.photo_news_box",
    "cnbnews.com": "#news_body_area",
    "cstimes.com": "#article-view-content-div",
    "dailian.co.kr": "div.article",
    "daily.hankooki.com": "#article-view-content-div",
    "dailypop.kr": "#article-view-content-div",
    "dailysecu.com": "#article-view-content-div",
    "datanet.co.kr": "#article-view-content-div",
    "ddaily.co.kr": "div.article_content",
    "ddanzi.com": "div.pop-body.normal",
    "dealsite.co.kr": "div.rnmc-right.rnmc-right1",
    "digitalbizon.com": "#article-view-content-div",
    "digitalchosun.dizzo.com": "div.cont_body",
    "digitaltoday.co.kr": "#article-view-content-div",
    "dnews.co.kr": "div.text",
    "doctorstimes.com": "#article-view-content-div",
    "donga.com": "section.news_view",
    "ebn.co.kr": "#article-view-content-div",
    "econotimes.com": "article.viewArticle",
    "econovill.com": "#article-view-content-div",
    "edaily.co.kr": "div.news_body",
    "edu.donga.com": "#article-view-content-div",
    "efnews.co.kr": "#article-view-content-div",
    "enewstoday.co.kr": "#article-view-content-div",
    "epnc.co.kr": "#article-view-content-div",
    "etnews.com": "#articleBody",
    "etoday.co.kr": "div.articleView",
    "fetv.co.kr": "#news_body_area",
    "financialpost.co.kr": "#article-view-content-div",
    "financialreview.co.kr": "#article-view-content-div",
    "fnnews.com": "#article_content",
    "fntimes.com": "#articleBody",
    "fntoday.co.kr": "#article-view-content-div",
    "fortunekorea.co.kr": "#article-view-content-div",
    "ftoday.co.kr": "#article-view-content-div",
    "g-enews.com": "div.vtxt.detailCont",
    "game.dailyesports.com": "div.vcon_con.detailCont",
    "gamefocus.co.kr": "div.detail_view",
    "gamemeca.com": "div.article",
    "gametoc.co.kr": "#article-view-content-div",
    "gamevu.co.kr": "#article-view-content-div",
    "getnews.co.kr": "#article-view-content-div",
    "gg.newdaily.co.kr": "#article_conent",
    "gnmaeil.com": "#articleBody",
    "gokorea.kr": "#article-view-content-div",
    "gukjenews.com": "#article-view-content-div",
    "hankyung.com": "#articletxt",
    "hansbiz.co.kr": "#article-view-content-div",
    "hbnpress.com": "#viewConts",
    "health.chosun.com": "#news_body_id",
    "hellodd.com": "#article-view-content-div",
    "hellot.net": "#news_body_area",
    "hitnews.co.kr": "#article-view-content-div",
    "inews24.com": "#articleBody",
    "insightkorea.co.kr": "#article-view-content-div",
    "inthenews.co.kr": "#news_body_area",
    "inven.co.kr": "#imageCollectDiv",
    "irobotnews.com": "#article-view-content-div",
    "issuenbiz.com": "#article-view-content-div",
    "it-b.co.kr": "#article-view-content-div",
    "it.chosun.com": "#article-view-content-div",
    "it.donga.com": "div.article",
    "itbiznews.com": "#article-view-content-div",
    "itdaily.kr": "#article-view-content-div",
    "itworld.co.kr": "div.article-column__content",
    "jbnews.com": "#article-view-content-div",
    "jeonmae.co.kr": "#article-view-content-div",
    "jndn.com": "#content",
    "jnilbo.com": "#article-view-content-div",
    "joongangenews.com": "#article-view-content-div",
    "joongdo.co.kr": "article.hd-news-info",
    "joynews24.com": "#articleBody",
    "kdpress.co.kr": "#article-view-content-div",
    "khgames.co.kr": "#article-view-content-div",
    "klnews.co.kr": "#article-view-content-div",
    "koit.co.kr": "#article-view-content-div",
    "koreajoongangdaily.joins.com": "div.article_body_container",
    "koreatimes.co.kr": "div.EditorContents_contents__i9nZI.light",
    "kpenews.com": "div.article-body",
    "ktnews.com": "#article-view-content-div",
    "kyosu.net": "#article-view-content-div",
    "lawtimes.co.kr": "#article-view-content-div",
    "m-economynews.com": "#news_body_area",
    "m-i.kr": "#article-view-content-div",
    "magazine.hankyung.com": "#magazineView",
    "mdilbo.com": "div.tag_foot_article.border-dark",
    "mediafine.co.kr": "#article-view-content-div",
    "medicaltimes.com": "div.view_cont.ck-content",
    "medigatenews.com": "div.newsinfo",
    "megaeconomy.co.kr": "#viewConts",
    "metroseoul.co.kr": "div.row.article-txt-contents",
    "mk.co.kr": "div.news_cnt_detail_wrap",
    "mt.co.kr": "#articleView",
    "mtnews.net": "#article-view-content-div",
    "nbntv.kr": "#article-view-content-div",
    "news.einfomax.co.kr": "#article-view-content-div",
    "news.kbs.co.kr": "#cont_newstext",
    "news.mtn.co.kr": "article",
    "news.sbs.co.kr": "div.text_area",
    "news.tvchosun.com": "div.text-box",
    "news.unn.net": "#article-view-content-div",
    "news1.kr": "article.col-lg-7.article-padding-lg-right",
    "news2day.co.kr": "div.view_con_wrap",
    "newscj.com": "#article-view-content-div",
    "newsfc.co.kr": "#article-view-content-div",
    "newsian.co.kr": "#article-view-content-div",
    "newsis.com": "div.viewer",
    "newspim.com": "#news-contents",
    "newstown.co.kr": "#_article",
    "newsway.co.kr": "#view-text",
    "newswell.co.kr": "#article-view-content-div",
    "newswhoplus.com": "#article-view-content-div",
    "newsworks.co.kr": "#articleBody",
    "nocutnews.co.kr": "#pnlContent",
    "ohmynews.com": "div.text",
    "paxetv.com": "#article-view-content-div",
    "pinpointnews.co.kr": "#article-view-content-div",
    "popcornnews.net": "#article-view-content-div",
    "ppss.kr": "#article-view-content-div",
    "pressman.kr": "#article-view-content-div",
    "public25.com": "#article-view-content-div",
    "rapportian.com": "#article-view-content-div",
    "rightknow.co.kr": "#article-view-content-div",
    "sedaily.com": "#ttsBody",
    "segye.com": "article.viewBox2",
    "seoul.co.kr": "div.viewContent.body19",
    "seoulwire.com": "#article-view-content-div",
    "shinailbo.co.kr": "#article-view-content-div",
    "sidae.com": "div.article-body",
    "siminilbo.co.kr": "#viewConts",
    "sisacast.kr": "#article-view-content-div",
    "sisaon.co.kr": "#article-view-content-div",
    "slownews.kr": "div.kt-infobox-textcontent",
    "smartbizn.com": "#article-view-content-div",
    "smarttimes.co.kr": "#article-view-content-div",
    "smedaily.co.kr": "#article-view-content-div",
    "socialvalue.kr": "#viewConts",
    "sportschosun.com": "div.news_text",
    "sportsworldi.com": "article.viewBox2",
    "swtvnews.com": "#viewConts",
    "techm.kr": "#article-view-content-div",
    "the-pr.co.kr": "#article-view-content-div",
    "thefirstmedia.net": "#article-view-content-div",
    "thegolftimes.co.kr": "#article-view-content-div",
    "tokenpost.kr": "div.article_content",
    "topstarnews.net": "div.article-view-page.clearfix",
    "us.aving.net": "#article-view-content-div",
    "vegannews.co.kr": "#news_body_area",
    "venturesquare.net": "div.entry-content",
    "veritas-a.com": "#article-view-content-div",
    "view.asiae.co.kr": "#txt_area",
    "vogue.co.kr": "div.post_content.common_content",
    "wikileaks-kr.org": "#article-view-content-div",
    "wikitree.co.kr": "#wikicon",
    "wowtv.co.kr": "#divNewsContent",
    "yna.co.kr": "article.story-summary",
    "youthdaily.co.kr": "#news_bodyArea",
    "ytn.co.kr": "#CmAdContent",
    "zdnet.co.kr": "#articleBody",
    "ziksir.com": "#article-view-content-div",
}

SKIPPED_SELECTORS = {
    "biz.chosun.com",
    "biz.heraldcorp.com",
    "biz.sbs.co.kr",
    "breaknews.com",
    "byline.network",
    "chosun.com",
    "dongascience.com",
    "dt.co.kr",
    "economist.co.kr",
    "ekn.kr",
    "hani.co.kr",
    "heraldmuse.com",
    "joongboo.com",
    "khan.co.kr",
    "koreaherald.com",
    "news.jtbc.co.kr",
    "newsprime.co.kr",
    "nytimes.com",
    "platum.kr",
    "thebell.co.kr",
    "thisisgame.com",
}



class NewsFinder :
    def __init__(self, display_size : int, sort_criteria : str = 'sim') :
        self.display_size = display_size
        if(sort_criteria not in ('sim', 'date')) :
            raise ValueError('invalid sorting criteria. expect -> [\'sim\' or \'date\']')
        
        self.criteria = sort_criteria
    
    def search_news(self, topic : str, page : int) :
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
        return self.parse_and_crawl(response_text= response.text)

    def parse_and_crawl(self, response_text) :
        article_list = json.loads(response_text)['items']
        # with open("./candidates.txt", "+a") as f :
        #     for article in article_list :
        #         f.write(article + "\n")
        #     f.flush()
        
        article_collection = []
        for article_summary in article_list :
            article = dict()
            article['title'] = article_summary['title']
            article['link'] = article_summary['originallink']
            article['pubDate'] = article_summary['pubDate']
            article['content'] = self.crawl(article_summary['originallink'])
            if article['content'] is not None :
                article_collection.append(article)
        
        return article_collection
    
    def crawl(self, url) :
        from bs4 import BeautifulSoup
        html = None
        try :
            html = requests.get(url=url).text
        except Exception as e :
            return None

        crawler = BeautifulSoup(html, "html.parser")
        selector = self.get_selector_for_site(url=url)
        
        if selector is None :
            return None
        
        elements = crawler.select(selector=selector)
        return "\n".join(e.get_text() for e in elements)

    def get_selector_for_site(self, url : str) -> str :
        site_name = self.get_site_name(url)
        if site_name not in SITE_SELECTORS.keys() :
            return None
        return SITE_SELECTORS[site_name]
    
    def get_site_name(self, url) :
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        netlocs = parsed_url.netloc.split(".")
        
        if netlocs[0] == 'www' :
            netlocs = netlocs[1:]
        
        return '.'.join(netlocs)
