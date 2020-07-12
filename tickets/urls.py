from django.urls import path
from . import views

urlpatterns = [
    path('', views.tickets_list, name='tickets_list'),
    path('ticket/<int:pk>', views.ticket_detail, name='ticket_detail'),
    path('ticket/<int:pk>/edit/', views.edit_ticket, name='edit_ticket'),
    path('ticket/new/', views.ticket_new, name='ticket_new'),
]