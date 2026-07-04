import csv
import json
import xml.etree.ElementTree as ET
from merchant_feeds.models import FeedType

class FeedParserService:
    @staticmethod
    def parse_feed(file_path, feed_type):
        """Generator that yields parsed items from a feed file."""
        if feed_type == FeedType.CSV:
            yield from FeedParserService._parse_csv(file_path)
        elif feed_type == FeedType.JSON:
            yield from FeedParserService._parse_json(file_path)
        elif feed_type == FeedType.XML:
            yield from FeedParserService._parse_xml(file_path)
        else:
            raise ValueError(f"Unsupported feed type: {feed_type}")

    @staticmethod
    def _parse_csv(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

    @staticmethod
    def _parse_json(file_path):
        # We assume the JSON is a simple array of objects
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    yield item
            elif isinstance(data, dict):
                # Guess where the array is
                for key, val in data.items():
                    if isinstance(val, list):
                        for item in val:
                            yield item
                        break
                else:
                    yield data
            else:
                yield data

    @staticmethod
    def _parse_xml(file_path):
        context = ET.iterparse(file_path, events=("end",))
        for event, elem in context:
            if elem.tag.lower() in ('product', 'item', 'listing'):
                data = {}
                for child in elem:
                    data[child.tag] = child.text
                yield data
                elem.clear()
