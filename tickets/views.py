from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Count
from django.db import IntegrityError
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Ticket, Comment, Vote, Payment
from .forms import TicketForm, CommentForm, PaymentForm
from crispy_forms.helper import FormHelper
from django.http import HttpResponseForbidden, JsonResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def tickets_list(request):
    """Displays the five latest tickets on the main site of the application"""
    bugs_list_short = Ticket.objects.filter(ticket_type="bug").annotate(total_votes=Count("vote")).order_by('-created_date')[:5]
    features_list_short = Ticket.objects.filter(ticket_type="feature").annotate(payments_sum=Sum("payment__payment_value")).order_by('-created_date')[:5]
    context = {
        'bugs_list_short': bugs_list_short,
        'features_list_short': features_list_short,
    }
    return render(request, "tickets/tickets_list.html", context)

def sort_list(tickets_list, sorting_order):
    order_map = { 
        'date_descending': '-created_date', 
        'date_ascending': 'created_date',
        'vote_descending': '-total_votes',
        'vote_ascending': 'total_votes',
        'payments_descending': '-payments_sum',
        'payments_ascending': 'payments_sum',
        'to do': 'T',
        'doing': 'D',
        'completed': 'C'
        }
    sorted_tickets_list = tickets_list.order_by(order_map[sorting_order])
    return sorted_tickets_list

def filter_list(tickets_list, request):
    q_objects = Q()
    statuses = request.POST.getlist('status')
    for status in statuses:
        q_objects |= Q(ticket_status__contains=status)
        print(q_objects)
    filtered_tickets_list = tickets_list.filter(q_objects)
    return filtered_tickets_list
    

def bugs_list(request):
    bug = Q(ticket_type="bug")
    bugs_all = Ticket.objects.filter(bug).annotate(total_votes=Count('vote'))
    
    # b_list = Ticket.objects.filter(bug).filter(q_objects)
    
    sorting_order = request.POST['date'] if request.method == "POST" else 'date_ascending'
    ticket_status = request.POST.getlist('status') if request.method == "POST" else ''
    sorted_bugs_list = sort_list(bugs_all, sorting_order)
    filtered_bugs_list = filter_list(sorted_bugs_list, request)
        
    context = {
        'bugs_list': filtered_bugs_list,
        'date_ascending_checked': 'checked' if sorting_order == 'date_ascending' else '',
        'date_descending_checked': 'checked' if sorting_order == 'date_descending' else '',
        'vote_ascending_checked': 'checked' if sorting_order == 'vote_ascending' else '',
        'vote_descending_checked': 'checked' if sorting_order == 'vote_descending' else '',
        'to_do_checked': 'checked' if ticket_status == 'T' else '',
        'doing_checked': 'checked' if ticket_status == 'D' else '',
        'completed_checked': 'checked' if ticket_status == 'C' else '',
    }
    return render(request, "tickets/bugs_list.html", context)

def features_list(request):
    feature = Q(ticket_type="feature")
    features_all = Ticket.objects.filter(feature).annotate(payments_sum=Sum('payment__payment_value'))
    
    sorting_order = request.POST['date'] if request.method == "POST" else 'date_ascending'
    ticket_status = request.POST.getlist('status') if request.method == "POST" else ''

    sorted_features_list = sort_list(features_all, sorting_order)
    filtered_features_list = filter_list(sorted_features_list, request)
        
    context = {
        'features_list': filtered_features_list,
        'date_ascending_checked': 'checked' if sorting_order == 'date_ascending' else '',
        'date_descending_checked': 'checked' if sorting_order == 'date_descending' else '',
        'payments_ascending_checked': 'checked' if sorting_order == 'payments_ascending' else '',
        'payments_descending_checked': 'checked' if sorting_order == 'payments_descending' else '',
    }
    return render(request, "tickets/features_list.html", context)

def ticket_detail(request, pk):
    if request.user.is_authenticated:
        print('zalogowany')
    else:
        print('niezalogowany')

    ticket = get_object_or_404(Ticket, pk=pk)
    votes = Vote.objects.filter(ticket_id=pk)
    payments_sum = Payment.objects.filter(ticket_id=pk).aggregate(Sum('payment_value'))
    payments = Payment.objects.filter(ticket_id=pk)
    is_user = request.user.is_authenticated
    ticket_type = ticket.ticket_type
    is_author = False
    if request.user.id == ticket.ticket_author_id:
        is_author = True
    context = {
        'ticket': ticket,
        'votes': votes,
        'payments_sum': payments_sum,
        'payments': payments,
        'is_author': is_author,
        'is_user': is_user
    }
    return render(request, "tickets/ticket_detail.html", context)

@login_required(login_url='account_login')
def ticket_new(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.ticket_author = request.user
            form.save()
            return redirect('tickets_list')
    else:
        form = TicketForm()
    context = {
        'form': form
    }
    return render(request, "tickets/ticket_new.html", context)

@login_required(login_url='account_login')
def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    # rozpoznanie czy użytkownik jest autorem ticketa (403 albo 406)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', pk)
    form = TicketForm(instance=ticket)
    context = {
        'form': form
    }
    return render(request, "tickets/edit_ticket.html", context)

@login_required(login_url='account_login')
def delete_ticket(request, pk):
    #autor albo deweloperzy
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.delete()
    return redirect('tickets_list')

@login_required(login_url='account_login')
def add_comment_to_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.comment_author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added')
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = CommentForm()
    context = {
        'form': form
    }
    return render(request, "tickets/add_comment_to_ticket.html", context)

@login_required(login_url='account_login')
def ticket_vote(request, ticket_id, user_id):
    user = User.objects.get(id=user_id)
    ticket = Ticket.objects.get(id=ticket_id)
    try:
        vote = Vote(user=user, ticket=ticket, date=timezone.now())
        vote.save()
        messages.success(request, 'Your vote has been added')
    except IntegrityError as e:
        messages.warning(request, 'You can\'t vote twice')
    except:
        pmessages.warning(request, 'Something went wrong')
    return redirect('ticket_detail', pk=ticket.pk)

def pay(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        print('method POST')
        form = PaymentForm(request.POST)
        if form.is_valid(): # akcja is_valid notuje wewnątrz formularza błędy
            # 2. przypadek gdy wszystkie dane są w porządku
            print('form valid')
            # tu tworzę dwa obiekty jakie są wymagane z poziomu stripe
            form.instance.user = request.user
            form.instance.ticket = ticket
            customer = stripe.Customer.create(
                email = request.user.email,
                name = request.user.username,
                source = request.POST['stripeToken']
            )
            charge = stripe.Charge.create(
                customer = customer,
                amount = form.instance.cents_amount(),
                currency  = 'eur',
                description = 'Donation',
                #idempotency_key=
            )
            print(charge)
            form.save()
            return redirect(reverse('success', args=[form.instance.payment_value]))
    else:
        # 1. odpala się tylko przy pierwszym wejściu na stronę
        form = PaymentForm()
    context = {
        'form': form, # gdy mamy POST to tutaj wpada form = PaymentForm(request.POST)
                      # gdy mamy GET wtedy wpada form = PaymentForm()
        'ticket': ticket
    }
    return render(request, "tickets/payment.html", context) # redirect do success

def charge(request):
    amount = 5
    if request.method == 'POST':
        print('Data', request.POST)
    return redirect(reverse('success', args=[amount]))

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

def successMsg(request, args):
    amount = args
    return render(request, 'tickets/success.html', {'amount': amount})