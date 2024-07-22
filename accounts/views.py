from django.contrib.auth import login
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.serializers import LoginSerializer, UserSerializer


# Create your views here.

def index(request):
    return render(request, 'index.html')


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            login(request, user)
            user_data = UserSerializer(user).data
            return Response(user_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
