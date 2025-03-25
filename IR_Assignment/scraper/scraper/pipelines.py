# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from elasticsearch import Elasticsearch
from scrapy.exceptions import DropItem

class ElasticCleanPipeline:
    def open_spider(self, spider):
        spider.logger.info('ElasticCleanPipeline: Opening spider and connecting to Elasticsearch.')
        self.es = Elasticsearch("http://localhost:9200")

    def process_item(self, item, spider):
        cleaned_item = self.clean_item(dict(item))
        try:
            self.es.index(index="cu_publication", body=cleaned_item)
            spider.logger.info(f"Publication indexed successfully: {cleaned_item.get('title')}")
        except Exception as e:
            spider.logger.error(f"Error indexing publication: {e}")
            raise DropItem(f"Failed to index publication: {e}")
        return cleaned_item

    def clean_item(self, item):
        # item['title'] = item.get('title', '').strip()
        #
        # authors = item.get('authors', '')
        # if isinstance(authors, str):
        #     authors = [authors]
        # item['authors'] = ', '.join(a.strip() for a in authors if a.strip()) or 'N/A'
        #
        # pub_year = item.get('publication_year', '').strip()
        # item['publication_year'] = pub_year or 'N/A'
        #
        # abstract = item.get('abstract', '').strip()
        # item['abstract'] = abstract or 'No Abstract'
        #
        # departments = item.get('departments', '').strip()
        # item['departments'] = departments or 'N/A'
        #
        # organizations = item.get('organizations', '')
        # if isinstance(organizations, str):
        #     organizations = [organizations]
        # item['organizations'] = ', '.join(o.strip() for o in organizations if o.strip()) or 'N/A'
        #
        # keywords = item.get('keywords', '')
        # if isinstance(keywords, str):
        #     keywords = [keywords]
        # item['keywords'] = ', '.join(k.strip() for k in keywords if k.strip()) or 'N/A'
        #
        # fingerprints = item.get('fingerprints', '')
        # if isinstance(fingerprints, str):
        #     fingerprints = [fingerprints]
        # item['fingerprints'] = ', '.join(f.strip() for f in fingerprints if f.strip()) or 'N/A'
        #
        # item['publication_url'] = item.get('publication_url', '').strip() or 'N/A'

        return item

    def close_spider(self, spider):
        spider.logger.info('ElasticCleanPipeline: Closing spider and Elasticsearch connection.')
        self.es.transport.close()
