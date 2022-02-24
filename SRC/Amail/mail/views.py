from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *


class NewAmail(LoginRequiredMixin, SuccessMessageMixin, View):
    success_message = "%(subject)s created successfully"

    form_class = NewAmailForm
    template_name = 'mail/new_amail.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST,  request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, self.get_success_message(form.cleaned_data))
            return redirect('inbox')

        return render(request, self.template_name, {'form': form})


class InboxList(ListView):
    """Return list of email inbox"""
    model = Amail
    ordering = ['-mail_date']


class InboxDetail(DetailView):
    """Return detail of inbox"""
    model = Amail
    context_object_name = 'amail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
