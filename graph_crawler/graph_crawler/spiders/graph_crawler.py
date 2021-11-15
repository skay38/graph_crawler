from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings

import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt

settings = get_project_settings()
G = nx.DiGraph()

class GraphCrawlerSpider(CrawlSpider):
    name = 'graph_crawler'
    allowed_domains = settings['ALLOWED_DOMAINS']

    start_urls = settings['START_URLS']
    rules = [Rule(LinkExtractor(deny=settings['DENY_LIST']), callback='parse_item', follow=True)]


    # def __init__(self, *a, **kv):
    #     super(GraphCrawlerSpider, self).__init__(*a, **kv)
    #     self.allowed_domains = kv['allowed_domains']

    #     self.start_urls = kv['start_urls']
    #     self.rules = [Rule(LinkExtractor(deny=kv['deny_list']), callback='parse_item', follow=True)]

    def parse_item(self, response):
        url = response.url[7:]
        if url not in G.nodes:
            G.add_node(url)
        G.add_edge('/'.join(url.split('/')[:-1]), url)
