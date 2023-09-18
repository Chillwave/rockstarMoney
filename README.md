# Email-IMAP-Transaction Python Script

This Python script connects to a mail server via IMAP, fetches unseen emails, and harvests transactions data to populate a json file (`data.json`). The harvested transactions are utilized to validate a opted transaction.

## Prerequisites

- Python 3+

## Dependencies

Install the necessary dependencies with:

```bash
pip install email, logging, datetime, time, asyncio, random, string, faker
```

## Usage

1. Overwrite the predefined mail server details and email account credentials:

```python
MAIL_USER = "example1@outlook.com"
MAIL_PSW = "makeAnAppPassword"
MAIL_SERVER = "outlook.office365.com"
INCOMING_EMAIL_ADDRESS = "cash@square.com"
FOLDER = u'"_Sorted Mail_/CashApp"'
```      

2. Ensure the permissions for the account are properly set.

3. Run the script:

4. Follow the interactive prompt to provide transaction information and validate the transaction.

## Working

1. `cashapp.check_if_paid(clientIdentifier, invoice_id, price)`: Checks whether a payment of specified price with a given invoice exists.
   
2. `cashapp.fetchmail()`: Fetches all unseen emails, extract transaction data from email, and update data.json.

3. `generate_invoice_id()`: Generates a random invoice ID.

Email is assumed to be in HTML format, and structured as specified in the regex extraction syntax utilized in the script.

> **Note:** Ensure secure handling of your mail credentials and protect the environment in which payment validation occurs. Report any issues you experience for continuous package improvement.

## Update:
Please refer to the original branch to use the upgraded revision which utilizes the webapp to determine if the transaction was sent through account balance or a credit card. This implementation is not capable of determining that. This version is not recomended for production enviroments and is for research purposes only.
----------------------------
