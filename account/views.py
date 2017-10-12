from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def home(request):
    name = "Tracker"
    args = {'name': name}
    return render(request, 'account/home.html', args)


def login(request):
    return render(request, 'account/login.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account/login')
        else:
            return render(request, 'account/signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'account/signup.html', {'form': form})


