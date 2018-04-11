from selenium import webdriver

driver= webdriver.Chrome()
#driver.implicitly_wait(5)

driver.get('https://www.acmicpc.net/user/firstock')
a= driver.find_element_by_xpath('//*[@id="statics"]/tbody/tr[2]\
        /td').text
b= driver.find_element_by_xpath('//*[@class="page-header"]/h1').text
print(a)
print(b)

