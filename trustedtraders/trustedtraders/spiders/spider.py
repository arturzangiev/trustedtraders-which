# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['trustedtraders.which.co.uk']
    start_urls = ['https://trustedtraders.which.co.uk/b-in-ky120pa?utf8=%E2%9C%93&tab_view=list&p_mode=name&b%5Bq%5D=b&request_seed=258404&b%5Bplace_shape_human_identifier%5D=KY120PA&b%5Bplace_shape_identifier%5D=pcpoints-shp_728693&b%5Bopen_24h%5D=0&b%5Bopen_weekends%5D=0&b%5Bsort_type%5D=distance&b%5Bsearch_radius%5D=999']

    def parse(self, response):
        urls = response.xpath('//div[@class="search-basic"]/a[1]/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)

        # Calling next page
        next_page_url = response.xpath('//a[@class="page-numbers next"]/@href').extract_first()
        next_page_full_url = response.urljoin(next_page_url)
        yield scrapy.Request(next_page_full_url, callback=self.parse)

    def individual_page(self, response):
        company_name = response.xpath('//h1[@class="fn org"]/text()').extract_first()
        address = ', '.join(response.xpath('//div[@class="contact-info adr"]/span/text()').extract())
        phone_number = response.xpath('//a[@class="primary-phone-number"]/text()').extract_first()
        email = response.xpath('//div[@class="contact-info email"]/a/text()').extract_first()

        fields = dict(company_name=company_name, address=address, phone_number=phone_number, email=email)

        yield fields