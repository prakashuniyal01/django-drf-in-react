from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('published/<int:article_id>/', views.article_detail, name='article_detail'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    # ========================================== admin start ====================================
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin_all_articles/', views.admin_all_articles, name='admin_all_articles'),  # URL for displaying all articles
    path('admin_article/<int:id>/', views.admin_article_detail, name='admin_article_detail'),
    path('admin_article_create/', views.admin_article_create, name='admin_article_create'),
    path('admin_update_profile/', views.admin_update_profile,name='admin_update_profile'),
    path('admin_users_list/', views.admin_users_list, name='admin_users_list'),  # URL for displaying all articles
    path('admin_update_article/', views.admin_update_article, name='admin_update_article'),
    # path('admin_article_create/', views.admin_article_create, name='admin_article_create'),
    # path('admin_update_profile/', views.admin_update_profile,name='admin_update_profile'),
    # ========================================== admin start ====================================
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
    path('journalist_update_profile/', views.journalist_update_profile,name='journalist_update_profile'),
    # ====================================== jounralist end ===========================================
]
