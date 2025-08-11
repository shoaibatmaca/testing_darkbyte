from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import *
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from datetime import datetime, timedelta, timezone


class SignupView(APIView):
    def post(self, request):
        remember_me = request.data.get('remember_me', False)
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Create refresh token
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            # Calculate expiry time depending on remember_me
            now = datetime.now(timezone.utc)
            if remember_me:
                exp = now + timedelta(days=1)
            else:
                exp = now + timedelta(minutes=15)

            # Override token expiry claim manually
            access['exp'] = exp

            # Return tokens and expiry info
            return Response({
                "message": "User registered successfully.",
                "access": str(access),
                "refresh": str(refresh),
                "expires_in": (exp - now).total_seconds()
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




