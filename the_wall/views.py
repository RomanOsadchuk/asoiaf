from django.http import Http404, JsonResponse
from .models import Section


def profile_ice_on_day(request, profile: int, day: int) -> JsonResponse:
    if not Section.objects.filter(profile=profile).exists():
        raise Http404("Profile does not exist")
    ice_amount = Section.objects.yards_on_day(profile=profile, day=day)
    result = {"ice_amount": ice_amount, "day": day}
    return JsonResponse(result)


def profile_cost_by_day(request, profile: int, day: int) -> JsonResponse:
    if not Section.objects.filter(profile=profile).exists():
        raise Http404("Profile does not exist")
    cost = Section.objects.cost_by_day(profile=profile, day=day)
    result = {"day": day, "cost": cost}
    return JsonResponse(result)


def total_cost_by_day(request, day: int) -> JsonResponse:
    if not Section.objects.exists():
        raise Http404("The wall does not exist")
    cost = Section.objects.cost_by_day(profile=None, day=day)
    result = {"day": day, "cost": cost}
    return JsonResponse(result)


def total_cost(request) -> JsonResponse:
    if not Section.objects.exists():
        raise Http404("The wall does not exist")
    cost = Section.objects.cost_by_day(profile=None, day=None)
    result = {"day": None, "cost": cost}
    return JsonResponse(result)
