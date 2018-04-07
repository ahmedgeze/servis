from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from koinplus_app.models import *
from rest_framework.authtoken.models import Token
from .bittrex import *
from .initial_table import *

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import UserRegistrationSerializer,UserLoginSerializer,UserLogoutSerializer,TokenSerializer
from django.contrib.auth.models import User
from django.core.mail import EmailMessage



def index(request):
    # deneme()
    control()
    deneme()
    # Coin.objects.all().delete()
    
    # return JsonResponse(control(),safe=False)
    return render(request,'index.html',{})

@api_view(['POST'])
def logout(request):
        serializer=UserLogoutSerializer(data=request.data)
        if serializer.is_valid():
            return Response(request.data,status=status.HTTP_201_CREATED)

class LogoutApi(CreateAPIView):
        authentication_classes = ()
        permission_classes = ()
        serializer_class = UserLogoutSerializer
        def create(self, request, *args, **kwargs):
            serializer=self.get_serializer(data=request.data)
            if serializer.is_valid() :

                x=request.data['token']
                Token.objects.filter(key=x).delete()
                # Token.objects.filter(key=serializer['key']).delete()
                return Response(request.data['username']+"logged out",status=status.HTTP_201_CREATED)



def activate(request,token_id):
    user_id_query=Token.objects.filter(key=token_id).values('user_id')
    user_id=user_id_query[0]['user_id']
    user_activate=User.objects.filter(id=user_id).values('is_active')
    user_activate_state=user_activate[0]['is_active']
    if user_activate_state==False :
        User.objects.filter(id=user_id).update(is_active=True)



    return render(request,'index.html',{})


class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        username=str(data['username'])
        email=str(data['email'])
        usertoken=str(data['token'])

        email=EmailMessage("User Activation","Merhaba "+username+" Hesabını aktif etmek için linke tıklayınız "+" http://127.0.0.1:8000/activate/"+str(usertoken),
                            to=[email])
        email.send()

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLogoutAPIView(APIView):

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)


def showmarket(request):
    usdt_query=Price.objects.filter(kur_id=3).order_by('-time','koin_id__koin_name').values('time','kur_id__kur_name','koin_id__koin_name','last','high','low','volume','base_volume','change')
    actual_usdt=usdt_query[0:15]

    btc_query=Price.objects.filter(kur_id=1).order_by('-time','koin_id__koin_name').values('time','kur_id__kur_name','koin_id__koin_name','last','high','low','volume','base_volume','change')
    actual_btc=btc_query[0:195]

    eth_query=Price.objects.filter(kur_id=2).order_by('-time','koin_id__koin_name').values('time','kur_id__kur_name','koin_id__koin_name','last','high','low','volume','base_volume','change')
    actual_eth=eth_query[0:58]

    dict={'usdt':actual_usdt,'btc':actual_btc,'eth':actual_eth}
    return render(request,'showMarket.html',{'dict':dict})


def showtopcoin(request):
    usdt_query=Price.objects.filter(kur_id=3).order_by('-time','-last').values('time','kur_id__kur_name','koin_id__koin_name','last','high','low','volume','base_volume','change')
    actual_usdt=usdt_query[0:5]

    btc_query=Price.objects.filter(kur_id=1).order_by('-time','-last').values('time','kur_id__kur_name','koin_id__koin_name','last','high','low','volume','base_volume','change')
    actual_btc=btc_query[0:5]

    eth_query=Price.objects.filter(kur_id=2).order_by('-time','-last').values('time','kur_id__kur_name','koin_id__koin_name','last','high','low','volume','base_volume','change')
    actual_eth=eth_query[0:5]

    dict={'usdt':actual_usdt,'btc':actual_btc,'eth':actual_eth}
    return render(request,'showMarket.html',{'dict':dict})


def returntop25(request):
        usdt_query=Price.objects.filter(kur_id=3).order_by('-time','last').values('time','kur_id__kur_name','koin_id__koin_name','last','high','low','volume','base_volume','change')
        actual_usdt=usdt_query[0:15]

        btc_query=Price.objects.filter(kur_id=1).order_by('-time','last').values('time','kur_id__kur_name','koin_id__koin_name','last','high','low','volume','base_volume','change')
        actual_btc=btc_query[0:40]

        eth_query=Price.objects.filter(kur_id=2).order_by('-time','last').values('time','kur_id__kur_name','koin_id__koin_name','last','high','low','volume','base_volume','change')
        actual_eth=eth_query[0:35]

        info=True

        top_list=(list(actual_usdt)+list(actual_eth)+list(actual_btc))
        data={
             'messages': info,
             'result':top_list
        }


        return JsonResponse(data,safe=False)


def top25(request,kur_type):
    filter_code=0
    if kur_type=='BTC':
        filter_code=1
        total_size=197
    elif kur_type=='ETH':
        filter_code=2
        total_size=64
    elif kur_type=='USDT':
        filter_code=3
        total_size=16



    coin_query=Price.objects.filter(kur_id=filter_code).order_by('-time','koin_id__koin_name').values('time','kur_id__kur_name','koin_id__koin_name','last','high','low','volume','base_volume','change')
    actual_query=coin_query[0:total_size]
    actual_list=list(actual_query)


    info=True
    data= {
    'messages':info,
    'result':actual_list
    }
    return JsonResponse(data,safe=False)


def graphicData(request,kur_type,koin_type):




    data={
        'kur':kur_type,
        'koin':koin_type
    }
    return JsonResponse(data,safe=False)







    # def api_get_usdt(request):
    # x=Usdt.objects.all().order_by('id').values()
    # usdt=list(x[len(x)-15:len(x)+15])
    #
    # return JsonResponse(usdt,safe=False)
