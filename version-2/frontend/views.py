from django.shortcuts import render



# home for public articles views 
def index(request):
    return render(request,'home.html')

# login for users already exist
def login(request):
    return render(request, 'login.html')

# register 
def register(request):
    return render(request, 'register.html')