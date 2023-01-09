import time
from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from degewo import Degewo
from gesobau import Gesobau
from howoge import Howoge


def initialize_files():
    exceptions = open("exceptions.txt", 'a+')
    done_file = open("done_file.txt", 'a+')
    return exceptions, done_file


def get_done_list():
    done_file_path = "done_file.txt"
    temp_done_file = Path(done_file_path)
    temp_done_file.touch(exist_ok=True)
    temp_done_file = open(done_file_path, 'r')
    done_list = temp_done_file.readlines()
    temp_done_file.close()
    return done_list


def set_search_parameters(driver):
    # go to second slider where the search exists -_-
    driver.implicitly_wait(2)
    driver.find_element(By.CLASS_NAME, "flex-control-nav") \
        .find_elements(By.TAG_NAME, 'li')[1] \
        .click()

    # get input fields from search box
    quick_search = driver.find_element(By.CLASS_NAME, 'quicksearch')
    inputs = quick_search.find_elements(By.TAG_NAME, 'input')
    rent_input = inputs[0]
    aria_input = inputs[1]
    rooms_input = inputs[2]

    # set input values
    rent_input.send_keys("900")
    aria_input.send_keys('45')
    rooms_input.send_keys('2')

    # click search
    search_btn = quick_search.find_element(By.TAG_NAME, 'button')
    search_btn.click()


def remove_cookies_popup(driver):
    WebDriverWait(driver, 10) \
        .until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="BorlabsCookieBox"]/div/div/div/div[1]/div/div/div/p[2]/a')))
    accept_cookies_button = driver.find_element(By.XPATH,
                                                '//*[@id="BorlabsCookieBox"]/div/div/div/div[1]/div/div/div/p[2]/a')
    accept_cookies_button.click()


def get_list_of_items(driver):
    # wait until apartments are loaded
    WebDriverWait(driver, 10) \
        .until(EC.visibility_of_element_located((By.XPATH, '//*[@id="_tb_relevant_results"]')))
    # get items wrapper
    items_wrapper = driver.find_element(By.XPATH, '//*[@id="_tb_relevant_results"]')
    # get items
    items_list = items_wrapper.find_elements(By.TAG_NAME, 'li')
    return items_list


def needWbs(driver):
    # get icon in the right sides
    right_side = driver.find_element(By.CLASS_NAME, '_tb_right')
    icons = [item for item in right_side.find_elements(By.TAG_NAME, 'a')]
    # if wbs icon exist return false
    for icon in icons:
        if icon.get_property('title') == 'Wohnberechtigungsschein':
            return True
    return False


def send_telegram_message(url):
    if url.startswith('https://inberlinwohnen.de/'):
        return
    TOKEN = "5556389728:AAFXR_4F91GHIa_R_gPb1rJRZRj71y0yp6I"
    chat_id = "742614558"
    message = url
    bot_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(bot_url).json())  # this sends the message


def scroll_to_top(driver):
    WebDriverWait(driver, 10) \
        .until(EC.visibility_of_element_located((By.XPATH, '//*[@id="_wf_contentholder"]/div[2]')))
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="_wf_contentholder"]/div[2]')).perform()

def get_driver():
    chrome_options = Options()
    #    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("window-size=1920x1080")
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options, service=s)
    return driver


if __name__ == '__main__':
    # get driver
    driver = get_driver()

    # save first page
    inBerlin_wohnen_page = driver.window_handles[0]

    # get home page
    driver.get("https://inberlinwohnen.de/")

    # remove cookies popup
    remove_cookies_popup(driver)

    # set search parameters
    set_search_parameters(driver)

    # loop forever and refresh the page
    while True:
        # get all items
        list_of_items = get_list_of_items(driver)

        # filter old items
        done_list = get_done_list()
        exceptions, done_file = initialize_files()

        # initialize action chain
        actions = ActionChains(driver)

        for item in list_of_items:
            # try:
            # ignore WBS items
            if needWbs(item):
                continue

            # expand the item
            item.click()

            # scroll to the element to make it clickable
            actions.move_to_element(item).perform()

            WebDriverWait(item, 10) \
                .until(EC.visibility_of_element_located((By.CLASS_NAME, 'org-but')))

            # get all details button that take us to application page
            all_details_button = item.find_element(By.CLASS_NAME, 'org-but')

            # check if this button was already clicked
            if all_details_button.get_property('href') + '\n' in done_list:
                print('already visited')
                continue
            all_details_button.click()

            # switch to new page
            inBerlin_wohnen_page = driver.window_handles[0]
            company_page = driver.window_handles[1]
            driver.switch_to.window(company_page)

            # check if this page already visited
            url = driver.current_url
            if url + '\n' in done_list:
                print('already done')
                driver.close()
                driver.switch_to.window(inBerlin_wohnen_page)
                continue


            # check witch company is it
            if 'howoge' in url:
                Howoge().apply(driver)
            elif 'degewo' in url:
                Degewo().apply(driver)
            elif 'gesobau' in url:
                Gesobau().apply(driver)
            else:
                exceptions.write(url + '\n')
                exceptions.write('undefined company\n')
                exceptions.write(('-' * 30) + '\n')
            # save results
            done_file.write(url + '\n')
            #done_file.write(all_details_button.get_property('href') + '\n')
            send_telegram_message(url)
            #        except Exception as e:
            #            exceptions.write(url)
            #            exceptions.write(str(sys.exc_info()[0]))
            #            exceptions.write('-' * 30)
            #        finally:
            # close and back to home page
            driver.close()
            driver.switch_to.window(inBerlin_wohnen_page)
            done_file.write(all_details_button.get_property('href') + '\n')
        time.sleep(1200)
        print('new start')
        driver.refresh()
        # to ensure everytime we start from the top
        scroll_to_top(driver)
