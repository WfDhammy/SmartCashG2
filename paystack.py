import os
import hashlib
import hmac

import json
import requests
from dotenv import load_dotenv
from rest_framework.views import APIView

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


