import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

class MotointegratorSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def ajax_complete(self, driver):
	 try:
		return 0 == self.driver.execute_script("return jQuery.active")
	 except WebDriverException:
		pass

    def test_search_in_motointegrator_pl(self):
        driver = self.driver
        driver.get("http://www.motointegrator.pl")
        self.assertIn("Motointegrator", driver.title)
	#Wybierz pojazd
	self.search(driver, '//button[text()="Wybierz pojazd"]', '')	
	#wyszukanie modelu Opel ASTRA J 1.4 Turbo, moc: 140 KM/103 kW
	self.searchForVehicle(driver)
	#klikniecie w menu Opony
	self.chooseTyres(driver)
	#filtrowanie po: Typ pojazdu: samochody osobowe
	self.chooseTypeOfVehicle(driver)
	#Szukaj opon
	self.search(driver, '//button[text()="Szukaj opon"]', '')
	#Przejdz na druga strone
	self.goToPage(driver)
	#sortuj od najtanszych
	self.sortFromCheapest(driver)

	
	

    def searchForVehicle(self, driver):
	#rok produkcji
	self.selectElement(driver, "#jqs-vehicle-chain select[name='year']+span>a", '/html/body/div[10]/div/div[9]/div/div/form/div/ul/li[2]/div/span/a', '2009')
	#marka pojazdu
	self.selectElement(driver, "#jqs-vehicle-chain select[name='manufacturer_id']+span>a", '/html/body/div[10]/div/div[9]/div/div/form/div/ul/li[3]/div/span/a', 'Opel')
	#model pojazdu
	driver.execute_script("(document.evaluate('/html/body/div[10]/div/div[9]/div/div/form/div/ul/li[4]/div/span/a/span[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).innerHTML='<div class=""selectmenu-wrapper clearfix""><table class=""selectmenu-opts""><tbody><tr><td style=""width:300px"">ASTRA J</td><td>2009</td></tr></tbody></table></div>'")	
	self.selectElement(driver, "#jqs-vehicle-chain select[name='model_id']+span>a", '/html/body/div[10]/div/div[9]/div/div/form/div/ul/li[4]/div/span/a', 'ASTRA J 2009')
	#typ
	driver.execute_script("(document.evaluate('/html/body/div[10]/div/div[9]/div/div/form/div/ul/li[5]/div/span/a/span[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).innerHTML='<div class=""selectmenu-wraper clearfix""><table class=""selectmenu-opts""><tbody><tr class=""selected-show""><td valign=""top"">1.4 Turbo, 140 KM (103 kW)</td></tr></tbody></table></div>'")
	self.selectElement(driver, "#jqs-vehicle-chain select[name='vehicle_id']+span>a", '/html/body/div[10]/div/div[9]/div/div/form/div/ul/li[5]/div/span/a', '1.4 Turbo, 140 KM (103 kW)')
	#wybierz
	WebDriverWait(driver, 10).until(self.ajax_complete,  "Timeout waiting for page to load")
	self.search (driver, '/html/body/div[10]/div/div[9]/div/div/form/div/div[1]/button', "Opel ASTRA J 1.4 Turbo, moc: 140 KM/103 kW")

    def search(self, driver, xpath, textToAssert):
	element = driver.find_element(By.XPATH, xpath)
	ActionChains(driver).move_to_element(element).click(element).perform()
	WebDriverWait(driver, 10).until(self.ajax_complete,  "Timeout waiting for page to load")
	self.assertIn(textToAssert, driver.page_source)	

    def selectElement(self, driver, css_selector, xpath, text):
	driver.find_element_by_css_selector(css_selector).click()
	element = driver.find_element(By.XPATH, xpath)
	ActionChains(driver).move_to_element(element).click(element).perform()
	ActionChains(driver).send_keys(text).perform()
	WebDriverWait(driver, 10).until(self.ajax_complete,  "Timeout waiting for page to load")

    def chooseTyres(self, driver):
	driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/section[1]/nav/ul/nav/ul/li/ul/li[2]/ul/li[1]/a').click()
	WebDriverWait(driver, 10).until(self.ajax_complete,  "Timeout waiting for page to load")
	self.assertIn('Rozmiary opon dla Twojego auta', driver.page_source)

    def chooseTypeOfVehicle(self, driver):
	element = driver.find_element_by_css_selector("div.select-field:nth-child(5) > button:nth-child(3)")
	element.click()
	driver.find_element_by_css_selector("#ui-multiselect-16-option-1").click()
	element.click()
	WebDriverWait(driver, 10).until(self.ajax_complete,  "Timeout waiting for page to load")

    def goToPage(self, driver):
	driver.find_element_by_css_selector("div.sort-paginator-wrap:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(3) > a:nth-child(1)").click()
	WebDriverWait(driver, 10).until(self.ajax_complete,  "Timeout waiting for page to load")

    def sortFromCheapest(self, driver):
	driver.find_element_by_css_selector("#id_sort > li:nth-child(2) > a:nth-child(1)").click()
	WebDriverWait(driver, 10).until(self.ajax_complete,  "Timeout waiting for page to load")

    def tearDown(self):
        self.driver.close()



if __name__ == "__main__":
    unittest.main()
