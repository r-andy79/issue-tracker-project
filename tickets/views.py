from django.shortcuts import render, get_object_or_404
from .models import Ticket


def tickets_list(request):
    tickets = Ticket.objects.all()
    context = {
        'tickets': tickets
    }
    return render(request, "tickets/tickets_list.html", context)

def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    context = {
        'ticket': ticket
    }
    return render(request, "tickets/ticket_detail.html", context)

