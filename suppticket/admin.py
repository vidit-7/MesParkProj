from django.contrib import admin
from django.urls.base import reverse
from django.utils.html import format_html
from suppticket.models import SupportTicket, SupportMessage

# Register your models here.

class SupportAdmin(admin.ModelAdmin):

    def ticket_chat_link(self, ticketobj):
        # ticket_url = reverse("suppTicketChat", args=[str(ticketobj.disp_slug)])
        ticket_url = reverse("suppTicketConvoAdm", args=[str(ticketobj.disp_slug)])
        return format_html("<a target='_blank' href='{}'>Open ticket chat page</a>", ticket_url)
    
    # list_display = ("id","disp_slug","user","subject","priority_code","ticket_chat_link","booking_sup","ord_sup","status_closed","created_at","closed_at")
    list_display = ("id","user","subject","priority_code","ticket_chat_link","created_at","status_closed","closed_at")


admin.site.register(SupportTicket, SupportAdmin)
admin.site.register(SupportMessage)
