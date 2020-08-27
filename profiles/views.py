from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tickets.models import Ticket, Vote, Payment, Comment

# Create your views here.

@login_required(login_url='account_login')
def profile_view(request):

    tickets = Ticket.objects.filter(ticket_author=request.user)

    context = {
        'user': request.user,
        'tickets': tickets,
    }
    return render(request, "profiles/profile.html", context)