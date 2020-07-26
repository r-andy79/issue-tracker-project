from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Ticket, Comment, Vote
from .forms import TicketForm, CommentForm


def tickets_list(request):
    tickets = Ticket.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('tickets_list'))
            
            queries = Q(title__icontains=query) | Q(description__icontains=query)
            tickets = tickets.filter(queries)
            print(tickets)

    bugs = []
    features = []
    for ticket in tickets:
        if ticket.ticket_type == "bug":
            bugs.append(ticket)
        else:
            features.append(ticket)
    bugs_count = len(bugs)
    features_count = len(features)
    context = {
        'tickets': tickets,
        'search_term': query,
        'tickets': tickets,
        'bugs': bugs,
        'features': features,
        'bugs_count': bugs_count,
        'features_count': features_count
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

def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.delete()
    return redirect('tickets_list')

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
