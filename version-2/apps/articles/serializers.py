from rest_framework import serializers
from .models import Article, Category, Tag, City, State, Country, ArticleImage
import django_filters

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'  # Adjust fields as needed
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']

class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    
    class Meta:
        model = State
        fields = ['name', 'country']

class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer()
    
    class Meta:
        model = City
        fields = ['name', 'state']

class SimplifiedCitySerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='state.name')
    country = serializers.CharField(source='state.country.name')
    
    class Meta:
        model = City
        fields = ['name', 'state', 'country']

class ArticleImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ArticleImage
        fields = ['id', 'image', 'order']
    
    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class ArticleDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    city = SimplifiedCitySerializer(read_only=True)
    images = ArticleImageSerializer(source='article_images', many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'author_name', 'author_email', 'title', 'subtitle', 'content',
            'publish_date', 'status', 'latitude', 'longitude', 'categories',
            'tags', 'city', 'images', 'agreed_to_terms'
        ]

class ArticleSerializer(serializers.ModelSerializer):
    categories_input = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False
    )
    tags_input = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False
    )
    city = serializers.JSONField(write_only=True, required=False)
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'subtitle', 'content', 'publish_date',
            'categories_input', 'tags_input', 'city', 'status', 'latitude',
            'longitude', 'agreed_to_terms', 'images'
        ]
        read_only_fields = ['author']

    def create_or_get_city(self, city_data):
        """Helper method to create or get city instance"""
        if not city_data:
            return None
            
        country_name = city_data['state']['country']['name']
        state_name = city_data['state']['name']
        city_name = city_data['name']

        country, _ = Country.objects.get_or_create(name=country_name)
        state, _ = State.objects.get_or_create(
            name=state_name,
            country=country
        )
        city, _ = City.objects.get_or_create(
            name=city_name,
            state=state
        )
        return city

    def create(self, validated_data):
        # Extract related data
        category_names = validated_data.pop('categories_input', [])
        tag_names = validated_data.pop('tags_input', [])
        city_data = validated_data.pop('city', None)
        images_data = validated_data.pop('images', [])
        
        # Create or get city
        city = self.create_or_get_city(city_data)

        # Create article
        article = Article.objects.create(
            city=city,
            **validated_data
        )

        # Add categories
        for category_name in category_names:
            category, _ = Category.objects.get_or_create(
                name=category_name.lower().strip()
            )
            article.categories.add(category)

        # Add tags
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(
                name=tag_name.lower().strip()
            )
            article.tags.add(tag)

        # Add images
        if images_data:
            for index, image in enumerate(images_data):
                ArticleImage.objects.create(
                    article=article,
                    image=image,
                    order=index
                )

        return article

    def update(self, instance, validated_data):
        # Handle city data first
        city_data = validated_data.pop('city', None)
        if city_data:
            instance.city = self.create_or_get_city(city_data)

        # Handle categories
        category_names = validated_data.pop('categories_input', None)
        if category_names is not None:
            categories = []
            for name in category_names:
                category, _ = Category.objects.get_or_create(name=name.lower().strip())
                categories.append(category)
            instance.categories.set(categories)

        # Handle tags
        tag_names = validated_data.pop('tags_input', None)
        if tag_names is not None:
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name.lower().strip())
                tags.append(tag)
            instance.tags.set(tags)

        # Handle images
        images_data = validated_data.pop('images', None)
        if images_data is not None:
            # Remove old images
            ArticleImage.objects.filter(article=instance).delete()
            # Add new images
            for index, image in enumerate(images_data):
                ArticleImage.objects.create(
                    article=instance,
                    image=image,
                    order=index
                )

        # Update remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
   