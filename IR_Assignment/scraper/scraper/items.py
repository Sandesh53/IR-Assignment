# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PublicationItem(scrapy.Item):
    title = scrapy.Field()
    authors = scrapy.Field()
    departments = scrapy.Field()
    organizations = scrapy.Field()
    abstract = scrapy.Field()
    journal = scrapy.Field()
    volume = scrapy.Field()
    issue_number = scrapy.Field()
    keywords = scrapy.Field()
    fingerprints = scrapy.Field()
    publication_year = scrapy.Field()
    publication_url = scrapy.Field()
