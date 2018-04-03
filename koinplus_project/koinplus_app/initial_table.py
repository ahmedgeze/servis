from bittrex.bittrex import Bittrex, API_V2_0
from .models import Kur,Coin,Price


def enjoycointable():
    my_bittrex = Bittrex(None, None, api_version=API_V2_0)
    data=my_bittrex.get_market_summaries()



    for x in range(len(data['result'])):
        market_name=data['result'][x]['Summary']['MarketName']
        coin_name=market_name[4:len(market_name)]
        if market_name[0:3]=='BTC':
            coin=Coin.objects.create(koin_name=coin_name)

    print(str(data))
