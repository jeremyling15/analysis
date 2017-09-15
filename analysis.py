__author__ = "JL"
__version__ = "0.1a"

"""
script for gathering data for analaysis. This iteration is going to use the NFL as a testing ground
"""

from webscrape import Webscrape
from database import TableFactory
from collections import OrderedDict
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import create_session
from sqlalchemy.ext.automap import automap_base
import time


engine_url = 'sqlite:///football.db'
engine = create_engine(engine_url, echo=False)
session = create_session(bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)
Base = automap_base()

#base nfl url
base_url = "http://api.fantasy.nfl.com"

#stats reference page
stats_url = "v1/game/stats?format=json"
stats_url = "/".join((base_url, stats_url))

stats_page = Webscrape(url=stats_url)
stats = stats_page.content.get('stats')

## stats table db load ##
table = TableFactory(tablename='statsref', metadata=metadata, engine=engine, session=session, tabledata=stats)
# http://api.fantasy.nfl.com/v1/players/researchinfo?season=2017&week=1&count=10000&format=json
player_url = "v1/players/researchinfo"
player_url = "/".join((base_url, player_url))
player_p = OrderedDict()
player_p["season"] = None
player_p["week"] = None
player_p["count"] = 10000
player_p["format"] = "json"

stats_url = "v1/players/stats"
stats_url = "/".join((base_url, stats_url))
stats_p = OrderedDict()
stats_p["stattype"] = "weekStats"
stats_p["season"] = 2010
stats_p["week"] = 1
stats_p["format"] = "json"

year = 2009
while year < 2018:
    player_p["season"] = year
    stats_p["season"] = year
    week = 1
    for wk in range(17):
        player_p["week"] = wk + 1
        print(player_p)
        player_page = Webscrape(url=player_url, params=player_p)
        player_page = player_page.content["players"]
        player_table = TableFactory(tablename="playerinfo", metadata=metadata, engine=engine, session=session,
                                    tabledata=player_page)

        stats_p["week"] = wk + 1
        stats_page = Webscrape(url=stats_url, params=stats_p)
        stats_page = stats_page.content["players"]
        stats_list = []
        for row in stats_page:
            row_dict = {}
            for key in row:
                if key != 'stats':
                    row_dict[key] = row[key]
                else:
                    for stat in row[key]:
                        # TODO: finish the row contruction
                        row_dict['stat'] = stat
                        row_dict['stat_value'] = row[key][stat]
            stats_list.append(row_dict)
        stat_table = TableFactory(tablename='playerstats', metadata=metadata, engine=engine, session=session,
                                  tabledata=stats_list)

        time.sleep(1)
    year += 1
    player_p["season"] += 1


#http://api.fantasy.nfl.com/v1/players/stats?statType=seasonStats&season=2010&week=1&format=json
#'v1/players/stats?statType=seasonStats&season=2010&week=1&format=json'
