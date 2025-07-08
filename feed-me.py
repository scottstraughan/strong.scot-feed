#!/usr/bin/python python3

import logging

from markdownfeeds.Gatherer import Gatherer
from markdownfeeds.Generators import GeneratorSettings
from markdownfeeds.Generators.Json.JsonFeedGenerator import JsonFeedGenerator
from markdownfeeds.Generators.Json.Models.JsonFeed import JsonFeed

logging.basicConfig(level=logging.INFO)

Gatherer([
    JsonFeedGenerator(
        feed=JsonFeed(title='Rants'),
        generator_settings=GeneratorSettings(
            source_directory='content/rants',
            target_directory='build/rants',
            feed_items_per_export=20
        )
    ),
]).generate()