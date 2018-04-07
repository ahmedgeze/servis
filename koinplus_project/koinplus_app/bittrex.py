
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
    #
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

        pickle_twelve_control(hash_date_hour,hash_date_minute,hash_date_sec,len(data['result']),hash_coin_twelve,'twelve_pickle',data)
        twelve_pickle=pickle.load(open('twelve.pickle','rb'))
        price_dbsave(data,twelve_pickle,start_date)



    except Exception as e:   #ValueError as e1, TypeError, DecimalException
        print (e)

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



def pickle_twelve_control(hour,minute,seconds,length,picklefile,picklefile_name,datas):
    if hour==12 and minute==0 and seconds>1 and seconds<10:
        count=0
        for x in range(0,length,1):
            picklefile[datas['result'][x]['MarketName']]=datas['result'][x]['Summary']['Last']
            count+=1
            pickle.dump(picklefile,open(picklefile_name,'wb'))
        print("Pickle File Güncellendi",count)


def price_dbsave(datas,pickle_file,starting_time):
    bc=0
    et=0
    us=0
    for x in range(0,len(datas['result']),1):
        market_name=datas['result'][x]['Summary']['MarketName']
        coin_name=market_name[4:len(market_name)]
        usd_coinname=market_name[5:len(market_name)]
        hash_dictionary={}
        hash_dictionary=pickle_file

        if str(datas['result'][x]['Summary']['MarketName'][0:3]) == 'BTC':
            bc+=1
            btc=Price.objects.create(koin_id=Coin.objects.get(koin_name=str(coin_name)),
                                     kur_id=Kur.objects.get(kur_name="BTC"),
                                     last=datas['result'][x]['Summary']['Last'],
                                     high=datas['result'][x]['Summary']['High'],
                                     low=datas['result'][x]['Summary']['Low'],
                                     time=starting_time,
                                     base_volume=datas['result'][x]['Summary']['BaseVolume'],
                                     volume=datas['result'][x]['Summary']['Volume'],
                                     change=((datas['result'][x]['Summary']['Last']-hash_dictionary[datas['result'][x]['Summary']['MarketName']])*100)/datas['result'][x]['Summary']['Last'])


        elif str(datas['result'][x]['Summary']['MarketName'][0:3]) == 'ETH':
            et+=1
            eth=Price.objects.create(koin_id=Coin.objects.get(koin_name=str(coin_name)),
                                    kur_id=Kur.objects.get(kur_name="ETH"),
                                    last=datas['result'][x]['Summary']['Last'],
                                    high=datas['result'][x]['Summary']['High'],
                                    low=datas['result'][x]['Summary']['Low'],
                                    time=starting_time,
                                    base_volume=datas['result'][x]['Summary']['BaseVolume'],
                                    volume=datas['result'][x]['Summary']['Volume'],
                                    change=((datas['result'][x]['Summary']['Last']-hash_dictionary[datas['result'][x]['Summary']['MarketName']])*100)/datas['result'][x]['Summary']['Last'])

        elif str(datas['result'][x]['Summary']['MarketName'][0:4]) == 'USDT':
            us+=1
            usd=Price.objects.create(koin_id=Coin.objects.get(koin_name=str(usd_coinname)),
                                   kur_id=Kur.objects.get(kur_name="USDT"),
                                   last=datas['result'][x]['Summary']['Last'],
                                   high=datas['result'][x]['Summary']['High'],
                                   low=datas['result'][x]['Summary']['Low'],
                                   time=starting_time,
                                   base_volume=datas['result'][x]['Summary']['BaseVolume'],
                                   volume=datas['result'][x]['Summary']['Volume'],
                                   change=((datas['result'][x]['Summary']['Last']-hash_dictionary[datas['result'][x]['Summary']['MarketName']])*100)/datas['result'][x]['Summary']['Last'])


    print("BTC:",bc,"ETH",et,"USDT",us)












        # return data
