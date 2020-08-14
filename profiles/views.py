from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tickets.models import Ticket, Vote, Payment
from django.http import HttpResponseForbidden

# Create your views here.

@login_required(login_url='account_login')
def profile_view(request, user_id, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    user = User.objects.get(id=user_id)
    if request.user.id == user_id:
        print('prawda')
    else:
        return HttpResponseForbidden()
    username = User.objects.get(username=request.user.username)
    tickets = Ticket.objects.filter(ticket_author=username)
    bugs_to_do = Ticket.objects.filter(ticket_author=username).filter(ticket_type="bug").filter(ticket_status="T")
    bugs_doing = Ticket.objects.filter(ticket_author=username).filter(ticket_type="bug").filter(ticket_status="D")
    features_to_do = Ticket.objects.filter(ticket_author=username).filter(ticket_type="feature").filter(ticket_status="T")
    features_doing = Ticket.objects.filter(ticket_author=username).filter(ticket_type="feature").filter(ticket_status="D")

    context = {
        'user': user,
        'tickets': tickets,
        'bugs_to_do': bugs_to_do,
        'bugs_doing': bugs_doing,
        'features_to_do': features_doing,
        'features_to_do': features_to_do
    }
    return render(request, "profiles/profile.html", context)