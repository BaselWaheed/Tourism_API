from .models import EmailAddress, User ,PhoneNumber
from django.contrib.auth.backends import ModelBackend

class CommonAuthBackend(ModelBackend):
    def authenticate(self,request,username=None,password=None,**kwargs):
        if(EmailAddress.objects.filter(email=username).exists()):
            mego=EmailAddress.objects.get(email=username)
            text = mego.user

        elif(PhoneNumber.objects.filter(phone=username).exists()):
            mego=PhoneNumber.objects.get(phone=username)
            text = mego.user

        elif(User.objects.filter(username=username).exists()):
            text=User.objects.get(username=username)
            
        else :
            return None
        
        try :
            user = User.objects.get(username=text)

        except User.DoesNotExist:
            return None
        if user.check_password(password):
            user.backend="%s.%s"%(self.__module__,self.__class__.__name__)
            return user