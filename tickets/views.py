from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Ticket, Comment
from .forms import TicketForm


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

def ticket_new(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, "tickets/ticket_new.html", {'form': form})


