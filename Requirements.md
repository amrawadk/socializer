# Requirements

- I can send a message to a whatsapp number
- I can use their contact info in the message
    - I could make the contact names in Arabic

## Next Steps
- [x] Filter out english names in targeting
- [x] Preview messages with auto updates (use `watch`)
- [ ] figure out how to add religion to profiles and auto fill it (similar to gender)
- [ ] Start Collect data from linkedin connections
- [x] Workaround the 50 resource per request limit for groups
- [ ] Figure out how to run the following scripts before each build
    - scripts/generate_markdown_tables.sh
    - all python scripts in `docs_src`
- [ ] figure out why messages are over new lines in `messages.md`
- [ ] remove table-renderer config

## Caviets
- On Mac, you need to allow `chromedriver` to execute without a certification, using the command:
```bash
xattr -d com.apple.quarantine $(which chromedriver)
```
## Improvements
- [ ] Document cli using https://github.com/click-contrib/sphinx-click
- [ ] Use Configuration files for messaging campaigns
- [ ] Generate release notes
- [ ] Replace `type.echo` more structured logs: https://github.com/hynek/structlog
- [ ] use `tqdm` for nicer progress bars


## Organization
- Figure out how to preview messages for people while writing templates.
- Figure out how to perform updates on `Contact` and have other systems pick them up
    - use an event bus
## Open questions
- Should we use requests cache for 'get' requests from Google Contacts API?
- How can we handle english and arabic contacts? (is there a 'language' field in contacts?)
- How can we build a processing pipeline for pre processing contacts?
    - set appropriate name
    - set gender
    - set language
    - ...

# Product Ideas
- API for name translations
- API for gender identification for arabic names

# Project Names
- Egtma3y: The full product suite
    - Should be pay per usage, aim for serverless architecture.

# Interesting mkdocs integrations
- [ ] Inject social media cards: https://github.com/carlosperate/mkdocs-awesome-list-plugin/blob/master/README.md
- [ ] Resolve links to issue trackers: https://github.com/theskumar/autolink-references-mkdocs-plugin/
- [ ] URL Validator: https://github.com/manuzhang/mkdocs-htmlproofer-plugin
- [ ] Add rich tooltips: https://github.com/midnightprioriem/mkdocs-tooltipster-links-plugin/blob/master/README.md
- [ ] Add plantuml diagrams: https://github.com/christo-ph/mkdocs_build_plantuml/blob/master/README.md
- [ ] Add test coverage: https://pawamoy.github.io/mkdocs-coverage/
- [ ] Highlight new features: https://github.com/kevin-411/mkdocs-new-features-notifier/blob/master/README.md
- [ ] Create mind maps: https://github.com/neatc0der/mkdocs-markmap
- [ ] generate documentation dynamically: https://oprypin.github.io/mkdocs-gen-files/
- [ ] Critic Markup, tracking changes to markdown: http://criticmarkup.com/
- [ ] Architecture decision records: https://github.com/npryce/adr-tools