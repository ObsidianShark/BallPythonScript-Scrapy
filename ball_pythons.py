from datetime import date, datetime

from scrapy import Field, Item, Request, Spider
from scrapy.crawler import CrawlerProcess


class SnakeItem(Item):
    # Snake info
    price = Field()
    amount_genes = Field()
    gene = Field()
    sex = Field()
    year = Field()
    category = Field()
    # Spider info
    url = Field()
    spider_name = Field()
    scraping_date = Field()


class BallPythonsSpider(Spider):
    name = "dreptiles"
    allowed_domains = ["dreptiles.com"]
    start_urls = [
        "https://dreptiles.com/ball-python-for-sale-shop/?filter_categories=ball-python"
    ]

    def parse(self, response):
        for snake in response.xpath(
            "//a[@class='woocommerce-LoopProduct-link woocommerce-loop-product__link']/@href"
        ):
            yield Request(url=snake.get(), callback=self.parse_snake)

        # next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        # if not next_page:
        #     yield Request(url=next_page, callback=self.parse)

    def parse_snake(self, response):
        snake = SnakeItem()
        snake["price"] = float(response.xpath("//p[@class='price']//bdi/text()").get())
        snake["amount_genes"] = int(
            response.xpath(
                "//tr[@class='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_amount-of-genes']/td/p/a/text()"
            ).get()
        )
        snake["gene"] = response.xpath(
            "//tr[@class='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_gene']/td/p/a/text()"
        ).getall()
        snake["sex"] = response.xpath(
            "//tr[@class='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_sex']/td/p/a/text()"
        ).get()
        snake["year"] = int(
            response.xpath(
                "//tr[@class='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_year-2']/td/p/a/text()"
            ).get()
        )
        snake["category"] = response.xpath(
            "//tr[@class='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_categories']/td/p/a/text()"
        ).get()

        snake["url"] = response.url
        snake["spider_name"] = self.name
        snake["scraping_date"] = datetime.now()

        yield snake


process = CrawlerProcess(
    settings={
        "HEADERS": {
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
        },
        "FEEDS": {
            f"dreptiles_ballpythons_{date.today()}.json": {"format": "json"},
        },
        "HTTPCACHE_ENABLED": True,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "CONCURRENT_REQUESTS": 1,
    }
)

process.crawl(BallPythonsSpider)
process.start()
