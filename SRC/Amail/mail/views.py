import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import NewAmailForm, ReplyForm, AddCategoryForm, ForwardForm, AddMailToCategoryForm, FilterForm
from .models import Amail, Category
from user.models import User, Signature, ContactBook
from .serializers import ContactsSerializer, EmailSerializer
import logging

logger = logging.getLogger('mail')


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
        logger.error('mail not found')
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
            mail.bcc.add(*bcc)
            mail.cc.add(*cc)
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
            mail.bcc.add(*bcc)
            mail.cc.add(*cc)
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
            mail_1 = Amail.objects.get(pk=pk)
            receiver = mail_1.sender
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            signature = form.cleaned_data['signature']
            sender = user
            mail_2 = Amail.objects.create(sender=sender, status='send', file=file, subject=subject, body=body,
                                          signature=signature)
            mail_2.receiver.add(receiver)
            mail_1.reply.add(mail_2)
            mail_2.save()
            mail_1.save()
            messages.success(request, 'send mail Successfully')
            return redirect('home')
        else:
            form = ReplyForm()
        return render(request, 'mail/reply.html', {'form': form})

    elif 'save' in request.POST:
        form = ReplyForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid() is False or form.is_valid() is True:
            mail_1 = Amail.objects.get(pk=pk)
            receiver = mail_1.sender
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            file = form.cleaned_data['file']
            signature = form.cleaned_data['signature']
            sender = user
            mail_2 = Amail.objects.create(sender=sender, status='draft', file=file, subject=subject, body=body,
                                          signature=signature)
            mail_2.receiver.add(receiver)
            mail_1.reply.add(mail_2)
            mail_2.save()
            mail_1.save()
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
            mail_1 = Amail.objects.get(pk=pk)
            body = mail_1.body
            subject = mail_1.subject
            file = mail_1.file
            signature = mail_1.signature
            receiver = form.cleaned_data['receiver']
            cc = form.cleaned_data['cc']
            bcc = form.cleaned_data['bcc']
            sender = user
            mail = Amail.objects.create(sender=sender, status='send', body=body, subject=subject, file=file,
                                        signature=signature)
            mail.receiver.add(*receiver)
            mail.cc.add(*cc)
            mail.bcc.add(*bcc)
            mail.save()
            messages.success(request, 'send mail Successfully')
            return redirect('home')
        else:
            form = ForwardForm()
        return render(request, 'mail/forward.html', {'form': form})

    elif 'save' in request.POST:
        form = ForwardForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid() is False or form.is_valid() is True:
            mail_1 = Amail.objects.get(pk=pk)
            body = mail_1.body
            subject = mail_1.subject
            file = mail_1.file
            signature = mail_1.signature
            receiver = form.cleaned_data['receiver']
            cc = form.cleaned_data['cc']
            bcc = form.cleaned_data['bcc']
            sender = user
            mail = Amail.objects.create(sender=sender, status='send', body=body, subject=subject, file=file,
                                        signature=signature)
            mail.receiver.add(*receiver)
            mail.cc.add(*cc)
            mail.bcc.add(*bcc)
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
            cat = list(Category.objects.filter(name=category[0]))
            mail.category.add(*cat)
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
        user = self.request.user
        owner = user
        name = form.cleaned_data['name']
        cat = Category.objects.create(owner=owner, name=name)
        cat.save()
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
def delete_category(request, pk):
    cat = Category.objects.get(pk=pk)
    cat.delete()
    return redirect('category_list')


@login_required
def archive_mail(request, pk):
    mail = Amail.objects.get(pk=pk)
    mail.archive = True
    mail.save()
    return redirect('inbox_list')


@login_required
def trash_mail(request, pk):
    mail = Amail.objects.get(pk=pk)
    mail.trash = True
    mail.save()
    return redirect('inbox_list')


class ArchiveList(LoginRequiredMixin, ListView):
    """return archive mail"""
    model = Amail
    template_name = 'mail/archive.html'
    context_object_name = 'archive_mail'
    ordering = ['-mail_date']

    def get_queryset(self):
        return Amail.objects.filter(trash=False, archive=True).order_by('-mail_date')


class ArchiveDetail(LoginRequiredMixin, DetailView):
    """Return detail of archive"""
    model = Amail
    context_object_name = 'archive'
    template_name = 'mail/archive_detail.html'


class TrashList(LoginRequiredMixin, ListView):
    """return trash mail"""
    model = Amail
    template_name = 'mail/trash.html'
    context_object_name = 'trash_mail'
    ordering = ['-mail_date']

    def get_queryset(self):
        return Amail.objects.filter(trash=True).order_by('-mail_date')


class TrashDetail(LoginRequiredMixin, DetailView):
    """Return detail of trash"""
    model = Amail
    context_object_name = 'trash'
    template_name = 'mail/trash_detail.html'


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


class FilterEmail(LoginRequiredMixin, View):
    form_class = FilterForm

    def get(self, request):
        form = self.form_class
        return render(request, 'mail/filter.html', {'username': request.user, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            emails = Amail.objects.filter(Q(receiver=request.user) | Q(sender=request.user))
            if cd['sender']:
                try:
                    sender = User.objects.get(username=cd['sender'])
                    emails = emails.filter(user=sender.id)
                except:
                    messages.warning(request, "this user does not exist", 'danger')
                    return redirect('filteremail')
            if cd['subject']:
                emails = emails.filter(Q(subject__icontains=cd['subject']))
            if cd['body']:
                emails = emails.filter(Q(body__icontains=cd['body']))
            if cd['file'] == True:
                emails = emails.filter(~Q(file=''))
            for email in emails:
                if cd['action'] == 'trash':
                    trash = TrashList()
                    trash.get(request, email.id)
                elif cd['action'] == 'archive':
                    archive = ArchiveList()
                    archive.get(request, email.id)
                elif cd['action'] == 'label':
                    label = CategoryList()
                    label.get(request, email.id)
                else:
                    pass
            return render(request, 'mail/show_filter_email.html', {'username': request.user, 'emails': emails})
        return render(request, 'mail/filter.html', {'username': request.user, 'form': form})


class FilterAlpineJs(View):
    def post(self, request):
        text = self.request.POST.get('search', None)
        email_list = []
        if text:
            emails = Amail.objects.filter(Q(receiver=request.user) | Q(sender=request.user))
            if emails is not None:
                emails = emails.filter(Q(subject__icontains=text) | Q(receiver__icontains=text)
                                       | Q(body__icontains=text) | Q(sender__username__icontains=text))
            email_list = [{
                'id': email.id,
                'subject': email.subject,
                'sender': email.sender.username,
                'receiver': email.receiver} for email in emails]

        return HttpResponse(json.dumps({'list': email_list}))


class ContactsApiView(APIView):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        contacts = ContactBook.objects.filter(user=user)
        serializer = ContactsSerializer(contacts, many=True)
        return Response(serializer.data)


class EmailsApiView(APIView):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        emails = Amail.objects.filter(sender=user)
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data)


@login_required
def search_email(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        emails = Amail.objects.filter(
            Q(sender=request.user.pk) | Q(receiver=request.user.pk),
            Q(subject__icontains=search_str) |
            Q(body__icontains=search_str) |
            # Q(emails__category__name=search_str) |
            Q(mail_date__istartswith=search_str)
            # Q(receiver__icontains=search_str) |
            # Q(emails_senderusername_icontains=search_str)
        )
        data = emails.values()
        for email in data:
            email['sender_id'] = User.objects.get(pk=email['sender_id']).username
            email['mail_date'] = email['mail_date'].date()
        return JsonResponse(list(data), safe=False)  # safe let to return a not json response
