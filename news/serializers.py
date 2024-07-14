from rest_framework import serializers

from .models import Article, Category,Rating

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','headline', 'body', 'image', 'editor', 'category','ratings', 'created_at']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [ 'article', 'rating', 'user']
    
    def save(self):
        article = self.validated_data['article']
        rating = self.validated_data['rating']
        user = self.validated_data['user']
        if Rating.objects.filter(user=user, article=article).exists():
            raise serializers.ValidationError("You have already rated this article.")
        rating_obj = Rating(article=article, rating=rating, user=user)
        rating_obj.save()
        return rating_obj
    