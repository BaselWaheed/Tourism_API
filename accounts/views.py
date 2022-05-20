from django.contrib.auth import login as LOGIN
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny ,IsAuthenticated
from accounts.models import EmailAddress, User
from .serializers import LoginSerializer ,CustomerRegistrationSerializer , UserSerializer ,SendPAsswordSerializer , PasswordChangeSerializer, UserPasswordResetSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication


class LoginAPI(generics.GenericAPIView):   
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self , request , *args , **kwargs):
        serializer = self.get_serializer(data =request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token= Token.objects.get_or_create(user=user)
        LOGIN(request,user)
        serializer = UserSerializer(user)
        return Response({"status":True , "message":" تم تسجيل الدخول بنجاح" ,'data':serializer.data},status=status.HTTP_200_OK)


            
class CustomerRegistrationView(generics.GenericAPIView):  # signup 
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class =CustomerRegistrationSerializer
    def post(self , request , *args , **kwargs):
        serializer = self.get_serializer(data =request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response({ 'status' : True ,'message' :'account created successfully', "data" :serializer.data },status=status.HTTP_200_OK)



class LogoutVIEW(APIView):
    authentication_classes = (TokenAuthentication,)  # log out 
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):   
        tokens = Token.objects.filter(user=request.user)   
        for token in tokens:
            token.delete()
        return Response({'status' : True,'success': 'User logged out.'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    authentication_classes = (TokenAuthentication,)   #change password
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():   
            user = request.user
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            confermation_password = request.data.get('confermation_password')
            if not user.check_password(old_password):
                return Response({'status' : False,'message': 'password in correct'}, status=status.HTTP_200_OK)
            if confermation_password != new_password :
                return Response({'status' : False,'message': 'password bot match'}, status=status.HTTP_200_OK)
            user.set_password(new_password)
            user.save()
            return Response({'status' : True,'success': 'Password changed'}, status=status.HTTP_200_OK)
        return Response({'status' : False,'messege': 'Password incorrect'}, status=status.HTTP_400_BAD_REQUEST)


class SendpasswordResetEmail(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = SendPAsswordSerializer
    def post(self,request,format=None):
        serializer = self.get_serializer(data =request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'status': True,'messege' : 'check your email'},status=status.HTTP_200_OK)
        # return Response({'status' : False,'messege': 'email'}, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    # dah lw hy3mlo al page fe mobile aw website
    authentication_classes = ()
    permission_classes = (AllowAny,)
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)







class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response({"status":True,"message":"updated successfully","data":serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status":True,"message":" working","data":serializer.data})


from django.shortcuts import render
from django.utils.encoding import  smart_str
from django.utils.http import urlsafe_base64_decode   
from django.contrib.auth.tokens import PasswordResetTokenGenerator     

def resetassword(request, *args, **kwargs):
    token = kwargs['token']
    uid = kwargs['uid']
    id = smart_str(urlsafe_base64_decode(uid))
    user = EmailAddress.objects.get(id=id)
    print(user)
    if not PasswordResetTokenGenerator().check_token(user.user,token):
        return render(request,'reset_failed.html')
    if request.method== 'POST':
        password1 =request.POST.get('password1')
        password2 =request.POST.get('password2')
        print(password1)
        if password1 != password2 :
            return render(request,'reset_failed.html')
        user.user.set_password(password1)
        user.user.save()
        return render(request,'reset_complete.html')
    return render(request,'reset_password.html')