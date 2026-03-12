import requests
import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), './src'))

from configuration.config import NAVER_API_CLIENT_ID, NAVER_API_CLIENT_SECRET, NAVER_NEW_SEARCH_URL

queries = ["AI", "Agent AI", "SW", "바이브 코딩", "Claude", "Chat GPT", "Gemini"]

for query in queries :
    response = requests.get(url=NAVER_NEW_SEARCH_URL,
        params= {
            "query" : query,
            "display" : 100,
            "start" : 1,
            "sort" : 'sim'
        },
        headers= {
            "X-Naver-Client-Id" : NAVER_API_CLIENT_ID,
            "X-Naver-Client-Secret" : NAVER_API_CLIENT_SECRET
        })
    
    articles = json.loads(response.text)['items']
    for article in articles :
        with open(file="./candidates.txt", mode="a") as f :
            f.write(article['originallink'] + "\n")
            f.flush()
    