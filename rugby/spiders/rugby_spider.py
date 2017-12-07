import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request

from rugby.items import RugbyItem

from selenium import webdriver
from lxml import html
import time

class RugbySpider(scrapy.Spider):
    name = "rugby"
    detail_url = "https://www.flashscores.co.uk/match/%s/#match-summary"

    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")
        self.file = open("result.csv", "wb")
        self.file.write('"Competition Name","Season","Match Date","Home Team","Away Team","    ","Score Home","Score Away","    ","Score Home HT","Score Away HT","    ","Odds Home", "Odds Away"' )

        self.target = [
                {'url': "https://www.flashscores.co.uk/rugby-union/europe/six-nations-2017/results/", 'competition_name': "6 Nations", 'season': "2017"},
                {'url': "https://www.flashscores.co.uk/rugby-union/europe/six-nations-2016/results/", 'competition_name': "6 Nations", 'season': "2016"},
                {'url': "https://www.flashscores.co.uk/rugby-union/europe/six-nations-2015/results/", 'competition_name': "6 Nations", 'season': "2015"},
                {'url': "https://www.flashscores.co.uk/rugby-union/europe/six-nations-2014/results/", 'competition_name': "6 Nations", 'season': "2014"},
                {'url': "https://www.flashscores.co.uk/rugby-union/europe/six-nations-2013/results/", 'competition_name': "6 Nations", 'season': "2013"},
                {'url': "https://www.flashscores.co.uk/rugby-union/europe/six-nations-2012/results/", 'competition_name': "6 Nations", 'season': "2012"},
                {'url': "https://www.flashscores.co.uk/rugby-union/europe/six-nations-2011/results/", 'competition_name': "6 Nations", 'season': "2011"},
                {'url': "https://www.flashscores.co.uk/rugby-union/world/world-cup/results/", 'competition_name': "World Cup", 'season': "2015"},
                {'url': "https://www.flashscores.co.uk/rugby-union/world/world-cup-2011/results/", 'competition_name': "World Cup", 'season': "2011"},
                {'url': "https://www.flashscores.co.uk/rugby-union/world/rugby-championship/results/", 'competition_name': "Rugby Championship", 'season': "2017"},
                {'url': "https://www.flashscores.co.uk/rugby-union/world/rugby-championship-2016/results/", 'competition_name': "Rugby Championship", 'season': "2016"},
                {'url': "https://www.flashscores.co.uk/rugby-union/world/rugby-championship-2015/results/", 'competition_name': "Rugby Championship", 'season': "2015"},
                {'url': "https://www.flashscores.co.uk/rugby-union/world/rugby-championship-2014/results/", 'competition_name': "Rugby Championship", 'season': "2014"},
                {'url': "https://www.flashscores.co.uk/rugby-union/world/rugby-championship-2013/results/", 'competition_name': "Rugby Championship", 'season': "2013"},
                {'url': "https://www.flashscores.co.uk/rugby-union/world/rugby-championship-2012/results/", 'competition_name': "Rugby Championship", 'season': "2012"},
                {'url': "https://www.flashscores.co.uk/rugby-union/england/aviva-premiership-rugby-2016-2017/results/", 'competition_name': "Aviva Premiership", 'season': "2016/17"},
                {'url': "https://www.flashscores.co.uk/rugby-union/england/aviva-premiership-rugby-2015-2016/results/", 'competition_name': "Aviva Premiership", 'season': "2015/16"},
                {'url': "https://www.flashscores.co.uk/rugby-union/england/aviva-premiership-rugby-2014-2015/results/", 'competition_name': "Aviva Premiership", 'season': "2014/15"},
                {'url': "https://www.flashscores.co.uk/rugby-union/england/aviva-premiership-rugby-2013-2014/results/", 'competition_name': "Aviva Premiership", 'season': "2013/14"},
                {'url': "https://www.flashscores.co.uk/rugby-union/england/aviva-premiership-rugby-2012-2013/results/", 'competition_name': "Aviva Premiership", 'season': "2012/13"},
                {'url': "https://www.flashscores.co.uk/rugby-union/england/aviva-premiership-rugby-2011-2012/results/", 'competition_name': "Aviva Premiership", 'season': "2011/12"},
                {'url': "https://www.flashscores.co.uk/rugby-union/france/top-14-2016-2017/results/", 'competition_name': "Top 14", 'season': "2016/17"},
                {'url': "https://www.flashscores.co.uk/rugby-union/france/top-14-2015-2016/results/", 'competition_name': "Top 14", 'season': "2015/16"},
                {'url': "https://www.flashscores.co.uk/rugby-union/france/top-14-2014-2015/results/", 'competition_name': "Top 14", 'season': "2014/15"},
                {'url': "https://www.flashscores.co.uk/rugby-union/france/top-14-2013-2014/results/", 'competition_name': "Top 14", 'season': "2013/14"},
                {'url': "https://www.flashscores.co.uk/rugby-union/france/top-14-2012-2013/results/", 'competition_name': "Top 14", 'season': "2012/13"},
                {'url': "https://www.flashscores.co.uk/rugby-union/france/top-14-2011-2012/results/", 'competition_name': "Top 14", 'season': "2011/12"}]


    def start_requests(self):

        for target in self.target:
            self.driver.get(target['url'])
            time.sleep(1)
            try:
                self.driver.find_element_by_xpath("//table[@id='tournament-page-results-more']//td//a").click()
                time.sleep(3)
            except:
                pass

            source = self.driver.page_source.encode("utf8")

            tree = html.fromstring(source)
            matches = tree.xpath("//tr[contains(@id, 'g_8')]")
            urls = []
            for match in matches:
                team_home = self.validate(match.xpath(".//td[contains(@class, 'team-home')]//span/text()"))
                team_away = self.validate(match.xpath(".//td[contains(@class, 'team-away')]//span/text()"))
                score = self.validate(match.xpath(".//td[contains(@class, 'score')]/text()"))
                key = self.validate(match.xpath("./@id")).split("_")[-1]

                urls.append({'team_home': team_home, 'team_away': team_away, 'url': self.detail_url % key, 'score': score})

            for url in urls:
                self.driver.get(url['url'])
                time.sleep(2)
                source = self.driver.page_source.encode("utf8")

                response = html.fromstring(source)

                item = dict()
                item['competition_name'] = target['competition_name']
                item['season'] = target['season']
                item['match_date'] = self.validate(response.xpath("//td[@id='utime']/text()"))
                item['home_team'] = url['team_home']
                item['away_team'] = url['team_away']
                item['score_home'] = url['score'].split(":")[0].strip()
                item['score_away'] = url['score'].split(":")[1].strip()
                item['score_home_ht'] = self.validate(response.xpath("//span[@class='p1_home']/text()"))
                item['score_away_ht'] = self.validate(response.xpath("//span[@class='p1_away']/text()"))
                item['odds_home'] = self.convert_to_float(self.validate(response.xpath("//table[@id='default-odds']//td[contains(@class, 'o_1')]//span[contains(@class, 'odds-wrap')]/text()")))
                item['odds_away'] = self.convert_to_float(self.validate(response.xpath("//table[@id='default-odds']//td[contains(@class, 'o_2')]//span[contains(@class, 'odds-wrap')]/text()")))

                self.file.write("\n\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"\",\"%s\",\"%s\",\"\",\"%s\",\"%s\",\"\",\"%s\",\"%s\"" % \
                    (item['competition_name'], item['season'], item['match_date'], item['home_team'], item['away_team'], \
                    item['score_home'], item['score_away'], item['score_home_ht'], item['score_away_ht'], item['odds_home'], item['odds_away']))
                print json.dumps(item, indent=4)

        self.driver.close()
        return [scrapy.Request(url="https://www.flashscores.co.uk", callback=self.parse), ]

    def parse(self, response):
        pass

    def validate(self, xpath_obj):
        try:
            return xpath_obj[0].strip()
        except:
            return ""

    def convert_to_float(self, frac_str):
        try:
            return float(frac_str)
        except ValueError:
            try:
                num, denom = frac_str.split('/')
            except ValueError:
                return None
            try:
                leading, num = num.split(' ')
            except ValueError:
                return float(num) / float(denom)        
            if float(leading) < 0:
                sign_mult = -1
            else:
                sign_mult = 1
            return float(leading) + sign_mult * (float(num) / float(denom))

