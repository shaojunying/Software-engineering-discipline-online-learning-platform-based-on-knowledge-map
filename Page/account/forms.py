from django import forms
from django.contrib.auth.models import User
 
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='再次输入密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("两次输入的密码不一致")
        return cd['password2']