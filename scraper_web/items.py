# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

def select_row_infobox_content(text):
    p = "".join(text[1:]).strip()
    return p

class PaintingItem(Item):
    title = Field()
    wiki_url = Field()
    artist = Field(input_processor=select_row_infobox_content)
    year = Field(input_processor=select_row_infobox_content)
    medium = Field(input_processor=select_row_infobox_content)
    dimensions = Field(input_processor=select_row_infobox_content)
    location = Field(input_processor=select_row_infobox_content)