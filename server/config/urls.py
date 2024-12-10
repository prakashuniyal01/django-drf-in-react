
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    # path('', lambda request: render(request, 'home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    # path('', include('apps.articles.urls')),
]

