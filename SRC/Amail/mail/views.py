from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .forms import NewAmailForm, ReplyForm
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


def inbox_detail(request, pk):
    mail = Amail.objects.filter(pk=pk).first()

    if mail is None:
        Http404('mail not found')

    reply_mail_dict = dict()
    unchecked = [mail]
    while True:
        check = unchecked.pop(0)
        reply_mail_dict[check.pk] = []
        for item in check.reply.all():
            reply_mail_dict[check.pk].append(item)
            unchecked.append(item)
        if len(unchecked) == 0:
            break

    context = {
        'amail': mail,
        'reply_mail_dict': reply_mail_dict
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


def reply(request, pk):
    if request.method == "GET":
        form = ReplyForm()
        return render(request, 'mail/reply.html', {"form": form})

    if request.method == "POST":
        mail = Amail.objects.filter(pk=pk).first()
        user = request.user
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            receiver = form.cleaned_data['receiver']
            file = form.cleaned_data['file']
            signature = form.cleaned_data['signature']
            reply = form.cleaned_data['reply']
            sender = user
            mail = Amail.objects.create(sender=sender, file=file, subject=subject, body=body, signature=signature)
            mail.receiver.add(*receiver)
            mail.receiver.add(*reply)
            mail.save()
            messages.success(request, 'send mail Successfully')
            return redirect('home')
        else:
            form = ReplyForm()
        return render(request, 'mail/reply.html', {'form': form})
