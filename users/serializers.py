from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Account


        
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'user_type', 'phone', 'image']
        
class UserSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField()
    account = AccountSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email', 'account']
        

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    user_type = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'user_type', 'phone', 'image']

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        user_type = self.validated_data['user_type']
        phone = self.validated_data['phone']
        image = self.validated_data.get('image')
        
        if password != password2:
            raise serializers.ValidationError({'error': "Two Password Doesn't Matched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email Already Exists"})
        
        user = User(username=username, email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.is_active = False
        user.save()
        
        account = Account(user=user, user_type=user_type, phone=phone, image=image)
        account.save()

        
        return user

class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user','image', 'phone', 'user_type']

    def save(self):
        user = self.validated_data['user']
        phone = self.validated_data['phone']
        image = self.validated_data['image']
        user_type = self.validated_data['user_type']
        account = Account(user=user, phone=phone, image=image, user_type=user_type)
        account.save()
        return account
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    