import datetime
import re

from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from openai.error import RateLimitError

from reads_me.functions.ai import get_buzzfeed_title, get_buzzfeed_article, get_category, get_the_onion_title, \
    get_the_onion_article
from reads_me.functions.wikipedia import get_popular, get_wikipedia_image_url, get_wikipedia_title
from reads_me.models import Post


def create(request):
    popular_date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    popular_articles = get_popular(popular_date)
    # trying day-before-yesterday if no articles retrieved
    if len(popular_articles) == 0:
        popular_date = (datetime.datetime.now() - datetime.timedelta(days=2)).date()
        messages.warning(request, "No trending articles for  yesterday; checking the day-before")
        popular_articles = get_popular(popular_date)

    # alerting to error if no articles retrieved
    if len(popular_articles) == 0:
        messages.error(request, f"No articles returned for yesterday or the day before")

    article_count = 0
    article_limit = 1
    for article_id in popular_articles:
        if article_count >= article_limit:
            break
        # check if this is new content
        if Post.objects.filter(wikipedia_id=article_id, date_popular=popular_date).exists():
            continue
        # getting the (more) human-readable title
        try:
            wikipedia_title = get_wikipedia_title(article_id)
            article_title = get_buzzfeed_title(wikipedia_title)
            # removing the quotes
            article_title = article_title.replace('"', '')
            print(article_title)
            print("---------------------------------------------")
            if len(article_title) == 0:
                messages.warning(request, f"No title produced for: {wikipedia_title}")
            else:
                article_content = get_buzzfeed_article(article_title)
                if len(article_content) == 0:
                    messages.warning(request, f"No article produced for: {article_title}")
                else:
                    print(article_content)
                    print("---------------------------------------------")
                    image_url = get_wikipedia_image_url(article_id)
                    print(image_url)
                    print("---------------------------------------------")
                    category = get_category(wikipedia_title)
                    print(category)
                    post = Post(
                        date_popular=popular_date,
                        wikipedia_id=article_id,
                        subject=wikipedia_title,
                        title=article_title,
                        content=article_content,
                        image_url=image_url,
                        category=category,
                        slug=create_url_slug(article_title)
                    )
                    post.save()
                    messages.success(request, f"New article: {article_title}")
                    article_count += 1
        except RateLimitError as rle:
            print(f"RateLimitError: {rle}")
            messages.error(request, f"RateLimitError: {rle}")
    return redirect('home')


def create_url_slug(input_str):
    # Remove all non-alphanumeric characters and convert spaces to underscores
    slug = re.sub(r'[^\w\s]', '', input_str).strip().replace(' ', '_')
    # Replace repeated underscores with a single underscore
    slug = re.sub(r'_+', '_', slug)
    return slug.lower()