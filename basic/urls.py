from django.urls import path
from basic.views import Index

urlpatterns = [
    path('', Index.as_view()),
]
