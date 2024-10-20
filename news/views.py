from django.shortcuts import render
from rest_framework import  filters, viewsets, status

from .models import Article, Rating, Category, BreakingNews, Review
from .serializers import ArticleSerializer, RatingSerializer, CategorySerializer, BreakingNewsSerializer, ReviewSerializer
from .permissions import IsEditorOrReadOnly, IsViewerOrReadOnly

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# for email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class ArticleForSpecificCategory(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category_id = request.query_params.get("category_id")
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


class ArticleViewset(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsEditorOrReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [ArticleForSpecificCategory]
    
    def perform_create(self, serializer):
        serializer.save(editor=self.request.user)
    
    
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class RatingApiView(viewsets.ModelViewSet):
    
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data) 
        if serializer.is_valid(): 
            rating = serializer.save()
            
            email_subject = "Rating Submitted"
            email_body = render_to_string('rating_email.html', {'rating':rating})
            email = EmailMultiAlternatives(email_subject, '', to=[rating.user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response({"message": "Rating submitted successfully"})
        return Response(serializer.errors, status=400)
  
    
class ReviewApiView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class BreakingNewsApiView(viewsets.ModelViewSet):
    queryset = BreakingNews.objects.all()
    serializer_class = BreakingNewsSerializer