from django.db import models
from django.utils import timezone

class Ticket(models.Model):
    title = models.CharField('Ticket title', max_length=120)
    ticket_author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
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

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    comment_author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    comment_text = models.TextField()

    def __str__(self):
        return self.comment_text

class Vote(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ":" + str(self.ticket) + str(self.date)

    class Meta:
        unique_together = ("user", "ticket")