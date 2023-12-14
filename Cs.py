from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class CsSpider(CrawlSpider):
    name = "Cs"
    allowed_domains = ["churches.sbc.net"]
    start_urls = ["https://churches.sbc.net/?_paged=%d/" % i for i in range(1, 43)]

    rules = [
        Rule(LinkExtractor(restrict_xpaths='//div[@class="fwpl-item el-69mw2i"]/a[@href]'), callback='parse')
    ]

    def parse(self, response):
        try:
            email1 = response.xpath('//*[@class="heading__mapit location is-style-quiet"]//following-sibling::p[2]//@href').get()
            email2 = email1.replace('/cdn-cgi/l/email-protection#', '')
            r = int(email2[:2], 16)
            email23 = ''.join([chr(int(email2[i:i + 2], 16) ^ r) for i in range(2, len(email2), 2)])
        except:
            email23 = ''
        Churches = {
            'Title': response.xpath('//h1[@class="heading__title beta"]').xpath('normalize-space(string())').get(),
            'Adress': response.xpath('//h3[@class="heading__address"]').xpath('normalize-space(string())').get(),
            'Phone': response.xpath('//*[@class="heading__mapit location is-style-quiet"]//following-sibling::p[1]').xpath('normalize-space(string())').get(),
            'Email': email23,
            'Website': response.xpath('//*[@class="heading__website"]').xpath('normalize-space(string())').get()
        }
        yield Churches