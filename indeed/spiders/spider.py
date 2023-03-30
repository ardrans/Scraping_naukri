import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import random
import json
from urllib.parse import urlencode


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['www.naukri.com']
    page_number = 1
    #start_urls = ['https://www.naukri.com/python-jobs?k=python']
    #start_urls = ['https://www.naukri.com/python-jobs-in-trivandrum?k=python&l=trivandrum']
    #custom_settings = {
        #'FEEDS': {"./self.keyword/%(file_name)s": {"format": "csv"}},
    #}




    def __init__(self,keyword,location):
        self.keyword = keyword
        self.location = location




    def start_requests(self):
        params = {
            "urlType": "search_by_key_loc",
            "searchType": "adv",
            "keyword": self.keyword,
            "location": self.location,

        }
        headers = {
            'Host': 'www.naukri.com',
            'appid': '109',
            'systemid': '109',
            'Connection': 'keep-alive'
        }
        urls = [
            'https://www.naukri.com/jobapi/v3/search?'+ urlencode(params),
        ]

        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)





        #headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    # def parse(self, response):
    #     print(response.body)
    #     #title = response.xpath("//a[@class='title ellipsis']/text()")
    #     #print(title)

    def parse(self, response):
        #print(response)
        d={}
        data = json.loads(response.text)
        #print(data['jobDetails'])
        jobs = data['jobDetails']
        for job in jobs:
            #d['job_title']=job['title']
            #d['company_name']=job['companyName']
            job_title=job['title']
            company_name=job['companyName']
            yield {
                'job_title': job_title,
                'company_name': company_name
            }

        self.page_number += 1
        params = {
            "urlType": "search_by_key_loc",
            "searchType": "adv",
            "keyword": self.keyword,
            "location": self.location,
            "pageNo": self.page_number

        }
        headers = {
            'Host': 'www.naukri.com',
            'appid': '109',
            'systemid': '109',
            'Connection': 'keep-alive'
        }
        next_page = 'https://www.naukri.com/jobapi/v3/search?'+ urlencode(params)
        yield response.follow(next_page, headers=headers, callback=self.parse)








        # def start_requests(self):s
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, callback=self.parse)
    #
    # def parse(self, response):
    #
    #     cookies = {}
    #     a= response.headers.getlist('Set-Cookie')
    #     for key, value in response.headers.getlist('Set-Cookie'):
    #         cookie = key.decode() + '=' + value.decode().split(';')[0]
    #         cookies.update({cookie.split('=')[0]: cookie.split('=')[1]})
    #
    #
    #     yield scrapy.Request('https://in.indeed.com/jobs?q=python&l=Thiruvananthapuram', cookies=cookies, callback=self.parse_page)
    #
    # def parse_page(self, response):
    #     print(response.status, response.url)






