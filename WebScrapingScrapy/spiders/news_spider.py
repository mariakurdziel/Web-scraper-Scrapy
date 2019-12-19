import csv
import random
import string
import time

import requests
import scrapy
from selenium import webdriver
from WebScrapingScrapy.article import Article


class NewsSpider(scrapy.Spider):
    name = 'news'
    first_url = 'https://www.onet.pl/'
    list_of_articles = []
    category = ''
    number_of_news = 0

    def __init__(self):
        self.start()

    def start_requests(self):
        yield scrapy.Request(url=self.first_url, callback=self.parse)

    def write_to_csv(self):
        with open('articles.csv', 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['title', 'description', 'text', 'image name']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for a in self.list_of_articles:
                writer.writerow(
                    {'title': a.title, 'description': a.description, 'text': a.text, 'image name': a.image_name})

    def scrape_image(self, url, image_name):
        response = requests.get('http:' + url)
        if response.status_code == 200:
            with open('./WebScrapingScrapy/images/onet/' + image_name, 'wb') as f:
                f.write(response.content)

    def set_image_name(self):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(10)) + '.jpg'

    def get_news_links(self, url):
        articles_links = []
        browser = webdriver.Chrome("C:/chromedriver.exe")
        browser.get(url)

        while len(articles_links) < self.number_of_news:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.3)
            articles_links = browser.find_elements_by_xpath("//div[contains(@class, 'items solrList ')]/a")

        articles_links = articles_links[0:self.number_of_news]

        return [x.get_attribute('href') for x in articles_links]

    def parse(self, response):
        category_url = ''
        if self.category == 'k':
            category_name = 'Kultura'
        elif self.category == 'w':
            category_name = 'Wiadomości'
        elif self.category == 's':
            category_name = 'Sport'
        list_of_links = response.xpath('//ul[@class = "mainMenu"]/li/a/@href').extract()
        list_of_names = response.xpath('//ul[@class = "mainMenu"]/li/a/text()').extract()

        list_of_names = [x.strip() for x in list_of_names]
        list_of_categories = [x for x in list_of_names if len(x) != 0]

        for i in range(0, len(list_of_categories)):
            if list_of_categories[i] == category_name:
                category_url = list_of_links[i]
                break

        list_of_news_urls = self.get_news_links(category_url)

        for url in list_of_news_urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        raw_title = response.xpath('//title/text()').extract()
        title = raw_title[0].splitlines()[1]
        description = response.xpath('//meta[@name = "description"]/@content').extract()[0]
        paragraphs = response.xpath('//p[@class = "hyphenate "]/text()').extract()
        text = ''
        for p in paragraphs:
            text += p
        image_name = ''

        if len(response.xpath('//picture')) != 0:
            image_url = response.xpath('//picture/meta/@content').extract()[0]
            image_name = image_url.rsplit('/', 1)[1]
            if image_name == '.jpg':
                image_name = self.set_image_name()

            self.scrape_image(image_url, image_name)
        else:
            image_name = "No image found"

        self.list_of_articles.append(Article(title, description, text, image_name))

        if len(self.list_of_articles) == self.number_of_news:
            self.write_to_csv()

    def start(self):
        print('Wybierz kategorię newsów: w - Wiadomości, k - Kultura, s - Sport')
        self.category = input()
        print('Wpisz ilość newsów:')
        self.number_of_news = int(input())