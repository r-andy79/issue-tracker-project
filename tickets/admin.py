from django.contrib import admin
from django.db.models import Sum, Count
from .models import Ticket, Comment, Vote, Payment, BugTicket, FeatureTicket

@admin.register(BugTicket)
class TicketBugAdmin(admin.ModelAdmin):
    list_display=['title', 'total_votes', 'ticket_author', 'ticket_status', 'created_date']

    def get_queryset(self, request):
        return BugTicket.objects.get_queryset_for_admin()
    
    def total_votes(self, ticket):
        return ticket.total_votes

@admin.register(FeatureTicket)
class TicketFeatureAdmin(admin.ModelAdmin):
    list_display=['title', 'payments_sum', 'ticket_author', 'ticket_status', 'created_date']
    
    def get_queryset(self, request):
        return FeatureTicket.objects.get_queryset_for_admin()
    
    def payments_sum(self, ticket):
        return ticket.payments_sum

admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Payment)
