import os

from django.conf import settings
from .entities import UnfinishedSection


def parse_input_file() -> list[UnfinishedSection]:
    """
    Adaps data from input file to list of UnfinishedSections
    In input file every line represents one profile
    With section heights separated with space char
    """
    result = []
    file_path = os.path.join(settings.BASE_DIR, settings.CONFIG_FILE)
    with open(file_path, "r") as conf_file:
        for profile_idx, line in enumerate(conf_file.readlines()):
            for section_idx, height in enumerate(line.split(" ")):
                height = int(height)
                if height < 0 or height > settings.WALL_HEIGHT:
                    raise ValueError(f"{height} not in required range")
                result.append(UnfinishedSection(
                    height=height,
                    profile=profile_idx + 1,  # 1-based index in UnfinishedSections
                    order=section_idx + 1
                ))
    return result
