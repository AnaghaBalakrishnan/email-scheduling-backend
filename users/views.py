# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterSerializer, VerifyOTPSerializer, ProfilePictureSerializer
from .models import User
from .utils import send_otp_via_email
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView


class RegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Debug information
        print(f"📁 Files in request: {request.FILES}")
        print(f"📄 Data in request: {request.data}")
        print(f"🔍 Content type: {request.content_type}")
        
        serializer = self.get_serializer(data=request.data)
        print(f"📝 Serializer data: {serializer.initial_data}")
        
        serializer.is_valid(raise_exception=True)
        print(f"✅ Serializer is valid")
        print(f"📋 Validated data: {serializer.validated_data}")
        
        user = serializer.save()
        print(f"✅ User created: {user.email}")
        print(f"📸 Profile picture: {user.profile_picture}")
        print(f"📸 Profile picture URL: {user.profile_picture.url if user.profile_picture else 'None'}")

        # Send OTP
        send_otp_via_email(user.email)

        return Response({
            "message": "User registered successfully. Please check your email for the OTP.",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)

class VerifyOTPView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer
    permission_classes = [AllowAny] # It's good practice to add this here too


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            user = User.objects.get(email=email)
            if user.otp == otp and user.otp_expiry > timezone.now():
                user.is_active = True
                user.is_verified = True
                user.otp = None # Clear OTP fields after successful verification
                user.otp_expiry = None
                user.save()
                return Response({"message": "Email verified successfully. You can now log in."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class ProfilePictureUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilePictureSerializer
    permission_classes = [IsAuthenticated] # Only logged-in users can update

    def get_object(self):
        return self.request.user

# ADD THIS NEW VIEW AT THE END OF THE FILE
class LogoutView(APIView):
    """
    Blacklists the refresh token to securely log out a user.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            # 205 Reset Content: Tells the client to reset the view, but no content to return.
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)