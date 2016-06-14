from django.shortcuts import render, HttpResponse
from django.core.urlresolvers import reverse
from .forms import CustomerForm
from models import Group, CustomerUser, Club
from logic import distribute


def get_param(request, param_name, default_value=None):
    return request.POST.get(param_name, request.GET.get(param_name, default_value))


def distribute_players(request):
    club_title = get_param(request, "club")
    club = Club.objects.filter(title=club_title)
    if club:
        players = CustomerUser.objects.filter(club=club[0])
        distribute(players)
        return HttpResponse("OK")
    return HttpResponse("Doesn't found club")
