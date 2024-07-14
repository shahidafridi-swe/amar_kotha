from django.shortcuts import render
from rest_framework import  filters, viewsets

from .models import Article, Rating
from .serializers import ArticleSerializer, RatingSerializer
from .permissions import IsEditorOrReadOnly, IsViewerOrReadOnly

from rest_framework.views import APIView
from rest_framework.response import Response

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
    permission_classes = [IsEditorOrReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [ArticleForSpecificCategory]



class RatingApiView(APIView):
    permission_classes = [IsViewerOrReadOnly]
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
            return Response("Rating submitted Successfully")
        return Response(serializer.errors)
    
        