from django.conf import settings

from .entities import UnfinishedSection
from .models import Section


def build_wall(unfinished_sections: list[UnfinishedSection]) -> None:
    for section in unfinished_sections:
        build_section(section)


def build_section(data: UnfinishedSection, day: int = 1) -> int:
    """
    Day parameter represents on what day section building is started
    Calculates how many days are needed to complete input section and returns it
    Creates database records for this section and ledger records on what days it bas built
    """
    days_needed = settings.WALL_HEIGHT - data.height
    days_range = range(day, days_needed + day)
    Section.objects.create(
        profile=data.profile,
        order=data.order,
        building_days_str=','.join(str(d) for d in days_range)
    )
    return days_needed


def count_cost_by_day(profile: int | None, day: int | None) -> int:
    """
    Counts how much was spent on building given profile accumulated by a given day
    If profile is None - counts spends for entire wall
    If day is None - counts total spent for all days
    """
    query_set = Section.objects.all()
    if profile:
        query_set = query_set.filter(profile=profile)
    if not day:
        return sum(section.cost_total() for section in query_set)
    return sum(section.cost_by_day(day) for section in query_set)


def count_ice_on_day(profile: int, day: int) -> int:
    """Counts how many yards were built for a given profile on a given day"""
    query_set = Section.objects.filter(profile=profile)
    return sum(section.yards_on_day(day) for section in query_set)


def profile_exists(profile: int) -> bool:
    return Section.objects.filter(profile=profile).exists()
