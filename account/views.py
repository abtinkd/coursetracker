from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# function based view
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
            return redirect('/account')
    else:
     form = UserCreationForm()
     args = {'form' : form}
     return render(request, 'account/signup.html', args)


