from selenium import webdriver

PATH = "E:/Git/Projekt-Programistyczny/testy_selenium/chromedriver.exe"
driver = webdriver.Chrome(PATH)

site = "https://techwithtim.net"

driver.get(site)
print(driver.title)
driver.quit()
