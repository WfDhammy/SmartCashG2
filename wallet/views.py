from rest_framework import generics, status, response
from .serializers import WalletSerializer, WalletFundingSerializer
from .models import Wallet, WalletFunding
from rest_framework.views import APIView
from paystack import initialize
from user.models import User
import os
import hashlib
import hmac

import json
import requests
from dotenv import load_dotenv
from rest_framework.views import APIView

load_dotenv()  # load environment variables from.env file

YOUR_API_KEY = os.getenv("PAYSTACK")





class WalletListCreateAPIView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class WalletDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = 'id'


from rest_framework.response import Response

class FundWallet(APIView):
    def post(self, request):
        # Deserialize the request data using the WalletFundingSerializer
        serializer = WalletFundingSerializer(data=request.data)
        
        # If serializer is not valid, return the errors as response
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Extract necessary data from the validated serializer
        wallet = serializer.validated_data['wallet']
        user_data = serializer.validated_data['user']
        amount = serializer.validated_data['amount']
        
        # Retrieve the user object by email
        user = User.objects.filter(email=user_data).first()
        
        # If the user is not found, return an error message
        if user is None:
            return Response({"error": "User not found"}, status=404)

        # Call the initialize function with the user's email and amount
        response = initialize(user.email, amount)
        
        # Extract the reference and URL from the Paystack response
        reference = response.get('reference')
        if not reference:
            return Response({"error": "Failed to retrieve payment reference"}, status=500)
        
        payment = WalletFunding.objects.create(
            user=user, 
            amount=amount,
            wallet=wallet,
            reference=reference
        )

        # Return the Paystack authorization URL in the response
        return Response({"url": response['url']})


class FundWalletView(generics.ListAPIView):
    queryset = WalletFunding.objects.all()
    serializer_class = WalletFundingSerializer


class RetrieveFunding(generics.RetrieveUpdateDestroyAPIView):
    queryset = WalletFunding.objects.all()
    serializer_class = WalletFundingSerializer
    lookup_field = 'id'

    

class WebHook(APIView):
    def post(self, request):
        raw_body = request.body
        computed_hash = hmac.new(bytes(YOUR_API_KEY, 'utf-8'), raw_body, hashlib.sha512).hexdigest()
        paystack_signature = request.headers.get('x-paystack-signature')
        if paystack_signature == computed_hash:
            event = json.load(raw_body.decode('utf-8'))
            print('Recieved paystack payload', event)
            return 200
        else:
            print("Invalid paystack signature")