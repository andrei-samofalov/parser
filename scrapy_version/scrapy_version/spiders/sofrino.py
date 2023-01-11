import scrapy
from scrapy.http.response import Response

from .urls import CATALOG, URL


class SofrinoSpider(scrapy.Spider):
    name = 'sofrino'
    start_urls = [URL.format(cat) for cat in CATALOG.values()]

    def parse(self, response: Response, **kwargs):

        category = response.css("div.container-header-mobile > h2::text").get().strip()
        for good in response.css('div.product'):
            try:
                yield {
                    'category': category,
                    'code': good.css('div.product__footer::text').get().strip(),
                    'title': good.css('a.product__title::text').get().strip(),
                    'price': good.css(
                        'div.product__price__current::text'
                    ).get().strip(),
                    'url': good.css('div.product__buy > a::attr(href)').get(),
                }
            except AttributeError:
                continue

        next_page = response.css('a.page-link_next::attr(href)').get()

        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
