from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Article, Category, Tag
from .serializers import ArticleSerializer, ArticleDetailSerializer,CategorySerializer, TagSerializer
from .permissions import IsAdminUser, IsJournalistOrEditor
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .filter import ArticleFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

class ArticlePagination(PageNumberPagination):
    page_size = 5  # Set the number of items per page
    page_size_query_param = 'page_size'  # Allow clients to override the page size using a query parameter
    max_page_size = 100  # Maximum number of items per page

class AllArticlesView(APIView):
    permission_classes = [IsAuthenticated]  # Optional, adjust as needed

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()  # Fetch all articles
        serializer = ArticleSerializer(articles, many=True)  # Serialize all articles
        return Response(serializer.data)  # Return all articles without pagination
    
# admin crud views 
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = ArticlePagination  # Use the custom pagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ArticleDetailSerializer
        return ArticleSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        """
        Set the author when creating an article.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Update the article and set updated_at timestamp.
        """
        serializer.save(updated_at=timezone.now())

    def perform_destroy(self, instance):
        """
        Hard delete the article.
        """
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        """
        Override the default destroy method to hard delete the article.
        """
        instance = self.get_object()  # Get the instance to delete
        self.perform_destroy(instance)  # Perform the actual deletion
        return Response(status=status.HTTP_204_NO_CONTENT)  # Respond with success
    
# admin categories control
class CategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = ArticlePagination  # Use custom pagination class
    
    def list(self, request):
        # Get all categories
        categories = Category.objects.all()
        
        # Apply pagination
        paginator = self.pagination_class()
        paginated_categories = paginator.paginate_queryset(categories, request)
        
        # Serialize the paginated categories
        serializer = CategorySerializer(paginated_categories, many=True)
        
        # Return the paginated data
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# admin tags control
class TagViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = ArticlePagination  # Use custom pagination class

    def list(self, request):
        # Get all tags
        tags = Tag.objects.all()
        
        # Apply pagination
        paginator = self.pagination_class()
        paginated_tags = paginator.paginate_queryset(tags, request)
        
        # Serialize the paginated tags
        serializer = TagSerializer(paginated_tags, many=True)
        
        # Return the paginated data
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def update(self, request, pk=None):
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# journalist or editor crud
class ArticleViewSetJournalist(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    pagination_class = ArticlePagination
    permission_classes = [IsAuthenticated, IsJournalistOrEditor]

    def get_queryset(self):
        """
        Restrict the queryset based on user role.
        - Journalists see only their own articles.
        - Editors see all articles.
        """
        user = self.request.user
        if user.role == 'journalist':
            return self.queryset.filter(author=user)
        return self.queryset

    def get_serializer_class(self):
        """
        Use different serializers for list/retrieve and create/update actions.
        """
        if self.action in ['list', 'retrieve']:
            return ArticleDetailSerializer
        return ArticleSerializer

    def get_serializer_context(self):
        """
        Add additional context for serializers.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        """
        Journalists can create articles.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Restrict update based on article status and user role.
        """
        article = self.get_object()
        user = self.request.user

        if user.role == 'journalist' and article.status in ['approved', 'published']:
            raise PermissionDenied(
                "You cannot update an article once it's approved or published."
            )

        serializer.save(updated_at=timezone.now())

    def perform_destroy(self, instance):
        """
        Restrict delete operations:
        - Journalists cannot delete published articles.
        - Editors can delete any article.
        """
        user = self.request.user
        if user.role == 'journalist' and instance.status == 'published':
            raise PermissionDenied("You cannot delete a published article.")
        instance.delete()

    @action(detail=True, methods=['patch'], url_path='change-status', name='Change Status')
    def change_status(self, request, pk=None):
        """
        Editors can change the status of articles.
        """
        user = request.user
        # Restrict this action to editors only
        if user.role != 'editor':
            return Response(
                {"detail": "Only editors can change the status of articles."},
                status=status.HTTP_403_FORBIDDEN
            )

        article = self.get_object()
        new_status = request.data.get('status')
        current_status = article.status

        # Define valid status transitions
        allowed_transitions = {
            'pending': ['approved', 'rejected'],
            'approved': ['published'],
            'published': ['rejected'],
            'rejected': []
        }

        if new_status not in allowed_transitions.get(current_status, []):
            return Response(
                {
                    "detail": f"Cannot change status from '{current_status}' to '{new_status}'."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        article.status = new_status
        article.save()

        return Response(
            {"detail": f"Status changed from '{current_status}' to '{new_status}' successfully."},
            status=status.HTTP_200_OK
        )





# published articles  all users 
class PublishedArticleListView(ListAPIView):
    queryset = Article.objects.filter(status='published')  # Filter only published articles
    serializer_class = ArticleDetailSerializer
    permission_classes = [AllowAny]  # No authentication required
    pagination_class = ArticlePagination  # Use the custom pagination class

class PublishedArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.filter(status='published')  # Filter only published articles
    serializer_class = ArticleDetailSerializer
    permission_classes = [AllowAny]  # No authentication required
    lookup_field = 'id'  # Use 'id' to lookup a specific article
    
    
class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter
    permission_classes = [IsAuthenticated]  # Optional: You can add permissions

    def get_queryset(self):
        """
        Optionally restricts the queryset by filtering against query parameters.
        """
        queryset = super().get_queryset()
        return queryset