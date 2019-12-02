import requests


def is_good_response(response):
    # check if the url have a good connection and either a html file or not
    content_type = response.headers['Content-Type'].lower()
    # return the status code and content type
    return (response.status_code == 200
            and content_type is not None)


def web_scraper(url):
    # return the content of the link
    page = requests.get(url, stream=True)
    if is_good_response(page):
        return page.content
    else:
        return None

