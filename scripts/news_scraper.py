import requests
from bs4 import BeautifulSoup
from newspaper import Article
from pet.models import NewsScrap

url = 'https://news.google.com/rss/search?q=%EB%B0%98%EB%A0%A4%EB%8F%99%EB%AC%BC&hl=ko&gl=KR&ceid=KR%3Ako'
res = requests.get(url)
web = res.content
soup = BeautifulSoup(web, features='xml')
items = soup.find_all('item')
def run():
    
        
    for item in items:
        try:
            link = item.find('link').text
            #article_list.append(link)
            # print(news_link)
            article = Article(link)
            article.download()
            article.parse()
            news_img_url = article.top_image
            news_title = article.title
            # news_content = post_list 에 나올 본문 요약본
            # news_content = article.text[:150]
            # news_text(본문) 
            news_text = article.text
            news_authors = article.authors
            news_link = article.url
            print(news_link)
            news_postdate = article.publish_date
            # HOSTNO = {
            #         'https://news.google.com/__i/rss/rd/articles/CBMiLmh0dHBzOi8vd3d3LmNuZXQuY28ua3Ivdmlldy8_bm89MjAyMjEyMjIwOTU1MTLSAQA?oc=5',
                    
            #         }
            db_link_count = NewsScrap.objects.filter(news_link__iexact=news_link).count()
            print(db_link_count)
            if db_link_count == 0 and news_link != 'https://news.google.com/__i/rss/rd/articles/CBMiLmh0dHBzOi8vd3d3LmNuZXQuY28ua3Ivdmlldy8_bm89MjAyMjEyMjIwOTU1MTLSAQA?oc=5': 
                NewsScrap( news_link=news_link, news_top_image=news_img_url, news_title=news_title,news_authors=news_authors, news_content=news_text, news_udate=news_postdate).save()
                print("저장")
                
            else :
                print("중복존재")
        except Exception as e:
            continue
        # print('---------------------------------')
        # print(f"{'top_image'}:",top_image)
        # print(f"{'title'}:",title)
        # print(f"{'content'}:",content)
        # print(f"{'news_link'}:",news_link)
        # print('---------------------------------')