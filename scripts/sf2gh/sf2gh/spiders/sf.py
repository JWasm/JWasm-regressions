# -*- coding: utf-8 -*-
import re
import pprint
import scrapy

re_bug = re.compile('bugs')
re_feature = re.compile('feature-requests')

class SfSpider(scrapy.Spider):
    name = "sf"
    allowed_domains = ["sourceforge.net"]
    start_urls = (
        'http://www.sourceforge.net/p/jwasm/bugs/?limit=1024',
        'http://www.sourceforge.net/p/jwasm/feature-requests/?limit=1024',
    )

    def extract(self, values, index = 0):
        try:
            return values.extract()[index]
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
                issue["created"] = self.extract(tr.xpath('td[6]//span/@title'))
                issue["updated"] = self.extract(tr.xpath('td[7]//span/@title'))
                issue["priority"] = self.extract(tr.xpath('td[8]//text()'))

                if re_bug.search(self.extract(tr.xpath('td[1]//a/@href'))):
                    bugs.append(issue)
                    continue

                if re_feature.search(self.extract(tr.xpath('td[1]//a/@href'))):
                    features.append(issue)
                    continue
                
            except:
                continue

        print ">> BUGS"
        pprint.pprint(bugs)
        print ">> FEATURES"
        pprint.pprint(features)

        pass

