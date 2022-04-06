from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('new_amail/', new_amail, name='new_amail'),

    path('inbox_list/', InboxList.as_view(), name='inbox_list'),
    path('inbox_detail/<int:pk>', inbox_detail, name='inbox_detail'),

    path('sent_list/', SentList.as_view(), name='sent_list'),
    path('sent_detail/<int:pk>', SentDetail.as_view(), name='sent_detail'),

    path('reply/<int:pk>', reply, name='reply'),
    path('forward/<int:pk>', forward_mail, name='forward'),

    path('add_category/', AddCategory.as_view(), name='add_category'),
    path('add_category_mail/<int:pk>', add_category_mail, name='add_category_mail'),
    path('category_list/', CategoryList.as_view(), name='category_list'),
    path('category_detail/<int:pk>', CategoryDetail.as_view(), name='category_detail'),
    path('delete_category/<int:pk>', delete_category, name='delete_category'),

    path('archive_mail/<int:pk>', archive_mail, name='archive_mail'),
    path('trash_mail/<int:pk>', trash_mail, name='trash_mail'),

    path('archive/', ArchiveList.as_view(), name='archive'),
    path('archive_detail/<int:pk>', ArchiveDetail.as_view(), name='archive_detail'),

    path('trash/', TrashList.as_view(), name='trash'),
    path('trash_detail/<int:pk>', TrashDetail.as_view(), name='trash_detail'),

    path('draft/', DraftList.as_view(), name='draft'),
    path('draft_detail/<int:pk>', DraftDetail.as_view(), name='draft_detail'),

    path('filteremail/', FilterEmail.as_view(), name='filteremail'),

    # path('alpine/', FilterAlpineJs.as_view(), name='alpine'),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('contacts-api/', ContactsApiView.as_view(), name='contacts-api'),
    path('emails-api/', EmailsApiView.as_view(), name='emails-api'),

    path('search-email/', csrf_exempt(search_email), name="search_email"),

]
