from api.models import User
from django.contrib.auth import get_user_model, login, logout, authenticate
from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer,UserLoginSerializer, UserSerializer

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from django.conf import settings
from django.http import HttpResponse
import requests
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



def google_login_callback(request):
    # Retrieve the authorization code from the query parameters
    code = request.GET.get('code', '')

    # Exchange the authorization code for an access token
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        'redirect_uri': 'https://bit.up.railway.app/google/login/callback/',
        'grant_type': 'authorization_code',
    }
    token_response = requests.post(token_url, data=token_data)

    if token_response.status_code == 200:
        # Access token successfully obtained
        access_token = token_response.json().get('access_token', '')

        # Use the access token to retrieve user information from Google
        user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)

        if user_info_response.status_code == 200:
            # User information retrieved successfully
            user_info = user_info_response.json()

            # Check if the user is already registered
            User = get_user_model()
            try:
                # Try to retrieve the user from the database based on their email
                user = User.objects.get(email=user_info['email'])
                # Authenticate and log in the user
                user = authenticate(request, username=user.username, password=user.password, backend='django.contrib.auth.backends.ModelBackend')
                login(request, user)
                return HttpResponse("Login successful. Redirecting...")
            except User.DoesNotExist:
                # User is not registered, proceed with registration
                user = User.objects.create_user(email=user_info['email'], username=user_info['email'])
                # You may set additional properties or perform other actions here
                user.save()
                # Authenticate and log in the newly registered user
                user = authenticate(request, username=user.username, password=user.password, backend='django.contrib.auth.backends.ModelBackend')
                login(request, user)
                return HttpResponse("Registration successful. Redirecting...")
        else:
            # Error retrieving user information from Google
            return HttpResponse("Error retrieving user information from Google.")
    else:
        # Error exchanging authorization code for access token
        return HttpResponse("Error exchanging authorization code for access token.")
