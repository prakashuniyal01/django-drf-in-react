from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.core.validators import FileExtensionValidator,MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from decimal import Decimal

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    """
    Represents an article category.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Represents a tag that can be assigned to articles.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name='states', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'country']

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'state']

    def __str__(self):
        return f"{self.name}, {self.state.name}, {self.state.country.name}"
    
class Article(models.Model):
    """
    Represents an article in the system.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
    ]

    title = models.TextField()
    subtitle = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles'
    )
    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_articles'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    # Location Fields
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        validators=[MinValueValidator(Decimal('-90.0')), MaxValueValidator(Decimal('90.0'))],
        null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        validators=[MinValueValidator(Decimal('-180.0')), MaxValueValidator(Decimal('180.0'))],
        null=True, blank=True
    )
    
    categories = models.ManyToManyField(
        'Category',
        related_name='articles'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='articles'
    )
    images = models.ManyToManyField(
        'ArticleImage',  # Reference to the ArticleImage model
        related_name='articles_images',  # Changed related_name to avoid conflict
        blank=True  # Allow articles without images
    )
    
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Agreed to terms field (if necessary)
    agreed_to_terms = models.BooleanField(default=False)

    def clean(self):
        # Convert now() to datetime to match the type of publish_date
        if self.publish_date and self.publish_date <= now():
            raise ValidationError('Publish date must be in the future.')

        if not self.agreed_to_terms:
            raise ValidationError('You must agree to the terms.')

        if not self.categories.exists():
            raise ValidationError("At least one category must be selected.")
        if not self.tags.exists():
            raise ValidationError("At least one tag must be selected.")

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.approved_at:
            self.approved_at = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']
# Signal to send an email notification when an article's status changes
@receiver(post_save, sender=Article)
def send_status_change_notification(sender, instance, **kwargs):
    """
    Sends an email notification to the author when the status of an article changes.
    """
    try:
        previous_instance = Article.objects.get(pk=instance.pk)
        if previous_instance.status != instance.status:
            # Send an email notification to the author
            subject = f"Your article status has changed: {instance.title}"
            message = f"Dear {instance.author.full_name},\n\nYour article titled '{instance.title}' status has been updated to {instance.status}."
            recipient_list = [instance.author.email]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    except Article.DoesNotExist:
        pass  # The article is being created for the first time, no previous status exists

class ArticleImage(models.Model):
    """
    Represents an image related to an article.
    """
    article = models.ForeignKey(
        'Article',
        related_name='article_images',  # Changed related_name to avoid conflict
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='articles/images/', 
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        ]
    )
    order = models.PositiveIntegerField(default=0, help_text="Order in which the images appear.")
    
    def __str__(self):
        return f"Image for {self.article.title}"

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.order:
            # Get the maximum order value for the article and increment by 1
            max_order = ArticleImage.objects.filter(article=self.article).aggregate(models.Max('order'))['order__max']
            self.order = (max_order or 0) + 1
        super().save(*args, **kwargs)



class Comment(models.Model):
    """
    Represents a comment on an article.
    """
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Automatically set `edited` if the content is modified.
        """
        if self.pk:
            original = Comment.objects.get(pk=self.pk)
            if original.content != self.content:
                self.edited = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"


class Like(models.Model):
    """
    Represents a like on an article or comment.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    comment = models.ForeignKey('Comment', null=True, blank=True, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Enforce unique constraints for likes on either an article or a comment.
        """
        if self.article and self.comment:
            raise ValueError("A like cannot be linked to both an article and a comment.")
        
        if self.article:
            if Like.objects.filter(user=self.user, article=self.article).exists():
                raise ValueError("You have already liked this article.")
        
        if self.comment:
            if Like.objects.filter(user=self.user, comment=self.comment).exists():
                raise ValueError("You have already liked this comment.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        if self.comment:
            return f"Like by {self.user} on Comment {self.comment.id}"
        return f"Like by {self.user} on Article {self.article.id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'article'],
                condition=models.Q(comment=None),
                name='unique_article_like'
            ),
            models.UniqueConstraint(
                fields=['user', 'comment'],
                name='unique_comment_like'
            )
        ]
