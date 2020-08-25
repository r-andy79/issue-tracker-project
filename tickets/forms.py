from django import forms
from .models import Ticket, Comment, Payment

class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('title', 'ticket_type', 'description')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment_text', )

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ('payment_value', )

class SearchBugForm(forms.Form):
    text = forms.CharField(max_length=100, required=False)
    ticket_status = forms.MultipleChoiceField(
        choices=Ticket.TICKET_STATUSES, 
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    DATE_SORT_CHOICES = (
        ('', '------'),
        ('O', 'oldest'),
        ('N', 'newest'),
    )
    
    date_sort = forms.ChoiceField(
        label="Sort by creation date",
        choices=DATE_SORT_CHOICES, 
        required=False
    )
    
    VOTE_SORT_CHOICES = (
        ('', '------'),
        ('P', 'highest voted'),
        ('U', 'least voted'),
    )
    
    vote_sort = forms.ChoiceField(
        label="Sort by vote count",
        choices=VOTE_SORT_CHOICES,
        required=False
    )

    def get_sorting_order(self):
        vote_sort = self.cleaned_data['vote_sort']
        if vote_sort == 'P':
            return 'vote_descending'
        elif vote_sort == 'U':
            return 'vote_ascending'
        
        date_sort = self.cleaned_data['date_sort']
        if date_sort == 'N':
            return 'date_descending'
        elif date_sort == 'O':
            return 'date_ascending'

        return 'vote_descending'

class SearchFeatureForm(forms.Form):
    text = forms.CharField(max_length=100, required=False)
    ticket_status = forms.MultipleChoiceField(
        choices=Ticket.TICKET_STATUSES, 
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    DATE_SORT_CHOICES = (
        ('', '------'),
        ('O', 'oldest'),
        ('N', 'newest'),
    )
    
    date_sort = forms.ChoiceField(
        label="Sort by creation date",
        choices=DATE_SORT_CHOICES, 
        required=False
    )
    
    PAYMENT_SUM_SORT_CHOICES = (
        ('', '------'),
        ('H', 'descending'),
        ('L', 'ascending'),
    )
    
    payment_sum_sort = forms.ChoiceField(
        label="Sort by contributed payments value",
        choices=PAYMENT_SUM_SORT_CHOICES,
        required=False
    )

    def get_sorting_order(self):
        payment_sum_sort = self.cleaned_data['payment_sum_sort']
        if payment_sum_sort == 'H':
            return 'payment_sum_descending'
        elif payment_sum_sort == 'L':
            return 'payment_sum_ascending'
        
        date_sort = self.cleaned_data['date_sort']
        if date_sort == 'N':
            return 'date_descending'
        elif date_sort == 'O':
            return 'date_ascending'

        return 'payment_sum_descending'