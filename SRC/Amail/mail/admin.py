from django.contrib import admin
from user.models import *
from mail.models import *


admin.site.register(User)
admin.site.register(ContactBook)
admin.site.register(Amail)
admin.site.register(Category)
admin.site.register(Signature)
