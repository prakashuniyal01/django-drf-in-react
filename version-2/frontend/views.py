from django.shortcuts import render
import requests


# home for public articles views 
def index(request):
    # Fetch published articles from API
    response = requests.get("http://127.0.0.1:8000/articles/articles/published/")
    articles = response.json().get("results", [])
    return render(request, "home.html", {"articles": articles})

import requests
from django.shortcuts import render

def article_detail(request, article_id):
    # Article data fetch from API
    response = requests.get(f"http://127.0.0.1:8000/articles/articles/published/{article_id}/")
    if response.status_code == 200:
        article = response.json()
    else:
        article = None
    return render(request, "article_detail.html", {"article": article})


def home(request):
    page = request.GET.get("page", 1)
    response = requests.get(f"http://127.0.0.1:8000/articles/articles/published/?page={page}")
    data = response.json()
    return render(request, "home.html", {"articles": data.get("results", []), "next": data.get("next"), "previous": data.get("previous")})

# login for users already exist
def login(request):
    return render(request, 'login.html')

# register 
def register(request):
    return render(request, 'register.html')