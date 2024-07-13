from rest_framework import serializers

from .models import Article, Category,Rating

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','headline', 'body', 'image', 'editor', 'category','ratings', 'created_at']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'article', 'rating', 'user']
    
    def validate(self, data):
        user = self.context['request'].user
        article = data['article']
        if Rating.objects.filter(user=user, article=article).exists():
            raise serializers.ValidationError("You have already rated this article.")
        return data