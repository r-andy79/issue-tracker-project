from django.urls import path
from . import views

urlpatterns = [
    path('', views.tickets_list, name='tickets_list'),
    path('bugs', views.bugs_list, name='bugs_list'),
    path('features', views.features_list, name='features_list'),
    path('ticket/<int:pk>', views.ticket_detail, name='ticket_detail'),
    path('ticket/<int:pk>/edit/', views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:pk>/delete/', views.delete_ticket, name='delete_ticket'),
    path('ticket/<int:pk>/add_comment/', views.add_comment_to_ticket, name='add_comment'),
    path('ticket/new/', views.ticket_new, name='ticket_new'),
    path('ticket/<int:ticket_id>/user/<int:user_id>/vote', views.ticket_vote, name='ticket_vote'),
    path('ticket/<int:pk>/pay/', views.pay, name='pay'),
    path('config/', views.stripe_config),
]