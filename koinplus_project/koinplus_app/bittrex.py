from bittrex.bittrex import Bittrex, API_V2_0
from .models import Kur,Coin,Price
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.utils import timezone
import threading
import time
import pickle

# import pymysql.cursors


def deneme():
    threading.Timer(5.0,deneme).start()
    try:

        my_bittrex = Bittrex(None, None, api_version=API_V2_0)  # or defaulting to v1.1 as Bittrex(None, None)
        data=my_bittrex.get_market_summaries()
        start_date=timezone.now()
        hash_date=time.localtime(time.time())
        hash_date_hour=hash_date[3]
        hash_date_minute=hash_date[4]
        hash_date_sec=hash_date[5]
        hash_coin_twelve={}
        hash_dict={}

        if hash_date_hour==1 and hash_date_minute == 20 and hash_date_sec>10and hash_date_sec <15:
             for x in range(len(data['result'])):
                 hash_coin_twelve[data['result'][x]['Summary']['MarketName']]=data['result'][x]['Summary']['Last']
                 pickle.dump(hash_coin_twelve,open('twelve.pickle','wb'))

        else:
                hash_dict=pickle.load(open('twelve.pickle','rb'))

                for x in range(len(data['result'])):
                    market_name=data['result'][x]['Summary']['MarketName']
                    coin_name=market_name[4:len(market_name)]
                    coin_name_usd=market_name[5:len(market_name)]

                    if str(data['result'][x]['Summary']['MarketName'][0:3])=='BTC':
                        btc=Price.objects.create(koin_id=Coin.objects.get(koin_name=str(coin_name)),
                                                 kur_id=Kur.objects.get(kur_name="BTC"),
                                                 last=data['result'][x]['Summary']['Last'],
                                                 high=data['result'][x]['Summary']['High'],
                                                 low=data['result'][x]['Summary']['Low'],
                                                 time=start_date,
                                                 base_volume=data['result'][x]['Summary']['BaseVolume'],
                                                 volume=data['result'][x]['Summary']['Volume'],
                                                 change=((data['result'][x]['Summary']['Last']-hash_dict[data['result'][x]['Summary']['MarketName']])*100)/data['result'][x]['Summary']['Last'])

                    elif str(data['result'][x]['Summary']['MarketName'][0:3])=='ETH':
                       eth=Price.objects.create(koin_id=Coin.objects.get(koin_name=str(coin_name)),
                                                kur_id=Kur.objects.get(kur_name="ETH"),
                                                last=data['result'][x]['Summary']['Last'],
                                                high=data['result'][x]['Summary']['High'],
                                                low=data['result'][x]['Summary']['Low'],
                                                time=start_date,
                                                base_volume=data['result'][x]['Summary']['BaseVolume'],
                                                volume=data['result'][x]['Summary']['Volume'],
                                                change=((data['result'][x]['Summary']['Last']-hash_dict[data['result'][x]['Summary']['MarketName']])*100)/data['result'][x]['Summary']['Last'])

                    elif str(data['result'][x]['Summary']['MarketName'][0:4])=='USDT':
                      usd=Price.objects.create(koin_id=Coin.objects.get(koin_name=str(coin_name_usd)),
                                               kur_id=Kur.objects.get(kur_name="USDT"),
                                               last=data['result'][x]['Summary']['Last'],
                                               high=data['result'][x]['Summary']['High'],
                                               low=data['result'][x]['Summary']['Low'],
                                               time=start_date,
                                               base_volume=data['result'][x]['Summary']['BaseVolume'],
                                               volume=data['result'][x]['Summary']['Volume'],
                                               change=((data['result'][x]['Summary']['Last']-hash_dict[data['result'][x]['Summary']['MarketName']])*100)/data['result'][x]['Summary']['Last'])

    except Exception as e:
        print(e)
        return e

    x=User.objects.filter(username="ahmovski").values('id')
    y=Token.objects.filter(key="d8c0376f09cf2c3c30d26949d74acf408fae0278").values('user_id')
    z=x[0]['id']
    t=y[0]['user_id']
    print(str(x)+" "+str(y)+str(z)+str(t))
    return 'başarılı'
