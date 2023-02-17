import datetime

import openai

from reads_me.functions.wikipedia import is_person_dead, \
    is_first_revision_in_past_month

openai.api_key = "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"

#
# response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=question,
#         temperature=1,
#         max_tokens=128,
#     )
#
# print(response.choices[0].text)


def days_since(date):
    """Returns the number of days since the input date up until the current date"""
    today = datetime.datetime.now()
    delta = today - date
    return delta.days


date = datetime.datetime(2022, 1, 1)  # A datetime object representing Jan 1, 2022
print(days_since(date))
