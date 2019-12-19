import csv
from time import sleep

import scrapy
from selenium import webdriver

from WebScrapingScrapy.offer import Offer

class OffersSpider(scrapy.Spider):
    name = 'offers'
    first_url = 'https://www.olx.pl/praca/'
    list_of_offers = []
    pages_counter = 0
    number_of_pages = []

    def write_to_csv(self):
        with open('offers.csv', 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['title', 'location', 'time_of_work', 'type_of_agreement', 'salary', 'article_url']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for o in self.list_of_offers:
                writer.writerow(
                    {'title': o.title, 'location': o.location, 'time_of_work': o.time_of_work,
                     'type_of_agreement': o.type_of_agreement, 'salary': o.salary, 'article_url': o.article_url})

    def fill_form(self,city, category, type_of_agreement):
        browser = webdriver.Chrome("C:/chromedriver.exe")
        browser.get("https://www.olx.pl/praca/")
        if category == 'i':
            category = 'IT / telekomunikacja'
        elif category == 'b':
            category = 'Budowa / remonty'
        elif category == 'g':
            category = 'Gastronomia'
        elif category == 'a':
            category = 'Administracja biurowa'

        if type_of_agreement == 'a':
            xpath = '//*[@id="f-part_contract"]'
        elif type_of_agreement == 'b':
            xpath = '//*[@ id = "param_contract"]/div/ul/li[3]/label[2]'
        elif type_of_agreement == 'c':
            xpath = '//*[@id="param_contract"]/div/a/span[1]'

        show_all = browser.find_element_by_xpath('//*[@id="topLinkShowAll"]/span/span')
        browser.execute_script("arguments[0].click()", show_all)
        category = browser.find_element_by_link_text(category)
        browser.get(category.get_attribute('href'))
        browser.find_element_by_id('cityField').send_keys(city)
        contract = browser.find_element_by_xpath('//*[@id="param_contract"]/div/a/span[1]')
        browser.execute_script("arguments[0].click()", contract)
        sleep(0.5)
        type = browser.find_element_by_xpath(xpath)
        browser.execute_script("arguments[0].click()", type)
        search = browser.find_element_by_id('search-submit')
        browser.execute_script("arguments[0].click()", search)
        sleep(1)
        print(browser.current_url)
        return browser.current_url

    def __init__(self):
        print('Wpisz miasto')
        city = input()
        print('Wybierz specjalność: i - IT, g - Gastronomia, b - Budownictwo, a - Administracja')
        category = input()
        print('Wybierz czas pracy: a - umowa o pracę, b - umowa o dzieło, c - umowa zlecenie')
        type_of_agreement = input()
        self.first_url = self.fill_form(city, category, type_of_agreement)

    def start_requests(self):
        yield scrapy.Request(url=self.first_url, callback=self.parse)

    def parse_page(self,response):
        self.pages_counter = self.pages_counter+1
        offer_element = response.css('a[class = "marginright5 link linkWithHash detailsLink"]')
        titles = response.css('a[class = "marginright5 link linkWithHash detailsLink"] strong::text').extract()
        offers_urls = response.css('a[class = "marginright5 link linkWithHash detailsLink"]::attr(href)').extract()
        locations = response.css('small[class = "breadcrumb x-normal"] span::text').extract()
        times_of_work = response.css('small[class = "breadcrumb breadcrumb--job-type x-normal"] span::text').extract()
        types_of_agreements = response.css('small[class = "breadcrumb breadcrumb--with-divider x-normal"] span::text').extract()
        salaries = response.css('div[class = "list-item__price"] span::text').extract()

        for i in range(0, len(offer_element)):
            title = titles[i]
            url = offers_urls[i]
            location = locations[4*i+1].strip()
            time_of_work = times_of_work[i].strip()
            type_of_agreement = types_of_agreements[i].strip()
            if 4*i+3<=len(salaries)-1:
                salary=salaries[4*i]+salaries[4*i+1]+salaries[4*i+2]+salaries[4*i+3]
            else:
                salary = "None"

            offer = Offer(title,location,time_of_work, type_of_agreement, salary, url)
            self.list_of_offers.append(offer)

        if self.pages_counter == self.number_of_pages:
            self.write_to_csv()


    def parse(self, response):
        link_elements = response.xpath('//*[@id="body-container"]/div[3]/div/div[8]/span/a/@href').extract()
        link_elements.pop()
        self.number_of_pages = len(link_elements)

        for l in link_elements:
            yield scrapy.Request(url=l, callback=self.parse_page)