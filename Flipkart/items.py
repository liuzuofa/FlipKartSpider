# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FlipkartItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    review_mark = scrapy.Field()
    review_title = scrapy.Field()
    review_content = scrapy.Field()
    review_author = scrapy.Field()
    review_position = scrapy.Field()
    review_date = scrapy.Field()
    review_like = scrapy.Field()
    review_unlike = scrapy.Field()

    pass
