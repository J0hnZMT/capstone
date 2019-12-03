import os
import requests
import logging

from harvest.scraper import web_scraper


def is_url_downloadable(url):
    # check if the url contain a downloadable resource or an html file
    link = requests.head(url, allow_redirects=True)
    header = link.headers
    content_type = header.get('content-type')
    # test if the content type is not html or text file
    if 'text' in content_type.lower() or 'html' in content_type.lower():
        return False
    return True


def download_program(url):
    # download the downloadable files
    dl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
    if not os.path.exists(dl_path):
        os.makedirs(dl_path)
    os.chdir(dl_path)
    html_content = web_scraper(url)
    if is_url_downloadable(url):
        file_name = url.rsplit('/', 1)[1]
        try:
            if not os.path.exists(file_name):
                with open(file_name, "wb") as file:
                    file.write(html_content)
            else:
                logging.info("{} file already saved".format(file_name))
        except TypeError as e:
            logging.error("Download Fail!", e)


