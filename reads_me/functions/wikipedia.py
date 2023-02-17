import requests

from datetime import datetime, timedelta

# Define the API endpoint
endpoint = "https://en.wikipedia.org/w/api.php"

headers = {
    'User-Agent': 'WhatsUpWiki 1.0'
}


def get_wikipedia_title(wikipedia_id):
    if "_" not in wikipedia_id:
        return wikipedia_id
    # Define the parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "prop": "info",
        "titles": wikipedia_id,
    }

    # Make the API request
    response = requests.get(endpoint, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON data from the response
        data = response.json()

        # Get the page with the ID
        title = data["query"]["normalized"][0]["to"]
        return title
    else:
        return None


def get_popular(date):
    date_string = date.strftime("%Y/%m/%d")
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top-per-country/US/all-access/{date_string}"
    print(url)
    response = requests.get(url, headers=headers)

    popular_articles = []
    if response.status_code == 200:
        data = response.json()
        items = data.get('items')
        if items:
            first_element = items[0]
            articles = first_element.get('articles')
            if articles:
                count = 0
                for article in articles:
                    # if count == 10:
                    #     break
                    if article.get('project') == 'en.wikipedia':
                        title = article.get('article')
                        if title != 'Main_Page'\
                                and not title.startswith("Special:") \
                                and not title.startswith("Deaths_in_"):
                            views = article.get('views_ceil')
                            count += 1
                            popular_articles.append(title)
    return popular_articles


def get_wikipedia_image_url(article_title):
    # Format the API request URL
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&titles={article_title}&pithumbsize=500'

    # Make a GET request to the API
    response = requests.get(url)
    data = response.json()

    # Get the page ID for the article
    page_id = list(data['query']['pages'].keys())[0]

    # Get the URL of the main article image
    image_url = data['query']['pages'][page_id].get('thumbnail', {}).get('source', '')

    return image_url


def get_wikipedia_external_links_section_id(article_title):
    # Format the API request URL
    url = f'https://en.wikipedia.org/w/api.php?action=parse&format=json&prop=sections&page={article_title}'

    # Make a GET request to the API
    response = requests.get(url)
    data = response.json()

    # Get the list of sections for the article
    sections = data['parse'].get('sections', [])

    # Find the section with the title "External links"
    for section in sections:
        if section['line'] == "External links":
            return str(section['number'])

    # Return None if the section was not found
    return None


def get_wikipedia_external_links(article_title):
    # get the section ID
    section_id = get_wikipedia_external_links_section_id(article_title)

    # Format the API request URL
    url = f'https://en.wikipedia.org/w/api.php?action=parse&format=json&section={section_id}&prop=externallinks&page={article_title}'

    # Make a GET request to the API
    response = requests.get(url)
    data = response.json()

    # Get the list of external links
    external_links = data['parse'].get('externallinks', [])

    return external_links


def is_person_dead(article_title):
    # Define the Wikidata API endpoint for getting the article information
    endpoint = "https://www.wikidata.org/w/api.php"

    # Define the parameters to send to the API
    params = {
        "action": "wbgetentities",
        "titles": article_title,
        "sites": "enwiki",
        "props": "claims",
        "format": "json"
    }

    # Send the API request
    response = requests.get(endpoint, params=params)

    # Parse the JSON response
    data = response.json()

    # catching exceptions in accessing dictionary keys that might not be there
    try:

        # Get the Wikidata ID of the article
        page_id = next(iter(data["entities"]))

        # Check if the article has a "date of death" claim
        if "P570" in data["entities"][page_id]["claims"]:
            death_date = data["entities"][page_id]["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"]

            # Remove the '+' character from the beginning of the date string
            date_string = death_date[1:]

            # Convert the date string to a datetime object
            date_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')

            return date_obj

    except Exception:
        return None

    # default output
    return None


def is_first_revision_in_past_month(article_title):
    # Define the Wikipedia API endpoint for getting the page revisions
    endpoint = "https://en.wikipedia.org/w/api.php"

    # Define the parameters to send to the API
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": article_title,
        "rvlimit": 1,
        "rvprop": "timestamp",
        "rvdir": "newer"
    }

    # Send the API request
    response = requests.get(endpoint, params=params)

    # Parse the JSON response
    data = response.json()

    # handling any missing dictionary keys
    try:

        # Get the page ID of the article
        page_id = next(iter(data["query"]["pages"]))

        # Get the timestamp when the first revision was made
        timestamp_str = data["query"]["pages"][page_id]["revisions"][0]["timestamp"]

        # Convert the timestamp string to a datetime object
        # timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')

        # Get the current date and time
        now = datetime.utcnow()

        # Calculate the time difference between the current date and the article creation date
        time_diff = now - timestamp

        # Check if the time difference is less than or equal to 1 month (30 days)
        if time_diff <= timedelta(days=30):
            return True
        else:
            return False

    except Exception:
        return False
