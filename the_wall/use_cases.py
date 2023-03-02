from django.conf import settings

from .entities import UnfinishedSection
from .models import Section, Ledger

YARDS_PER_FOOT = 195
FEET_PER_DAY = 1
YARDS_PER_DAY = YARDS_PER_FOOT * FEET_PER_DAY
PRICE_PER_YARD = 1900


def build_wall(unfinished_sections: list[UnfinishedSection]) -> None:
    for section in unfinished_sections:
        build_section(section)


def build_section(data: UnfinishedSection, day: int = 1) -> int:
    days_needed = settings.WALL_HEIGHT - data.height
    days_range = range(day, days_needed + day)
    section = Section.objects.create(profile=data.profile, order=data.order)
    Ledger.objects.bulk_create(Ledger(section=section, day=d) for d in days_range)
    return days_needed


def count_cost_by_day(profile: int | None, day: int | None) -> int:
    """
    Counts how much was spent on building given profile accumulated by a given day
    If profile is None - counts spends for entire wall
    If day is None - counts total spent for all days
    """
    query_set = Ledger.objects.all()
    if profile:
        query_set = query_set.filter(section__profile=profile)
    if day:
        query_set = query_set.filter(day__lte=day)
    return query_set.count() * YARDS_PER_DAY * PRICE_PER_YARD


def count_ice_on_day(profile: int, day: int) -> int:
    """Counts how many yards were built for a given profile on a given day"""
    query_set = Ledger.objects.filter(section__profile=profile, day=day)
    return query_set.count() * YARDS_PER_DAY


def profile_exists(profile: int) -> bool:
    return Section.objects.filter(profile=profile).exists()
