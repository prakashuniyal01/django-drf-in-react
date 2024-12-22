from django.urls import path
from .views import ArticleViewSet, CategoryViewSet, TagViewSet, ArticleViewSetJournalist, PublishedArticleListView, PublishedArticleDetailView, ArticleListView
from .views import AllArticlesView

article_list = ArticleViewSetJournalist.as_view({
    'get': 'list',
    'post': 'create'
})

article_detail = ArticleViewSetJournalist.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    # published all articles 
    path('articles/published/', PublishedArticleListView.as_view(), name='published-articles'),
    path('articles/published/<int:id>/', PublishedArticleDetailView.as_view(), name='published-article-detail'),
    # admin routes 
    path('articles/admin/', ArticleViewSet.as_view({'get': 'list', 'post': 'create'}), name='article-list-create'),
    path('articles/admin/<int:pk>/', ArticleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='article-detail'),
     # admin Category URLs
    path('categories/admin/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list-create'),
    path('categories/admin/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),

    # Tag URLs
    path('tags/admin/', TagViewSet.as_view({'get': 'list', 'post': 'create'}), name='tag-list-create'),
    path('tags/admin/<int:pk>/', TagViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='tag-detail'),

    
    #journalist and editor routes 
    path('articles/', article_list, name='article-list'),  # Endpoint for listing and creating articles
    path('articles/<int:pk>/', article_detail, name='article-detail'),  # Endpoint for retrieving, updating, or deleting a specific article
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/all/', AllArticlesView.as_view(), name='all-articles'),
]

