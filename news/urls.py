from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('articles',views.ArticleViewset, basename='articles')

router.register('categories',views.CategoryViewset, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
    path('rating/', views.RatingApiView.as_view(), name="rating"),
    
]



