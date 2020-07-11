from django.db import models
from django.utils import timezone

class Ticket(models.Model):
    title = models.CharField('Ticket title', max_length=120)
    ticket_author = models.CharField(max_length=60)
    description = models.TextField(blank=True)
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