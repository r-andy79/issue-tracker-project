from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tickets.models import Ticket
from django.http import HttpResponseForbidden

# Create your views here.

@login_required(login_url='account_login')
def profile_view(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user.id == user_id:
        print('prawda')
    else:
        return HttpResponseForbidden()
    username = User.objects.get(username=request.user.username)
    tickets = Ticket.objects.filter(ticket_author=username)
    context = {
        'user': user,
        'tickets': tickets,
    }
    return render(request, "profiles/profile.html", context)