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
    ledger_data = team.get_buid_data(section_data)
    Section.save_entities(section_data=section_data, ledger_data=ledger_data)
    return len(ledger_data)


def count_cost_by_day(profile: int | None, day: int | None) -> int:
    ice_used = Ledger.count_ice_by_day(day=day, profile=profile)
    return ice_used * PRICE_PER_YARD


def count_ice_on_day(profile: int, day: int) -> int:
    return Ledger.count_ice_on_day(day=day, profile=profile)


def profile_exists(profile: int) -> bool:
    return Section.check_profile(profile)
