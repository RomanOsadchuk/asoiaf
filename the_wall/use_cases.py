from django.conf import settings
from django.db.models import F, IntegerField, Sum

from .entities import UnfinishedSection
from .models import Section, CountDaysByDay


YARDS_PER_FOOT = 195
PRICE_PER_YARD = 1900


def build_wall_fast(unfinished_sections: list[UnfinishedSection], batch_size=1000) -> None:
    """Build wall function for tessting performance"""
    sections = []
    for i, data in enumerate(unfinished_sections):
        sections.append(Section(
            profile=data.profile,
            order=data.order,
            start_day=1,
            end_day=settings.WALL_HEIGHT - data.height,
        ))
        if i % batch_size == 0:
            Section.objects.bulk_create(sections)
            sections = []
            print(i)
    Section.objects.bulk_create(sections)


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
    Section.objects.create(
        profile=data.profile,
        order=data.order,
        start_day=day,
        end_day=day + days_needed - 1,
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
    if day:
        query_set = query_set.filter(start_day__lte=day)
        # using custom CountDaysByDay: min(end_day, {day}) - start_day + 1
        days_func = CountDaysByDay(day=day, output_field=IntegerField())
    else:
        days_func = F("end_day") - F("start_day") + 1
    work_days = query_set.aggregate(total=Sum(days_func))["total"] or 0
    return work_days * YARDS_PER_FOOT * PRICE_PER_YARD


def count_ice_on_day(profile: int, day: int) -> int:
    """Counts how many yards were built for a given profile on a given day"""
    query_set = Section.objects.filter(profile=profile, start_day__lte=day, end_day__gte=day)
    return query_set.count() * YARDS_PER_FOOT


def profile_exists(profile: int) -> bool:
    return Section.objects.filter(profile=profile).exists()
