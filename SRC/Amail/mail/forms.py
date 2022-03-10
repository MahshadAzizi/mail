from django import forms
from django.forms import ValidationError
from .models import Amail, Category
from django_select2.forms import Select2MultipleWidget
from user.models import User


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
    receiver = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'style': 'max-width: 400px;'}
        )
    )
    reply = forms.ModelMultipleChoiceField(
        queryset=Amail.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'style': 'max-width: 400px;'}
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

    def clean_reply(self):
        reply = self.cleaned_data['reply']
        replys = []
        for r in reply:
            mail = Amail.objects.filter(reply=r).first()
            if mail is None:
                raise ValidationError('user by this username not found')
            replys.append(mail)
        return replys


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
