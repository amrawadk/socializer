.PHONY: docs docs-cli docs-generate-markdown-tables

docs: docs-cli docs-generate-markdown-tables

docs-cli:
	typer socializer.cli.main utils docs --output docs/cli.md
