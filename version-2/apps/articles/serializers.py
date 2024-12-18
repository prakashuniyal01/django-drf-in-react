from rest_framework import serializers
from .models import Article, Category, Tag, City, ArticleImage, Comment, Like

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CitySerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    country_name = serializers.CharField(source='state.country.name', read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'state_name', 'country_name']


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ['id', 'image', 'order']
        
class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_at', 'edited')

class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'article', 'author', 'content', 'replies', 'likes_count', 'edited', 'created_at', 'updated_at')
        read_only_fields = ('author', 'likes_count', 'edited', 'created_at', 'updated_at')
        
# get serializer
class ArticleGetSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)  # Serialize the related categories
    tags = TagSerializer(many=True)  # Serialize the related tags
    author_name = serializers.CharField(source='author.full_name', read_only=True)  # Add author name
    author_email = serializers.EmailField(source='author.email', read_only=True)  # Add author email
    images = ArticleImageSerializer(many=True)  # Serialize the related images
    city = CitySerializer()  # Serialize the city details
    city_name = serializers.CharField(source='city.name', read_only=True)  # Extract city name directly
    state_name = serializers.CharField(source='city.state.name', read_only=True)  # Extract state name from the related city
    country_name = serializers.CharField(source='city.state.country.name', read_only=True)  # Extract country name from the related city
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id','author_name', 'author_email', 'title', 'subtitle', 'content', 'author',
            'publish_date', 'status', 'created_at', 'updated_at',
            'latitude', 'longitude', 'categories', 'tags', 'images',
            'city', 'city_name', 'state_name', 'country_name','comments', 'agreed_to_terms'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

        
# create articles 
class ArticleCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
    categories = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )    # Serialize tags
    city = CitySerializer(read_only=True)  # Serialize city (read-only, optional)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), write_only=True, source='city', required=False  # Make city_id optional
    )
    images = ArticleImageSerializer(many=True, required=False)  # Handle images, optional

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'subtitle', 'content', 
            'publish_date', 'status', 'city', 'city_id', 'latitude','status',
            'longitude', 'categories', 'tags', 'images', 'agreed_to_terms'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        tags = validated_data.pop('tags', [])
        categories = validated_data.pop('categories', [])
        
        # Handle city (get or create)
        city_data = validated_data.pop('city', None)
        city_id = validated_data.get('city_id')
        if city_id:
            city = City.objects.get(id=city_id)  # If city_id is provided, fetch existing city
        elif city_data:
            city, created = City.objects.get_or_create(
                name=city_data['name'],
                state__name=city_data['state_name'],  # Assuming city name and state name are provided
                state__country__name=city_data['country_name']
            )
        else:
            city = None
        
        # Create the article instance
        article = Article.objects.create(**validated_data)
        
        # Handle tags
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            article.tags.add(tag)

        # Handle categories
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            article.categories.add(category)

        # Handle images (only create if provided)
        for image_data in images_data:
            image_url = image_data.get('image')  # Use the image URL or file if available
            ArticleImage.objects.create(article=article, image=image_url, order=image_data.get('order'))

        return article

    def validate(self, data):
        
        # Ensure agreed_to_terms is True
        if not data.get('agreed_to_terms'):
            raise serializers.ValidationError("You must agree to the terms.")
        
        return data

# update 
class ArticlePutPatchSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    images = ArticleImageSerializer(many=True)  # Allow multiple images to be updated
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=False)  # Allow city to be updated if provided

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'subtitle', 'content', 'status', 'categories', 'tags', 'images', 'city', 'latitude', 'longitude', 'agreed_to_terms'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Update categories, tags, and images
        categories_data = validated_data.pop('categories', None)
        tags_data = validated_data.pop('tags', None)
        images_data = validated_data.pop('images', None)

        # Update the article itself
        instance = super().update(instance, validated_data)

        if categories_data:
            instance.categories.set(categories_data)  # Update categories
        if tags_data:
            instance.tags.set(tags_data)  # Update tags
        if images_data:
            # Update or create new images
            for image_data in images_data:
                image_data['article'] = instance  # Attach image to article
                ArticleImage.objects.create(**image_data)

        instance.save()  # Save the updated article
        return instance



# datele articles 
class ArticleDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id']

    def validate(self, data):
        # Ensure that the article exists before attempting deletion
        try:
            article = Article.objects.get(id=data['id'])
        except Article.DoesNotExist:
            raise serializers.ValidationError("Article not found.")
        return data
