from django.db import models
from django.utils import timezone
from .managers import BugTicketManager, FeatureTicketManager

class Ticket(models.Model):
    title = models.CharField('Ticket title', max_length=120)
    ticket_author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    description = models.TextField(blank=True, max_length=2000)
    TICKET_TYPES = [
        ('bug', 'Bug'),
        ('feature', 'Feature')
    ]
    TICKET_STATUSES = [
        ('T', 'To do'),
        ('D', 'Doing'),
        ('C', 'Completed')
    ]

    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPES)
    ticket_status = models.CharField(max_length=1, choices=TICKET_STATUSES, default='T')
    created_date = models.DateTimeField('Date created', default=timezone.now)

    def __str__(self):
        return self.title

class FeatureTicket(Ticket):
    objects=FeatureTicketManager()
    class Meta:
        proxy=True

class BugTicket(Ticket):
    objects=BugTicketManager()
    class Meta:
        proxy=True

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    comment_author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    created_date = models.DateTimeField('Date created', default=timezone.now)
    comment_text = models.TextField(max_length=2000)
    class Meta:
        ordering=['-created_date']

    def __str__(self):
        return self.comment_text

class Vote(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ":" + str(self.ticket) +" " + str(self.date)

    class Meta:
        unique_together = ("user", "ticket")

class Payment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)
    PAYMENT_VALUES = [
        (1, '1'),
        (2, '2'),
        (5, '5'),
        (10, '10')
    ]
    payment_value = models.IntegerField(choices=PAYMENT_VALUES)
    charge_id = models.CharField(max_length=50)
    class Meta:
        ordering=['-date']

    def __str__(self):
        return str(self.user) + ":" + str(self.ticket) + " " + str(self.date) + " " + str(self.payment_value)

    def cents_amount(self):
        return int(self.payment_value) * 100