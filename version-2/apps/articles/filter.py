import django_filters
from .models import Article
from .models import Tag, Category, City, State, Country

class ArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    tags = django_filters.CharFilter(method='filter_tags', label='Tags')
    categories = django_filters.CharFilter(method='filter_categories', label='Categories')
    author_name = django_filters.CharFilter(field_name='author__full_name', lookup_expr='icontains', label='Author Name')
    city = django_filters.CharFilter(method='filter_city', label='City')
    state = django_filters.CharFilter(method='filter_state', label='State')
    country = django_filters.CharFilter(method='filter_country', label='Country')
    publish_date = django_filters.DateFilter(lookup_expr='exact', label='Publish Date')

    class Meta:
        model = Article
        fields = []

    def filter_tags(self, queryset, name, value):
        """Filter articles by tags"""
        tags = value.split(',')
        return queryset.filter(tags__name__in=tags).distinct()

    def filter_categories(self, queryset, name, value):
        """Filter articles by categories"""
        categories = value.split(',')
        return queryset.filter(categories__name__in=categories).distinct()

    def filter_city(self, queryset, name, value):
        """Filter articles by city name"""
        return queryset.filter(city__name__icontains=value)

    def filter_state(self, queryset, name, value):
        """Filter articles by state name"""
        return queryset.filter(city__state__name__icontains=value)

    def filter_country(self, queryset, name, value):
        """Filter articles by country name"""
        return queryset.filter(city__state__country__name__icontains=value)
