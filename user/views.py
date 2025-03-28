from .serializers import UserSerializer, UserLoginSerializer, UserSignupSerializer, VerifySerializer
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import User
from wallet.models import Wallet
from datetime import datetime
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .verify import send_otp_email
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



class UserSignup(generics.CreateAPIView):
    serializer_class =  UserSignupSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email = serializer.validated_data.get("email")
        # send_otp_email(request, email) 
        refresh = RefreshToken.for_user(user)
        response_data = {
            "message": "Registration successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": str(user.id),
                "role": user.role,
                "email": user.email,
                "username": user.username
            },
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class VerifyUserAccount(generics.GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        otp = serializer.validated_data.get("otp")

        session_email = request.session.get("create_account_email")
        session_otp = request.session.get("create_account_otp")

        if session_email != email or session_otp != otp:
            return response.Response({"error": "Invalid OTP or email"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            user.verified = True  
            user.save()
            del request.session["create_account_email"]
            del request.session["create_account_otp"]
            return response.Response({"message": "Account verified successfully!"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return response.Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    

class LoginView(APIView):
    def post(self, request):
        # Deserialize incoming data
        serializer = UserLoginSerializer(data=request.data)
        
        # Check if the serializer is valid
        if serializer.is_valid():
            # Retrieve the validated user from the serializer
            user = serializer.validated_data['user']
            
            # Generate refresh and access tokens
            refresh = RefreshToken.for_user(user)
            login(request, user)
            wallet_data = Wallet.objects.filter(user=user).first()
            # Prepare the user data to return in the response
            user_data = {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'email': user.email
            }
            wallet_info = {
                "id": wallet_data.id,
                "balance": wallet_data.balance
            }
            
            # # Try sending the login notification email to the user
            # try:
            #     send_mail(
            #         subject='Smart IoT User Login Notification',
            #         message=f'Dear {user.username},\n\nYou logged in successfully at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.\n\nBest Regards,\nSmart IoT Team',
            #         from_email='abimbolaokeyedun919@gmail.com',  # Replace with your sender email
            #         recipient_list=[user.email],
            #     )
            # except Exception as e:
            #     # If there was an issue with the email, log the error or handle accordingly
            #     print(f"Error sending email: {e}")
            #     # You can return a message here or log it for further monitoring
            #     # For now, we will not interrupt the login process, just inform the user
            # return Response({
            #     "message": "Login successful, but there was an issue sending the email. Please try again later.",
            #     "refresh": str(refresh),
            #     "access": str(refresh.access_token),
            #     "data": user_data
            # }, status=status.HTTP_200_OK)
            
            # If email is sent successfully, return the success response with tokens and user data
            return Response({
                "message": "Login successful. Please check your email (and spam folder).",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "data": user_data,
                "wallet": wallet_info  # Include the wallet information in the response for convenience and user reference
            }, status=status.HTTP_200_OK)
        
        # If serializer is not valid, return serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):

    def get(self, request):
        obj = User.objects.all()
        serializer = UserSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    




# @csrf_exempt  # Exempt from CSRF for simplicity (use with caution in production)
# def otp_request(request):
#     if request.method == "POST":
#         recipient_email = request.POST.get("email")

#         if recipient_email:
#             result = send_otp_email(recipient_email)
#             return JsonResponse(result)
#         else:
#             return JsonResponse({"status": "error", "message": "Email is required."}, status=400)

#     return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
