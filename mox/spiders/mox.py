import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from mox.items import Article
import requests
import json
import re


class moxSpider(scrapy.Spider):
    name = 'mox'
    start_urls = ['https://mox.com/media/']

    def parse(self, response):
        json_response = json.loads(requests.get("https://mox.com/page-data/media/page-data.json").text)
        articles = json_response["result"]["data"]["allContentfulBlogPost"]["edges"]
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article["node"]["title"]
            if title and title.strip():
                title = title.strip()
            date = article["node"]["publishDate"]
            if date and date.strip():
                date = date.strip()
            content = article["node"]["content"]["childMarkdownRemark"]["html"]
            p = re.compile(r'<.*?>')
            content = p.sub('', content)

            if content == "Video":
                continue

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()
