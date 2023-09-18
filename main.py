import asyncio
import random
import string
from cashapp import cashapp
from faker import Faker


def generate_invoice_id():
    fake = Faker('en_US')
    generatedTransactionId = fake.name()
    print(generatedTransactionId)
    return generatedTransactionId

invoiceid = generate_invoice_id()
print("Generated transaction ID: ")
print(invoiceid)
# DIAGNOSTICS REMOVE IN PROD
amount = 1 #20 Dolars
clientIdentifier = input("Enter clientIdentifier: ")
print(f"Invoice ${amount}, Invoice ID (NOTE): {invoiceid}")
input("Press enter when transaction is complete.")
# Query for new transactions
cashapp().fetchmail()
print(cashapp.check_if_paid(clientIdentifier, invoiceid, amount))
