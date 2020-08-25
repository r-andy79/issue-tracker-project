from django.contrib import admin
from django.db.models import Sum, Count
from .models import Ticket, Comment, Vote, Payment, BugTicket, FeatureTicket

@admin.register(BugTicket)
class TicketBugAdmin(admin.ModelAdmin):
    list_display=['title', 'total_votes']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (
            qs
            .annotate(total_votes=Count("vote"))
            .order_by('-total_votes')
        )
    
    def total_votes(self, ticket):
        return ticket.total_votes

@admin.register(FeatureTicket)
class TicketFeatureAdmin(admin.ModelAdmin):
    list_display=['title', 'payments_sum']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (
            qs
            .annotate(payments_sum=Sum("payment__payment_value"))
            .order_by('-payments_sum')
        )
    
    def payments_sum(self, ticket):
        return ticket.payments_sum

admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Payment)
