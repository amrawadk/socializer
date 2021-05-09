# `socializer`

Automation first approach to building and maintaing personal networks.

**Usage**:

```console
$ socializer [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `analyze-group`: Analyze Google Contacts Group and optionally...
* `campaign`: Build messaging campaigns
* `export-contacts`: Export Contacts in a google contact group to...
* `export-people`: Export People in a google contact group to a...

## `socializer analyze-group`

Analyze Google Contacts Group and optionally add any missing data.

**Usage**:

```console
$ socializer analyze-group [OPTIONS]
```

**Options**:

* `--name TEXT`: [required]
* `--limit INTEGER`: [default: 20]
* `--help`: Show this message and exit.

## `socializer campaign`

Build messaging campaigns

**Usage**:

```console
$ socializer campaign [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `generate-audience`: Export Audience filtered by certain...
* `generate-messages`: Generate Message for a list of contacts based...
* `send-whatsapp-messages`: Send messages using whatsapp

### `socializer campaign generate-audience`

Export Audience filtered by certain conditions to a csv file.

**Usage**:

```console
$ socializer campaign generate-audience [OPTIONS]
```

**Options**:

* `--group-name TEXT`: [required]
* `-f, --field [gender]`: A required field that the audience should have  [default: ]
* `--arabic-only`: [default: False]
* `--output FILENAME`: [default: contacts.csv]
* `--limit INTEGER`: [default: 20]
* `--help`: Show this message and exit.

### `socializer campaign generate-messages`

Generate Message for a list of contacts based on a template

**Usage**:

```console
$ socializer campaign generate-messages [OPTIONS]
```

**Options**:

* `-c, --contacts FILENAME`: [default: contacts.csv]
* `-t, --template FILENAME`: [default: template.txt]
* `--output FILENAME`: [default: messages.csv]
* `--help`: Show this message and exit.

### `socializer campaign send-whatsapp-messages`

Send messages using whatsapp

**Usage**:

```console
$ socializer campaign send-whatsapp-messages [OPTIONS]
```

**Options**:

* `-m, --messages-file FILENAME`: [default: messages.csv]
* `--mode [live|test]`: [default: test]
* `-p, --test-phone-num TEXT`: A phone number to send messages to when mode is 'test'
* `--help`: Show this message and exit.

## `socializer export-contacts`

Export Contacts in a google contact group to a csv file.

**Usage**:

```console
$ socializer export-contacts [OPTIONS]
```

**Options**:

* `--group-name TEXT`: [required]
* `--output FILENAME`: [default: contacts.csv]
* `--limit INTEGER`: [default: 20]
* `--help`: Show this message and exit.

## `socializer export-people`

Export People in a google contact group to a csv file.

This includes more details than Contact

**Usage**:

```console
$ socializer export-people [OPTIONS]
```

**Options**:

* `--group-name TEXT`: [required]
* `--output FILENAME`: [default: people.csv]
* `--limit INTEGER`: [default: 20]
* `--help`: Show this message and exit.
