from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer, AccountRegisterSerializer
from .permissions import OwnerPatchOnlyOrReadOnly
from rest_framework.response import Response

class AccountViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [OwnerPatchOnlyOrReadOnly]

class UserRegistrationApiView(APIView):
    serializer_class = AccountRegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data) 
        
        if serializer.is_valid(): 
            user = serializer.save()
            return Response("Form Submission Done")
        return Response(serializer.errors)