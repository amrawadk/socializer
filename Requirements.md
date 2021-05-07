# Requirements

- I can send a message to a whatsapp number
- I can use their contact info in the message
    - I could make the contact names in Arabic

## Next Steps
- Now that we have genders in 'contacts_with_gender',
    - figure out how to handle low confidence detections
    - sync genders back to google contacts
    - Use gender specific templates to generate messages.

## Organization
- Figure out how to represent flows (perhaps a cli with typer?) to replace main_* files and allow easy reruns
- 

## Open questions
- Should we use requests cache for 'get' requests from Google Contacts API?
