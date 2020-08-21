from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.test, name='test'),
]