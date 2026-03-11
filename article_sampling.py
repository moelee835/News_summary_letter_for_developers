import requests

if __name__ == "__main__" :
    urls = None
    with open("./candidates.txt", mode="r") as f :
        urls = f.readlines()
    urls = list(map(lambda i : i[:len(i)-1], urls))
    
    for url in urls :
        from urllib.parse import urlparse
        from requests.exceptions import SSLError
        parsed = urlparse(url)
        netloc_units = parsed.netloc.split(".")
        site_name = netloc_units[(1 if len(netloc_units) > 2 else 0)]
        try :
            plain_html = requests.get(url=url).text
            with open(f"./article_html/{site_name}.html", "w", encoding="utf-8") as f:
                f.write(plain_html)
                f.flush()
        except SSLError as e :
            print(e)
