import csv
from django.db.models import Q
from django.http import HttpResponse
from django.utils.encoding import force_str
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView, View, ListView
from .forms import *
from .models import *
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import logging

logger = logging.getLogger('user')


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'user/sign_up.html'
    success_url = 'login'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.username += "@Amail.com"
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your MySite Account'
        message = render_to_string('user/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)

        messages.success(self.request, 'Please Confirm your email to complete registration.')

        return redirect('login')


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Your account have been confirmed.')
            return redirect('login')

        messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
        logger.warning('The confirmation link was invalid, possibly because it has already been used.')
        return redirect('signup')


class LogInView(FormView):
    form_class = LogInForm
    template_name = 'user/login.html'
    success_url = 'home'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'welcome to Amail')
            return redirect('home')
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        if '@Amail.com' not in username:
            username += '@Amail.com'

        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.info(self.request, "You are now logged in as {}".format(user.username))
            return redirect('home')

        messages.error(self.request, "Invalid username or password.")
        logger.error(f'{username} Invalid username or password')
        # logger.warning(f'{username} Invalid username or password')
        return self.render_to_response(self.get_context_data())


@login_required(login_url="login")
def logout_user(request):
    logout(request)
    return redirect(reverse('login'))


class ActivateAccountForgotPassword(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            login(request, user)
            messages.success(request, 'Your account have been confirmed.')
            return redirect('change_password')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('signup')


class ForgotPassword(FormView):
    form_class = ForgetPasswordForm
    template_name = 'user/forgot_password.html'
    success_url = 'change_password'

    def form_valid(self, form):
        user = form.cleaned_data.get('email')
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your MySite Account'
        message = render_to_string('user/forgot_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        messages.success(self.request, 'Please Confirm your email to change password.')
        return redirect(reverse('change_password'))


class ChangePassword(FormView):
    form_class = ChangePasswordForm
    template_name = 'user/change_password.html'
    success_url = 'home'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        if '@Amail.com' not in username:
            username += '@Amail.com'
        user = User.objects.get(username=username)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        return redirect('home')


@login_required(login_url='login')
def home(request):
    return render(request, 'user/home.html')


class AddContact(LoginRequiredMixin, FormView):
    form_class = AddContactForm
    template_name = 'user/add_contact.html'
    success_url = 'contact_list'

    def form_valid(self, form):
        user = self.request.user
        user = user
        birth_date = form.cleaned_data.get('birth_date')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        phone_number = form.cleaned_data.get('phone_number')
        username = form.cleaned_data.get('username')
        if '@Amail.com' not in username:
            username += '@Amail.com'
        if User.objects.filter(username=username).exists():
            contact_book = ContactBook.objects.create(user=user, username=username, first_name=first_name,
                                                      last_name=last_name, email=email, phone_number=phone_number,
                                                      birth_date=birth_date)
            contact_book.save()
            return redirect('contact_list')
        else:
            messages.error(self.request, 'user does not exist!!')
            logger.error(f'username {username} does not exist!!')
            return redirect('contact_list')


class ContactList(LoginRequiredMixin, View):
    """Return list of email contact"""
    model = ContactBook
    template_name = 'user/contact_list.html'

    def get(self, request):
        contacts = ContactBook.objects.filter(user=request.user.id)
        form = SearchForm()
        if 'search' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data['search']
                contacts = contacts.filter(Q(username__icontains=cd) | Q(email__icontains=cd))
        return render(request, self.template_name, {'form': form, 'contacts': contacts})


class ContactDetail(LoginRequiredMixin, DetailView):
    """Return detail of contact"""
    model = ContactBook
    context_object_name = 'contact'
    template_name = 'user/contact_detail.html'


class AddSignature(LoginRequiredMixin, FormView):
    form_class = AddSignatureForm
    template_name = 'user/add_signature.html'
    success_url = 'signature_list'

    def form_valid(self, form):
        user = self.request.user
        owner = user
        signature = form.cleaned_data['signature']
        sig = Signature.objects.create(user=owner, signature=signature)
        sig.save()
        return redirect('signature_list')


class SignatureList(LoginRequiredMixin, ListView):
    """Return list of user signature"""
    model = Signature
    template_name = 'user/signature_list.html'
    context_object_name = 'all_signature'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Signature.objects.filter(user=user)


@login_required
def delete_signature(request, pk):
    sig = Signature.objects.get(pk=pk)
    sig.delete()
    return redirect('signature_list')


def contact_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    writer = csv.writer(response)
    allcontacts = ContactBook.objects.filter(user=request.user)
    writer.writerow(['username', 'first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'user'])
    for venue in allcontacts:
        writer.writerow([venue.username, venue.first_name, venue.last_name, venue.email, venue.phone_number,
                         venue.birth_date, venue.user])
    return response
