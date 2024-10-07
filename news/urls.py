from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('articles',views.ArticleViewset, basename='articles')

router.register('categories',views.CategoryViewset, basename='categories')
router.register('rating',views.RatingApiView, basename='rating')
router.register('review',views.ReviewApiView, basename='review')
router.register('breaking_news',views.BreakingNewsApiView, basename='breaking_news')

urlpatterns = [
    path('', include(router.urls)),
    
]



