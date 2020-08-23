from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Count
from tickets.models import Ticket, Vote, Payment, Comment
from django.http import HttpResponseForbidden

# Create your views here.

@login_required(login_url='account_login')
def profile_view(request):

    tickets = Ticket.objects.filter(ticket_author=request.user)
    votes = Vote.objects.filter(user=request.user)

    context = {
        'user': request.user,
        'tickets': tickets,
        'votes': votes,
    }
    return render(request, "profiles/profile.html", context)