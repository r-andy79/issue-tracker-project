from django import forms
from .models import Ticket, Comment, Payment

class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('title', 'ticket_type', 'ticket_author', 'description')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment_author', 'comment_text')

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ('payment_value', )