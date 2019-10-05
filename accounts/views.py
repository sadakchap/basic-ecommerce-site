from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from .forms import UserRegisterForm
# Create your views here.

User = get_user_model()

def register(request):
    _next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        usr = form.save(commit=False)
        usrnm = form.cleaned_data.get('username')
        pwrd = form.cleaned_data.get('password2')
        usr.set_password(pwrd)
        usr.save()
        new_usr = authenticate(username=usrnm, password=pwrd)
        if new_usr:
            login(request, new_usr)
            if _next:
                redirect(_next)
            redirect('/')
    return render(request, 'accounts/register.html', {'form': form})