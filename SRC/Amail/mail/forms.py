from django import forms
from django.forms import ValidationError, RadioSelect
from .models import Amail, Category, Filter
from django_select2.forms import Select2MultipleWidget
from user.models import User, Signature


class NewAmailForm(forms.ModelForm):
    receiver = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'style': 'max-width: 400px;'}
        )
    )
    bcc = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'style': 'max-width: 400px;', 'required': False}
        )
    )
    cc = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'style': 'max-width: 400px;', 'required': False}
        )
    )

    class Meta:
        model = Amail
        fields = ['body', 'subject', 'file', 'signature']

    def clean_receiver(self):
        receiver = self.cleaned_data['receiver']
        receivers = []
        for r in receiver:
            user = User.objects.filter(username=r).first()
            if user is None:
                raise ValidationError('user by this username not found')
            receivers.append(user)
        return receivers

    def clean_bcc(self):
        bcc = self.cleaned_data['bcc']
        bcc_list = []
        for r in bcc:
            user = User.objects.filter(username=r).first()
            if user is None:
                raise ValidationError('user by this username not found')
            bcc_list.append(user)
        return bcc_list

    def clean_cc(self):
        cc = self.cleaned_data['cc']
        cc_list = []
        for r in cc:
            user = User.objects.filter(username=r).first()
            if user is None:
                raise ValidationError('user by this username not found')
            cc_list.append(user)
        return cc_list


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Amail
        fields = ['body', 'subject', 'file', 'signature']


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class AddMailToCategoryForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(),
        widget=Select2MultipleWidget(
            attrs={'style': 'max-width: 400px;'}
        ))

    class Meta:
        model = Amail
        fields = []

    def clean_category(self):
        category = self.cleaned_data['category']
        category_list = []
        for r in category:
            category_name = Category.objects.filter(name=r).first()
            if category_name is None:
                raise ValidationError('user by this username not found')
            category_list.append(category_name)
        return category_list


class ForwardForm(forms.ModelForm):
    receiver = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'style': 'max-width: 400px;'}
        )
    )
    bcc = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'style': 'max-width: 400px;', 'required': False}
        )
    )
    cc = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'style': 'max-width: 400px;', 'required': False}
        )
    )

    class Meta:
        model = Amail
        fields = ['receiver', 'cc', 'bcc']

    def clean_receiver(self):
        receiver = self.cleaned_data['receiver']
        receivers = []
        for r in receiver:
            user = User.objects.filter(username=r).first()
            if user is None:
                raise ValidationError('user by this username not found')
            receivers.append(user)
        return receivers

    def clean_bcc(self):
        bcc = self.cleaned_data['bcc']
        bcc_list = []
        for r in bcc:
            user = User.objects.filter(username=r).first()
            if user is None:
                raise ValidationError('user by this username not found')
            bcc_list.append(user)
        return bcc_list

    def clean_cc(self):
        cc = self.cleaned_data['cc']
        cc_list = []
        for r in cc:
            user = User.objects.filter(username=r).first()
            if user is None:
                raise ValidationError('user by this username not found')
            cc_list.append(user)
        return cc_list


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['sender', 'subject', 'body', 'file', 'action']
        file = forms.BooleanField(widget=RadioSelect(choices=[(True, 'Yes'),
                                                              (False, 'No')]))
