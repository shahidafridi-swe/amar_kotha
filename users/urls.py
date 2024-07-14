from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('list',views.AccountViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationApiView.as_view(), name="register"),
    path('register_account/', views.AccountRegistrationApiView.as_view(), name="register_account"),
    path('login/', views.UserLoginApiView.as_view(), name="login"),
    path('logout/', views.UserLogoutApiView.as_view(), name="logout"),
    path('activate/<uid64>/<token>/' , views.activateAccount, name="activate"),
    
]
