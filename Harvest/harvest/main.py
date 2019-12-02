import logging
import re
from bs4 import BeautifulSoup
from harvest import dbmanager
from harvest.config import config_opener
from harvest.logger import setup_logging
from harvest.scraper import web_scraper
from harvest.downloader import download_program


'''Logs'''
path = "logging.yml"
level = logging.INFO
env = 'LOG_CFG'
setup_logging(path, level, env)
logger = logging.getLogger(__name__)

''' Database Management'''
parameters = config_opener('setup.ini', 'db_parameters')
database = config_opener('setup.ini', 'database_name')
tables = config_opener('setup.ini', 'tables')
link_table = tables['link_table']
create_links = """id SERIAL NOT NULL PRIMARY KEY,
            app_name varchar NOT NULL,
            url varchar NOT NULL,
            saved_date TIMESTAMP NOT NULL DEFAULT NOW()"""
data_table = tables['data_table']
create_data = """id SERIAL NOT NULL PRIMARY KEY,
            app_name varchar NOT NULL,
            app_ver varchar NOT NULL"""
trans_table = tables['trans_table']
create_trans = """id SERIAL NOT NULL PRIMARY KEY,
            lang_name varchar NOT NULL,
            lang_ver varchar NOT NULL"""

'''
    Main Functions
'''


def get_all_link(base_url, content):
    # return the links found in index
    try:
        dbmanager.create_table(link_table, create_links, parameters, database)
        if content is not None:
            html = BeautifulSoup(content, 'lxml')
            links = html.find('ul').find_all('a')
            # list of links found
            links_found = []
            for link in links:
                found_link = link.get('href')
                app_name = link.get_text()
                check = 'http://' in str(found_link)
                if check is False:
                    if app_name != 'Read More >>':
                        if found_link not in [str(y) for x in links_found for y in x.split()]:
                            links_found.append(found_link)
                            # save the link to db
                            select_query = """SELECT url FROM {}""".format(link_table)
                            db_links = dbmanager.select(select_query, parameters, database)
                            if found_link not in [str(y) for x in db_links for y in x]:
                                query = """INSERT INTO {}(app_name, url) 
                                         VALUES ('{}', '{}');""".format(link_table, app_name.rstrip(), found_link)
                                dbmanager.insert(query, parameters, database)
                            else:
                                logger.info("Already saved to database...")
            # return links_found
            process_dl_page(base_url, links_found)
    except Exception as e:
        print(e)


def process_dl_page(main_link, links):
    dbmanager.create_table(data_table, create_data, parameters, database)
    dbmanager.create_table(trans_table, create_trans, parameters, database)
    for link in links:
        dl_url = "{}{}".format(main_link, link)
        # get all the content of the downloadable page
        dl_content = web_scraper(dl_url)
        # download links from the download page
        dl_links = get_download_link(main_link, dl_content)
        # get the app name and version and store into db
        app_name = get_metadata(dl_url)
        query = """ SELECT app_name FROM {}""".format(data_table)
        app_names = dbmanager.select(query, parameters, database)
        # for dl_link in dl_links:
        #     download_program(dl_link)
        if app_name not in [str(y) for x in app_names for y in x]:
            # download files
            for dl_link in dl_links:
                download_program(dl_link)
                logger.info("{} downloadable files saved.".format(app_name))
        else:
            print("Failed to download")


def get_download_link(main_url, content):
    # get all the url of the downloadable files
    html = BeautifulSoup(content, 'lxml')
    links = html.find_all("a")
    found_dl_url = []
    for link in links:
        dl_link = link.get('href')
        complete_link = check_dl_link(main_url, dl_link)
        if complete_link is not None:
            found_dl_url.append(complete_link)
    return found_dl_url


def check_dl_link(main_url, url):
    # check the download url if it is zip or exe file and add the base url
    if url is not None:
        if '.zip' in url or '.exe' in url:
            if '../' in url:
                dl_link = url.replace('../', '')
                new_dl_link = "{}{}".format(main_url, dl_link)
                return new_dl_link
            elif 'http://' in url:
                return url
            else:
                new_dl_link = "{}utils/{}".format(main_url, url)
                return new_dl_link


def get_metadata(url):
    # app name and version
    link = url.rsplit('0/', 1)[1]
    select_query = """SELECT app_name FROM {} WHERE url = '{}'""".format(link_table, link)
    result = dbmanager.select(select_query, parameters, database)[0][0]
    content = web_scraper(url)
    html = BeautifulSoup(content, 'lxml')
    if ':' in result:
        name = result.rsplit(':')[0]
        ver = html(text=re.compile(r'{} v'.format(name)))
    elif ' - ' in result:
        name = result.rsplit(' - ')[0]
        ver = html(text=re.compile(r'{} v'.format(name)))
    else:
        name = result
        ver = html(text=re.compile(r'{} v'.format(name)))
    if ' - ' in ver[0]:
        version = str(ver[0]).split(' - ')[0]
    else:
        version = str(ver[0]).strip('\n')
    app_version = version.lstrip('{} '.format(name))
    select_query = """SELECT app_name FROM {}""".format(data_table)
    app_names_db = dbmanager.select(select_query, parameters, database)
    if name not in [str(y) for x in app_names_db for y in x]:
        query = """INSERT INTO {}(app_name, app_ver) VALUES ('{}', '{}');""".format(data_table, name, app_version)
        dbmanager.insert(query, parameters, database)
    # language and version
    table = html.find_all('tr', class_='utiltableheader')[-1].find_parent('table')
    tr = table.find_all('tr')[1:]
    for td in tr:
        lang = td.find_all('td')[0].find('a').get('href')
        ver = td.find_all('td')[-1].text.strip('\n')
        select_query = """SELECT lang_name FROM {}""".format(trans_table)
        lang_names_db = dbmanager.select(select_query, parameters, database)
        if str(lang).lstrip('trans/') not in [str(y) for x in lang_names_db for y in x]:
            query = """INSERT INTO {}(lang_name, lang_ver) VALUES ('{}', '{}');"""\
                .format(trans_table, str(lang).lstrip('trans/'), ver)
            dbmanager.insert(query, parameters, database)
        else:
            logger.info("{} already saved in database".format(str(lang).lstrip('trans/')))
    return name


def main(url):
    dbmanager.create_db(parameters, database)
    web_content = web_scraper(url)
    get_all_link(url, web_content)



