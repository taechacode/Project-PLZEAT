from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout
from . import forms
from . import models
from django.views.generic.edit import FormView
from core import mixins

# Create your views here.


def log_out(request):
    logout(request)
    return redirect(reverse("core:login"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "email": "eunchae@naver.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        # user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do success message
    except models.User.DoesNotExist:
        # to do error message
        pass
    return redirect(reverse("core:home"))
