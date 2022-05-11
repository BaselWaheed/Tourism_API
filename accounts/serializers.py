from rest_framework import serializers
from accounts.exception import Validation
from .models import User  , EmailAddress , PhoneNumber
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.utils.encoding import smart_str , force_bytes ,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util

class LoginSerializer(serializers.Serializer):
    email= serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data , **kwargs):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if not user.is_active:
                    raise Validation({
                        'status' : False,
                        'message' :('y'),
                       })
            else:
                raise Validation({
                    'status' : False,
                    'message' :'Password or email or phone in correct',
                    'data':[]
                    })
        else:
            raise Validation({'status' : False,'message' :'Email or password incorrect'})

        data['user'] = user
        return data

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required= True)
    username = serializers.CharField(required= True)
    phone = serializers.CharField(required= True)
    gender = serializers.CharField(required= True)
    country = serializers.CharField(required= True)
    date_of_birth = serializers.DateField(required= True)
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username', 'email', 'password' ,'phone','gender','country','date_of_birth']
        read_only_fields = ['id']
        extra_kwargs={
            'password' :{'write_only':True}
        }
    def save(self , **kwargs):
        user =User(
            first_name =self.validated_data['first_name'],
            last_name =self.validated_data['last_name'],
            username =self.validated_data['username'],
            gender =self.validated_data['gender'],
            country =self.validated_data['country'],
            date_of_birth =self.validated_data['date_of_birth'],

        )       
        if EmailAddress.objects.filter(email=self.validated_data['email']).exists():
            raise Validation({
                'status' : False ,
                'message' :('email already exist')
                })
        if User.objects.filter(username=self.validated_data['username']).exists():
            raise Validation({
                'status' : False ,
                'message' :('username already taken')
                })
        if PhoneNumber.objects.filter(phone=self.validated_data['phone']).exists():
            raise Validation({
                'status' : False ,
                'message' :('phone already exist')
                })   
              
        password =self.validated_data['password']
        user.set_password(password)
        user.save()
        email =EmailAddress(email=self.validated_data['email'],user=user)
        phone =PhoneNumber(phone=self.validated_data['phone'],user=user)
        email.save()
        phone.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])

    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        user = EmailAddress.objects.get(user=obj)
        return user.email

    token =serializers.SerializerMethodField()

    def get_token(self, obj):
        user= Token.objects.get(user=obj)
        return user.key
        
    phone = serializers.SerializerMethodField()
    def get_phone(self,obj):
        user= PhoneNumber.objects.get(user=obj)
        return user.phone
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','country','date_of_birth','gender','email','phone', 'token']


    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.country = validated_data.get('country', instance.country)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()

        return instance




class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
    confermation_password = serializers.CharField(max_length=128)




class SendPAsswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email = attrs.get('email')
        if EmailAddress.objects.filter(email=email).exists():
            user = EmailAddress.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(user.id)
            print(user.user)
            print(user.user.id)
            h=User.objects.get(pk=user.user.id)
            print(user)
            token = PasswordResetTokenGenerator().make_token(h)
            request = self.context['request']
            site = get_current_site(request).domain
            link = 'http://'+site+'/api/reset/'+ uid + '/'+token+ '/'
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user
            }
            Util.send_email(data)
            return attrs
        else :
            raise serializers.ValidationError(
                {'status' : False,
                'message' :'Email incorrect'
            })

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']
  def validate(self, attrs):
    try:
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError('Token is not Valid or Expired')
        user.set_password(password)
        user.save()
        return attrs
    except DjangoUnicodeDecodeError as identifier:
        PasswordResetTokenGenerator().check_token(user, token)
        raise serializers.ValidationError('Token is not Valid or Expired')