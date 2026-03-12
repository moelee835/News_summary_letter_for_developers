from news_finder import NewsFinder

if __name__ == '__main__' :
    finder = NewsFinder(display_size=100, sort_criteria='sim')
    articles = finder.search_news(topic="AI", page=1)
    print(articles[0]['content'])