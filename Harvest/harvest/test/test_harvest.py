import unittest
import requests
from harvest import scraper, downloader, main, logger


class MyTestCase(unittest.TestCase):
    url = 'http://54.174.36.110/'

    def test_scraper(self):
        global url
        resp = requests.get(url)
        self.assertTrue(scraper.is_good_response(resp))
        self.assertIsNotNone(scraper.web_scraper(url))

    def test_downloader(self):
        global url
        self.assertFalse(downloader.is_url_downloadable(url))
        self.assertIsInstance(downloader.download_program(url))

    def test_main(self):
        global url
        con = scraper.web_scraper(url)
        self.assertListEqual(main.get_all_link(url, con))


if __name__ == '__main__':
    unittest.main()
