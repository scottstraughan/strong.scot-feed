#!/usr/bin/python python3

import logging
import os

from markdownfeeds import write_to_file
from markdownfeeds.Gatherer import Gatherer
from markdownfeeds.Generators import GeneratorSettings
from markdownfeeds.Generators.Default.Models.FeedItem import FeedItem
from markdownfeeds.Generators.Json.JsonFeedGenerator import JsonFeedGenerator
from markdownfeeds.Generators.Json.Models.JsonFeed import JsonFeed
from markdownfeeds.Generators.Json.Models.JsonFeedItem import JsonFeedItem
from markdownfeeds.MarkdownFile import MarkdownFile
from slugify import slugify

logging.basicConfig(level=logging.INFO)

site_base_url = 'https://www.strong.scot'


def generate_routes_file(
    generator_settings: GeneratorSettings,
    collection: str,
    feed_items: [FeedItem]
):
    routes = [f"{site_base_url}/{collection}/{x.get('tag')}" for x in feed_items]
    target_routes_file = os.path.join(generator_settings.get('target_directory'), 'routes.txt')
    write_to_file(target_routes_file, os.linesep.join(routes))


class CustomFeedGenerator(JsonFeedGenerator):
    def _sort_feed_items(
        self,
        feed_items: [FeedItem]
    ) -> [FeedItem]:
        feed_items.sort(key=lambda item: item.get('date'), reverse=True)

        # Generate routes
        generate_routes_file(self.generator_settings, 'rants', feed_items)

        # Return feed items
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