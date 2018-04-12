from django.conf.urls import url
from . import views




app_name='koinplus_app'


urlpatterns=[
    url(r'^register/$',views.UserRegistrationAPIView.as_view(),name='list'),
    url(r'^login/$',views.UserLoginAPIView.as_view(),name='login'),
    url(r'^logout/$', views.LogoutApi.as_view(), name="logout"),
    url(r'^activate/(?P<token_id>\w{0,50})/$',views.activate,name='activate'),
    url(r'^index$',views.index,name='index.html'),
    url(r'^showmarket$',views.showmarket,name='showMarket.html'),
    url(r'^showtopcoin$',views.showtopcoin,name='getTopCoin.html'),
    url(r'^returnTop25$',views.returntop25,name='returnTop25.html'),
    url(r'^top25/(?P<kur_type>\w{0,50})/$',views.top25,name='top25'),
    url(r'^getCoin/(?P<kur_name>\w{0,50})/(?P<coin_name>\w{0,50})/$',views.getSingleCoin,name="getSingleCoin"),
    url(r'^graphic/(?P<kur_type>\w{0,50})/(?P<koin_type>\w{0,50})$',views.graphicData,name='graphicData')


]
