import os
import requests
from datetime import datetime, timedelta, date
import json
import time
from celery import shared_task


@shared_task()
def news_data():
    from .models import Article, Domain
    

    newskey = os.getenv("newskey", "")
    params = {
        "apiKey": newskey,
        "from": date.today() - timedelta(days=1),
        "to": date.today() - timedelta(days=1),
        "q": "technology",
        "language": "en",
        "pageSize": 25,
        "page": 1,
        "sortBy": "relavancy",
    }
    response = requests.get("https://newsapi.org/v2/everything", params=params)

    articles = response.json()["articles"]

    for article in articles:
        try:
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
            summary = generate_summary(source_link, prompt=prompt)

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
            get_domain(title, Domain, article)

            article.save()
        except Exception as e:
            print("Article data has a different pattern", e)



def generate_summary(target, prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    api_key = os.getenv("gem_api_key", "")
    params = {"key": api_key}
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"text": target},
                ]
            }
        ]
    }
    response = requests.post(url, params=params, headers=headers, data=json.dumps(data))
    while response.status_code == 503:
        print("Waiting...", response["error"])
        time.sleep(10)
        response = requests.post(
            url, params=params, headers=headers, data=json.dumps(data)
        )
    summary = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    return summary


def get_domain(target_title, Domain, article):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    api_key = os.getenv("gem_api_key", "")
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
    response = requests.post(url, params=params, headers=headers, data=json.dumps(data))
    while response.status_code == 503:
        print("Waiting...", response["error"])
        time.sleep(10)
        response = requests.post(
            url, params=params, headers=headers, data=json.dumps(data)
        )
    domain = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    tag, created = Domain.objects.get_or_create(category=domain)
    article.domain = tag


@shared_task()
def products_data():
    from .models import Product
    product_api_key = os.getenv("producthunt_key", "")
    if not product_api_key:
        raise ValueError("Missing ProductHunt API key")

    try:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Host": "api.producthunt.com",
            "Authorization": product_api_key,
            "User-Agent": "curl/8.11.1",  # normal useragent was not working for some reason
        }

        url = "https://api.producthunt.com/v2/api/graphql"
        reqday = datetime.today().date() - timedelta(days=7)

        query = f"""
    query Posts {{
        posts(order: VOTES, first: 20, postedAfter: "{reqday}") {{
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

        response = requests.post(url, headers=headers, json={"query": query})

        print(response.status_code, "got the products")
        posts = response.json()["data"]["posts"]["nodes"]

    except Exception as e:
        print(f"The product request was not success {response.status_code}", e,)

    for post in posts:
        try:
            name = post["name"]
            print(name, post["featuredAt"])
            if not post["featuredAt"]:
                featured_date = datetime.now().date()
            else:
                featured_date = datetime.fromisoformat(post["featuredAt"])

            des = post["description"]
            tagline = post["tagline"]
            featuredat =  featured_date
            media = post["media"][0]["url"]
            thumbnail = post["thumbnail"]["url"]
            votes = post["votesCount"]
            topic = post["topics"]["nodes"][0]["name"]
            link = post["productLinks"][0]["url"]

            prompt = "You are an expert at summarizing the problems that software products aim to solve. Provide a detailed and elaborate summary in plain text, approximately 120 words long. Make it clear, engaging, and easy to understand. Focus on explaining what problem the product addresses and why it’s important. Don't use any Formatting"

            time.sleep(10)
            summary = generate_summary(prompt=prompt, target=des)

            product = Product(
                name=name,
                short=tagline,
                description=des,
                media=media,
                thumbnail=thumbnail,
                featuredat=featuredat,
                summary=summary,
                link=link,
                domain=topic,
                upvotes=votes,
            )

            product.save()

            print("product made")
        except Exception as e:
            print("Product data has a different pattern", e)
