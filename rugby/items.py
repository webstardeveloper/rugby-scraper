# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class RugbyItem(scrapy.Item):
    competition_name = Field()
    season = Field()
    match_date = Field()
    home_team = Field()
    away_team = Field()
    score_home = Field()
    score_away = Field()
    score_home_ht = Field()
    score_away_ht = Field()
    odds_home = Field()
    odds_away = Field()
