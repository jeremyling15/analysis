__author__ = 'Jeremy L'
__version__ = '0.1a'

import requests
from json.decoder import JSONDecodeError
from collections import OrderedDict
from lxml import html as lxmlhtml

class Webscrape(object):
    """
    Class for scraping a webpage. Allows for html/xml parsing using lxml, also allows for JSON returns using requests.
    """

    def __init__(self, url, params=None):
        if params:
            assert isinstance(params, OrderedDict)
        self.page = requests.get(url=url, params=params)
        if self.page.status_code != 200:
            print("HTTP Error %s: please check URL and params" % self.page.status_code)
        else:
            ## attempt to parse the page ##
            try:
                self.content = self.page.json()
            except JSONDecodeError:
                # parses even non html... Need to check string passed for tags.
                self.content = lxmlhtml.fromstring(self.page.content)
