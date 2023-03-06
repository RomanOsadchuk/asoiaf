from django.db.models import Sum

from .entities import UnfinishedSection, BuildingTeam
from .models import Section, Ledger

PRICE_PER_YARD = 1900


def build_wall(unfinished_sections: list[UnfinishedSection]) -> None:
    for section in unfinished_sections:
        build_section(section)


def build_section(section_data: UnfinishedSection, team: BuildingTeam = None) -> int:
    """
    Creates db records for UnfinishedSection built by BuildingTeam
    returns amount of days spent on building
    """
    team = team or BuildingTeam("default team")
    build_schedule = team.get_buid_schedule(section_data)
    section = Section.create_from_entity(section_data)
    Ledger.objects.bulk_create(
        Ledger(section=section, day=day, team=team.name, ice_used=ice_used)
        for day, ice_used in build_schedule.items()
    )
    return len(build_schedule)


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
    ice_used = query_set.aggregate(total=Sum("ice_used"))["total"] or 0
    return ice_used * PRICE_PER_YARD


def count_ice_on_day(profile: int, day: int) -> int:
    """Counts how many yards were built for a given profile on a given day"""
    query_set = Ledger.objects.filter(section__profile=profile, day=day)
    return query_set.aggregate(total=Sum("ice_used"))["total"] or 0


def profile_exists(profile: int) -> bool:
    return Section.objects.filter(profile=profile).exists()
