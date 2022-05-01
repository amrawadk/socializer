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

* `campaign`: Build messaging campaigns
* `main`

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

* `-n, --group-name TEXT`: [default: ]
* `-f, --filters [gender|arabic]`: Supported ways to filter contacts  [default: ]
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
* `-o, --output FILENAME`: [default: messages.csv]
* `--help`: Show this message and exit.

### `socializer campaign send-whatsapp-messages`

Send messages using whatsapp

**Usage**:

```console
$ socializer campaign send-whatsapp-messages [OPTIONS]
```

**Options**:

* `-m, --messages FILENAME`: [default: messages.csv]
* `--mode [live|test]`: [default: test]
* `-p, --test-phone-num TEXT`: A phone number to send messages to when mode is 'test'
* `--help`: Show this message and exit.

## `socializer main`

**Usage**:

```console
$ socializer main [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `analyze-group`: Analyze Google Contacts Group and optionally...
* `export-contacts`: Export Contacts in a google contact group to...
* `export-people`: Export People in a google contact group to a...

### `socializer main analyze-group`

Analyze Google Contacts Group and optionally add any missing data.

**Usage**:

```console
$ socializer main analyze-group [OPTIONS]
```

**Options**:

* `-n, --group-name TEXT`: [default: ]
* `--limit INTEGER`: [default: 20]
* `--help`: Show this message and exit.

### `socializer main export-contacts`

Export Contacts in a google contact group to a csv file.

**Usage**:

```console
$ socializer main export-contacts [OPTIONS]
```

**Options**:

* `--group-name TEXT`: [required]
* `--output FILENAME`: [default: contacts.csv]
* `--limit INTEGER`: [default: 20]
* `--help`: Show this message and exit.

### `socializer main export-people`

Export People in a google contact group to a csv file.

This includes more details than Contact

**Usage**:

```console
$ socializer main export-people [OPTIONS]
```

**Options**:

* `--group-name TEXT`: [required]
* `--output FILENAME`: [default: people.csv]
* `--limit INTEGER`: [default: 20]
* `--help`: Show this message and exit.
