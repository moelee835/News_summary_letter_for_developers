# AI News Summary Letter for Developers

네이버 뉴스 검색 API를 활용해 AI 관련 뉴스를 수집하고, OpenAI GPT로 분석하여 개발자를 위한 HTML 동향 리포트를 자동 생성하는 파이프라인입니다.

## 프로젝트 구조

```
ai_news/
├── src/
│   ├── configuration/
│   │   └── config.py              # 환경변수 기반 API 키 설정
│   ├── NewsParsing/
│   │   ├── news_finder.py         # 뉴스 검색 및 크롤링 핵심 모듈
│   │   └── news_finder_test.py    # NewsFinder 동작 확인 스크립트
│   ├── Summarizing/
│   │   └── news_summarizer.py     # 뉴스 수집 → LLM 요약 → HTML 리포트 생성
│   └── news_topics.txt            # 뉴스 검색 주제 목록
├── article_html/                  # 사이트별 기사 HTML 샘플 (선택자 분석용)
├── article_sampling.py            # candidates.txt URL 기반 HTML 샘플 수집
├── news_link_sampling.py          # 다중 쿼리로 뉴스 URL 수집 → candidates.txt 저장
├── candidates.txt                 # 크롤링 대상 뉴스 기사 URL 목록
└── var_setting.cmd                # Windows 환경변수 설정 스크립트
```

## 주요 기능

- **뉴스 검색**: 네이버 뉴스 검색 API로 키워드 기반 기사 URL 수집
- **다중 주제 검색**: `news_topics.txt`에 정의된 주제별로 일괄 검색
- **사이트별 크롤링**: 180개 이상 뉴스 사이트에 대한 BeautifulSoup CSS 선택자 정의
- **에러 사이트 제외**: `SKIPPED_SELECTORS`로 크롤링 불가 도메인 자동 스킵
- **LLM 요약**: 수집된 기사를 번들 단위로 OpenAI GPT에 전달하여 점진적으로 요약
- **HTML 리포트 생성**: IT 동향 분석 리포트를 완전한 HTML 문서로 출력

## 환경 설정

### 필수 환경변수

```bash
NAVER_API_CLIENT_ID=<네이버 개발자 센터 클라이언트 ID>
NAVER_API_CLIENT_SECRET=<네이버 개발자 센터 클라이언트 Secret>
OPENAI_API_KEY=<OpenAI API 키>
```

Windows 환경에서는 `var_setting.cmd`를 편집하여 실행하거나, 직접 시스템 환경변수로 등록합니다.

### 의존 패키지 설치

```
pip install requests beautifulsoup4 openai
```

## 사용 방법

### 1. HTML 리포트 자동 생성 (전체 파이프라인)

```bash
python -m src.Summarizing.news_summarizer
```

`src/news_topics.txt`의 주제별로 뉴스를 수집하고, GPT가 분석한 HTML 리포트를 stdout으로 출력합니다.

### 2. 뉴스 URL 일괄 수집

```bash
python news_link_sampling.py
```

`AI`, `Agent AI`, `SW`, `바이브 코딩`, `Claude`, `Chat GPT`, `Gemini` 등 사전 정의된 쿼리로 뉴스 URL을 수집해 `candidates.txt`에 저장합니다.

### 3. HTML 샘플 수집 (선택자 분석용)

```bash
python article_sampling.py
```

`candidates.txt`의 각 URL에 GET 요청 후 `article_html/<도메인>.html`로 저장합니다.

### 4. NewsFinder API 사용

```python
from src.NewsParsing.news_finder import NewsFinder

finder = NewsFinder(display_size=100)
articles = finder.search_news(topic="AI Agent", page=1)
# 반환값: [{"title": ..., "link": ..., "pubDate": ..., "content": ...}, ...]
```

### 5. 크롤링 선택자 참조

```python
from src.NewsParsing.news_finder import SITE_SELECTORS, SKIPPED_SELECTORS
# SITE_SELECTORS["mk.co.kr"] -> "div.news_cnt_detail_wrap"
# SKIPPED_SELECTORS -> 크롤링 불가 도메인 집합
```

## 검색 주제 설정

`src/news_topics.txt`에 한 줄씩 주제를 입력합니다.

```
AI 에이전트
생성형 AI
대형 언어 모델
AI 인프라
AI 개발 도구
클라우드 컴퓨팅
...
```

## 지원 뉴스 사이트

매일경제, 한국경제, 전자신문, 뉴스핌, 디지털데일리, 연합뉴스, KBS, 동아일보, 서울신문, 머니투데이 등 180개 이상의 국내외 뉴스 사이트를 지원합니다.

크롤링이 불가하여 제외된 사이트(`SKIPPED_SELECTORS`): `biz.chosun.com`, `chosun.com`, `hani.co.kr`, `khan.co.kr`, `nytimes.com` 등 20개
