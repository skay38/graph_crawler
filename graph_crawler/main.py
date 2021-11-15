from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from graph_crawler.spiders.graph_crawler import GraphCrawlerSpider, G

import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt

from scrapy.utils.project import get_project_settings
settings = get_project_settings()

process = CrawlerProcess(settings)
process.crawl(GraphCrawlerSpider)
process.start()

pos_ = nx.spring_layout(G)

def make_edge(x, y, width):
    return  go.Scatter(
        x=x,
        y=y,
        line=dict(
            width=width,
            color='cornflowerblue'),
        mode ='lines')

edge_trace = []
for edge in G.edges():
    char_1 = edge[0]
    char_2 = edge[1]
    x0, y0 = pos_[char_1]
    x1, y1 = pos_[char_2]

    trace = make_edge([x0, x1, None], [y0, y1, None], width = 0.3)
    edge_trace.append(trace)

node_trace = go.Scatter(x=[], y=[], text=[], textposition="top center", textfont_size=10, mode='markers+text', hoverinfo='none',
    marker=dict(color=[], size=[], line=None))

for node in G.nodes():
    x, y = pos_[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['marker']['color'] += tuple(['cornflowerblue'])
    node_trace['text'] += tuple(['<b>' + node + '</b>'])

layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)', # transparent background
    plot_bgcolor='rgba(0,0,0,0)', # transparent 2nd background
    xaxis =  {'showgrid': False, 'zeroline': False}, # no gridlines
    yaxis = {'showgrid': False, 'zeroline': False}, # no gridlines
)


fig = go.Figure(layout = layout)
for trace in edge_trace:
    fig.add_trace(trace)
fig.add_trace(node_trace)
fig.update_layout(showlegend = False)
fig.update_xaxes(showticklabels = False)
fig.update_yaxes(showticklabels = False)
fig.show()