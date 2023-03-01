import os

from django.conf import settings
from .models import Section, Ledger


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


def ledger_entries_from_height(section: Section, height: int) -> list[Ledger]:
    bulding_days = range(1, settings.WALL_HEIGHT - height + 1)
    return [Ledger(section=section, day=d) for d in bulding_days]


def build_wall(data: list[list[int]]):
    for i, profile in enumerate(data):
        for j, height in enumerate(profile):
            section = Section.objects.create(profile=i+1, order=j+1)
            items = ledger_entries_from_height(section, height)
            Ledger.objects.bulk_create(items)
