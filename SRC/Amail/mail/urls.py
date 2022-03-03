from django.urls import path
from .views import *

urlpatterns = [
    path('new_amail/', new_amail, name='new_amail'),

    path('inbox_list/', InboxList.as_view(), name='inbox_list'),
    path('inbox_detail/<int:pk>', inbox_detail, name='inbox_detail'),

    path('sent_list/', SentList.as_view(), name='sent_list'),
    path('sent_detail/<int:pk>', SentDetail.as_view(), name='sent_detail'),

    path('reply/<int:id>', reply, name='reply'),

]