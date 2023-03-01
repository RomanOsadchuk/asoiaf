from django.http import Http404, JsonResponse
from .models import Section, Ledger


def profile_ice_on_day(request, profile: int, day: int) -> JsonResponse:
    """View for ice amount spent on building given profile ON a given day"""
    if not Section.objects.filter(profile=profile).exists():
        raise Http404("Profile does not exist")
    ice_amount = Ledger.objects.yards_on_day(profile=profile, day=day)
    return JsonResponse({"ice_amount": ice_amount, "day": day})


def profile_cost_by_day(request, profile: int, day: int) -> JsonResponse:
    """View for accumulated cost spent on given profile BY a given day"""
    if not Section.objects.filter(profile=profile).exists():
        raise Http404("Profile does not exist")
    cost = Ledger.objects.cost_by_day(profile=profile, day=day)
    return JsonResponse({"day": day, "cost": cost})


def total_cost_by_day(request, day: int) -> JsonResponse:
    """View for accumulated cost spent on the wall BY a given day"""
    cost = Ledger.objects.cost_by_day(profile=None, day=day)
    return JsonResponse({"day": day, "cost": cost})


def total_cost(request) -> JsonResponse:
    """View for total accumulated cost spent on the wall"""
    cost = Ledger.objects.cost_by_day(profile=None, day=None)
    return JsonResponse({"day": None, "cost": cost})
