import csv
from dataclasses import dataclass

from dataclass_csv.dataclass_writer import DataclassWriter
from mako.template import Template

template = Template(filename="template.txt")


@dataclass
class Message:
    full_name: str
    phone_num: str
    message: str


with open("contacts.csv") as contacts_csv:
    reader = csv.DictReader(contacts_csv)
    messages = [
        Message(
            full_name=contact["full_name"],
            phone_num=contact["phone_num"],
            message=template.render(**contact),
        )
        for contact in reader
    ]

with open("messages.csv", "w") as messages_csv:
    writer = DataclassWriter(messages_csv, messages, Message)
    writer.write()
