import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse

# home for public articles views 
def index(request):
    # Fetch published articles from API
    # response = requests.get("http://127.0.0.1:8000/articles/articles/published/")
    # articles = response.json().get("results", [])
    return render(request, "home.html")


def article_detail(request, id):
    # Article data fetch from API
    return render(request, "article_detail.html", {"article": id})


def home(request):
    return render(request, "home.html")

# Login page
def login(request):
    return render(request, 'login.html')  # Frontend se login handle hoga

def forgat_password(request):
    return render(request, 'forget_password.html')
# =========================================== admin view start ===================================================
# Admin Dashboard view
def admin_dashboard(request):
    # Only serve the dashboard page, JavaScript will handle the rest
    return render(request, 'admin/dashboard.html')

def admin_all_articles(request):
    return render(request, 'admin/all_articles.html')

def admin_article_detail(request, id):
    return render(request, 'admin/article_detail.html', {'article': id})

def admin_article_create(request):
    return render(request, "admin/create_article.html")

def admin_update_profile(request):
    return render(request, "admin/update_profile.html")
def admin_update_article(request, id):
    return render(request, "admin/article_update.html", {'article': id})
def admin_users_list(request):
    return render(request, "admin/users.html")

def admin_users_create(request):
    return render(request, "admin/user_create.html")

def admin_users_pubilished(request):
    return render(request, "admin/published.html")

def admin_users_panding(request):
    return render(request, "admin/panding.html")
def admin_users_approved(request):
    return render(request, "admin/approved.html")
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
def editor_users_pubilished(request):
    return render(request, "editor/published.html")

def editor_users_panding(request):
    return render(request, "editor/panding.html")
def editor_users_approved(request):
    return render(request, "editor/approved.html")
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
def journalist_update_article(request, id):
    return render(request, "journalist/article_update.html", {'article': id})
def journalist_article_create(request):
    return render(request, "journalist/create_article.html")

def journalist_update_profile(request):
    return render(request, "journalist/update_profile.html")

def journalist_users_pubilished(request):
    return render(request, "journalist/published.html")

def journalist_users_panding(request):
    return render(request, "journalist/panding.html")
def journalist_users_approved(request):
    return render(request, "journalist/approved.html")
# ====================================== jounralist end ===========================================

# Register page
def register(request):
    return render(request, 'register.html')