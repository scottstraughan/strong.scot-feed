#!/usr/bin/python python3

import logging

from markdownfeeds.Gatherer import Gatherer
from markdownfeeds.Generators import GeneratorSettings
from markdownfeeds.Generators.Default.Models.FeedItem import FeedItem
from markdownfeeds.Generators.Json.JsonFeedGenerator import JsonFeedGenerator
from markdownfeeds.Generators.Json.Models.JsonFeed import JsonFeed
from markdownfeeds.Generators.Json.Models.JsonFeedItem import JsonFeedItem
from markdownfeeds.MarkdownFile import MarkdownFile
from slugify import slugify

logging.basicConfig(level=logging.INFO)


class CustomFeedGenerator(JsonFeedGenerator):
    def _sort_feed_items(
        self,
        feed_items: [FeedItem]
    ) -> [FeedItem]:
        feed_items.sort(key=lambda item: item.get('date'), reverse=True)
        return feed_items

    def process_markdown_file_to_feed_item(
        self,
        markdown_file: MarkdownFile
    ) -> JsonFeedItem:
        feed_item = super().process_markdown_file_to_feed_item(markdown_file)
        feed_item.set('content', markdown_file.html)
        feed_item.set('tag', CustomFeedGenerator.create_tag(feed_item))
        return feed_item

    @staticmethod
    def create_tag(
        feed_item: FeedItem
    ) -> str:
        date = feed_item.markdown_file.date.strftime("%Y-%m-%d")

        return slugify(date + '-' + feed_item.get('title'))


Gatherer([
    CustomFeedGenerator(
        feed=JsonFeed(title='Rants'),
        generator_settings=GeneratorSettings(
            source_directory='content/rants',
            target_directory='build/rants',
            feed_items_per_export=20,
        )
    ),
]).generate()