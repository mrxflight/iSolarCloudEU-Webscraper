from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

#uses Selenium WebDriver to webScrape data from https://www.isolarcloud.eu/
#Made by Mr_X_flight

firefox_options = Options()
firefox_options.headless = True

USER_ACCOUNT = 'Your Username'
USER_PASSWORD = 'Your Password'

driver = webdriver.Firefox(options=firefox_options)

delay = 6

driver.get('https://www.isolarcloud.eu/')
driver.find_element_by_class_name('agree-btn').click()
driver.find_element(By.NAME, "userAcct").send_keys(USER_ACCOUNT)
driver.find_element(By.NAME, "userPswd").send_keys(USER_PASSWORD)
driver.find_element(By.ID, "login-btn").click()

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'privacy-agree')))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")

driver.execute_script('agreeService()')

delay = 6

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'data')))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")

driver.find_element(By.CLASS_NAME, "two-row-hide").click()

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, '文本_发电to电网')))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")

html = driver.page_source

soup = BeautifulSoup(html, features="lxml")

energy_values_array = []

energy_values_array.append(["current_Energy_Consumption", soup.find("div",{"id":"文本_用电"}).string])
energy_values_array.append(["current_Energy_Production" , soup.find("div",{"id":"文本_发电"}).string])
energy_values_array.append(["current_Energy_Feed" , soup.find("div",{"id":"文本_发电to电网"}).string])
energy_values_array.append(["current_Energy_From_Grid" , soup.find("div",{"id":"文本_电网to用电"}).string])
energy_values_array.append(["current_Battery_Charge" , soup.find("div",{"id":"文本_电量"}).string])
energy_values_array.append(["current_Energy_Charging_Battery" , soup.find("div",{"id":"文本_发电to电池"}).string])
energy_values_array.append(["current_Battery_Usage" , soup.find("div",{"id":"文本_电池to用电"}).string])

for x in energy_values_array:
    if isinstance(x[1], str):
        print(x[0] + ": " + x[1])
    else:
        print(x[0] + ": 0 W")

driver.quit()