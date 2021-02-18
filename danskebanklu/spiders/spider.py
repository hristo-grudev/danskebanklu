import scrapy

from scrapy.loader import ItemLoader
from ..items import DanskebankluItem
from itemloaders.processors import TakeFirst


class DanskebankluSpider(scrapy.Spider):
	name = 'danskebanklu'
	start_urls = ['https://danskebank.lu/private-banking/news']

	def parse(self, response):
		post_links = response.xpath('//li[@class="overview-item"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="row article-body"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="meta"]/span/text()').get()

		item = ItemLoader(item=DanskebankluItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()