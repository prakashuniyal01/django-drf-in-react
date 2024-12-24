import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse

# home for public articles views 
def index(request):
    # Fetch published articles from API
    response = requests.get("http://127.0.0.1:8000/articles/articles/published/")
    articles = response.json().get("results", [])
    return render(request, "home.html", {"articles": articles})


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

# Login page
def login(request):
    return render(request, 'login.html')  # Frontend se login handle hoga

# Admin Dashboard view
def admin_dashboard(request):
    # Only serve the dashboard page, JavaScript will handle the rest
    return render(request, 'admin/dashboard.html')

# Editor Dashboard view
def editor_dashboard(request):
    return render(request, 'editor/dashboard.html')

# ========================================== jounralist start =====================================================
# Journalist Dashboard view
def journalist_dashboard(request):
    return render(request, 'journalist/dashboard.html')

# View to display all articles (for 'all_articles.html')
def journalist_all_articles(request):
    # articles = Article.objects.all()  # Adjust this query based on your model or filtering criteria
    return render(request, 'journalist/all_articles.html')


def journalist_article_detail(request, id):
    # Construct the API URL dynamically
    url = f'http://127.0.0.1:8000/articles/articles/{id}/'

    # Fetch the article data from the API
    response = requests.get(url)
    if response.status_code == 200:
        article = response.json()
    else:
        article = None  # Handle error case if article not found

    return render(request, 'journalist/article_detail.html', {'article': article})

# ====================================== jounralist end ===========================================

# Register page
def register(request):
    return render(request, 'register.html')