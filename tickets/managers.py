from django.db import models
from django.db.models import Sum, Count

class BugTicketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ticket_type="bug")

    def _annotate_total_votes(self):
        return (
            self.get_queryset()
            .annotate(total_votes=Count("vote"))
        )
    
    def get_queryset_for_admin(self):
        return self._annotate_total_votes().order_by('-total_votes')

    def get_queryset_for_user(self):
        return self._annotate_total_votes().order_by('-created_date')[:5]

class FeatureTicketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ticket_type="feature")

    def _annotate_payments_sum(self):
        return (
            self.get_queryset()
            .annotate(payments_sum=Sum("payment__payment_value"))
        )
    
    def get_queryset_for_admin(self):
        return self._annotate_payments_sum().order_by('-payments_sum')

    def get_queryset_for_user(self):
        return self._annotate_payments_sum().order_by('-created_date')[:5]