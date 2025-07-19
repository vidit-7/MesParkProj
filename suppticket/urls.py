from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('view-your-tickets/', views.suppShowTickets, name="suppTicketUser"),
    path('create-support-ticket/', views.suppCreateTicket, name="suppTicketCreate"),
    path('support-converstion/<slug:pk>', views.suppTicketChat, name="suppTicketChat"),
    path('add-supmessage/', views.suppSendMess, name="suppSendJsonMessage"),
    path('msgrefresh-polling/', views.suppMsgRefresh, name="suppTickJsonMsgRef"),
    path('support-admin-conversation/<slug:pk>', views.suppConvoAdminAll, name="suppTicketConvoAdm")
]