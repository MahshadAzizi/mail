from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .forms import NewAmailForm
from .models import Amail
from user.models import User


class InboxList(LoginRequiredMixin, ListView):
    """Return list of email inbox"""
    model = Amail
    template_name = 'mail/inbox_list.html'
    ordering = ['-mail_date']
    context_object_name = 'mails'

    def get_context_data(self, **kwargs):
        context = super(InboxList, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.request.user)
        context['receiver'] = user
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Amail.objects.filter(receiver=user).order_by('-mail_date')


class InboxDetail(DetailView):
    """Return detail of inbox"""
    model = Amail
    context_object_name = 'amail'
    template_name = 'mail/inbox_detail.html'


def inbox_detail(request, mail_pk):
    mail = Amail.objects.filter(pk=mail_pk).first()
    new_mail = []

    while True:
        if mail.reply is not None:
            break
        else:
            new_mail.append(mail)
            mail = mail.reply

    context = {
        'amail': mail
    }
    return render(request, 'mail/inbox_detail.html', context)


class SentList(LoginRequiredMixin, ListView):
    """Return list of email sent"""
    model = Amail
    template_name = 'mail/sent_list.html'
    context_object_name = 'mails'
    ordering = ['-mail_date']

    def get_context_data(self, **kwargs):
        context = super(SentList, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.request.user)
        context['receiver'] = user
        return context

    def get_queryset(self):
        return Amail.objects.filter(sender=self.request.user).order_by('-mail_date')


class SentDetail(DetailView):
    """Return detail of sent"""
    model = Amail
    context_object_name = 'mail'
    template_name = 'mail/sent_detail.html'


@login_required
def new_amail(request):
    user = request.user
    if request.method == "POST":
        form = NewAmailForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            receiver = form.cleaned_data['receiver']
            file = form.cleaned_data['file']
            signature = form.cleaned_data['signature']
            sender = user
            mail = Amail.objects.create(sender=sender, file=file, subject=subject, body=body, signature=signature)
            mail.receiver.add(*receiver)
            mail.save()

            messages.success(request, 'send mail Successfully')
            return redirect('home')
    else:
        form = NewAmailForm()
    return render(request, 'mail/new_amail.html', {'form': form})
