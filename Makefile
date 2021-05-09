.PHONY: docs

docs:
	typer socializer.cli.main utils docs --output docs/cli.md
