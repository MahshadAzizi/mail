from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from .forms import NewAmailForm, ReplyForm, AddCategoryForm, ForwardForm, AddMailToCategoryForm
from .models import Amail, Category
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
        return Amail.objects.filter(receiver=user, status='send',
                                    trash=False, archive=False).order_by('-mail_date')


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
        return Amail.objects.filter(sender=self.request.user, status='send', trash=False,
                                    archive=False).order_by('-mail_date')


class SentDetail(DetailView):
    """Return detail of sent"""
    model = Amail
    context_object_name = 'mail'
    template_name = 'mail/sent_detail.html'


@login_required
def new_amail(request):
    user = request.user
    if 'send' in request.POST:
        form = NewAmailForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            receiver = form.cleaned_data['receiver']
            bcc = form.cleaned_data['bcc']
            cc = form.cleaned_data['cc']
            file = form.cleaned_data['file']
            signature = form.cleaned_data['signature']
            sender = user
            mail = Amail.objects.create(sender=sender, status='send', file=file, subject=subject, body=body,
                                        signature=signature)
            mail.receiver.add(*receiver)
            mail.receiver.add(*bcc)
            mail.receiver.add(*cc)
            mail.save()

            messages.success(request, 'send mail Successfully')
            return redirect('home')

    elif 'save' in request.POST:
        form = NewAmailForm(request.POST, request.FILES)
        if form.is_valid() is False or form.is_valid() is True:
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            receiver = form.cleaned_data['receiver']
            bcc = form.cleaned_data['bcc']
            cc = form.cleaned_data['cc']
            file = form.cleaned_data['file']
            signature = form.cleaned_data['signature']
            sender = user
            mail = Amail.objects.create(sender=sender, status='draft', file=file, subject=subject, body=body,
                                        signature=signature)
            mail.receiver.add(*receiver)
            mail.receiver.add(*bcc)
            mail.receiver.add(*cc)
            mail.save()

            messages.success(request, 'save mail Successfully')
            return redirect('home')

    else:
        form = NewAmailForm()
    return render(request, 'mail/new_amail.html', {'form': form})


def reply(request, pk):
    if request.method == "GET":
        form = ReplyForm()
        return render(request, 'mail/reply.html', {"form": form})

    if 'send' in request.POST:
        form = ReplyForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            mail = Amail.objects.get(pk=pk)
            receiver = mail.sender
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            signature = form.cleaned_data['signature']
            sender = user
            mail = Amail.objects.create(sender=sender, status='send', file=file, subject=subject, body=body,
                                        signature=signature)
            mail.receiver.add(receiver)
            mail.reply.add(mail.reply)
            mail.save()
            messages.success(request, 'send mail Successfully')
            return redirect('home')
        else:
            form = ReplyForm()
        return render(request, 'mail/reply.html', {'form': form})

    elif 'save' in request.POST:
        form = ReplyForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid() is False or form.is_valid() is True:
            mail = Amail.objects.get(pk=pk)
            receiver = mail.sender
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            signature = form.cleaned_data['signature']
            sender = user
            mail = Amail.objects.create(sender=sender, status='draft', file=file, subject=subject, body=body,
                                        signature=signature)
            mail.receiver.add(receiver)
            mail.reply.add(mail.reply)
            mail.save()
            messages.success(request, 'save mail Successfully')
            return redirect('home')
    else:
        form = ReplyForm()
    return render(request, 'mail/reply.html', {'form': form})


@login_required
def forward_mail(request, pk):
    if request.method == "GET":
        form = ForwardForm()
        return render(request, 'mail/forward.html', {"form": form})

    if 'send' in request.POST:
        form = ForwardForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            mail = Amail.objects.get(pk=pk)
            body = mail.body
            subject = mail.subject
            file = mail.file
            receiver = form.cleaned_data['receiver']
            cc = form.cleaned_data['cc']
            bcc = form.cleaned_data['bcc']
            sender = user
            mail = Amail.objects.create(sender=sender, status='send', body=body, subject=subject, file=file)
            mail.receiver.add(*receiver)
            mail.receiver.add(*cc)
            mail.receiver.add(*bcc)
            mail.save()
            messages.success(request, 'send mail Successfully')
            return redirect('home')
        else:
            form = ReplyForm()
        return render(request, 'mail/reply.html', {'form': form})

    elif 'save' in request.POST:
        form = ForwardForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid() is False or form.is_valid() is True:
            mail = Amail.objects.get(pk=pk)
            body = mail.body
            subject = mail.subject
            file = mail.file
            receiver = form.cleaned_data['receiver']
            cc = form.cleaned_data['cc']
            bcc = form.cleaned_data['bcc']
            sender = user
            mail = Amail.objects.create(sender=sender, status='send', body=body, subject=subject, file=file)
            mail.receiver.add(*receiver)
            mail.receiver.add(*cc)
            mail.receiver.add(*bcc)
            mail.save()
            messages.success(request, 'save mail Successfully')
            return redirect('home')
    else:
        form = ForwardForm()
    return render(request, 'mail/forward.html', {'form': form})


@login_required
def add_category_mail(request, pk):
    user = request.user
    if request.method == 'GET':
        form = AddMailToCategoryForm()
        return render(request, 'mail/add_category_mail.html', {'form': form})
    elif request.method == 'POST':
        form = AddMailToCategoryForm(request.POST)
        if form.is_valid():
            mail = Amail.objects.get(pk=pk)
            category = form.cleaned_data['category']
            mail.category = category
            mail.objects.get(*category)
            mail.save()
            return redirect('inbox_list')

        return render(request, 'mail/add_category_mail.html', {'form': form})
    else:
        form = AddMailToCategoryForm()
        return render(request, 'mail/add_category_mail.html', {'form': form})


class AddCategory(LoginRequiredMixin, FormView):
    form_class = AddCategoryForm
    template_name = 'mail/add_category.html'
    success_url = 'category_list'

    def form_valid(self, form):
        form.save()
        return redirect('category_list')


class CategoryList(LoginRequiredMixin, ListView):
    """Return list of email category"""
    model = Category
    template_name = 'mail/category_list.html'
    context_object_name = 'all_category'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Category.objects.filter(owner=user)


class CategoryDetail(LoginRequiredMixin, View):
    """Return detail of category"""
    model = Amail
    context_object_name = 'category'
    template_name = 'mail/category_detail.html'

    def get(self, request, pk):
        name = Category.objects.get(pk=pk)
        all_category = Amail.objects.filter(category=name)
        return render(request, self.template_name, {"all_category": all_category})


@login_required
def archive_mail(request, pk):
    mail = Amail.objects.get(pk=pk)
    mail.archive = True
    mail.save()
    return redirect('inbox_list')


@login_required
def trash_mail(request, pk):
    mail = Amail.objects.get(pk=pk)
    mail.archive = True
    mail.save()
    return redirect('inbox_list')


class Archive(LoginRequiredMixin, View):
    """return archive mail"""

    def get(self, request):
        archive_mail = Amail.objects.filter(archive=True)
        return render(request, 'mail/archive.html', {'archive_mail': archive_mail})


class Trash(LoginRequiredMixin, View):
    """return trash mail"""

    def get(self, request):
        trash_mail = Amail.objects.filter(trash=True)
        return render(request, 'mail/trash.html', {'trash_mail': trash_mail})


class DraftList(LoginRequiredMixin, ListView):
    """return draft mail"""
    model = Amail
    template_name = 'mail/draft.html'
    context_object_name = 'draft_mail'
    ordering = ['-mail_date']

    def get_queryset(self):
        return Amail.objects.filter(sender=self.request.user, status='draft', trash=False,
                                    archive=False).order_by('-mail_date')


class DraftDetail(LoginRequiredMixin, DetailView):
    """Return detail of draft"""
    model = Amail
    context_object_name = 'draft'
    template_name = 'mail/draft_detail.html'
