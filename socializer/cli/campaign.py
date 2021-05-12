"""Build messaging campaigns"""
import csv
import enum
import random
import time
from dataclasses import dataclass
from typing import List, Optional

import typer
from dataclass_csv import DataclassReader, DataclassWriter
from mako.template import Template

from socializer.cli.utils import _is_arabic
from socializer.google_contacts import GoogleContactsAdapter
from socializer.models import Contact
from socializer.whatsapp_manager import WhatsAppManager

app = typer.Typer(name="campaign", help=__doc__)


# TODO should this be dynamic?
class FieldFilters(enum.Enum):
    GENDER = "gender"


def _filter_required_fields(
    contacts: List[Contact], fields: List[FieldFilters]
) -> List[Contact]:
    filtered_contacts = [
        c for c in contacts if all((getattr(c, f.value) for f in fields))
    ]
    fields_str = [f.value for f in fields]
    typer.echo(
        f"{len(filtered_contacts)}/{len(contacts)} contacts matched the filters: '{' & '.join(fields_str)}'"
    )
    return filtered_contacts


def _filter_arabic_only_contacts(contacts: List[Contact]) -> List[Contact]:
    filtered_contacts = [c for c in contacts if _is_arabic(name=c.first_name)]
    typer.echo(
        f"{len(filtered_contacts)}/{len(contacts)} contacts matched the filter: 'arabic-only'"
    )
    return filtered_contacts


@app.command()
def generate_audience(
    group_names: List[str] = typer.Option([], "--group-name", "-n"),
    fields: List[FieldFilters] = typer.Option(
        [], "--field", "-f", help="A required field that the audience should have"
    ),
    arabic_only: bool = typer.Option(False, "--arabic-only"),
    output: typer.FileTextWrite = typer.Option("contacts.csv"),
    limit: int = 20,
):
    """Export Audience filtered by certain conditions to a csv file."""
    gcontacts_manager = GoogleContactsAdapter()

    all_contacts: List[Contact] = []
    for group_name in group_names:
        contacts = gcontacts_manager.get_contacts_in_group(
            group_name=group_name, limit=limit
        )

        typer.echo(f"Found {len(contacts)} people in the group")

        if fields:
            contacts = _filter_required_fields(contacts=contacts, fields=fields)

        if arabic_only:
            contacts = _filter_arabic_only_contacts(contacts=contacts)

        all_contacts.extend(contacts)

    writer = DataclassWriter(output, all_contacts, Contact)
    writer.write()
    typer.echo(f"contacts written to {output.name}")


## Message Generation


@dataclass
class Message:
    full_name: str
    phone_num: str
    message: str


@app.command()
def generate_messages(
    contacts: typer.FileText = typer.Option("contacts.csv", "--contacts", "-c"),
    template_file: typer.FileText = typer.Option("template.txt", "--template", "-t"),
    output: typer.FileTextWrite = typer.Option("messages.csv", "--output", "-o"),
):
    """Generate Message for a list of contacts based on a template"""
    template = Template(filename=template_file.name)

    reader = csv.DictReader(contacts)
    messages = [
        Message(
            full_name=contact["full_name"],
            phone_num=contact["phone_num"],
            message=template.render(**contact),
        )
        for contact in reader
    ]

    writer = DataclassWriter(output, messages, Message)
    writer.write()
    typer.echo(f"messages written to {output.name}")


class SendMode(str, enum.Enum):
    LIVE = "live"
    TEST = "test"


@app.command()
def send_whatsapp_messages(
    messages_csv: typer.FileText = typer.Option("messages.csv", "--messages", "-m"),
    mode: SendMode = SendMode.TEST,
    test_phone_num: Optional[str] = typer.Option(
        None,
        "--test-phone-num",
        "-p",
        help="A phone number to send messages to when mode is 'test'",
    ),
):
    """Send messages using whatsapp"""
    if mode == SendMode.TEST and test_phone_num is None:
        typer.echo(
            "A test phone number is required when using 'test' mode. Aborting!",
            err=True,
        )
        raise typer.Exit(code=1)

    whats_manager = WhatsAppManager()

    reader = DataclassReader(messages_csv, Message)
    messages: List[Message] = list(reader)
    not_sent: List[Message] = []
    with typer.progressbar(
        messages, label=f"Sending {len(messages)} messages"
    ) as progress:
        for message in progress:
            destination = message.phone_num if mode == SendMode.LIVE else test_phone_num
            try:
                whats_manager.sendwhatmsg(phone_no=destination, message=message.message)
            except Exception:  # pylint: disable=broad-except
                not_sent.append(message)
            time.sleep(random.randint(3, 7))

    with open("failed_messages.csv", "w") as failed_messages_csv:
        writer = DataclassWriter(failed_messages_csv, not_sent, Message)
        writer.write()
        typer.echo("failed messages written to failed_messages.csv")
