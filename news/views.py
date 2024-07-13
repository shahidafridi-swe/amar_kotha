from django.shortcuts import render
from rest_framework import  filters, viewsets

from .models import Article, Rating
from .serializers import ArticleSerializer, RatingSerializer
from .permissions import IsEditorOrReadOnly, IsViewerOrReadOnly


class ArticleForSpecificCategory(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category_id = request.query_params.get("category_id")
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


class ArticleViewset(viewsets.ModelViewSet):
    permission_classes = [IsEditorOrReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [ArticleForSpecificCategory]


class RatingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsViewerOrReadOnly]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
        