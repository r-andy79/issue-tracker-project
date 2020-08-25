from django.db import models

class BugTicketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ticket_type="bug")


class FeatureTicketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ticket_type="feature")