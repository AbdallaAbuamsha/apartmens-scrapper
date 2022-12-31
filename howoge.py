import time

from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from company import Company


class Howoge(Company):
    def apply(self, driver: webdriver):
        if driver.current_url == 'https://www.howoge.de/404-wohnungssuche.html':
            return
        self.remove_cookies_popup(driver)
        try:
            driver.find_element(By.XPATH, '//*[@id="gewerbe-form-wrapper"]/div/div/div/div/div[1]/div[3]/a').click()
            email = driver.find_element(By.XPATH, '//*[@id="input-email"]')
            email.send_keys("eng.a.abuamsha@gmail.com")
            driver.find_element(By.XPATH, '//*[@id="email-form"]/div[3]/div[2]/input').click()
        except:
            #driver.find_element(By.XPATH, '//*[@id="gewerbe-form-wrapper"]/div/div/div/div/div[1]/div[3]/a').click()
            try:
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[2]/div[1]/div/div/div[2]/label').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[2]/div[2]/div/div/div[2]/button').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[3]/div[1]/div/div[3]/label').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[3]/div[2]/div/div/div[2]/button').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[4]/div[2]/div/label').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[4]/div[3]/div/div/div[2]/button').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[5]/div[1]/div/label').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[5]/div[2]/div/div/div[2]/button').click()
            except:
                driver.find_element(By.XPATH, '//*[@id="gewerbe-form-wrapper"]/div/div/div/div/div[1]/div[2]/a').click()
                driver.find_element(By.XPATH,
                                    '//*[@id="main"]/div[4]/div/div/div[2]/div[1]/div/div/div[2]/label').click()
                driver.find_element(By.XPATH,
                                    '//*[@id="main"]/div[4]/div/div/div[2]/div[2]/div/div/div[2]/button').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[3]/div[1]/div/div[3]/label').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[3]/div[2]/div/div/div[2]/button').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[4]/div[2]/div/label').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[4]/div[3]/div/div/div[2]/button').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[5]/div[1]/div/label').click()
                driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/div/div[5]/div[2]/div/div/div[2]/button').click()


            driver.find_element(By.XPATH, '//*[@id="show-visit-form"]/div[2]/div[2]/div[2]/div[1]/div/input').send_keys(
                "Abdallah")
            driver.find_element(By.XPATH, '//*[@id="show-visit-form"]/div[2]/div[2]/div[2]/div[2]/div/input').send_keys(
                "Abuamsha")
            driver.find_element(By.XPATH, '//*[@id="email"]').send_keys("eng.a.abuamsha@gmail.com")
            driver.find_element(By.XPATH, '//*[@id="show-visit-form"]/div[2]/div[2]/div[3]/div[2]/div/input').send_keys(
                "017646601946")
            driver.find_element(By.XPATH, '//*[@id="show-visit-form"]/div[3]/div/div[1]/div[2]/button').click()

            WebDriverWait(driver, 5) \
                .until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="main"]/div[4]/div/div/div[7]/div/div/div[1]')))
            time.sleep(3)
    def remove_cookies_popup(self, driver):
        try:
            WebDriverWait(driver, 1) \
                .until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="cmpwelcomebtnyes"]/a')))
            accept_cookies_button = driver.find_element(By.XPATH,
                                                        '//*[@id="cmpwelcomebtnyes"]/a')
            accept_cookies_button.click()
        finally:
            return

if __name__ == '__main__':
    # get driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    inBerlin_wohnen_page = driver.window_handles[0]
    # get home page
    driver.get("https://www.howoge.de/wohnungen-gewerbe/wohnungssuche/detail/1771-14576-989.html?t=ibw")
    Howoge().apply(driver)