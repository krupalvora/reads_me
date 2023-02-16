import openai

from reads_me.functions.wikipedia import is_person_dead, \
    is_first_revision_in_past_month

openai.api_key = "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"

question = "Help me write a text message to my friend Maqui that I don't want to see for the time being and don't want to give any specific reasons though leave it open for seeing them in the future"
#
# response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=question,
#         temperature=1,
#         max_tokens=128,
#     )
#
# print(response.choices[0].text)

article_id = "Raquel_Welch"
article_id = "2023_Ohio_train_derailment"
article_id = "Tahnee_Welch"

print(is_first_revision_in_past_month(article_id))


# I hope you're doing well. I hope you understand but, for the moment, I kind of want to take a
# break from hanging out because I'm really busy right now. I'm looking forward to seeing you
# again soon. Take care.

# I need some space right now and won't be able to hang out for a while, but I look forward to
# catching up with you in the future.

# I hope you understand that I don't want to see you for the time being. It's nothing personal,
# it's just that I need some time and space right now. Please don't take it negatively. I
# definitely look forward to seeing you

# Hey Maqui, I'm sorry to hear about your neighbor.  That's very sad and I'm sure is difficult.  I'm going through
# a bit of a difficult period also.  I hope you understand that I don't feel like hanging out for the time being.
# Please don't take it negatively.