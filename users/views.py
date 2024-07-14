from django.shortcuts import render, redirect
from rest_framework import viewsets,status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer, AccountRegisterSerializer, UserRegisterSerializer,UserLoginSerializer
from .permissions import OwnerPatchOnlyOrReadOnly
from rest_framework.response import Response

# for token
from django.contrib.auth.tokens import default_token_generator
# for uid
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
# for email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# for login
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

class AccountViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [OwnerPatchOnlyOrReadOnly]

class UserRegistrationApiView(APIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data) 
        if serializer.is_valid(): 
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/users/activate/{uid}/{token}"
            email_subject = "Confirmation Email for Activate Account"
            email_body = render_to_string('confirmation_email.html', {'confirm_link':confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            
            return Response("Check Your Email For Confirmation")
        return Response(serializer.errors)
    
class AccountRegistrationApiView(APIView):
    serializer_class = AccountRegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data) 
        if serializer.is_valid(): 
            account = serializer.save()
            return Response("Account Created Successfully")
        return Response(serializer.errors)
    
def activateAccount(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except User.DoesNotExist:
        user=None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    
class UserLoginApiView(APIView):
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        serializer = UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token':token.key, 'user_id': user.id})
            else:
                return  Response({'error':'Invalid Credential'})
        return Response(serializer.errors)
                
class UserLogoutApiView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')