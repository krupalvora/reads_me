import openai

from django_project.settings import env
from reads_me.constants import CATEGORIES

openai.api_key = env('OPENAI_API_KEY')

# https://platform.openai.com/docs/models/gpt-4
model_version = "text-davinci-003"

def get_buzzfeed_title(subject):
    response = openai.Completion.create(
        model=model_version,
        prompt=f"Write an online article title about \"{subject}\" in the style of Buzzfeed",
        temperature=0.6,
        max_tokens=32,
        # stop="\n",
    )
    return response.choices[0].text.strip()


def get_buzzfeed_deceased_title(subject):
    response = openai.Completion.create(
        model=model_version,
        prompt=f"Write an online article title about \"{subject}\" in the past tense in the style of Buzzfeed",
        temperature=0.6,
        max_tokens=32,
        # stop="\n",
    )
    return response.choices[0].text.strip()


def get_buzzfeed_article(buzzfeed_title):
    response = openai.Completion.create(
        model=model_version,
        # prompt=f"An article in the style of BuzzFeed.  {buzzfeed_title}:",
        # prompt=f"An article in the style of BuzzFeed using HTML markup:\n<h1>{buzzfeed_title}</h1>\n",
        prompt=f"An listicle article in the style of BuzzFeed where each list item takes the form of \"<li><b>claim</b> - detailed explanation of claim</li>\" using HTML markup:\n\n<h1>{buzzfeed_title}</h1>\n\n<ol>",
        temperature=0.6,
        max_tokens=1024,
        stop="</ol>",
    )
    return response.choices[0].text.strip()


def ai_get_category(subject):
    prompt = f"The categories are: {', '.join(CATEGORIES)}. \"{subject}\" is best describe by which category?"
    response = openai.Completion.create(
        model=model_version,
        prompt=prompt,
        temperature=0.0,
        max_tokens=16,
    )
    return response.choices[0].text.strip()


def get_informative_article(subject):
    response = openai.Completion.create(
        model=f"write an entertaining and informative article on {subject}",
        prompt=subject,
        temperature=0.6,
        max_tokens=1024,
    )
    return response.choices[0].text.strip()

