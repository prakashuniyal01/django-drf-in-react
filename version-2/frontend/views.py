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
# =========================================== admin view start ===================================================
# Admin Dashboard view
def admin_dashboard(request):
    # Only serve the dashboard page, JavaScript will handle the rest
    return render(request, 'admin/dashboard.html')

# =========================================== admin view end ===================================================
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# =========================================== editor view start ===================================================
# Editor Dashboard view
def editor_dashboard(request):
    return render(request, 'editor/dashboard.html')

def editor_all_articles(request):
    return render(request, 'editor/all_articles.html')

def editor_article_detail(request, id):
    return render(request, 'editor/article_detail.html', {'article': id})

def editor_update_profile(request):
    return render(request, "editor/update_profile.html")
# =========================================== editor view end ===================================================
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# ========================================== jounralist start =====================================================
# Journalist Dashboard view
def journalist_dashboard(request):
    return render(request, 'journalist/dashboard.html')

# View to display all articles (for 'all_articles.html')
def journalist_all_articles(request):
    return render(request, 'journalist/all_articles.html')


def journalist_article_detail(request, id):
    return render(request, 'journalist/article_detail.html', {'article': id})

def journalist_article_create(request):
    return render(request, "journalist/create_article.html")

def journalist_update_profile(request):
    return render(request, "journalist/update_profile.html")
# ====================================== jounralist end ===========================================

# Register page
def register(request):
    return render(request, 'register.html')