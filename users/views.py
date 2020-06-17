import os
import requests
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from django.contrib import messages
from core import mixins
from . import forms, models

# Create your views here.


def log_out(request):
    logout(request)
    return redirect(reverse("core:login"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        print(email)
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"환영합니다, {user.nickname}님!")
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


#### 소셜 로그인 ####
def kakao_login(request):
    client_id = "e72f124e5a2a725a6aee644df5be6a83"
    redirect_uri = "http://plzeat-demo3.eba-ytmtwqdh.ap-northeast-2.elasticbeanstalk.com/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = "e72f124e5a2a725a6aee644df5be6a83"
        redirect_uri = "http://plzeat-demo3.eba-ytmtwqdh.ap-northeast-2.elasticbeanstalk.com/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email", None)
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        if email is None:
            email = f"{nickname}@plzeatSociaLogin.com"
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(
                    f"Please login with: {user.login_method}.")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                nickname=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save(social_login=True)
            # if profile_image is not None:
            #     photo_request = requests.get(profile_image)
            #     user.avatar.save(
            #         f"{nickname}-avatar", ContentFile(photo_request.content)
            #     )
        messages.success(request, f"환영합니다, {user.nickname}님!")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("core:login"))


def profile_update(request, pk):
    try:
        user = models.User.objects.get(pk=pk)
    except models.User.DoesNotExist:
        messages.error(request, "접근할 수 없습니다")
        return redirect(reverse('core:home'))
    if user != request.user:
        messages.error(request, "접근할 수 없습니다")
        return redirect(reverse('core:home'))
    if request.method == 'POST':
        form = forms.ProfileUpdateForm(
            request.POST, request.FILES, instance=user)
        if form.is_valid():
            user.avatar = form.cleaned_data.get("avatar")
            user.nickname = form.cleaned_data.get("nickname")
            print(form.cleaned_data.get("password") == "")
            if form.cleaned_data.get("password") != "":
                user.set_password(form.cleaned_data.get("password"))
            user.save(udt=True)
            messages.success(request, f"회원정보가 수정되었습니다")
            return redirect(reverse('core:home'))

    else:
        form = forms.ProfileUpdateForm(instance=user)

    return render(request, 'users/profile_update.html', {"form": form})
