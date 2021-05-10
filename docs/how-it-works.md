# How it works

The main steps are as follows:

1. import your contacts
2. enrich your contacts
3. build messaging templates
4. send personalized messages

!!! note
    Currently, [Google Contacts](https://contacts.google.com/) is the main backend for persisting contact details and structure, hence why most steps will be specific to google contacts, but as the project evolves, this is subject to change.

## Importing contacts

### Importing from google contacts

Contacts can be imported from [Google Contact Groups](https://support.google.com/contacts/answer/30970?co=GENIE.Platform%3DDesktop&hl=en) using the `--group-name` argument that's available in some of the sub commands.

## Enriching contacts

Enriching contacts refers to filling out the details of the contact, to help drive personalization. 

### Contact fields

The supported fields can be found in the `Contact` class's attributes:

!!! info "`Content` class documentation"
    ::: socializer.models.Contact
        rendering:
            show_root_toc_entry: False


For each field, there're 2 actions that can be performed:

1. check the field matches criteria
2. suggest values based on other contact details

### Contact field checkers
<!-- TODO add field changes -->

### Contact field suggestors
<!-- TODO should the name 'suggestors' change? -->

<!-- TODO add suggestion details -->

## Building Messaging Templates

### Creating message templates

Socializer integrates with python's powerful templating engine [Mako](https://www.makotemplates.org/) to support writing message temapltes using the details available in [contact fields](#contact-fields). Here's an example:

if you have contacts with the following details:

=== "Rendered Table"
    --8<-- "docs_src/message_template/contacts.md"

=== "CSV"
    ```csv
    --8<-- "docs_src/message_template/contacts.csv"
    ```

You can write a mako template like this:

```mako
--8<-- "docs_src/message_template/template.txt"
```

Then using the following command:

```bash
--8<-- "docs_src/message_template/render.sh"
```

You get the following output:

=== "Rendered Table"
    --8<-- "docs_src/message_template/messages.md"

=== "CSV"
    ```csv
    --8<-- "docs_src/message_template/messages.csv"
    ```

### Previewing messages for specific audience

<!-- TODO add examples on how to preview -->