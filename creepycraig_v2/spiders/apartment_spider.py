import scrapy
from creepycraig_v2.items import ApartmentItem


class ApartmentSpider(scrapy.Spider):
    name = "hoodlum"
    allowed_domains = ["sfbay.craigslist.org"]
    start_urls = ["http://sfbay.craigslist.org/search/apa"]

    def parse(self, response):
        # follow links to apartment pages
        results = response.xpath('//p[@class="result-info"]')
        for result in results:
            href = result.xpath("a/@href").extract_first()
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_post)

        # follow pagination links
        next_page = response.xpath('//a[@class="button next"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_post(self, response):

        scrape_count = self.crawler.stats.get_value('item_scraped_count')

        title   = response.xpath("//span[@class='postingtitletext']")
        dollars = response.xpath("//span[@class='price']/text()").extract_first()
        post_id = response.xpath("//p[@class='postinginfo'][contains(text(), 'post id: ')]").extract_first()

        item = ApartmentItem()
        item["cl_id"]    = post_id.strip("post id: ")
        item["title"]    = response.xpath("//span[@id='titletextonly']/text()").extract_first()
        item["price"]    = float(dollars.strip('$'))

        item["where"]    = title.xpath("small/text()").extract_first()
        item["datetime"] = response.xpath("//p[@id='display-date']/time/@datetime").extract_first()
        item["url"]       = response.urljoin('')
        item["latitude"]  = response.xpath("//div[@id='map']/@data-latitude").extract_first()
        item["longitude"] = response.xpath("//div[@id='map']/@data-longitude").extract_first()

        yield item
