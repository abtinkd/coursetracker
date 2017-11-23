from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    """Sign the user up and log them in."""
    if request.user.is_authenticated():  # they're already logged in
        return redirect('/courses')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')  # log in the user
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('/courses')
        else:
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        return render(request, 'accounts/signup.html', {'form': UserCreationForm()})

def startup(request):
        return render(request, 'accounts/welcome.html')



