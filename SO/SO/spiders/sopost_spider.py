import scrapy
from urllib.parse import urlencode
import re

from SO.items import SoItem


def url_page_decor(url, params):
    params = urlencode(params)
    return url + '?' + params


class SopostSpider(scrapy.Spider):
    name = 'sopost'
    allowed_domains = ['stackoverflow.com']

    start_page = 15
    end_page = 20
    tag = 'drupal'
    url = f'https://stackoverflow.com/questions/tagged/{tag}'

    def start_requests(self):
        for i in range(self.start_page, self.end_page):
            params = {'tab': 'newest', 'page': i, 'pagesize': '50'}
            new_url = url_page_decor(self.url, params)
            yield scrapy.Request(url=new_url, callback=self.parse)

    def parse(self, response):
        for post in response.css('div.js-post-summary'):
            item = SoItem()
            pid = post.css('::attr(id)').get()
            item['qid'] = re.findall('\d+', pid)[0]
            item['qvotes'], item['qanswers'], item['qviews'] = post.css(
                'div.js-post-summary-stats span.mr4::text').getall()
            item['qasktime'] = post.css('span.relativetime::attr(title)').get()

            detail_page = post.css('h3.s-post-summary--content-title a::attr(href)').get()
            detail_page = url_page_decor(detail_page, {'answertab': 'old'})

            yield response.follow(url=detail_page, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        item['qactivetime'] = response.css('div.snippet-hidden div.fw-wrap a.s-link__inherit::attr(title)').get()
        avotes = response.css('#answers div.js-vote-count::attr(data-value)').getall()
        item['avotesum'] = sum(abs(int(i)) for i in avotes)
        signaturetime = []
        for answer in response.css('#answers div.post-layout'):
            signaturetime = answer.css('div.post-signature span.relativetime::attr(title)').getall()
            break    # to get the first answer
        if signaturetime!=[]:
            item['responsetime'] = signaturetime[-1]     # to avoid getting editing time

        # todo get view in detail page

        yield item
