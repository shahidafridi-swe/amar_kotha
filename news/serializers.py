from rest_framework import serializers

from .models import Article, Category,Rating

class ArticleSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    image_url = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Article
        fields = ['id', 'headline', 'body', 'image_url', 'editor', 'average_rating', 'category', 'created_at']
        read_only_fields = ['editor', 'average_rating']

    def create(self, validated_data):
        image_url = validated_data.pop('image_url', None)
        
        article = Article.objects.create(**validated_data)
        if image_url:
            article.image_url = image_url  
            article.save()
        return article

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / ratings.count()
        return None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [ 'id','article', 'rating', 'user']
    
    def save(self):
        article = self.validated_data['article']
        rating = self.validated_data['rating']
        user = self.validated_data['user']
        print("rating->>", rating)
        if Rating.objects.filter(user=user, article=article).exists():
            raise serializers.ValidationError("You have already rated this article.")
        rating_obj = Rating(article=article, rating=rating, user=user)
        rating_obj.save()
        print("ratobj",rating_obj)
        return rating_obj
    