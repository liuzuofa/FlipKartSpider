# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FlipkartPipeline(object):
    def process_item(self, item, spider):
        with open("flipkart_reviews.txt", 'a', encoding='utf-8') as fp:
            fp.write(item['review_title'] + '\t')
            fp.write(item['review_content'] + '\t')
            fp.write(item['review_author'] + '\t')
            fp.write(item['review_date'] + '\t')
            fp.write(item['review_mark'] + '\t')
            fp.write(item['review_position'] + '\t')
            fp.write(item['review_like'] + '\t')
            fp.write(item['review_unlike'] + '\n')
            pass
        return item
