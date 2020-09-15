from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
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
    oil_queue = deque()
    tires_queue = deque()
    diag_queue = deque()
    line_of_cars = {"oil": oil_queue, "tires": tires_queue, "diagnostic": diag_queue}
    ticket_num = 1

    # change everything so I just have one dictionary of ticket queues.
    # For wait times, just get the length and subtract the currect request length by one for wait time

    def get(self, request, *args, **kwargs):
        wait = 0
        if "change_oil" in request.path:
            self.line_of_cars["oil"].append(self.ticket_num)
            wait += (len(self.line_of_cars["oil"]) - 1) * 2
        elif "inflate_tires" in request.path:
            self.line_of_cars["tires"].append(self.ticket_num)
            wait += len(self.line_of_cars["oil"]) * 2 + (len(self.line_of_cars["tires"]) - 1) * 5
        elif "diagnostic" in request.path:
            self.line_of_cars["diagnostic"].append(self.ticket_num)
            wait += len(self.line_of_cars["oil"]) * 2 + len(self.line_of_cars["tires"]) * 5 + (len(self.line_of_cars["diagnostic"]) - 1) * 30
        else:
            raise Http404
        context = {"ticket": self.ticket_num, "wait": wait}
        TicketView.ticket_num += 1
        return render(request, "tickets/ticket.html", context)


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "tickets/processing.html", {service: len(q) for service, q in TicketView.line_of_cars.items()})

    def post(self, request, *args, **kwargs):
        ticket = 0
        for service in TicketView.line_of_cars:
            if len(TicketView.line_of_cars[service]):
                ticket = TicketView.line_of_cars[service].popleft()
                break
        return redirect("/processing")

class NextView(View):
    def get(self, request, *args, **kwargs):
        for service in TicketView.line_of_cars:
            if len(TicketView.line_of_cars[service]):
                ticket = TicketView.line_of_cars[service][-1]
                return HttpResponse(f"<div>Next ticket #{ticket}</div>")
        return HttpResponse("<div>Waiting for the next client</div>")