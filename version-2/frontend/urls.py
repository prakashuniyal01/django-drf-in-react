from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('published/<int:article_id>/', views.article_detail, name='article_detail'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    # ========================================== editor start ====================================
    path('editor-dashboard/', views.editor_dashboard, name='editor-dashboard'),
    path('editor_all_articles/', views.editor_all_articles, name='editor_all_articles'),  # URL for displaying all articles
    path('editor_article/<int:id>/', views.editor_article_detail, name='editor_article_detail'),
    path('editor_update_profile/', views.editor_update_profile,name='editor_update_profile'),
    # ========================================== editor end ====================================
    # ========================================== jounralist start ====================================
    path('journalist-dashboard/', views.journalist_dashboard, name='journalist-dashboard'),
    path('journalist_all_articles/', views.journalist_all_articles, name='journalist_all_articles'),  # URL for displaying all articles
    path('journalist_article/<int:id>/', views.journalist_article_detail, name='journalist_article_detail'),
    path('journalist_article_create/', views.journalist_article_create, name='journalist_article_create'),
    path('journalist_update_profile/', views.journalist_update_profile,name='journalist_update_profile')
    # ====================================== jounralist end ===========================================
]
