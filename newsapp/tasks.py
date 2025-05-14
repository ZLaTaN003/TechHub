import os
import requests
from datetime import datetime,timedelta,date
import json
import time
from celery import shared_task


@shared_task()
def news_data():
    from .models import Article, Domain

    newskey = os.getenv("newskey","")
    params = {
        "apiKey": newskey,
        "from": date.today() - timedelta(days=1),
        "to":  date.today() - timedelta(days=1),
        "q": "technology",
        "language": "en",
        "pageSize": 25,
        "page": 1,
        "sortBy": "relavancy",
    }
    response = requests.get("https://newsapi.org/v2/everything", params=params)

    articles = response.json()["articles"]

    for article in articles:
        author = article["author"]
        title = article["title"]
        short_description = article["description"]
        source_link = article["url"]
        image_url = article["urlToImage"]
        published = datetime.fromisoformat(article["publishedAt"])


        if Article.objects.filter(title=title).exists():  # Prevent duplicate articles
            continue
        

        time.sleep(10)
        prompt = "Provide a detailed summary for the following Article Link,Give the Summary directly in paragraph don't format the text as bold or anything."
        summary = generate_summary(source_link,prompt=prompt)


        article = Article(
            title=title,
            short_description=short_description,
            image_url=image_url,
            post_published=published,
            source_link=source_link,
            author=author,
            summary=summary,
        )
        print("its made")
        get_domain(title,Domain,article)

        article.save()

    

    

def generate_summary(target,prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    api_key = os.getenv("gem_api_key","")
    params = {"key": api_key}
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    },
                    {"text": target},
                ]
            }
        ]
    }
    response = requests.post(
        url, params=params, headers=headers, data=json.dumps(data)
    )
    summary = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    return summary


def get_domain(target_title,Domain,article):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    api_key = os.getenv("gem_api_key","")
    params = {"key": api_key}
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Provide one word for the category of the following title, about which domain does the title belong only one category word should be given."
                    },
                    {"text": target_title},
                ]
            }
        ]
    }
    response = requests.post(
        url, params=params, headers=headers, data=json.dumps(data)
    )
    domain = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    tag,created = Domain.objects.get_or_create(category=domain)
    article.domain = tag


@shared_task()
def products_data():
    from .models import Product
  
    try:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Host": "api.producthunt.com",
            "Authorization": os.getenv("producthunt_key",""),
            "User-Agent": "curl/8.11.1", #normal useragent was not working for some reason
        }

        url = "https://api.producthunt.com/v2/api/graphql"
        today = datetime.today().date()

        query = f"""
    query Posts {{
        posts(order: VOTES, first: 20, postedAfter: "{today}") {{
            nodes {{
                id
                name
                description
                media {{
                    type
                    url
                }}
                thumbnail {{
                    type
                    url
                }}
                tagline
                featuredAt
                createdAt
                votesCount
                topics {{
                    totalCount
                    nodes {{
                        name
                    }}
                }}
                productLinks {{
                    type
                    url
                }}
            }}
        }}
    }}
    """


        response = requests.post(url,headers=headers,json={"query":query})

        print(response.status_code,"got the products")
        posts = response.json()["data"]["posts"]["nodes"]

        for post in posts:
            name = post["name"]
            des = post["description"]
            tagline = post["tagline"]
            featuredat = datetime.fromisoformat(post["featuredAt"])
            media = post["media"][0]["url"]
            thumbnail = post["thumbnail"]["url"]
            votes = post["votesCount"]
            topic = post["topics"]["nodes"][0]["name"]
            link = post["productLinks"][0]["url"]




            prompt = "You are an expert at giving Summaries of the problems that Software products are trying to Solve. Give the Detailed Summary for the following product in about 700 characters in a elaborate and easy manner. Just respond in plain text without any formatting"

            time.sleep(10)
            summary = generate_summary(prompt=prompt,target=des)

            product = Product(name=name,short=tagline,description=des,media=media,thumbnail=thumbnail,featuredat=featuredat,summary=summary,link=link,domain=topic,upvotes=votes)

            product.save()

            print("product made")
    except Exception as e:
        print("An error occured",e)
        pass # different pattern







    