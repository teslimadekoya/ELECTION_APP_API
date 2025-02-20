from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . serializers import UserSerializer
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse
from . models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.urls import path

from django.urls import path
from rest_framework import generics
from .models import User
from .serializers import UserSerializer


# users/urls.py







# Create your views here.
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'User Registered Successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post (self, request):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
            
        user = authenticate(email=email, password=password)

        if not user:
            return Response ({'error': 'This uses does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
        access = AccessToken.for_user(user)
        return Response({'token': str(access)}, status=status.HTTP_200_OK)
        

@api_view(['GET', 'POST'])
def user_list (request):
    
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many= True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_detail(request, id):
    try:
        users = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(users)
        return Response (serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = UserSerializer(users, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        users.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    
