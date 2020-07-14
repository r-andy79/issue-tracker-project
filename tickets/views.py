from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Ticket, Comment
from .forms import TicketForm, CommentForm


def tickets_list(request):
    tickets_list = Ticket.objects.all()
    paginator = Paginator(tickets_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        tickets = paginator.page(page)
    except(EmptyPage, InvalidPage):
        tickets = paginator.page(paginator.num_pages)

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
        'tickets_list': tickets_list,
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

