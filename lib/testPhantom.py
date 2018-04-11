from selenium import webdriver

driver= webdriver.PhantomJS()
#driver= webdriver.Chrome()
#driver.implicitly_wait(5) # 3sec for resouce load

driver.get('https://kor.tellburgerking.com/')
driver.find_element_by_xpath('//*[@id="NextButton"]').click()
#btnClick.click()

inCode= "8306743170460160"

driver.find_element_by_xpath('//*[@id="CN1"]').send_keys(inCode[0:3])
driver.find_element_by_xpath('//*[@id="CN2"]').send_keys(inCode[3:6])
driver.find_element_by_xpath('//*[@id="CN3"]').send_keys(inCode[6:9])
driver.find_element_by_xpath('//*[@id="CN4"]').send_keys(inCode[9:12])
driver.find_element_by_xpath('//*[@id="CN5"]').send_keys(inCode[12:15])
driver.find_element_by_xpath('//*[@id="CN6"]').send_keys(inCode[15])

driver.find_element_by_xpath('//*[@id="NextButton"]').click()


#driver.find_element_by_xpath('//*div[@class="Opt3 rbloption"]/span/span[@class="radioBranded"]').click()
driver.find_element_by_xpath('//*div[contains(@class,"Opt3") and contains(@class,"rbloption")]\
        /span/input[@type="radio"]').click()


driver.find_element_by_xpath('//*[@id="NextButton"]').click()

