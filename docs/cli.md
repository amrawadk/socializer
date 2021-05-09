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
