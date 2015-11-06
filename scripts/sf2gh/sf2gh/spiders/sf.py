# -*- coding: utf-8 -*-
import re
import json
import pprint
import scrapy
import requests
from urlparse import urljoin

re_bug = re.compile('bugs')
re_feature = re.compile('feature-requests')

bugsFile = open("sf-bugs.txt", "w")
featuresFile = open("sf-features.txt", "w")

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
        
class SfSpider(scrapy.Spider):
    name = "sf"
    allowed_domains = ["sourceforge.net"]
    start_urls = (
        'http://www.sourceforge.net/p/jwasm/bugs/?limit=1024',
        'http://www.sourceforge.net/p/jwasm/feature-requests/?limit=1024',
    )

    def extract(self, values, index = 0):
        try:
            return re.sub("\s\s+", " ", values.extract()[index]).strip()
        except:
            return ''

    def parse(self, response):

        bugs = []
        features = []

	for tr in response.xpath('//table[@class="ticket-list"]//tr'):
            issue = {}
            try:
                issue["id"] = self.extract(tr.xpath('td[1]//a/text()'))
                issue["summary"] = self.extract(tr.xpath('td[2]//a/text()'))
                issue["milestone"] = self.extract(tr.xpath('td[3]/text()'))
                issue["status"] = self.extract(tr.xpath('td[4]/text()'))
                issue["owner"] = self.extract(tr.xpath('td[5]/text()'))
                issue["created"] = self.extract(tr.xpath('td[6]//span/text()'))
                issue["updated"] = self.extract(tr.xpath('td[7]//span/text()'))
                issue["priority"] = self.extract(tr.xpath('td[8]//text()'))

                if (issue["owner"] is None) or (str(issue["owner"]).strip()==""):
                    issue["owner"] = "nobody";
                
                if re_bug.search(self.extract(tr.xpath('td[1]//a/@href'))):
                    bugs.append(issue)
                    continue

                if re_feature.search(self.extract(tr.xpath('td[1]//a/@href'))):
                    features.append(issue)
                    continue
                
            except:
                continue

        for bug in bugs:
            url = urljoin("http://sourceforge.net/p/jwasm/bugs/", bug["id"])
            request = scrapy.Request(url, callback = self.parseBugCallback)
            request.meta["item"] = bug
            yield request

        for feature in features:
            url = urljoin("http://sourceforge.net/p/jwasm/feature-requests/", feature["id"])
            request = scrapy.Request(url, callback = self.parseFeatureCallback)
            request.meta["item"] = feature
            yield request

    def parseBugCallback(self, response):
        response.meta["item"]["content"] = self.extract(response.xpath('//*[@id="ticket_content"]/div'))
        item = response.meta["item"];
        issue = {}
        issue["title"] = "[SF-BUG-%s] %s" % (item["id"], item["summary"])
        issue["labels"] = { "sf-import", "bug" }
        issue["body"] = '''**SF-BUG-{id}** | [{summary}]({link}) *created on* `{created}` *by* `{author}`

---

{content}'''.format(id = item["id"]
            , summary = item["summary"]
            , link = "http://www.sourceforge.net/p/jwasm/bugs/%s" % (item["id"])
            , created = item["created"]
            , author = item["owner"]
            , content = item["content"] )
        json.dump(issue, bugsFile, default = set_default)
        print >>bugsFile

    def parseFeatureCallback(self, response):
        response.meta["item"]["content"] = self.extract(response.xpath('//*[@id="ticket_content"]/div'))
        item = response.meta["item"];
        issue = {}
        issue["title"] = "[SF-FEATURE-%s] %s" % (item["id"], item["summary"])
        issue["labels"] = { "sf-import", "feature" }
        issue["body"] = '''**SF-FEATURE-{id}** | [{summary}]({link}) *created on* `{created}` *by* `{author}`

---

{content}'''.format(id = item["id"]
            , summary = item["summary"]
            , link = "http://www.sourceforge.net/p/jwasm/feature-requests/%s" % (item["id"])
            , created = item["created"]
            , author = item["owner"]
            , content = item["content"] )
        json.dump(issue, featuresFile, default = set_default)
        print >>featuresFile

