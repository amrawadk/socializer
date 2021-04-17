import socializer as sz
import time

def main():
    gcontacts = sz.GoogleContactsManager()
    whats = sz.WhatsAppManager()

    contacts = gcontacts.get_contacts(limit=5)

    for contact in contacts:
        translated_name = sz.NameTranslator.translate_name(contact.name)
        whats.sendwhatmsg(
            phone_no="+201115492142",
            message=f"{contact.name} ({translated_name}) -> {contact.phone_num}"
        )
        time.sleep(10)

main()