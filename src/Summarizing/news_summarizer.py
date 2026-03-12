import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from configuration.config import OPENAI_API_KEY
from NewsParsing.news_finder import NewsFinder

AGGREGATE_PROMPT_TEMPLATE = '''
[ROLE]
당신은 IT 산업 전문 분석가입니다.

[IMPORTANT]
- 반드시 한국어로 작성하십시오.
- HTML 형식으로만 출력하십시오.
- 기존 리포트를 유지하면서 새로운 정보를 통합하십시오.

[OBJECTIVE]
기존 동향 리포트를 유지하면서 새로운 뉴스 데이터를 반영하여 업데이트하십시오.

-----------------------------------------------------------
[뉴스 주제]
{}

-----------------------------------------------------------
[기존 리포트]
{}

-----------------------------------------------------------
[추가 뉴스(JSON)]
{}

-----------------------------------------------------------
[작업]

1. 새로운 뉴스에서 등장하는 기술, 기업, 사건을 분석하십시오.
2. 기존 리포트와 비교하여 다음을 판단하십시오.

- 새로운 트렌드 등장 여부
- 기존 트렌드 강화 여부
- 산업 변화 신호

3. 기존 리포트를 유지하면서 필요한 부분만 업데이트하십시오.

4. 불필요한 반복은 제거하십시오.

[OUTPUT]

업데이트된 전체 HTML 리포트를 출력하십시오.
'''

FINAL_PROMPT_TEMPLATE = '''
당신은 IT 산업 전문 분석가입니다.

반드시 한국어로, 완전한 HTML 문서 형식으로만 응답하십시오.
JSON, Markdown, 설명문은 출력하지 마십시오.
-----------------------------------------------------------
주제:
{}
-----------------------------------------------------------
앞선 뉴스 요약 :
{}

-----------------------------------------------------------
뉴스 데이터(JSON):
{}

-----------------------------------------------------------
뉴스 데이터가 너무 크기 때문에 여러 번들로 나누어 앞쪽 파트들을 요약한 내용이 함께 제공되었습니다.
위 뉴스 데이터와 요약을 바탕으로 HTML 형식의 IT 동향 분석 리포트를 작성하십시오.

리포트에는 반드시 다음 섹션이 포함되어야 합니다:
1. 리포트 제목
2. 개요
3. 주요 기술 및 기업
4. 핵심 트렌드 분석
5. 산업 변화 신호
6. 개발자 관점 해설
7. 향후 전망

요구사항:
- 입력 뉴스에 근거하여 분석할 것
- 중복 기사는 하나의 흐름으로 묶어 정리할 것
- 단순 요약이 아니라 기술적·산업적 의미를 해설할 것
- HTML5 semantic tag(section, article, ul, li, p, h1~h3 등)를 사용할 것
- `<html>`, `<head>`, `<meta charset="UTF-8">`, `<title>`, `<body>`를 포함할 것
- 필요 시 `<style>` 태그를 포함하되 외부 CSS/JS는 사용하지 말 것

출력은 반드시 HTML만 작성하십시오.
'''

class NewsSummarizer :

    def __init__(self) :
        self.finder = NewsFinder(display_size=50, sort_criteria='sim')
        self.BUNDLE_SIZE = 5

        topic_list = None
        with open("./src/news_topics.txt", mode="r", encoding='utf-8') as f :
            topic_list = f.readlines()
        self.topics = []
        for topic in topic_list :
            self.topics.append(topic.strip("\n"))
    
    def summarize_news(self) :
        articles = self.search_news_for_topics()
        article_bundles = []
        
        for i in range(0, len(articles), self.BUNDLE_SIZE) :
            article_bundles.append(articles[i:(min(i+self.BUNDLE_SIZE, len(articles)))])
        prior_summary = ''
        for i in range(0, len(article_bundles)) :
            prompt = self.form_prompt(articles=article_bundles[i], prior_summary=prior_summary, is_final= (i == (len(article_bundles)-1)))
            report = self.ask_LLM(prompt=prompt)
            prior_summary = report
        return report

    def ask_LLM(self, prompt : str) :
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.responses.create(
            model="gpt-5.4",
            input=prompt
        )
        return response.output_text

    def form_prompt(self, articles : list, prior_summary : str, is_final : bool) :
        import json
        
        article_string = json.dumps(articles)

        template = FINAL_PROMPT_TEMPLATE if is_final else AGGREGATE_PROMPT_TEMPLATE

        formatted_prompt = template.format(
            ",".join(self.topics), prior_summary, article_string
        )
        return formatted_prompt

    def search_news_for_topics(self) :
        articles = []
        for topic in self.topics :
            articles.extend(self.finder.search_news(topic=topic, page=1))
        return articles

if __name__ == "__main__" :
    summarizer = NewsSummarizer()
    print(summarizer.summarize_news())