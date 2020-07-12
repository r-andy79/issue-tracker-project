from django import forms
from .models import Ticket, Comment

class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('title', 'ticket_type', 'ticket_author', 'description')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment_author', 'comment_text')