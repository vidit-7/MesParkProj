from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import SupportTicket, SupportMessage
from .forms import SupportTicketForm

import json

# Create your views here.

@login_required(login_url="centBaseLoginUser")
def suppShowTickets(request):
    allSupportTickets = SupportTicket.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'suppticket/supporthome.html', {'allSupTick':allSupportTickets})

@login_required(login_url="centBaseLoginUser")
def suppCreateTicket(request):
    if request.method == "POST":
        support_form = SupportTicketForm(request.POST, user=request.user)
        if support_form.is_valid():
            supportTicket = support_form.save(commit=False)
            supportTicket.user = request.user
            supportTicket.save()
            return redirect("suppTicketChat", pk=supportTicket.disp_slug)
        else:
            return render(request, 'suppticket/create_ticket.html', {"support_form":support_form})
    support_form = SupportTicketForm(user=request.user)
    context = {"support_form":support_form}
    return render(request, 'suppticket/create_ticket.html', context)

@login_required(login_url="centBaseLoginUser")
def suppTicketChat(request, pk):
    groupedMessages = dict()
    allSupportTickets = SupportTicket.objects.filter(user=request.user).order_by('created_at')
    try:
        suppTicket = SupportTicket.objects.get(disp_slug=pk)
    except:
        return HttpResponse("404 not found")
    
    if(suppTicket.user == request.user):

        ticketMessages = SupportMessage.objects.filter(ticket=suppTicket).order_by('msg_timestamp')

        for ticketMessage in list(ticketMessages):
            msgKeyDate = ticketMessage.msg_timestamp.date() 
            if msgKeyDate in groupedMessages:
                groupedMessages[msgKeyDate].append(ticketMessage)
            else:
                groupedMessages[msgKeyDate] = [ticketMessage]
            
        context = {'allSupTick':allSupportTickets,'currTick': suppTicket,'grpMsgs': groupedMessages}
        return render(request, 'suppticket/convo.html', context)
    return HttpResponse("Forbidden u")

@login_required(login_url='centBaseLoginUser')
def suppSendMess(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ticketId = data['ticketId']
            messageBody = data['messageBody']
            suppTick = SupportTicket.objects.get(id=ticketId)
        except:
            return JsonResponse({'success':False, 'error':'invalid'})
        
        if str(messageBody).strip() == "":
            return JsonResponse({'success':False, 'error':'empty'})
        if not (request.user.is_staff or request.user.is_superuser):
            if request.user != suppTick.user:
                return JsonResponse({'success':False, 'error':'forbidden'})
        
        createdMessage = SupportMessage.objects.create(
            ticket = suppTick,
            user = request.user,
            msg_body = messageBody
        )
        # context = {'success':True, 'msgUser': createdMessage.user, 'msgTick': createdMessage.ticket, 'msgBody': createdMessage.msg_body}
        # messages.success(request, "")
        context = {'success':True, 'createdMsg': messageBody}
        return JsonResponse(context)
    
    else:
        return HttpResponse("Invalid request")

def suppMsgRefresh(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ticketId = data['ticketId']
            lastMsgId = data['lastMsgId']
            suppTick = SupportTicket.objects.get(id=ticketId)
            freshLastMsgId = SupportMessage.objects.filter(ticket=suppTick).order_by('id').last()
        except:
            return JsonResponse({"success": False, "error": "invalid data"})
        
        if suppTick.user != request.user:
            return JsonResponse({"success": False, "error": "Forbidden"})
        
        # print(str(freshLastMsgId.id))
        # print(str(lastMsgId))
        if str(freshLastMsgId.id) == str(lastMsgId):
            return JsonResponse({"success":True, "newMsgRec":False})
        else:
            return JsonResponse({"success":True, "newMsgRec":True})
    
    else:
        return HttpResponse("Invalid request")

@login_required(login_url="centBaseLoginUser")
def suppConvoAdminAll(request, pk):
    if request.user.is_staff or request.user.is_superuser:
        # return HttpResponse("List")
        allSupportTickets = SupportTicket.objects.all().order_by('created_at', '-priority_code')
        try:
            suppTicket = SupportTicket.objects.get(disp_slug=pk)
        except:
            return HttpResponse("ticket not present")
        ticketMessages = SupportMessage.objects.filter(ticket=suppTicket).order_by('msg_timestamp')
        groupedMessages = dict()

        for ticketMessage in list(ticketMessages):
            msgKeyDate = ticketMessage.msg_timestamp.date() 
            if msgKeyDate in groupedMessages:
                groupedMessages[msgKeyDate].append(ticketMessage)
            else:
                groupedMessages[msgKeyDate] = [ticketMessage]

        context = {'allSupTick':allSupportTickets, 'currTick': suppTicket, 'grpMsgs': groupedMessages}
        return render(request, 'suppticket/staff_convo.html', context)

    else:
        return HttpResponse("Forbidden")
