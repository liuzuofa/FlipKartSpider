# -*- coding: utf-8 -*-
import scrapy

from bs4 import BeautifulSoup
from Flipkart.items import FlipkartItem

# scrapy crawl flipkart


# 读取目标网站
def import_urls_from_file(filename):
    url_list = []
    for url in open(filename, encoding='utf-8'):
        if url.startswith("#") or len(url) == 0 or url.isspace():
            continue
        url_list.append(url.strip().replace('\r', '').replace('\n', ''))
        pass
    return url_list


# 写入目标网站综合描述
def export_urls_review_to_file(name, price, mark, ratings, reviews, star_sum):
    with open("flipkart_product_review.txt", 'a', encoding='utf-8') as fp:
        fp.write(name + '\t')
        fp.write(price + '\t')
        fp.write(mark + '\t')
        fp.write(ratings + '\t')
        fp.write(reviews + '\t')
        for num in star_sum:
            fp.write(num + '\t')
        fp.write('\n')
        pass


class FlipkartSpider(scrapy.Spider):
    name = 'flipkart'
    allowed_domains = ['flipkart.com']

    def start_requests(self):

        # 从文件导入目标网站
        urls = import_urls_from_file("sources.txt")

        # 依次对导入的网站进行爬取
        for target_url in urls:
            print(target_url)
            yield scrapy.Request(url=target_url, callback=self.parse)

        pass

    def parse(self, response):

        # 解析评论简报
        soup = BeautifulSoup(response.body.decode(), features="lxml")

        # 产品名称
        product_name = soup.find_all('div', attrs={'class': '_1SFrA2'})[0].get_text()

        # 产品价格
        product_price = soup.find_all('div', attrs={'class': '_1vC4OE'})[0].get_text().replace(',', '')

        # 综合评分
        product_mark = soup.find_all('div', attrs={'class': '_1i0wk8'})[0].get_text()

        # 投票数
        product_ratings = soup.find_all('div', attrs={'class': 'col-12-12'})[1].get_text().split()[0].replace(',', '')
        # 评论数
        product_reviews = soup.find_all('div', attrs={'class': 'col-12-12'})[2].get_text().split()[0].replace(',', '')

        # 每一级评分数
        star_sum_list = []
        product_star_nums = soup.find_all('div', attrs={'class': 'CamDho'})
        for num in product_star_nums:
            star_sum_list.append(num.get_text().strip().replace(',', ''))
            pass

        # 写入文件
        export_urls_review_to_file(product_name, product_price, product_mark, product_ratings, product_reviews, star_sum_list)

        # 获取评论总页数
        # 范例 Page 1 of 1,000
        # 对应标签 <span class="_3v8VuN"><span>Page 1 of 1,000</span></span>
        page_info = soup.find_all('span', attrs={'class': '_3v8VuN'})[0].get_text()
        page_sum = int(page_info.split()[3].replace(',', ''))

        # 对链接进行分割 方便后续加入页号
        # https://www.flipkart.com/XXX/product-reviews/YYY?pid=ZZZ
        # 添加page页码之后的链接对比
        # https://www.flipkart.com/XXX/product-reviews/YYY?page=16&pid=ZZZ
        url_slices = response.url.split('?')

        # 循环抓取每页评论
        for page in range(1, page_sum):
            # 拼凑评论页链接
            sub_url = "%s?page=%d&%s" % (url_slices[0], page, url_slices[1])
            # 请求页面 解析评论信息
            yield scrapy.Request(url=sub_url, callback=self.parse_page, encoding='utf-8')

        pass

    def parse_page(self, response):

        # BeautifulSoup加载解析评论信息
        soup = BeautifulSoup(response.body.decode(), features="lxml")

        # 分数
        # 评论对应星级
        mark_list = soup.find_all('div', attrs={'class': 'hGSR34 _2beYZw E_uFuv'})

        # 标题
        # 一句话评论
        title_list = soup.find_all('p', attrs={'class': '_2xg6Ul'})

        # 评价
        # 评论详细文字
        content_list = soup.find_all('div', attrs={'class': 'qwjRop'})

        # 作者
        # 评论着昵称
        author_list = soup.find_all('p', attrs={'class': '_3LYOAd _3sxSiS'})

        # 地区
        position_list = soup.find_all('p', attrs={'class': '_19inI8'})

        # 日期
        raw_date_list = soup.find_all('p', attrs={'class': '_3LYOAd'})
        # 滤除作者获取日期 由于这两个标签相似我不知道怎么搞
        date_list = []
        index = 0
        for date in raw_date_list:
            if index % 2 == 1:
                date_list.append(date)
            index += 1
            pass

        # 赞踩数
        like_unlike_list = soup.find_all('span', attrs={'class': '_1_BQL8'})
        # 用于分开存储赞和踩数
        like_list = []
        unlike_list = []
        # 根据奇偶来分
        index = 0
        # 循环取赞踩数
        for item in like_unlike_list:
            if index % 2 == 0:
                like_list.append(item)
            else:
                unlike_list.append(item)
            index += 1
            pass

        # 循环获取信息
        for t, c, a, d, m, p, l, u in zip(title_list, content_list, author_list, date_list, mark_list, position_list, like_list, unlike_list):
            item = FlipkartItem()
            item['review_mark'] = m.get_text()
            item['review_title'] = t.get_text()
            item['review_content'] = c.get_text().replace("READ MORE", '').strip()
            item['review_author'] = a.get_text()
            item['review_position'] = p.get_text().replace("Certified Buyer,", '').strip()
            item['review_date'] = d.get_text()
            item['review_like'] = l.get_text()
            item['review_unlike'] = u.get_text()
            yield item

        pass
