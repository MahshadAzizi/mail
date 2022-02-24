from django import forms
from .models import *


class NewAmailForm(forms.ModelForm):
    class Meta:
        model = Amail
        fields = ['reciever', 'subject', 'signature', 'body', 'file']