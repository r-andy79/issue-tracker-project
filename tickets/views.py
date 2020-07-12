from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def tickets_list(request):
    return render(request, "tickets/tickets_list.html")

