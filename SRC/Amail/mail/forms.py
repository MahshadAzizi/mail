from django import forms
from .models import *


class NewAmailForm(forms.ModelForm):
    class Meta:
        model = Amail
        fields = ['receiver', 'subject', 'signature', 'body', 'file']
