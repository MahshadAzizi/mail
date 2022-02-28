from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *


# class NewAmail(LoginRequiredMixin, SuccessMessageMixin, View):
#     success_message = "%(subject)s created successfully"
#
#     form_class = NewAmailForm
#     template_name = 'mail/new_amail.html'
#
#     def get(self, request):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             user = Amail.objects.get('sender')
#             sender = user
#             form.save()
#             messages.success(request, self.get_success_message(form.cleaned_data))
#             return redirect('inbox')
#
#         return render(request, self.template_name, {'form': form})


class InboxList(LoginRequiredMixin, ListView):
    """Return list of email inbox"""
    model = Amail
    template_name = 'mail/inbox_list.html'
    ordering = ['-mail_date']

    def get_context_data(self, **kwargs):
        context = super(InboxList, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['receiver'] = user
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Amail.objects.filter(receiver=user).order_by('-mail_date')


class InboxDetail(DetailView):
    """Return detail of inbox"""
    model = Amail
    context_object_name = 'amail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]

        user = get_object_or_404(User, pk=pk)
        receiver = user.amail_receiver.all()

        context['receiver'] = receiver
        # context['user'] = user
        return context


class SentList(LoginRequiredMixin, ListView):
    """Return list of email inbox"""
    model = Amail
    template_name = 'mail/sent_list.html'
    ordering = ['-mail_date']

    def get_context_data(self, **kwargs):
        context = super(SentList, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['sender'] = user
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Amail.objects.filter(senderw=user).order_by('-mail_date')


class SentDetail(DetailView):
    """Return detail of sent"""
    model = Amail
    context_object_name = 'amail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]


# @login_required
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     user = request.user
#     is_liked = Like.objects.filter(user=user, post=post)
#     if request.method == 'POST':
#         form = NewCommentForm(request.POST)
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.post = post
#             data.username = user
#             data.save()
#             return redirect('post-detail', pk=pk)
#     else:
#         form = NewCommentForm()
#     return render(request, 'feed/post_detail.html', {'post': post, 'is_liked': is_liked, 'form': form})


@login_required
def new_amail(request):
    user = request.user
    if request.method == "POST":
        form = NewAmailForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.sender = user
            data.save()
            messages.success(request, f'send mail Successfully')
            return redirect('home')
    else:
        form = NewAmailForm()
    return render(request, 'mail/new_amail.html', {'form': form})
