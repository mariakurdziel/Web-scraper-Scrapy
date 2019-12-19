import time
from selenium import webdriver
from selenium.webdriver.support.select import Select


def fill_form(url, brand, model, min_price, max_price, min_mileage, max_mileage, min_year, max_year):
    browser = webdriver.Chrome("C:/chromedriver.exe")
    browser.get(url)
    browser.find_element_by_link_text('Osobowe').click()
    time.sleep(0.4)
    select_brand = Select(browser.find_element_by_id('param571'))
    select_brand.select_by_value(brand)
    select_model = Select(browser.find_element_by_id('param573'))
    select_model.select_by_visible_text(model)
    select_min_price = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[4]/span[1]/select"))
    select_min_price.select_by_value(min_price)
    select_max_price = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[4]/span[2]/select"))
    select_max_price.select_by_value(max_price)
    select_min_production_year = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[5]/span[1]/select"))
    select_min_production_year.select_by_value(min_year)
    select_max_production_year = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[5]/span[2]/select"))
    select_max_production_year.select_by_value(max_year)
    select_min_mileage = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[6]/span[1]/select"))
    select_min_mileage.select_by_value(min_mileage)
    select_max_mileage = Select(browser.find_element_by_xpath("//*[@id='searchmain_29']/div[6]/span[2]/select"))
    select_max_mileage.select_by_value(max_mileage)
    fuel_type = browser.find_element_by_xpath("//*[@id='searchmain_29']/div[7]/span[2]")
    fuel_type.click()
    search_button = browser.find_element_by_xpath("//*[@id='searchmain_29']/button[1]/span[1]")
    browser.execute_script("arguments[0].click();", search_button)
    time.sleep(0.5)
    return browser.current_url
