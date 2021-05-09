import random
import time

from dataclass_csv import DataclassReader

from main_template import Message
from socializer.whatsapp_manager import WhatsAppManager

wm = WhatsAppManager()
with open("messages.csv") as messages_csv:
    reader = DataclassReader(messages_csv, Message)
    for message in reader:
        wm.sendwhatmsg(phone_no="", message=message.message)
        time.sleep(random.randint(3, 7))
