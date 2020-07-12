from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Ticket, Comment
from .forms import TicketForm, CommentForm


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
            form.save()
            return redirect('tickets_list')
    else:
        form = TicketForm()
    context = {
        'form': form
    }
    return render(request, "tickets/ticket_new.html", context)

def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('tickets_list')
    form = TicketForm(instance=ticket)
    context = {
        'form': form
    }
    return render(request, "tickets/edit_ticket.html", context)

def add_comment_to_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = CommentForm()
    context = {
        'form': form
    }
    return render(request, "tickets/add_comment_to_ticket.html", context)

