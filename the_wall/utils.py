import os

from django.conf import settings
from .models import Section, Ledger


def build_wall(initial_heights_data: list[list[int]]):
    """
    Creates database records from list[list[int]] data structure
    Integers position i, j in this "matrix" defines profile section
    Their values represent initial height of that section
    """
    for i, profile_data in enumerate(initial_heights_data):
        for j, height in enumerate(profile_data):
            # profiles and sections order starts from 1 - therefore +1
            section = Section.objects.create(profile=i+1, order=j+1)
            items = _ledger_entries_from_height(section, height)
            Ledger.objects.bulk_create(items)


def _ledger_entries_from_height(section: Section, height: int) -> list[Ledger]:
    """
    Creates ledger entries for a given section with given initial height
    Building process starts from day 1, ends when height reachs WALL_HEIGHT
    """
    bulding_days = range(1, settings.WALL_HEIGHT - height + 1)
    return [Ledger(section=section, day=d) for d in bulding_days]


def parse_input_file() -> list[list[int]]:
    result = []
    file_path = os.path.join(settings.BASE_DIR, settings.CONFIG_FILE)
    with open(file_path, "r") as conf_file:
        for line in conf_file.readlines():
            profile = []
            for height in line.split(" "):
                height = int(height)
                if height < 0 or height > settings.WALL_HEIGHT:
                    raise ValueError(f"{height} not in required range")
                profile.append(height)
            result.append(profile)
    return result
