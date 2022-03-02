from django import forms
from .models import *


class NewAmailForm(forms.Form):
    receiver = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
    subject = forms.CharField()
    body = forms.CharField()
    signature = forms.CharField()
    file = forms.FileField()

    def clean_receiver(self):
        receiver = self.cleaned_data['receiver']
        receivers = []
        for r in receiver:
            receivers.append(r)
        return receivers



    # class Meta:
    #     model = Amail
    #     fields = ['receiver', 'subject', 'signature', 'body', 'file']

    # receiver = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
