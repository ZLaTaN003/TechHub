import bs4
from celery import shared_task
import requests
from datetime import datetime, timezone, timedelta


@shared_task()
def get_news():
    from .models import Article, Domain

    url = "https://techcrunch.com/latest/"
    page = requests.get(url).text
    soup = bs4.BeautifulSoup(page, "html.parser")
    ist = timezone(timedelta(hours=5, minutes=30))

    links_tag = soup.find_all(class_="loop-card__title-link")

    for link in links_tag:
        class_list = link.find_parent("li")["class"]
        if "tag-in-brief" in class_list:
            continue

        author = soup.find(class_="wp-block-tc23-author-card-name__link")

        title = link.text
        article_url = link.attrs["href"]
        image_url, pub, short, content = get_des_and_content(article_url)
        if not content:
            continue
        published = datetime.fromisoformat(pub).astimezone(tz=ist)

        if Article.objects.filter(title=title).exists():
            continue

        print(title, short, content, image_url, published, article_url)

        article = Article(
            title=title,
            short_description=short,
            content=content,
            image_url=image_url,
            post_published=published,
            source_link=article_url,
            author=author.text if author else None,
        )

        get_category_tags(class_list, article, Domain)
        article.save()


def get_des_and_content(url):
    page = requests.get(url).text
    soup = bs4.BeautifulSoup(page, "html.parser")
    paras, image_url, pub_date, short_des, content = None, None, None, None, None

    try:
        image_url = soup.find(class_="wp-post-image").attrs["src"]
        pub_date = soup.find(class_="wp-block-post-date").find("time").attrs["datetime"]

        paras = soup.find_all(class_="wp-block-paragraph")

        short_des = paras[0].text
    except Exception as e:
        print("Different Pattern", e)

    if paras:
        content = ""
        for para in paras[1:]:
            content += para.text
    return image_url, pub_date, short_des, content


def get_category_tags(class_list, article, Tag):

    for cls in class_list:
        if cls.startswith("category"):
            category = cls.replace("category-", "")
            tag, created = Tag.objects.get_or_create(category=category)
            article.domain = tag


@shared_task()
def clean_db():
    from .models import Article

    articles_to_delete = Article.objects.all().delete()
