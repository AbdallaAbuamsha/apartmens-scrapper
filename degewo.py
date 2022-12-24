import sys

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from company import Company


class Degewo(Company):
    def apply(self, driver: webdriver):
        try:
            driver.execute_script("window.scrollTo(0,100)")
            contact_btn = driver.find_element(By.CLASS_NAME, 'js-expose-form-open')
            contact_btn.click()
            driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="kontakt"]/section/div/iframe'))

            WebDriverWait(driver, 10) \
                .until(EC.visibility_of_element_located((By.XPATH, '//*[@id="firstName"]')))
            driver.implicitly_wait(3)

            driver.find_element(By.XPATH, '//*[@id="firstName"]').send_keys("Abdallah")
            ActionChains(driver) \
                .key_down(Keys.SHIFT) \
                .send_keys(Keys.TAB) \
                .send_keys(Keys.SPACE) \
                .send_keys(Keys.ARROW_DOWN) \
                .send_keys(Keys.ARROW_DOWN) \
                .send_keys(Keys.ENTER) \
                .perform()

            driver.find_element(By.ID, 'lastName').send_keys("Abuamsha")
            driver.find_element(By.ID, 'email').send_keys("eng.a.abuamsha@gmail.com")
            driver.find_element(By.ID, 'phone-number').send_keys("017646601946")
            driver.find_element(By.ID, 'formly_2_input_numberPersonsTotal_0').send_keys("2")
            driver.find_element(By.CLASS_NAME, 'form-actions').find_element(By.TAG_NAME, 'button').click()
            #/html/body/el-root/div/el-listing-application/div
            WebDriverWait(driver, 10) \
                .until(EC.visibility_of_element_located((By.XPATH, '/html/body/el-root/div/el-listing-application/div')))
        except Exception as e:
            print(str(sys.exc_info()[0]))
            return