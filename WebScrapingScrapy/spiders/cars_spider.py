import scrapy
import csv

from WebScrapingScrapy.annoucement import Annoucement
from WebScrapingScrapy.form import fill_form


class CarsSpider(scrapy.Spider):
    name = 'cars'
    first_url = 'https://www.otomoto.pl/'
    list_of_articles = []
    pages_counter = 0
    number_of_pages = 0

    def __init__(self):
        self.first_url = fill_form(self.first_url)

    def start_requests(self):
        yield scrapy.Request(url=self.first_url, callback=self.parse)

    def write_to_csv(self):
        with open('cars.csv', 'w', newline='') as csv_file:
            fieldnames = ['model', 'production year', 'mileage', 'engine capacity', 'price', 'currency', 'city',
                          'region']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for a in self.list_of_articles:
                writer.writerow({'model': a.model_name, 'production year': a.production_year, 'mileage': a.mileage,
                                 'engine capacity': a.engine_capacity, 'price': a.price, 'currency': a.currency,
                                 'city': a.city, 'region': a.region})

    def parse(self, response):
        self.parse_page(response)
        list_of_pages = response.xpath('//ul[@class = "om-pager rel"]/li/a/@href').extract()
        base_url = list_of_pages[0][0:len(list_of_pages[0]) - 1]
        last_page_url = list_of_pages[len(list_of_pages) - 2]

        self.number_of_pages = int(last_page_url.split("page=", 1)[1])
        print(self.number_of_pages)

        for page in range(2, self.number_of_pages + 1):
            page_url = base_url + str(page)
            yield scrapy.Request(url=page_url, callback=self.parse_page)

    def parse_page(self, response):
        self.pages_counter += 1
        model_names = response.xpath('//h2[@class = "offer-title ds-title"]/a/text()').extract()
        general_infos = response.xpath('//ul[@class = "ds-params-block"]/li[@class = "ds-param"]/span/text()').extract()
        price_infos = response.xpath(
            '//div[@class = "offer-price ds-price-block"]/span[@class = "offer-price__number '
            'ds-price-number"]/span/text()').extract()
        location_infos = response.xpath('//h4[@class = "ds-location hidden-xs"]/span/text()').extract()
        for a in range(0, len(model_names) - 1):
            model_name = model_names[a].strip()
            production_year = general_infos[4 * a].strip()
            mileage = general_infos[4 * a + 1].strip()
            engine_capacity = general_infos[4 * a + 2].strip()
            fuel_type = general_infos[4 * a + 3].strip()
            price = price_infos[2 * a].strip()
            currency = price_infos[2 * a + 1].strip()
            city = location_infos[2 * a].strip()
            region = location_infos[2 * a + 1]
            region = region[1:len(region) - 1]
            self.list_of_articles.append(
                Annoucement(model_name, production_year, mileage, engine_capacity, fuel_type, price, currency, city,
                        region))

        if self.pages_counter == self.number_of_pages:
            self.write_to_csv()

