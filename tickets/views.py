from django.shortcuts import render
from .models import Ticket


def tickets_list(request):
    tickets = Ticket.objects.all()
    context = {
        'tickets': tickets
    }
    return render(request, "tickets/tickets_list.html", context)

