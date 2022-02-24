from django.urls import path
from .views import *

urlpatterns = [
    path('new_amail/', NewAmail.as_view(), name='new_amail'),
    path('inbox_list/', InboxList.as_view(), name='inbox_list'),
    path('inbox_detail/', InboxDetail.as_view(), name='inbox_detail'),

]