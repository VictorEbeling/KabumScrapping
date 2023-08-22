import scrapy
from scrapy.exceptions import CloseSpider
import json
from scrapy.utils.log import configure_logging
import logging


class KabumSpider(scrapy.Spider):
    
    pages = input('How many pages do you want to scrape? (1 - 253)\n')
    
    #Activating log.txt
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='C:/Users/PC/VsCodeProjects/KabumScrapping/.venv/KabumScraper/KabumScraper/spiders/log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    
    #Spider properties
    name = "KabumSpider"
    allowed_domains = ["www.kabum.com.br"]
    start_urls = ["https://www.kabum.com.br/busca/rtx?page_number=%d" % i for i in range(1, pages)]
    handle_httpstatus_list = [404]

    #Parse pages
    def parse(self, response):
        
        #Error handling
        if response.status == 404:
            raise CloseSpider('Recieved 404 response')
        
        #Get products list
        products = response.css('div.productCard')
        
        #Iterate through pages
        for product in products:
            
            product_url = product.css('a.productLink').attrib['href']
            
            yield response.follow(product_url, callback=self.parse_product_page)
        
    #Parse products
    def parse_product_page(self, response):
        
        #Preparing webpage JSON
        data_json = response.xpath('//script[contains(., "@context")]/text()').get()
        data_json = data_json.replace("\\\\\\\\", "\\")
        data_json = data_json.replace("\\\\\\", "\\")
        data_json = fr"{data_json}".replace("\\\\", "\\")
        data_json_obj = json.loads(data_json)
        
        #Defining product rating
        try:
            rating = data_json_obj['aggregateRating']['ratingValue']
        except:
            rating = 'No Rating'
            
        #Defining product name
        name = response.xpath('//div[@class="sc-liccgK ghutDt col-purchase"]/h1/text()').get()

        #Defining product link
        url = response.request.url
        
        #Defining product price
        price = (data_json_obj['offers']['price'])
        
        #Formatting prices to Brazil's currency
        if 'R$' not in price:
            price = 'R$'+price
        
        #Defining product code
        primary_key = response.xpath('//span[@class="sc-16f86c3f-4 ddgpcu"]/text()').get()
        
        #Returning values
        yield {
            'Primary Key' : primary_key[8:],
            'Name' : name,
            'Price' : price,
            'Rating': rating,
            'Link' : url
            }