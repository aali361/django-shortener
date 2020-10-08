from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.SignUpAPIView.as_view(), name='sign-up'),
    path('sign-in/', views.SignInAPIView.as_view(), name='sign-in')
]