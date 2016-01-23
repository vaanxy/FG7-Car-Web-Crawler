# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.spiders import Spider
from scrapy.selector import Selector
from shutil import rmtree
import os
import re


def add_url(start_urls):
    for i in range(1000):
        start_urls.append("http://jiage.autohome.com.cn/price/carlist/p-" + str(10001 + i))
    return start_urls


def make_output_path():
    new_path = os.path.join(os.getcwd(), "output")
    if os.path.isdir(new_path):
        rmtree(new_path)
    os.makedirs(new_path)
    return new_path


class CarSpider(Spider):
    name = "car"
    allowed_domains = ["autohome.com.cn"]
    start_urls = []
    start_urls = add_url(start_urls)
    output_path = make_output_path()

    def parse(self, response):
        sel = Selector(response)
        # date_list = sel.xpath('//ul[@class="price-list"]/li/div/div/span/text()').re(r'(.*)\xa0')
        # print date_list
        # for date in date_list:
        #     filename = os.path.join(
        #         self.output_path,
        #         response.url.split("/")[-1].replace("p-", "") + "-" + date.replace("-", "") + ".txt")
        #     f = open(filename, 'w')
        #     f.write(date.encode("utf-8"))
        #     f.close()
        sale_list = sel.xpath('//ul[@class="price-list"]')
        for item in sale_list.xpath('./li'):
            info_str = ""
            date = item.xpath('./div/div/span/text()').re(r'(.*)\xa0')
            if len(date) == 0:
                continue
            info_str += date[0] + "\t"
            info_list = item.xpath('.//ul[contains(@class, "price-item-info")]/li')
            count = 0
            for info in info_list.xpath('.//div[contains(@class, "txcon")]'):
                count += 1
                if count == 1:
                    text = info.xpath('.//a/text()').extract()
                elif count in [2, 6]:
                    text = info.xpath('.//span/text()').extract()
                elif count in [10, 13, 14]:
                    text = info.xpath('.//p/text()').extract()
                else:
                    text = info.xpath('./text()').extract()
                if len(text) != 0:
                    info_str += text[0].strip() + "\t"
            filename = os.path.join(
                self.output_path,
                response.url.split("/")[-1].replace("p-", "") + "-" + date[0].replace("-", "") + ".txt")
            f = open(filename, 'w')
            f.write(info_str.encode("utf-8"))
            f.close()


