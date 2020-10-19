import scrapy

class MagazineSpider(scrapy.Spider):
    name = 'magazine'

    def start_requests(self):
        url = 'https://sardine-system.com/media/'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for selector in response.css('.main-wrapper .container a'):
            yield {
                'title': selector.css('.main-text::text').extract_first(),
                'url': response.urljoin(selector.css('::attr(href)').extract_first())
            }