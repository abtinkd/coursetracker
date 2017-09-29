from django.shortcuts import render, HttpResponse

# Create your views here.
# function based view
def home(request):

    name = "Traker"
    args = {'name': name}
    return render(request, 'account/login.html', args)
