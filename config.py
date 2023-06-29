from typing import List

import yaml
from dataclass_csv import DataclassWriter
from mako.template import Template

from socializer import services
from socializer.cli.campaign import ContactFilters
from socializer.cli.main import analyze_group
from socializer.models import Message

with open("config.yaml", "r") as fh:
    config = yaml.load(fh)

messages: List[Message] = []

for campaign in config["campaigns"]:
    group = campaign["group"]
    template_filename = campaign.get("template", config["global"]["template"])
    template = Template(filename=template_filename)

    analyze_group(group_names=[group], limit=config["global"]["group_limit"])
    contacts = services.get_contacts(
        group_names=[group],
        filters=[ContactFilters.GENDER_EXISTS, ContactFilters.ARABIC_NAME],
        limit=config["global"]["group_limit"],
    )
    for contact in contacts:
        if contact.phone_num:
            message = services.create_message(contact=contact, template=template)
            messages.append(message)

with open("messages.csv", "w") as fh:
    writer = DataclassWriter(fh, messages, Message)
    writer.write()
