from django import forms
from .models import *


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender', 'recovery', 'phone_number',
                  'country', 'birth_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'txt', 'placeholder': 'first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'txt', 'placeholder': 'last_name'}),
            'username': forms.TextInput(attrs={'class': 'txt', 'placeholder': 'username'}),
            'email': forms.TextInput(attrs={
                'class': 'txt', 'placeholder': 'email', 'disabled': True, 'id': 'Email'

            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'txt', 'placeholder': 'phone_number', 'disabled': True, 'id': 'Email'
            }),
            'password': forms.TextInput(attrs={'class': 'txt', 'placeholder': 'password'}),
            'gender': forms.TextInput(attrs={'class': 'txt', 'placeholder': 'gender'}),

            'country': forms.TextInput(attrs={'class': 'txt', 'placeholder': 'country'}),
            'recovery': forms.Select(attrs={'class': 'txt', 'placeholder': 'recovery', 'id': 'recovery'},
                                     choices=RECOVERY),
            'birth_date': forms.TextInput(attrs={'class': 'txt', 'placeholder': 'birth_date'}),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LogInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'txt', 'placeholder': 'username'}),
            'password': forms.TextInput(attrs={'class': 'txt', 'placeholder': 'password'}),
        }


class ForgetPasswordForm(forms.Form):
    recovery = forms.CharField(
        widget=forms.Select(
            choices=RECOVERY, attrs={'class': 'txt', 'placeholder': 'recovery', 'id': 'recovery'}
        )
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'txt', 'placeholder': 'email', 'disabled': True, 'id': 'Email'

    }), required=False)
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'txt', 'placeholder': 'phone_number', 'disabled': True, 'id': 'Phone'
    }), required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user is None:
            ValidationError('کاربری با این مشخصات یافت نشد')
        return user


class ChangePasswordForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'txt', 'placeholder': 'password'
    }))

    re_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'txt', 'placeholder': 'repeat password'
    }))

    def clean_re_password(self):
        re_password = self.cleaned_data.get('re_password')
        password = self.cleaned_data.get('password')

        if re_password != password:
            ValidationError('رمز شما با اون یکی مغایرت دارد')

        return re_password