"""This Crawler is for study purpose and it crawls the below information """
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
#from scrapy.http import Request
import MySQLdb
class Thrillophilia(BaseSpider):
    """Starting spider name"""
    name = "thrillophilia"
    start_urls = ['https://www.thrillophilia.com/countries/india/tags/honeymoon']
    def __init__(self):
        """Connecting to Database"""
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd='01491a0237db', db="thrilldb", charset='utf8', use_unicode=True)
        self.cur = self.conn.cursor()
    def parse(self, response):
        """Extracting data and sending into Database"""
        sel = Selector(response)
        nodes = sel.xpath(
            '//div[@class="activities"]/ul[@class="row search-results js-search-results"]/div[@class="card-container"]/li[@class="grid-item case02"]')
        for node in nodes:
            rating = "".join(node.xpath(
                './div[@class="col-md-3"]/div[@class="rating"]/div[@class="rating-quality"]/span[@class="rating-text"]/text()').extract())
            title = "".join(node.xpath(
                './div[@class="desc row_no_marging_padding col-md-5"]/div[@class="name"]/a/text()').extract())
            image = "".join(node.xpath(
                './div[@class="image col-md-4"]/a/img/@src').extract())
            price = "".join(node.xpath(
                './div[@class="col-md-3"]/div[@class="right-bottom"]/div[@class="price"]/div[@class="col-md-7"]/div[@class="discounted-price"]/p/text()').extract())
            link = "".join(node.xpath(
                './div[@class="desc row_no_marging_padding col-md-5"]/div[@class="name"]/a/@href').extract())
            print(title, image, price, link, rating)
            qry = 'insert into thrill(title, image, price, link, rating)values(%s, %s, %s, %s, %s)on duplicate key update title=%s'
            values = (title, image, price, link, rating, title)
            print qry%values
            self.cur.execute(qry, values)
            self.conn.commit()
