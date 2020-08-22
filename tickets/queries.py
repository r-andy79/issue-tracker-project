from django.db.models import Q, Sum, Count
from django.db import IntegrityError
from django.utils import timezone
from .models import Ticket, Comment, Vote, Payment

def make_features_query(ticket_type, text=None, sorting_order=None, statuses=None):
    features_query = (
        Ticket.objects
        .filter(ticket_type=ticket_type)
        .annotate(payments_sum=Sum('payment__payment_value'))
    )

    if text:
        features_query = features_query.filter(title__icontains=text)

    if sorting_order:
        features_query = _tickets_order_by(features_query, sorting_order=sorting_order)
    
    if statuses:
        features_query = _ticket_filter_by_statuses(features_query, statuses)
    
    return features_query


def _ticket_filter_by_statuses(query, statuses):
    q_objects = Q()
    for status in statuses:
        q_objects |= Q(ticket_status__contains=status)
    return query.filter(q_objects)
  

def _tickets_order_by(query, sorting_order):
    order_map = { 
        'date_descending': '-created_date', 
        'date_ascending': 'created_date',
        'vote_descending': '-total_votes',
        'vote_ascending': 'total_votes',
        'payment_sum_descending': '-payments_sum',
        'payment_sum_ascending': 'payments_sum',
    }
    return query.order_by(order_map[sorting_order])


def make_bugs_query(ticket_type, text=None, sorting_order=None, statuses=None):
    bugs_query = (
        Ticket.objects
        .filter(ticket_type=ticket_type)
        .annotate(total_votes=Count('vote'))
    )

    if text:
        bugs_query = bugs_query.filter(title__icontains=text)

    if sorting_order:
        bugs_query = _tickets_order_by(bugs_query, sorting_order=sorting_order)
    
    if statuses:
        bugs_query = _ticket_filter_by_statuses(bugs_query, statuses)
    
    return bugs_query