import scrapy
from scrapy import Request
from .make_start_urls import start_request
from ..items import ZhilianItem


class MySpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['m.zhaopin.com']

    def start_requests(self):
        links = start_request()
        for link in links:
            yield Request(link, callback=self.parse_page)

    def parse_page(self, response):
        base_url = 'https://m.zhaopin.com'
        data = {}
        try:
            belong = ''
            for i in response.xpath('/html/head/meta[2]/@content').extract()[0].split(','):
                if i == '招聘信息' or i ==response.xpath('/html/head/meta[2]/@content').extract()[0].split(',')[0]:
                    continue
                else:
                    belong = belong+i+' '
            data['belong'] = belong
        except:
            data['belong'] = ''
        job_link_suffix = response.xpath('//*[@id="r_content"]/div/div/section/a/@href').extract()
        for job_link in job_link_suffix:
            link = base_url + job_link
            yield Request(link, meta=data, callback=self.parse_item)
            # yield Request(link, callback='self.parse_item')
        if len(response.xpath('//*[@id="r_content"]/div/div[2]/a/@href').extract()) != 0:
            next_page_url = response.xpath('//*[@id="r_content"]/div/div[2]/a/@href').extract()[0]
            return Request(base_url+next_page_url,callback=self.parse_page)

    def parse_item(self, response):
        self.logger.info('已抓取到页面 %s,页面大小 %s', response.url, str(len(response.text)))
        item = ZhilianItem()
        try:
            item['belong'] = response.meta['belong'].encode('utf8','ignore').decode('utf8')
        except:
            item['belong'] = ''
        try:
            item['job'] = response.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[1]/div[1]/text()').extract()[0].encode('utf8','ignore').decode('utf8')
        except:
            item['job'] = ''
        try:
            item['edu'] = response.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[3]/div[1]/span[3]/text()').extract()[0].replace('<br>','').replace('<p>','').replace('</p>', '').replace('\r', '').replace('\n', '').replace(' ', '').replace('</div>', '').encode('utf8','ignore').decode('utf8')
        except:
            item['edu'] = ''
        try:
            item['company'] = response.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[2]/text()').extract()[0].encode('utf8','ignore').decode('utf8')
        except:
            item['company'] = ''
        try:
            item['salary'] = response.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[1]/div[2]/text()').extract()[0].encode('utf8','ignore').decode('utf8')
        except:
            item['salary'] = ''
        try:
            item['experience'] = response.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[3]/div[1]/span[2]/text()').extract()[0].replace('<br>','').replace('<p>','').replace('</p>', '').replace('\r', '').replace('\n', '').replace(' ', '').replace('</div>', '').encode('utf8','ignore').decode('utf8')
        except:
            item['experience'] = ''
        try:
            item['address'] = response.xpath('//*[@id="r_content"]/div[1]/div/div[1]/div[3]/div[1]/span[1]/text()').extract()[0].encode('utf8','ignore').decode('utf8')
        except:
            item['address'] = ''
        try:
            item['address_detail'] = response.xpath('//*[@id="r_content"]/div[1]/div/div[2]/div/text()').extract()[0].encode('utf8','ignore').decode('utf8')
        except:
            item['address_detail'] = ''
        try:
            item['description'] = response.xpath('//*[@id="r_content"]/div[1]/div/article/div').extract()[0].replace('<br>','').replace('<p>','').replace('</p>', '').replace('\r', '').replace('\n', '').replace(' ', '').replace('</div>', '').replace('<divclass="about-main">','').encode('utf8','ignore').decode('utf8')
        except:
            item['description'] = ''
        return item