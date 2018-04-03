from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage


class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=('id','username','email','password','confirm_password','date_joined','is_active')

    def create(self,validated_data):
        del validated_data['confirm_password']
        validated_data['password']=make_password(validated_data['password'])
        validated_data['is_active']=0
        return super(UserRegistrationSerializer,self).create(validated_data)


    def validate(self,attrs):
        if attrs.get('password')!=attrs.get('confirm_password'):
            raise serializers.ValidationError("Those passwords dont match")
        return attrs


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])

class UserLogoutSerializer(serializers.Serializer):
    token=serializers.CharField(write_only=True,required=True)
    username=serializers.CharField(required=True)

    



    # def validate(self,username,token):
    #     user_id=User.objects.filter(username='username').values('id')[0]['id']
    #     if Token.objects.filter()






class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token",)
