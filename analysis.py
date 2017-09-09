__author__ = "JL"
__version__ = "0.1a"

"""
script for gathering data for analaysis. This iteration is going to use the NFL as a testing ground
"""

from webscrape import Webscrape
from collections import OrderedDict

#base nfl url
base_url = "http://api.fantasy.nfl.com"

#stats reference page
stats_url = "v1/game/stats?format=json"
stats_url = "/".join((base_url, stats_url))

stats_page = Webscrape(url=stats_url)
stats = stats_page.content.get('stats')
check = {}

## TODO: create analysis method to figure out column types