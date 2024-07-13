from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('articles',views.ArticleViewset)
router.register('ratings',views.RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]



