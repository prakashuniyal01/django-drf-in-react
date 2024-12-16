from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

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

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles'
    )
    # Image field with size and type validation
    image = models.ImageField(
        upload_to='articles/images/', 
        null=True, 
        blank=True, 
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        ]
    )

    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_articles'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    categories = models.ManyToManyField(
        'Category',
        related_name='articles'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='articles'
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def clean(self):
        # Custom validation for publish_date
        if self.publish_date and self.publish_date <= now().date():
            raise ValidationError('Publish date must be in the future.')

        # Validation for terms agreement
        if not self.agreed_to_terms:
            raise ValidationError('You must agree to the terms.')

        # Optional: additional validation to ensure the image is under a certain size
        if self.image:
            file_size = self.image.size  # In bytes
            if file_size > 5 * 1024 * 1024:  # 5 MB size limit
                raise ValidationError("Image file size must be less than 5MB.")
            elif file_size < 100 * 1024:  # 100 KB size limit
                raise ValidationError("Image file size must be at least 100KB.")
            
    def save(self, *args, **kwargs):
        """
        Automatically set `approved_at` if the status is 'published'.
        """
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
@receiver(pre_save, sender=Article)
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
        if self.pk and self.content:
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

