import requests
import time
from requests.exceptions import RequestException
from output import Output
from lxml import etree


# GET /realme-3-dynamic-black-32-gb/product-reviews/itmfe68wrbfnzqwz?pid=MOBFE68WZM7UFMDA&aid=overall&certifiedBuyer=false&sortOrder=NEGATIVE_FIRST&page=4 HTTP/1.1
# Host: www.flipkart.com
# Connection: keep-alive
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
# Referer: https://www.flipkart.com/realme-3-dynamic-black-32-gb/product-reviews/itmfe68wrbfnzqwz?pid=MOBFE68WZM7UFMDA&aid=overall&certifiedBuyer=false&sortOrder=NEGATIVE_FIRST&page=3
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9
# Cookie: T=TI155408291269051088271180464414101876800319121371635764130475883158; SN=2.VI0E6DB9FB64384AF09CEB0245DA5DFDBF.SIDBBCFC31EB314B9C8B650462E0480F8E.VS04109302537046BC9DC7ADA675D5512C.1555660730
class FlipkartSpider(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Cookie': 'T=TI155408291269051088271180464414101876800319121371635764130475883158; SN=2.VI0E6DB9FB64384AF09CEB0245DA5DFDBF.SIDBBCFC31EB314B9C8B650462E0480F8E.VS04109302537046BC9DC7ADA675D5512C.1555660730'
        }
        self.base_url = "https://www.flipkart.com"
        self.output = Output()

    def get_flipkart_html_by_url(self, url, page):
        try:
            params = {'pid': 'MOBFE68WZM7UFMDA', 'aid': 'overall', 'certifiedBuyer': 'false',
                      'sortOrder': 'NEGATIVE_FIRST',
                      'page': page}
            response = requests.post(url, data=params, headers=self.headers)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None

    def get_next_flipkart_comments_url(self, response):
        response = str(response)
        html = etree.HTML(response)
        next_urls = html.xpath('//nav[@class="_1ypTlJ"]/a[@class="_3fVaIS"]')
        for next_url in next_urls:
            print(next_url.xpath('./span/text()'))
            if next_url.xpath('./span/text()')[0] == 'Next':
                print("url: " + self.base_url + next_url.get('href'))
        if len(next_urls) == 1:
            return self.base_url + next_urls[0].get("href")
        elif len(next_urls) > 1:
            return self.base_url + next_urls[1].get("href")

    def get_flipkart_comments_by_url(self, response):
        response = str(response)
        response = response.replace("<br>", "")
        response = response.replace("<br />", "")
        html = etree.HTML(response)

        stars = html.xpath('//div[@class="col _390CkK _1gY8H-"]/div/div[@class="hGSR34 _1nLEql E_uFuv" or @class="hGSR34 _1x2VEC E_uFuv"]/text()')
        print(len(stars), " stars: ", stars)

        names = html.xpath(
            '//div[@class="col _390CkK _1gY8H-"]/div[@class="row _2pclJg"]/div[@class="row"]/p[@class="_3LYOAd _3sxSiS"]/text()')
        print(len(names), " names: ", names)

        times = html.xpath(
            '//div[@class="col _390CkK _1gY8H-"]/div[@class="row _2pclJg"]/div[@class="row"]/p[@class="_3LYOAd"]/text()')
        print(len(times), " times: ", times)

        # citys = html.xpath(
        #     '//div[@class="col _390CkK _1gY8H-"]/div[@class="row _2pclJg"]/div[@class="row"]/p[@class="_19inI8"]/span[5 mod 3]/text()')
        # print(len(citys), " citys: ", citys)

        titles = html.xpath('//div[@class="col _390CkK _1gY8H-"]/div/p[@class="_2xg6Ul"]/text()')
        print(len(titles), " titles: ", titles)

        comments_div = html.xpath('//div[@class="col _390CkK _1gY8H-"]/div/div[@class="qwjRop"]/div/div')
        comments = []
        for div in comments_div:
            comments.append(div.xpath('string(.)'))
        print(len(comments), " comments: ", comments)

        comments_list = []
        for index in range(len(stars)):
            comments_list.append(
                {"star": stars[index], "name": names[index], "time": times[index],
                 "city": "",
                 "title": titles[index], "comment": comments[index],
                 'trans': ""})
        return comments_list


if __name__ == '__main__':
    flipkart = FlipkartSpider()
    url = 'https://www.flipkart.com/realme-3-dynamic-black-32-gb/product-reviews/itmfe68wrbfnzqwz?pid=MOBFE68WZM7UFMDA&aid=overall&certifiedBuyer=false&sortOrder=NEGATIVE_FIRST&page=1'
    page = 1
    while page < 5:
        response = flipkart.get_flipkart_html_by_url(url, page)
        if response is None:
            print("get flipkart html wrong!")
        else:
            #comments_list = flipkart.get_flipkart_comments_by_url(response)
            #flipkart.output.add_comments((page - 1) * 10, comments_list)
            page = page + 1
            url = flipkart.get_next_flipkart_comments_url(response)
            print(str(url))
            time.sleep(1)
    #flipkart.output.save_comments()
    a = ["next"]
    print(a)
