"""Build messaging campaigns"""
import enum
from typing import List

import typer
from dataclass_csv import DataclassWriter

from socializer.cli.utils import _is_arabic
from socializer.google_contacts import GoogleContactsAdapter
from socializer.models import Contact

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
    group_name: str = typer.Option(...),
    fields: List[FieldFilters] = typer.Option(
        [], "--field", "-f", help="A required field that the audience should have"
    ),
    arabic_only: bool = typer.Option(False, "--arabic-only"),
    output: typer.FileTextWrite = typer.Option("contacts.csv"),
    limit: int = 20,
):
    """Export Audience filtered by certain conditions to a csv file."""
    gcontacts_manager = GoogleContactsAdapter()
    contacts = gcontacts_manager.get_contacts_in_group(
        group_name=group_name, limit=limit
    )

    typer.echo(f"Found {len(contacts)} people in the group")

    if fields:
        contacts = _filter_required_fields(contacts=contacts, fields=fields)

    if arabic_only:
        contacts = _filter_arabic_only_contacts(contacts=contacts)

    writer = DataclassWriter(output, contacts, Contact)
    writer.write()
    typer.echo(f"contacts written to {output.name}")
