import datetime
import random
import re

from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from openai.error import RateLimitError

from reads_me.constants import DEATHS, CATEGORIES, INTERESTING
from reads_me.functions.ai import get_buzzfeed_title, get_buzzfeed_article, ai_get_category, get_the_onion_title, \
    get_the_onion_article, get_buzzfeed_deceased_title
from reads_me.functions.wikipedia import get_popular, get_wikipedia_image_url, get_wikipedia_title, is_person_dead, \
    is_first_revision_in_past_month
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

        print(f"trying article {article_id}")

        # check if this is new content
        # if Post.objects.filter(wikipedia_id=article_id, date_popular=popular_date).exists():
        if Post.objects.filter(wikipedia_id=article_id).exists():
            continue

        # skipping new topics as ChatGPT won't know about those
        if is_first_revision_in_past_month(article_id):
            messages.warning(request, f"skipping '{article_id}' as it was recently created")
            continue

        # getting the (more) human-readable title
        # e.g. "Raquel_Welch" -> "Raquel Welch"
        wikipedia_title = get_wikipedia_title(article_id)

        try:
            # Using past tense if person has died
            deceased_date = is_person_dead(article_id)
            if deceased_date is not None:
                article_title = get_buzzfeed_deceased_title(wikipedia_title)
            else:
                article_title = get_buzzfeed_title(wikipedia_title)

            # removing the quotes
            article_title = article_title.replace('"', '').strip()
            print(f"'{article_title}'")
            # making sure the number of items in the listicle isn't huge
            article_title = replace_num(article_title)
            print(article_title)
            print("---------------------------------------------")
            if len(article_title) == 0:
                messages.warning(request, f"No title produced for: {wikipedia_title}")
            else:
                article_content = get_buzzfeed_article(article_title)
                if len(article_content) == 0:
                    messages.warning(request, f"No article produced for: {article_title}")
                else:
                    image_url = get_wikipedia_image_url(article_id)

                    category = determine_category(wikipedia_title, deceased_date)

                    # saving the post
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
            messages.error(request, f"RateLimitError: {rle}")
    return redirect('home')


def create_url_slug(input_str):
    # Remove all non-alphanumeric characters and convert spaces to underscores
    slug = re.sub(r'[^\w\s]', '', input_str).strip().replace(' ', '_')
    # Replace repeated underscores with a single underscore
    slug = re.sub(r'_+', '_', slug)
    return slug.lower()


def replace_num(string):
    """
     checks if a string starts with an integer and if that integer is greater than 10,
    it replaces it with a randomly chosen number from 5, 7, and 10, accounting for the
    fact that the number may be several digits long
    :param string:
    :return:
    """
    # find the length of the integer at the beginning of the string
    num_len = 0
    for char in string:
        if char.isdigit():
            num_len += 1
        else:
            break
    # check if the integer is greater than 10
    if num_len > 0:
        num = int(string[:num_len])
        # upper bound as after a certain point it is probably not a number of list items but a date
        if 10 < num < 30:
            new_num = random.choice([5, 7, 10])
            return str(new_num) + string[num_len:]
    return string


def days_since(date):
    """Returns the number of days since the input date up until the current date"""
    today = datetime.datetime.now()
    delta = today - date
    return delta.days


def determine_category(wikipedia_title, deceased_date):
    """ determining the category """
    if deceased_date is not None:
        if days_since(deceased_date) > 30:
            category = ai_get_category(wikipedia_title)
        else:
            category = DEATHS
    else:
        category = ai_get_category(wikipedia_title)

        # "Interesting" is the default category
        if category not in CATEGORIES:
            category = INTERESTING
    return category