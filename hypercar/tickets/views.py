from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.

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