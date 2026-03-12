import requests



if __name__ == "__main__" :
    urls = None
    with open("./candidates.txt", mode="r", encoding='utf-8') as f :
        urls = f.readlines()
    urls = list(map(lambda i : i[:len(i)-1], urls))
    
    for url in urls :
        from urllib.parse import urlparse
        from requests.exceptions import SSLError
        parsed = urlparse(url)
        netloc_units = parsed.netloc.split(".")
        if netloc_units[0] == 'www' :
            netloc_units = netloc_units[1:]
        print(netloc_units)
        site_name = '.'.join(netloc_units)
        try :
            plain_html = requests.get(url=url).text
            with open(f"./article_html/{site_name}.html", "w", encoding="utf-8") as f:
                f.write(plain_html)
                f.flush()
        except Exception as e :
            print(e)
