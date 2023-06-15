from django.shortcuts import render
from django.http import JsonResponse
from api.models import User
from django.contrib.auth import get_user_model, login, logout
from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer,UserLoginSerializer, UserSerializer
from rest_framework.decorators import api_view
# from . serializer import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from .validations import custom_validation, validate_email, validate_password
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserLogin(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        
        user_serializer = UserSerializer(user)  # Create UserSerializer instance
        return Response(user_serializer.data)



class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)

# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/register/',
        '/api/login/',
        '/api/token/',
        '/api/token/refresh/',
        '/api/logout/',
        '/links/',
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)