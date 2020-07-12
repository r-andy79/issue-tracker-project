from django.urls import path
from . import views

urlpatterns = [
    path('', views.tickets_list, name='tickets_list'),
    path('ticket/<int:pk>', views.ticket_detail, name='ticket_detail'),
]