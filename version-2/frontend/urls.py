from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('users/admin/', views.admin_dash, name='editor'),
    path('users/admin/create/user/', views.admin_create_user, name='admin'),
    path('users/admin/manage/user/', views.admin_manage_user, name='admin'),
    path('users/admin/published/article/', views.admin_published_article, name='admin'),
    path('users/dashboard/editor/', views.editor_dashboard, name='editor'),
    path('users/dashboard/journalist/', views.journalist_dashboard, name='editor'),
    path('users/Journalist/singleJournalistPage/<int:article_id>/', views.article_detail, name='article_detail'),
    path('users/Journalist/articles/create/', views.create_article, name='create_article'),
    path('users/Journalist/articles/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('users/published/', views.published_article, name='published_article'),
    path('users/editor-dashboard/', views.dashboard, name='editor_dashboard'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)