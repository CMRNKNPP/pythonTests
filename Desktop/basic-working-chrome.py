from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from sauceclient import SauceClient
import os
import time
import sys

def teardown(quit_msg, exception):
    print(f"{quit_msg}\n", exception)
    driver.quit()
    sys.exit(1)

username = os.environ.get('SAUCE_USERNAME')
access_key = os.environ.get('SAUCE_ACCESS_KEY')
sauce_client = SauceClient(username, access_key)

chrome_options = webdriver.ChromeOptions()
chrome_options.platform_name = 'Windows 10'
chrome_options.browser_version = 'latest'
sauce_options = {
    'name': "Generic Chrome Latest Test",
}

chrome_options.set_capability('sauce:options', sauce_options)

try:
    driver = webdriver.Remote(
        command_executor=f"http://{username}:{access_key}@ondemand.saucelabs.com/wd/hub",
        options=chrome_options
    )
    driver.maximize_window()

    driver.execute_script("sauce:context=Now moving to Google")
    driver.get("https://www.google.com")

    driver.get("https://saucelabs.com")
    # Directly wait for the element
    for _ in range(30):
        if driver.find_elements(By.CLASS_NAME, "container"):
            break
        time.sleep(1)
    else:
        raise Exception("Element with class name 'container' not found")

    driver.get("https://www.google.com/")
    for _ in range(30):
        query_input = driver.find_elements(By.NAME, "q")
        if query_input:
            query_input[0].send_keys("Selenium Testing" + Keys.RETURN)
            break
        time.sleep(1)
    else:
        raise Exception("Search input box not found")

    # Direct wait instead of implicitly_wait
    time.sleep(2)

    sauce_client.jobs.update_job(driver.session_id, passed=True)
except Exception as e:
    teardown("error:\n", e)

driver.quit()