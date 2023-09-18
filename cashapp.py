import imaplib
import email
import re
import json
import os
import logging
import datetime
import time

# get the current time as a datetime object
now = datetime.datetime.now()
# format the current time as a string globally
time_str = now.strftime("%Y-%m-%d %H:%M:%S")

# Obtain working directory
script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
print("Script directory:", script_directory)

# globally set the log filename to avoid time drift
logFile_name = (script_directory+"/logfiles/payments_manifest.txt")

DB_FILE = script_directory+'/data.json'
MAIL_USER = "example1@outlook.com"
MAIL_PSW = "makeAnAppPassword"
MAIL_SERVER = "outlook.office365.com"
INCOMING_EMAIL_ADDRESS = "cash@square.com"
FOLDER = u'"_Sorted Mail_/CashApp"'

def log_to_file(log_message):
    log_line = f"{time_str} {log_message}\n"

    with open(logFile_name, "a") as file:
        file.write(log_line)

class cashapp:
    def check_if_paid(clientIdentifier, invoice_id, price):
        try:
            with open(DB_FILE, 'r') as f:
                file_content = f.read()
                if file_content.strip():  # Check if the file content is not empty
                    data = json.loads(file_content)
                else:
                    print("data.json file detected as empty. Most likely no transactions located.")
                    data = {}  # Initialize as an empty dictionary if the file is empty
        except FileNotFoundError:
            logging.warning(f"Database file '{DB_FILE}' not found. Creating a new database.")
            data = {}  # Initialize as an empty dictionary if the file is not found
        except json.JSONDecodeError:
            logging.error(f"Error parsing the database file '{DB_FILE}'. Check if it contains valid JSON.")
            data = {}  # Initialize as an empty dictionary if the JSON is invalid

        if invoice_id in data and data[invoice_id] == price:
            transactionData = data[invoice_id]
            print("DIAG: TRANSACTION DATA - ")
            print(str(transactionData)+"$ InvoiceId: "+invoice_id+" PAID BY: "+clientIdentifier)
            log_to_file(str(transactionData)+"$ InvoiceId: "+invoice_id+" PAID BY: "+clientIdentifier)
            return True
        else:        
            return False
    # this needs to be run first (fetch mail, populate data.json)
    def fetchmail(self):
        # Set up logging to the console
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info("Fetching mail")
        try:
            logging.debug("Connecting to the mail server...")
            mail = imaplib.IMAP4_SSL(MAIL_SERVER)
            logging.debug("Connected successfully.")
            
            logging.debug("Logging in to the mail server...")
            mail.login(MAIL_USER, MAIL_PSW)
            logging.debug("Logged in successfully.")
            
            mail.select('inbox')
            typ, data = mail.search(None, 'UNSEEN')
            email_count = len(data[0].split())
            logging.debug(f"Found {email_count} unseen emails.")
            for idx, num in enumerate(data[0].split(), start=1):
                logging.debug(f"Processing email {idx}/{email_count}...")
                typ, data = mail.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
                subject = email_message.get("Subject", "Unknown Subject")
                logging.debug(f"Subject: {subject}")
                
                if INCOMING_EMAIL_ADDRESS in str(email_message):
                    logging.debug("Found email from the expected address.")
                    for part in email_message.walk():
                        if part.get_content_type() == 'text/html':
                            html_content = part.get_payload(decode=True).decode('utf-8')
                            cash_raw = re.search(r'<div class="value">\s*\$(\d+\.\d+)\s*</div>', html_content)
                            note_raw = re.search(r'<div class="text note" style="color:#999999overflow: hidden;">\s*(.*?)\s*</div>', html_content)
                            if cash_raw and note_raw:
                                cash = cash_raw.group(1)
                                logging.debug(f"Extracted cash value: {cash}")
                                _note_ = note_raw.group(1)
                                note = _note_[4:]
                                logging.debug(f"Extracted note: {note}")
                                try:
                                    with open(DB_FILE, 'r') as f:
                                        file_content = f.read()
                                        if file_content.strip():
                                            transactionDB = json.loads(file_content)
                                        else:
                                            transactionDB = {}
                                except FileNotFoundError:
                                    logging.warning(f"Database file '{DB_FILE}' not found. Creating a new database.")
                                    transactionDB = {}
                                except json.JSONDecodeError:
                                    logging.error(f"Error parsing the database file '{DB_FILE}'. Check if it contains valid JSON.")
                                    raise

                                if note not in transactionDB:
                                    transactionDB[note] = float(cash)
                                    try:
                                        with open(DB_FILE, 'w') as f:
                                            json.dump(transactionDB, f)
                                            logging.info("Transaction saved.")
                                    except Exception as e:
                                        logging.error(f"Error saving transaction to the database: {e}")
                                else:
                                    pass
        except Exception as e:
            logging.error(f"Error fetching mail or processing data: {e}")
