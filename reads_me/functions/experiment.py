import datetime


def days_since(date):
    """Returns the number of days since the input date up until the current date"""
    today = datetime.datetime.now()
    delta = today - date
    return delta.days


date = datetime.datetime(2022, 1, 1)  # A datetime object representing Jan 1, 2022
print(days_since(date))
