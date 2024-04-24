from django.urls import path
from .views import text_mining

urlpatterns = [
    path('text-mining/', text_mining, name='text-mining'),
]
