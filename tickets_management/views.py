from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tickets.models import Ticket, Vote, Payment, Comment
from django.http import HttpResponseForbidden

# Create your views here.
def test(request):
    tickets = Ticket.objects.filter(ticket_type="bug")|Ticket.objects.filter(ticket_type="feature")
    print(tickets)
    context = {
        'tickets': tickets,
    }
    return render(request, "tickets_management/tickets_panel.html", context)