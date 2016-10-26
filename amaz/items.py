# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    product_name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    offer_price = scrapy.Field()
    specs=scrapy.Field()
    excerpts=scrapy.Field()
    rating=scrapy.Field()
    image=scrapy.Field()
    rating_count=scrapy.Field()
    sold_out=scrapy.Field()
    cod=scrapy.Field()
    free_shipping=scrapy.Field()
    prebook=scrapy.Field()
    warranty=scrapy.Field()
    
    
    
	

