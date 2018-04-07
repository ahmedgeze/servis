
from bittrex.bittrex import Bittrex, API_V2_0
from .models import Kur,Coin,Price
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.utils import timezone
import threading
import time
import pickle

from decimal import Decimal, DecimalException

# import pymysql.cursors


def deneme():
    threading.Timer(5.0,deneme).start()
    # Price.objects.all().delete()
    try:

        my_bittrex = Bittrex(None, None, api_version=API_V2_0)
        data=my_bittrex.get_market_summaries()
        start_date=timezone.now()
        hash_date=time.localtime(time.time())
        hash_date_hour=hash_date[3]
        hash_date_minute=hash_date[4]
        hash_date_sec=hash_date[5]
        hash_coin_twelve={}
        hash_dict={}

        bc=0
        et=0
        us=0


        if hash_date_hour==8 and hash_date_minute == 7 and hash_date_sec>0and hash_date_sec <60:
             for x in range(len(data['result'])):
                 hash_coin_twelve[data['result'][x]['Summary']['MarketName']]=data['result'][x]['Summary']['Last']
                 pickle.dump(hash_coin_twelve,open('twelve.pickle','wb'))
                 print(hash_coin_twelve)

        else:
                hash_dict=pickle.load(open('twelve.pickle','rb'))

                for x in range(len(data['result'])):
                    market_name=data['result'][x]['Summary']['MarketName']
                    coin_name=market_name[4:len(market_name)]
                    usd_coinname=market_name[5:len(market_name)]
                    print("BTC:",bc,"ETH",et,"USDT",us)


                    if str(data['result'][x]['Summary']['MarketName'][0:3]) == 'BTC':
                        bc+=1
                        btc=Price.objects.create(koin_id=Coin.objects.get(koin_name=str(coin_name)),
                                                 kur_id=Kur.objects.get(kur_name="BTC"),
                                                 last=data['result'][x]['Summary']['Last'],
                                                 high=data['result'][x]['Summary']['High'],
                                                 low=data['result'][x]['Summary']['Low'],
                                                 time=start_date,
                                                 base_volume=data['result'][x]['Summary']['BaseVolume'],
                                                 volume=data['result'][x]['Summary']['Volume'],
                                                 change=((data['result'][x]['Summary']['Last']-hash_dict[data['result'][x]['Summary']['MarketName']])*100)/data['result'][x]['Summary']['Last'])


                    elif str(data['result'][x]['Summary']['MarketName'][0:3]) == 'ETH':
                        et+=1
                        eth=Price.objects.create(koin_id=Coin.objects.get(koin_name=str(coin_name)),
                                                kur_id=Kur.objects.get(kur_name="ETH"),
                                                last=data['result'][x]['Summary']['Last'],
                                                high=data['result'][x]['Summary']['High'],
                                                low=data['result'][x]['Summary']['Low'],
                                                time=start_date,
                                                base_volume=data['result'][x]['Summary']['BaseVolume'],
                                                volume=data['result'][x]['Summary']['Volume'],
                                                change=((data['result'][x]['Summary']['Last']-hash_dict[data['result'][x]['Summary']['MarketName']])*100)/data['result'][x]['Summary']['Last'])

                    elif str(data['result'][x]['Summary']['MarketName'][0:4]) == 'USDT':
                        us+=1
                        usd=Price.objects.create(koin_id=Coin.objects.get(koin_name=str(usd_coinname)),
                                               kur_id=Kur.objects.get(kur_name="USDT"),
                                               last=data['result'][x]['Summary']['Last'],
                                               high=data['result'][x]['Summary']['High'],
                                               low=data['result'][x]['Summary']['Low'],
                                               time=start_date,
                                               base_volume=data['result'][x]['Summary']['BaseVolume'],
                                               volume=data['result'][x]['Summary']['Volume'],
                                               change=((data['result'][x]['Summary']['Last']-hash_dict[data['result'][x]['Summary']['MarketName']])*100)/data['result'][x]['Summary']['Last'])








    except (ValueError, TypeError, DecimalException):
        print(self.error_message)


    print("BTC:",bc,"ETH",et,"USDT",us)
    return "BAŞARILI"




def control():
        my_bittrex = Bittrex(None, None, api_version=API_V2_0)
        data=my_bittrex.get_market_summaries()
        btcCount=0
        ethCount=0
        usdtCount=0
        for i in range(0,len(data['result'])):
            if data['result'][i]['Summary']['MarketName'][0:4]=="BTC-":
                btc_fmarket=data['result'][i]['Summary']['MarketName']
                btc_coinname=btc_fmarket[4:len(btc_fmarket)]
                query_btc=Coin.objects.filter(koin_name=btc_coinname)
                if len(query_btc)==0:
                    Coin.objects.create(koin_name=btc_coinname)
                    btcCount+=1

            elif data['result'][i]['Summary']['MarketName'][0:4]=="ETH-":
                eth_fmarket=data['result'][i]['Summary']['MarketName']
                eth_coinname=eth_fmarket[4:len(eth_fmarket)]
                query_eth=Coin.objects.filter(koin_name=eth_coinname)
                if len(query_eth)==0:
                    Coin.objects.create(koin_name=eth_coinname)
                    ethCount+=1


            if data['result'][i]['Summary']['MarketName'][0:5]=="USDT-":
                usdt_fmarket=data['result'][i]['Summary']['MarketName']
                usdt_coinname=usdt_fmarket[5:len(usdt_fmarket)]
                query_usdt=Coin.objects.filter(koin_name=usdt_coinname)
                if len(query_usdt)==0:
                    Coin.objects.create(koin_name=usdt_coinname)
                    usdtCount+=1

        print(btcCount,"btc")
        print(ethCount,"eth")
        print(usdtCount,"usd")






        # return data
