from django.contrib import admin
from django.db.models import Sum, Count
from .models import Ticket, Comment, Vote, Payment, BugTicket, FeatureTicket
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException

class TicketAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        old_obj = Ticket.objects.get(id=obj.id)
        if old_obj.ticket_status != obj.ticket_status:
            try:
                send_mail(
                    f'{obj.title} - change of status',
                    f'Please be advised that the status of your ticket has changed to {obj.get_ticket_status_display()}',
                    settings.DEFAULT_FROM_EMAIL,
                    [obj.ticket_author.email],
                    fail_silently=False,
                )
            except SMTPException:
                # TODO zmień print na logging
                print('There is something wrong with the email')
            super().save_model(request, obj, form, change)

@admin.register(BugTicket)
class TicketBugAdmin(TicketAdmin):
    list_display=['title', 'total_votes', 'ticket_author', 'ticket_status', 'created_date']

    def get_queryset(self, request):
        return BugTicket.objects.get_queryset_for_admin()
    
    def total_votes(self, ticket):
        return ticket.total_votes

@admin.register(FeatureTicket)
class TicketFeatureAdmin(TicketAdmin):
    list_display=['title', 'payments_sum', 'ticket_author', 'ticket_status', 'created_date']
    
    def get_queryset(self, request):
        return FeatureTicket.objects.get_queryset_for_admin()
    
    def payments_sum(self, ticket):
        return ticket.payments_sum

admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Payment)
