from django.urls import path

from .views import news, article

urlpatterns = [
    path('news/<str:id>/<str:slug>/', article),
    path('<str:page>/', news),
]
