from django.db import models
from django.contrib.auth.models import User

RATING_CHOICES = (
    (0,0),
    (1,1),
    (2,2),
    (3,3),
    (4,4),
)

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self) -> str:
        return self.name
    
    
class Article(models.Model):
    headline = models.CharField(max_length=255)
    editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    image = models.ImageField(upload_to='news/images/', blank=True, null=True)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='articles', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.headline} - {self.created_at}"


class Rating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('article', 'user')
    
    def __str__(self) -> str:
        return f"{self.article.headline} - Rating: {self.rating}"
