from rest_framework import generics, status, response
from .serializers import WalletSerializer, WalletFundingSerializer, TransferSerializer
from .models import Wallet, WalletFunding, Transfer
from rest_framework.views import APIView
from paystack import initialize, transfer
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

# balance, amount, description, accName, accNo, bankCode
from rest_framework.response import Response
from rest_framework import status

class TransferAction(APIView):
    def post(self, request):
        # Deserialize incoming data
        serializer = TransferSerializer(data=request.data)
        
        # Check if the serializer is valid
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user:
                # Query the user based on email
                data = User.objects.filter(email=user).first()
                
                if data:
                    # Get wallet associated with the user
                    wallet = Wallet.objects.filter(user=data).first()
                    if wallet:
                        balance = wallet.balance
                        amount = serializer.validated_data['amount']
                        description = serializer.validated_data['description']
                        bank_code = serializer.validated_data['bank_code']
                        account_number = serializer.validated_data['account_number']
                        account_name = serializer.validated_data['account_name']

                        # Convert Decimal to float before sending in the request
                        balance = float(balance)  # Convert Decimal to float
                        amount = float(amount)    # Convert Decimal to float

                        # Call the transfer function (ensure this function is correct and returns valid data)
                        transfer_response = transfer(
                            balance=balance,
                            accNo=account_number,
                            accName=account_name,
                            description=description,
                            bankCode=bank_code,
                            amount=amount
                        )
                        
                        # If transfer_response is successful, return success response
                        if transfer_response and transfer_response.get("status") == "success":
                            return Response(
                                {"message": "Transfer successful", "data": transfer_response},
                                status=status.HTTP_200_OK
                            )
                        else:
                            return Response(
                                {"error": "Transfer failed", "details": transfer_response},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        return Response(
                            {"error": "Wallet not found for the user"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {"error": "User not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {"error": "Invalid user data"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # If serializer is not valid, return serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)