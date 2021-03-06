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
from .models import Ticket, Comment, Vote, Payment, BugTicket, FeatureTicket
from .forms import TicketForm, CommentForm, PaymentForm, SearchBugForm, SearchFeatureForm
from crispy_forms.helper import FormHelper
from django.http import HttpResponseForbidden, JsonResponse
import stripe
from . import queries as qs

stripe.api_key = settings.STRIPE_SECRET_KEY


def tickets_list(request):
    """Displays five latest tickets on the main site of the application"""
    bugs_list_short = BugTicket.objects.get_queryset_for_user()
    features_list_short = FeatureTicket.objects.get_queryset_for_user()
    context = {
        'bugs_list_short': bugs_list_short,
        'features_list_short': features_list_short,
    }
    return render(request, "tickets/tickets_list.html", context)


def _bugs_list_default(request):
    """returns default results"""
    bugs = list(qs.make_bugs_query(
        ticket_type='bug',
        sorting_order='vote_descending'
    ))
    return render(request, "tickets/bugs_list.html", {
        'form': SearchBugForm(),
        'bugs_list': bugs,
    })


def _bugs_list_invalid(request, form):
    """returns default results and errors inside the form"""
    bugs = list(qs.make_bugs_query(
        ticket_type='bug',
        sorting_order=form.get_sorting_order()
    ))
    return render(request, "tickets/bugs_list.html", {
        'form': form,
        'bugs_list': bugs,
    })


def _bugs_list_valid(request, form):
    """always returns bug tickets by search form"""
    bugs = list(qs.make_bugs_query(
        ticket_type='bug',
        text=form.cleaned_data['search_phrase'],
        sorting_order=form.get_sorting_order(),
        statuses=form.cleaned_data['ticket_status']
    ))
    return render(request, "tickets/bugs_list.html", {
        'form': form,
        'bugs_list': bugs,
    })


def bugs_list(request):
    """returns bug tickets by search form or returns default features"""
    if len(request.GET) == 0:
        return _bugs_list_default(request)
    else:
        form = SearchBugForm(request.GET)
        if form.is_valid():
            return _bugs_list_valid(request, form)
        else:
            return _bugs_list_invalid(request, form)


def _features_list_default(request):
    """returns default results"""
    features = list(qs.make_features_query(
        ticket_type='feature',
        sorting_order='payment_sum_descending'
    ))
    return render(request, "tickets/features_list.html", {
        'form': SearchFeatureForm(),
        'features_list': features,
    })


def _features_list_invalid(request, form):
    """returns default results and errors inside the form"""
    featuress = list(qs.make_features_query(
        ticket_type='feature',
        sorting_order=form.get_sorting_order()
    ))
    return render(request, "tickets/features_list.html", {
        'form': form,
        'features_list': features,
    })


def _features_list_valid(request, form):
    """always returns feature tickets by search form"""
    features = list(qs.make_features_query(
        ticket_type='feature',
        text=form.cleaned_data['search_phrase'],
        sorting_order=form.get_sorting_order(),
        statuses=form.cleaned_data['ticket_status']
    ))
    return render(request, "tickets/features_list.html", {
        'form': form,
        'features_list': features,
    })


def features_list(request):
    """returns feature tickets by search form or returns default features"""
    if len(request.GET) == 0:
        return _features_list_default(request)
    else:
        form = SearchFeatureForm(request.GET)
        if form.is_valid():
            return _features_list_valid(request, form)
        else:
            return _features_list_invalid(request, form)


def ticket_detail(request, pk):
    """Function responsible for display detailed view of a ticket"""
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
    """function responsible for creating new tickets"""
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
    """function responsible for editing tickets"""
    ticket = get_object_or_404(Ticket, pk=pk)
    if not (request.user.id == ticket.ticket_author_id or request.user.is_superuser):
        return HttpResponseForbidden()

    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', pk)
    else:
        form = TicketForm(instance=ticket)
    context = {
        'form': form
    }
    return render(request, "tickets/edit_ticket.html", context)


@login_required(login_url='account_login')
def add_comment_to_ticket(request, pk):
    """function responsible for adding comments to tickets"""
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
    """function responsible for voting on bug tickets"""
    user = User.objects.get(id=user_id)
    ticket = Ticket.objects.get(id=ticket_id)
    try:
        vote = Vote(user=user, ticket=ticket, date=timezone.now())
        vote.save()
        messages.success(request, 'Your vote has been added')
    except IntegrityError as e:
        messages.warning(request, 'You can\'t vote twice')
    return redirect('ticket_detail', pk=ticket.pk)


def pay(request, pk):
    """function allowing users to make payments towards feature tickets"""
    ticket = get_object_or_404(Ticket, pk=pk)
    if not ticket.is_payment_allowed():
        messages.warning(request, 'Payments are no longer accepted')
        return redirect('tickets_list')

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.ticket = ticket
            customer = stripe.Customer.create(
                email=request.user.email,
                name=request.user.username,
                source=request.POST['stripeToken']
            )
            charge = stripe.Charge.create(
                customer=customer,
                amount=form.instance.cents_amount(),
                currency='eur',
                description='Donation',
            )
            form.instance.charge_id = charge.id
            form.save()
            amount = form.instance.payment_value
            messages.success(request, f'Thank you for your payment of %a euro' % amount)
            return redirect(reverse('ticket_detail', args=[pk]))
    else:
        form = PaymentForm()
    context = {
        'form': form,
        'ticket': ticket
    }
    return render(request, "tickets/payment.html", context)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
