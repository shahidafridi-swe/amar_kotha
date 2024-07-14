from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('articles',views.ArticleViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('rating/', views.RatingApiView.as_view(), name="rating"),
    
]



