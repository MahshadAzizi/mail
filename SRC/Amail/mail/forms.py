from django import forms
from django.forms import ValidationError
from .models import Amail
from django_select2.forms import Select2MultipleWidget

from user.models import User


class NewAmailForm(forms.ModelForm):
    receiver = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'style': 'max-width: 400px;'}
        )
    )

    class Meta:
        model = Amail
        fields = ['body', 'subject', 'file']

    def clean_receiver(self):
        receiver = self.cleaned_data['receiver']
        receivers = []
        for r in receiver:
            user = User.objects.filter(username=r).first()
            if user is None:
                raise ValidationError('user by this username not found')
            receivers.append(user)
        return receivers