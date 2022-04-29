from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WhatsAppManager:
    PAGE_LOAD_TIMEOUT_SECONDS = 10

    def __init__(self):
        options = Options()
        options.binary_location = (
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        )
        driver_path = "/usr/local/bin/chromedriver"
        self.driver = webdriver.Chrome(options=options, executable_path=driver_path)

    def sendwhatmsg(self, phone_no, message):
        parsed_massage = quote(message)
        self.driver.get(
            "https://web.whatsapp.com/send?phone="
            + phone_no
            + "&text="
            + parsed_massage
        )

        button_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button'
        button = WebDriverWait(
            driver=self.driver, timeout=self.PAGE_LOAD_TIMEOUT_SECONDS
        ).until(EC.presence_of_element_located((By.XPATH, button_xpath)))
        button.send_keys(Keys.RETURN)
