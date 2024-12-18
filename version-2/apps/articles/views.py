from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from .models import Article
from .serializers import ArticleCreateSerializer, ArticleGetSerializer
from .permissions import IsAdmin, IsJournalist, IsEditor, IsPublishedOrAuthenticated

# View to create articles (Admin and Journalist)
class ArticleCreateView(APIView):
    permission_classes = [IsAuthenticated, IsJournalist]

    def post(self, request):
        try:
            serializer = ArticleCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "An error occurred while creating the article.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to retrieve articles (Everyone can view, only published articles accessible without authentication)
class ArticleRetrieveView(APIView):
    permission_classes = [IsAuthenticated, IsPublishedOrAuthenticated]

    def get(self, request, pk):
        try:
            article = Article.objects.get(id=pk)
            serializer = ArticleGetSerializer(article)
            return Response(serializer.data)

        except Article.DoesNotExist:
            raise NotFound("Article not found.")
        except Exception as e:
            return Response({"detail": "An error occurred while retrieving the article."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to list articles (Admins and Journalists can list all, others can list only published)
class ArticleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Allow Admins and Journalists to list all articles, others can only see published
            if request.user.role == 'admin' or request.user.role == 'journalist':
                articles = Article.objects.all()
            else:
                articles = Article.objects.filter(status='published')

            serializer = ArticleGetSerializer(articles, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"detail": "An error occurred while listing the articles."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to update the article status (Only Editors can do this)
class ArticleStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsEditor]

    def patch(self, request, pk):
        try:
            article = Article.objects.get(id=pk)

            if 'status' not in request.data:
                raise ValidationError("Status is required.")

            article.status = request.data['status']
            article.save()
            return Response({"detail": "Article status updated successfully."}, status=status.HTTP_200_OK)

        except Article.DoesNotExist:
            raise NotFound("Article not found.")
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response({"detail": "You do not have permission to update the status."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"detail": "An error occurred while updating the article status."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

