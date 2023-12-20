from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '아이디'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': '성'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': '이름'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': '이메일 주소'}))  # Add this line

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 일치하지 않습니다.")
        if len(password2) < 8:
            raise ValidationError('비밀번호는 최소 8자 이상이어야 합니다.')
        return password2
