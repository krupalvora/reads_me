import requests

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
                        if title != 'Main_Page' and title != 'Special:Search' and not title.startswith("Deaths_in_"):
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
