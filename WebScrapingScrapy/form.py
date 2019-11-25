import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select


def fill_form(url):
    options = Options()
    options.headless = True
    browser = webdriver.Chrome("C:/chromedriver.exe", chrome_options=options)
    browser.get(url)
    browser.find_element_by_link_text('Osobowe').click()
    time.sleep(0.4)
    select_brand = Select(browser.find_element_by_id('param571'))
    select_brand.select_by_value('opel')
    select_model = Select(browser.find_element_by_id('param573'))
    select_model.select_by_visible_text('Corsa')
    select_min_price = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[4]/span[1]/select"))
    select_min_price.select_by_value('2000')
    select_max_price = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[4]/span[2]/select"))
    select_max_price.select_by_value('20000')
    select_min_production_year = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[5]/span[1]/select"))
    select_min_production_year.select_by_value('2009')
    select_max_production_year = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[5]/span[2]/select"))
    select_max_production_year.select_by_value('2019')
    select_min_mileage = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[6]/span[1]/select"))
    select_min_mileage.select_by_value('75000')
    select_max_mileage = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[6]/span[2]/select"))
    select_max_mileage.select_by_value('150000')
    fuel_type = browser.find_element_by_xpath("//*[@id='searchmain_29']/div[7]/span[2]")
    fuel_type.click()
    search_button = browser.find_element_by_xpath("//*[@id='searchmain_29']/button[1]/span[1]")
    browser.execute_script("arguments[0].click();", search_button)
    time.sleep(0.5)
    return browser.current_url
