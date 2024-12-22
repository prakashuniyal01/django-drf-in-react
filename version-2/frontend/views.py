from django.shortcuts import  render, get_object_or_404,redirect
from apps.articles.models import Article  # Import Article model from the journal app

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required



# home for public articles views 
def index(request):
    return render(request,'home.html')

# login for users already exist
def login(request):
    return render(request, 'login.html')

# register 
def register(request):
    return render(request, 'register.html')
#admin
def admin_dash(request):
    return render(request, 'dashboard/admin_dashBoard/admin_dashBoard.html')
def admin_create_user(request):
    return render(request, 'dashboard/admin_dashBoard/Create_user.html')
def admin_manage_user(request):
    return render(request, 'dashboard/admin_dashBoard/manage_users.html')
def admin_published_article(request):
    return render(request, 'dashboard/admin_dashBoard/published_article_admin.html')
# editor dashboard 
def editor_dashboard(request):
    return render(request, 'dashboard/editor.html')
# editor dashboard 
def journalist_dashboard(request):
    return render(request, 'dashboard/journalist.html')

def article_detail(request, article_id):
    # Fetch the article based on the ID, or return a 404 if not found
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'dashboard/Journalist/singleJournalistPage.html', {'article': article})


def create_article(request):
    if request.method == "POST":
        # Extract form data
        title = request.POST.get("title")
        subtitle = request.POST.get("subtitle")
        content = request.POST.get("content")
        categories = request.POST.get("categories")
        tags = request.POST.get("tags")
        image = request.FILES.get("image")

        # Process categories and tags
        categories_list = [category.strip() for category in categories.split(",")]
        tags_list = [tag.strip() for tag in tags.split(",")]

        try:
            # Handle file storage for the image
            fs = FileSystemStorage()
            if image:
                image_name = fs.save(image.name, image)
                image_url = fs.url(image_name)
            else:
                image_url = None

            # Create the article and save it to the database
            article = Article(
                title=title,
                subtitle=subtitle,
                content=content,
                categories=categories_list,
                tags=tags_list,
                image=image_url
            )
            article.save()

            # Redirect to article detail or some other page
            return redirect('dashboard/Journalist/singleJournalistPage.html', article_id=article.id)

        except Exception as e:
            return JsonResponse({"message": f"Error: {str(e)}"}, status=500)

    return render(request, 'dashboard/Journalist/createArticle.html')



def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        # Get the form data
        article.title = request.POST.get("title")
        article.subtitle = request.POST.get("subtitle")
        article.content = request.POST.get("content")
        article.categories = request.POST.get("categories").split(",")
        article.tags = request.POST.get("tags").split(",")
        image = request.FILES.get("image")

        if image:
            fs = FileSystemStorage()
            image_name = fs.save(image.name, image)
            article.image = fs.url(image_name)

        article.save()

        return redirect('article_detail', article_id=article.id)

    return render(request, 'dashboard/Journalist/editPage.html', {'article': article})

def published_article(request):
    return render(request, 'dashboard/editor/published_article.html')
def dashboard(request):
    return render(request, 'dashboard/editor/editor_dashboard.html')
