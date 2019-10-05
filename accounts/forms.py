from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    password1   = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2   = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Sorry, Email already taken!')
        pwrd1 = self.cleaned_data.get('password1')
        pwrd2 = self.cleaned_data.get('password2')
        if pwrd1 and pwrd2 and pwrd1 != pwrd2:
            raise forms.ValidationError('Both passwords must match!')
        return super(UserRegisterForm, self).clean(*args, **kwargs)
