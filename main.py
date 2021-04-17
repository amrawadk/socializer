from selenium import webdriver
from urllib.parse import quote

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup():
    options = Options()
    options.binary_location = (
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    )
    driver_path = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    return driver

def sendwhatmsg(driver, phone_no, message):
    parsedMessage = quote(message)
    driver.get(
        "https://web.whatsapp.com/send?phone=" + phone_no + "&text=" + parsedMessage
    )

    button_xpath = '//*[@id="main"]/footer/div[1]/div[3]/button'
    button = WebDriverWait(driver=driver, timeout=100).until(
        EC.presence_of_element_located((By.XPATH, button_xpath))
    )
    button.send_keys(Keys.RETURN)

driver = setup()
sendwhatmsg(
    driver=driver,
    phone_no="",
    message="TEST",
)
