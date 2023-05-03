<div align="center">
    <img src="https://reads.me/static/reads_me/images/header.jpg">
</div>

# ChatGPT Powered News Bot

View online:  [READS.ME](https://reads.me)

## What it does
* Downloads trending articles on Wikipedia
* Skips any that were created within the past two years (to avoid ChatGPT's recent-event limitation)
* Uses ChatGPT to:
  * create BuzzFeed-style article titles
  * write articles based on those titles
  * classify the topic

## Setup
* Requires some knowledge of Django
* Duplicate the `.env-sample` file and rename it to `.env`.  Set `OPENAI_API_KEY` to yourkey
* Install on your server (or run locally with `django-admin runserver`)
* Create a superuser with `manage.py`
* Signed in as the superuser, click the 'Create' menu header to generate a new article.