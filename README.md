# dropscan
Automated Mail-Forwarding for Dropscan Webhook Integration

## Create an .env File and fill the brackets:

```
DROPSCAN_IP=[18.198.97.171, 3.64.94.38, 3.64.100.254]
FALLBACK_MAIL=<MAIL>
FALLBACK_RECIPIENT=<RECIPIENT_ID>
SMTP_SERVER=<SMTP_SERVER>
SMTP_PORT=<SMTP_PORT>
SENDER_MAIL=<SENDER_MAIL>
SENDER_PASSWORD=<SENDER_PASSWORD>
KEY_PATH=<SOME RANDOM KEY FOR YOUR PATH>
RECIPIENTS={'<RECIPIENT_ID>': {'name': '<NAME>','email': '<MAIL>'}}
```

Hint: You can get your RECIPIENT_IDs from the Dropscan Service (or via their API-Services)
