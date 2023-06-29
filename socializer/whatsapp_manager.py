from urllib.parse import quote

from playwright.sync_api import sync_playwright


class WhatsAppManager:
    PAGE_LOAD_TIMEOUT_SECONDS = 10

    def __init__(self):
        # TODO remember to tear down
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(headless=False)
        self.page = browser.new_page()
        self.page.goto("https://web.whatsapp.com")

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

        self.page.goto(
            "https://web.whatsapp.com/send?phone="
            + phone_no
            + "&text="
            + parsed_massage
        )

        self.page.get_by_test_id("compose-btn-send").click()
