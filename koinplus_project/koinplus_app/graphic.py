from .models import Kur,Coin,Price
import threading
from django.utils import timezone
import time

def five_seconds_graphic_response(koin_type,kur_type):
    coinid=list(Coin.objects.filter(koin_name=koin_type).values('koin_id'))
    coin_price=list(Price.objects.filter(kur_id=kur_type,koin_id=coinid[0]['koin_id']).values('last'))
    print(coin_price[0]['last'])
    return coin_price[0]['last']
