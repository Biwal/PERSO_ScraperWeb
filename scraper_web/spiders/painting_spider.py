from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scraper_web.items import PaintingItem


class ExtractURLFromWikiCategorySpider(CrawlSpider):
    name = "Painting_Wiki"
    allowed_domains = ["wikipedia.org"]
    base_url = "https://en.wikipedia.org"
    start_urls = ["https://en.wikipedia.org/wiki/Category:Paintings"]
    rules = (
        Rule(
            LinkExtractor(
                allow=[
                    "https://en.wikipedia.org/wiki/Category",
                    "https://en.wikipedia/w",
                ],
                deny=[
                    "https://en.wikipedia.org/wiki/Category:Commons_category_link_is_on_Wikidata",
                    "https://en.wikipedia.org/wiki/Category:Categories_requiring_diffusion",
                ],
                unique=True,
                restrict_css=[
                    "div.mw-category-group a",
                    "div#mw-subcategories a",
                    "div.mw-category-generated a",
                ],
            ),
            callback="parse_category",
            follow=True,
        ),
    )

    def parse_start_url(self, response):
        return Request(url=self.start_urls[0], callback=self.parse_category,)

    def parse_category(self, response):
        for link in response.css(".mw-category-group a") or response.css(
            "div.mw-category-generated a"
        ):
            href = link.attrib["href"]
            url = self.base_url + href
            if any(s in href for s in ("Category:", "File:", "Wikipedia:")):
                continue
            # elif ("/List_of") in href:
            #     # yield Request(url, callable=self.parse_list)
            # else:
            #     yield Request(url, callback=self.parse_page)
            yield {"href": link.attrib["href"]}

    def parse_page(self, response):
        loader = ItemLoader(
            item=PaintingItem(),
            selector=response.css("table.infobox "),
            response=response,
        )
        loader.add_value("title", response.css("h1#firstHeading *::text").getall())
        loader.add_value("wiki_url", response.url)
        loader.add_xpath("artist", self.get_xpath_infobox_row("Artist"))
        loader.add_xpath("year", self.get_xpath_infobox_row("Year"))
        loader.add_xpath("medium", self.get_xpath_infobox_row("Medium"))
        loader.add_xpath("location", self.get_xpath_infobox_row("Location"))
        loader.add_xpath("dimensions", self.get_xpath_infobox_row("Dimensions"))
        yield loader.load_item()

    def parse_list(self, response):
        pass

    def get_xpath_infobox_row(self, string):
        return "".join(
            ['//th[starts-with(text(),"', string, '")]/../descendant::text()']
        )

    #  def parse_page_infobox(self, response):
    #     envart = response.css("table.infobox ")

    #     data = {}
    #     data["Title"] = response.css("h1#firstHeading *::text").getall()
    #     data["URL"] = response.url
    #     data["Artiste"] = self.get_row_box_text(envart, "Artist")
    #     data["Year"] = self.get_row_box_text(envart, "Year")
    #     data["Type"] = self.get_row_box_text(envart, "Type")
    #     data["Medium"] = self.get_row_box_text(envart, "Medium")
    #     data["Dimensions"] = self.get_row_box_text(envart, "Dimensions")
    #     data["Location"] = self.get_row_box_text(envart, "Location")
    #     yield data

    # def get_row_box_text(self, content, string):
    #     text = content.xpath(
    #         "".join(['//th[starts-with(text(),"', string, '")]/../descendant::text()'])
    #     ).getall()
    #     "".join(text[2:]).strip()
    #     return text[1:]
