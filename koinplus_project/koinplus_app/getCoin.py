from .models import Kur,Coin,Price

def singleCoin(kur,koin):
    if kur=="USDT":
        kur_id=3
    elif kur=="ETH":
        kur_id=2
    elif kur=="BTC":
        kur_id=1
    koinid_query=list(Coin.objects.filter(koin_name=koin).values('koin_id'))
    koinid=koinid_query[0]['koin_id']
    koin_list=(Price.objects.filter(kur_id=kur_id,koin_id=koinid).order_by('-time').values('change','last','volume','time','koin_id__koin_name','kur_id__kur_name').first())
    return koin_list
