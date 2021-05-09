# Requirements

- I can send a message to a whatsapp number
- I can use their contact info in the message
    - I could make the contact names in Arabic

## Next Steps
- [x] Filter out english names in targeting
- [x] Preview messages with auto updates (use `watch`)
- [ ] figure out how to add religion to profiles and auto fill it (similar to gender)
- [ ] Start Collect data from linkedin connections
- [ ] Workaround the 50 resource per request limit for groups

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
