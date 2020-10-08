from django.urls import path
from . import views

urlpatterns = [
    path('shorten/', views.ShortenAPIView.as_view(), name='shorten'),
    path('r/<slug:short>/', views.URLAPIView.as_view(), name='get-url'),
]