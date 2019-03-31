# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest 
from ..items import PopularSpiderItem
from random import randint
from time import sleep
from datetime import date
import re
import logging
from logging.handlers import RotatingFileHandler
import json

class RightnowSpiderSpider(scrapy.Spider):
    name = 'rightnow_spider'
    allowed_domains = ['www.etsy.com']
    start_urls = ['http://www.etsy.com/']
    log_file_handler = RotatingFileHandler('/tmp/etsy_popular.log', maxBytes=2**6*1024**2, backupCount=10, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')
    log_file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(log_file_handler)

    def start_requests(self):
        url = 'https://www.etsy.com/'
        sleep(randint(5,10))
        yield SplashRequest(url=url, callback=self.parse,args={'wait':1}, endpoint='render.html')

    def parse(self, response):
        sleep(randint(10,30))
        for idx in range(1, 7):        
            href = response.xpath('//*[@id="content"]/div[3]/div/div[2]/div/ul/li[' + str(idx) + ']/a/@href').get()            
            sleep(randint(30,90))
            url = response.urljoin(href)
            yield SplashRequest(url=url, callback=self.parse_product,args={'wait':1}, endpoint='render.html')

    def parse_product(self, response):
        items = PopularSpiderItem()

        tmp = ''.join(re.findall(r'/\d+/',response.url)).replace('/','')        
        items['_id'] = int(tmp)
        
        name = response.xpath('//*[@id="listing-page-cart"]/div[1]/div/div[2]/h1/text()').getall()
        tmp = ''.join(name)
        items['name'] = tmp
        
        description = response.xpath('//*[@id="description-text"]/div/div/div/text()').getall()
        tmp = ''.join(description)
        items['description'] = tmp

        shop_url = response.xpath('//*[@id="listing-page-cart"]/div[1]/div/div[1]/a[1]/@href').getall()
        tmp = ''.join(shop_url)
        items['shop_url'] = tmp

        tmp = ''.join(re.findall(r'shop/.+?ref',tmp)).replace('shop/','').replace('?ref','')
        items['shop_name'] = tmp

        bestseller = response.xpath('//*[@id="listing-page-cart"]/div[1]/div/div[2]/div/span/span[2]/text()').get()
        tmp = str(bestseller)        
        if bestseller is None:
            items['bestseller'] = 'No'            
        else:
            if re.search('Bestseller',bestseller):
                   items['bestseller'] = 'Yes'
            else:
                   items['bestseller'] = 'No'


        image_url = response.xpath('//*[@id="image-0"]/img/@src').get()
        tmp = ''.join(image_url)
        items['image_url'] = tmp
        
        url = response.url
        tmp = ''.join(url)
        items['url'] = tmp

        price = response.xpath('//*[@id="listing-page-cart"]/div[1]/div/div[3]/p/span[1]/text()').getall()
        if len(price) == 0:
            price = response.xpath('//*[@id="listing-page-cart"]/div[1]/div/div[4]/p/span[1]/text()').getall()
        if len(price) == 0:
            price = response.xpath('//*[@id="listing-page-cart"]/div[1]/div/div[4]/p[1]/span[1]/text()').getall()
        tmp = ''.join(price)        
        tmp = ''.join(re.findall(r'[$][,\d.]+\b',tmp)).replace('$','').replace(',','')
        if len(tmp) == 0:   tmp = '0'
        items['price'] = float(tmp)

        items['appeardate'] = []        
        items['appeardate'].append(str(date.today()))

        self.logger.info('function def parse_product generate item.')
        self.logger.info('%s', json.dumps(dict(items), indent=4))

        sleep(randint(10,30))
        return items

