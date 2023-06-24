# Socializer

Automation first approach to building and maintaing personal networks.

- [Documentation](/docs/index.md)

# How to run

- To prep the campaign in `config.yaml` and generate the messages
```python
python config.py
```

- To send the messages
```
rm secrets/token.json
```

- TO run a test
```
python socializer/cli/main.py campaign send-whatsapp-messages -m messages.csv --mode test -p <phone_num_with_country_code>
```

- To send
```