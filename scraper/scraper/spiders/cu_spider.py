import scrapy
from ..items import PublicationItem

class CuSpider(scrapy.Spider):
    name = "cu_spider"
    start_urls = [
        "http://pureportal.coventry.ac.uk/en/organisations/fbl-school-of-economics-finance-and-accounting/publications/"
    ]

    def parse(self, response):
        for pub in response.css("div.result-container"):
            publication_url = response.urljoin(pub.css('h3.title a::attr(href)').get())
            yield scrapy.Request(publication_url, callback=self.parse_publication)

        next_page = response.css('a.nextLink::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_publication(self, response):
        item = PublicationItem()
        item['title'] = response.css('div.introduction.no-metrics h1 span::text').get()

        names = response.css('p.relations.persons ::text').getall()
        item['authors'] = [name.strip().strip(',') for name in names if name.strip().strip(',')]
        item['departments'] = response.css('ul.relations.organisations li.school a.link span::text').get()
        item['organizations'] = response.css('ul.relations.organisations li a span::text').getall()
        item['abstract'] = response.css('div.rendering_researchoutput_abstractportal div.textblock p::text').get()
        item['journal'] = response.css('tr:contains("Journal") td span::text').get()
        item['volume'] = response.css('tr:contains("Volume") td::text').get()
        item['issue_number'] = response.css('tr:contains("Issue number") td::text').get()
        item['keywords'] = response.css('div.keyword-group ul.relations li span::text').getall()
        item['fingerprints'] = response.css('ul.publication-top-concepts span.concept::text').getall()
        item['publication_year'] = response.css('tr.status td span.date::text').get().split()[-1]
        item['publication_url'] = response.url
        yield item
