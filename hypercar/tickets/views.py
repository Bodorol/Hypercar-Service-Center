from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from collections import deque


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("<h2>Welcome to the Hypercar Service!</h2>")


class MenuView(View):
    def get(self, request, *args, **kwargs):
        options = [{"path": "change_oil","text": "Change oil"},
                   {"path": "inflate_tires","text": "Inflate tires"},
                   {"path": "diagnostic", "text": "Get diagnostic test"}]
        context = {"options": options}
        return render(request, "tickets/index.html", context)


class TicketView(View):
    line_of_cars = {"oil": 0, "tires": 0, "diagnostic": 0}
    ticket_num = 0
    queue = deque()

    def get(self, request, *args, **kwargs):
        wait = 0
        if len(TicketView.queue) > 0:
            TicketView.line_of_cars[TicketView.queue.popleft()] += 1
        if "change_oil" in request.path:
            TicketView.queue.append("oil")
            ProcessingView.tickets["oil"] += 1
            wait += TicketView.line_of_cars["oil"] * 2
        elif "inflate_tires" in request.path:
            TicketView.queue.append("tires")
            ProcessingView.tickets["tires"] += 1
            wait += TicketView.line_of_cars["oil"] * 2 + TicketView.line_of_cars["tires"] * 5
        elif "diagnostic" in request.path:
            TicketView.queue.append("diagnostic")
            ProcessingView.tickets["diagnostic"] += 1
            wait += TicketView.line_of_cars["oil"] * 2 + TicketView.line_of_cars["tires"] * 5 + TicketView.line_of_cars[
                "diagnostic"] * 30
        else:
            raise Http404
        TicketView.ticket_num += 1
        context = {"ticket": TicketView.ticket_num, "wait": wait}
        return render(request, "tickets/ticket.html", context)


class ProcessingView(View):
    tickets= {"oil": 0, "tires": 0, "diagnostic": 0}

    def get(self, request, *args, **kwargs):
        return render(request, "tickets/processing.html", ProcessingView.tickets)