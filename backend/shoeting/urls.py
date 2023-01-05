from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
from django.urls import path

urlpatterns = [
    path('join/', JoinView.as_view()),
    path('login/', LoginView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
]
