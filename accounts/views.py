from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SettingsForm, TimezoneUserCreationForm


def signup(request):  # TODO test TZ
    """Sign the user up and log them in."""
    if request.user.is_authenticated():  # they're already logged in
        return redirect('/courses')
    form = TimezoneUserCreationForm()
    if request.method == 'POST':
        form = TimezoneUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            auth_login(request, user)
            return redirect('/courses')
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def logout(request):  # TODO redirect somewhere better
    return redirect('/accounts/logout.html')


# TODO submit-less settings page
@login_required
def settings(request):
    """Let the user configure account settings (currently only supports timezone switching)."""
    if request.method == 'POST':
        # TODO implement request.user = request.POST['timezone']
        return redirect('/')
    return render(request, 'accounts/settings.html', {'form': SettingsForm()})


def welcome(request):
    return render(request, 'accounts/welcome.html')
