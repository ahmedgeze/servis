from django.db import models
from decimal import Decimal
from datetime import datetime






class Kur(models.Model):
    kur_id = models.AutoField(primary_key=True)
    kur_name=models.CharField(max_length=10)
    # kur_count=models.DecimalField(max_digits=5,decimal_places=1)




class Coin(models.Model):
    koin_id=models.AutoField(primary_key=True)
    koin_name=models.CharField(max_length=10)



class Price(models.Model):
    koin_id=models.ForeignKey(Coin,on_delete=models.CASCADE)
    kur_id=models.ForeignKey(Kur,on_delete=models.CASCADE)
    last=models.DecimalField(max_digits=20,decimal_places=10,default=Decimal('0.0000000000'))
    high=models.DecimalField(max_digits=20,decimal_places=10,default=Decimal('0.0000000000'))
    low=models.DecimalField(max_digits=20,decimal_places=10,default=Decimal('0.0000000000'))
    time=models.DateTimeField(default=datetime.now)
    base_volume=models.DecimalField(max_digits=20,decimal_places=10,default=Decimal('0.0000000000'))
    volume=models.DecimalField(max_digits=20,decimal_places=10,default=Decimal('0.0000000000'))
    change=models.DecimalField(max_digits=4,decimal_places=2,default=Decimal('0.00'))

    class Meta:
        unique_together=(('koin_id','kur_id','time'))
        ordering=('-time',)




# Create your models here.
