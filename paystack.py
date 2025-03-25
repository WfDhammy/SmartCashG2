import os
import hashlib
import hmac
import uuid
import json
import requests
from dotenv import load_dotenv


load_dotenv()  # load environment variables from.env file

YOUR_API_KEY = os.getenv("PAYSTACK")
def initialize(email: str, amount):
    url = 'https://api.paystack.co/transaction/initialize'
    headers = {
        'Authorization': f'Bearer {YOUR_API_KEY}',
        'Content-Type': 'application/json'
    }
    body = {
        'amount': int(amount * 100),  # Convert amount to kobo (100 kobo = 1 Naira)
        'email': email,  # Use email as string
    }
    
    # Perform the request to the Paystack API
    response = requests.post(url, headers=headers, data=json.dumps(body))
    
    if response.status_code == 200:
        data = response.json()
        url = data['data']['authorization_url']
        reference = data['data']['reference']
        payment_response = {
            'url': url,
            'reference': reference,
        }
        return payment_response
    
    # Return error if the response status is not OK
    return {"error": response.json().get('message', 'An error occurred')}


import uuid
import json
import requests

def generateRescipient(accNo: str, accName: str, bankCode: str):
    url = "https://api.paystack.co/transferrecipient"
    headers = {
        'Authorization': f'Bearer {YOUR_API_KEY}',
        'Content-Type': 'application/json'
    }
    body = {
        "type": "nuban",
        "name": accName,
        "account_number": accNo, 
        "bank_code": bankCode,
        "currency": "NGN"
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 201:
        data = response.json()
        recipient_code = data['data']['recipient_code']
        return recipient_code

import uuid
import json
import requests

def transfer(balance, amount, description, rcpt):
    url = "https://api.paystack.co/transfer"
    vUUID = uuid.uuid4()  
    headers = {
        'Authorization': f'Bearer {YOUR_API_KEY}',  
        'Content-Type': 'application/json'
    }
   
    body = {
        'source': 'balance', 
        'amount': int(amount * 100),  
        'reference': str(vUUID),  
        'reason': description,  
        'recipient': rcpt 
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        data = response.json()
        return data['data']['status']

    else:
        data2 = response.json()
        update = {
            "message": data2['message'],
            "status": data2['status']
        }
        return update

    #     status = data['data']['status']
    #     if status == "success":
    #         return status
    #     return {"message": status}

    # return {"message": status}

#print(generateRescipient("2270268887", "VICTOR CHUKWUEMEKA CHIBUOGWU", "057"))

#print(transfer("balance", 50000, "Payment for book purchase", "RCP_lb7uuy19zg04g0j"))