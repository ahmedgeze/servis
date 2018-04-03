from django.contrib import admin
from .models import Coin,Kur,Price





class KurAdmin(admin.ModelAdmin):
    list_display=('kur_id','kur_name')

class CoinAdmin(admin.ModelAdmin):
    list_display=('koin_id','koin_name')

class PriceAdmin(admin.ModelAdmin):
    list_display=('koin_id','kur_id','last','high','low','time','base_volume','volume','change')


# Register your models here.

admin.site.register(Coin,CoinAdmin)
admin.site.register(Kur,KurAdmin)
admin.site.register(Price,PriceAdmin)
