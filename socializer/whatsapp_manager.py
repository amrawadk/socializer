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
            "/Applications/Google Chrome 102.app/Contents/MacOS/Google Chrome"
        )
        driver_path = "/usr/local/bin/chromedriver"
        self.driver = webdriver.Chrome(options=options, executable_path=driver_path)
        # open whats app page and wait for manual input that the browser is linked correctly
        self.driver.get("https://web.whatsapp.com")
        input("hit 'Enter' when the browser is linked and the messages are open!")

    def sendwhatmsg(self, phone_no, message):
        parsed_massage = quote(message)

        # Whatsapp requires a country code in the phone number, we're assuming it's all
        # Egypt for now.
        # TODO: this should be updates in the Google contacts to add a prefix based on the country.
        if phone_no.startswith("00"):
            phone_no = f"+{phone_no[2:]}"

        if not phone_no.startswith("+"):
            phone_no = f"+2{phone_no}"

        self.driver.get(
            "https://web.whatsapp.com/send?phone="
            + phone_no
            + "&text="
            + parsed_massage
        )

        button_xpath = (
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
        )
        button = WebDriverWait(
            driver=self.driver, timeout=self.PAGE_LOAD_TIMEOUT_SECONDS
        ).until(EC.presence_of_element_located((By.XPATH, button_xpath)))
        button.send_keys(Keys.RETURN)
