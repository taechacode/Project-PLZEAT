from django import forms
from . import models
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "이메일 주소"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error(
                    "password", forms.ValidationError("비밀번호가 틀렸습니다"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("계정이 존재하지 않습니다"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("email",)
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "이메일 주소"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 재확인"}),
        label="Confirm Password",
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print(email)
        try:
            user = models.User.objects.get(email=email)
            raise forms.ValidationError("계정이 이미 존재합니다")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다")
        else:
            return password

    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = super().save(commit=False)
        user.username = email
        listed_email = email.split("@")
        user.nickname = listed_email[0]
        user.set_password(password)
        user.save()


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("avatar", "email", "nickname",)
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "이메일", "readonly": "readonly", "class": "update_email"}),
            "nickname": forms.TextInput(attrs={"placeholder": "닉네임"}),
        }
        labels = {
            'email': _('이메일'),
            'nickname': _('닉네임'),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호(선택)"}),
        label='비밀번호',
        required=False,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호 재확인(선택)"}),
        label="비밀번호 재확인",
        required=False,
    )

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다")
        else:
            return password
