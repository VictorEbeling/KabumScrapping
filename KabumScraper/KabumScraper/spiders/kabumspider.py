import scrapy
from scrapy.exceptions import CloseSpider
import json
from scrapy.utils.log import configure_logging
import logging


class KabumSpider(scrapy.Spider):
    
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    
    name = "kabumspider"
    allowed_domains = ["www.kabum.com.br"]
    start_urls = ["https://www.kabum.com.br/busca/rtx?page_number=%d" % i for i in range(1, 15)]
    #start_urls = ["https://www.kabum.com.br/busca/rtx?page_number=1"]
    handle_httpstatus_list = [404]
    #page_number=1

    def parse(self, response):
        
        if response.status == 404:
            raise CloseSpider('Recieved 404 response')
        
        products = response.css('div.productCard')
        
        for product in products:
            
            product_url = product.css('a.productLink').attrib['href']
            
            yield response.follow(product_url, callback=self.parse_product_page)
                
            #yield{
            #    'name' : product.css('span.nameCard::text').get(),
            #    'price' : product.css('span.priceCard::text').get(),
            #    'url' : product.css('a.productLink').attrib['href'],
            #    'page' : response
            #}
            
        #self.page_number += 1
        #next_page = f'https://www.kabum.com.br/busca/rtx?page_number={self.page_number}'
        #yield response.follow(next_page, callback=self.parse)
        yield
        
    def parse_product_page(self, response):
        
        data_json = response.xpath('//script[contains(., "@context")]/text()').get()
        data_json = data_json.replace("\\\\\\\\", "\\")
        data_json = data_json.replace("\\\\\\", "\\")
        data_json = fr"{data_json}".replace("\\\\", "\\")
        data_json_obj = json.loads(data_json)
        
        try:
            rating = data_json_obj['aggregateRating']['ratingValue']
        except:
            rating = 'No Rating'
            
        name = response.xpath('//div[@class="sc-liccgK ghutDt col-purchase"]/h1/text()').get()

        url = response.request.url
        
        price = (data_json_obj['offers']['price'])
        
        if 'R$' not in price:
            price = 'R$'+price
        
        primary_key = response.xpath('//span[@class="sc-16f86c3f-4 ddgpcu"]/text()').get()
        
        yield {
            'Primary Key' : primary_key[8:],
            'Name' : name,
            'Price' : price,
            'Rating': rating,
            'Link' : url
            }