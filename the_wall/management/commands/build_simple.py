import os
from django.conf import settings
from django.core.management.base import BaseCommand
from the_wall.models import Section


def build_section(profile: int, order: int, height: int):
    if height >= settings.WALL_HEIGHT:
        return
    building_days_list = range(1, settings.WALL_HEIGHT - height + 1)
    building_days_str = ",".join(str(d) for d in building_days_list)
    section = Section(profile=profile, order=order, building_days_str=building_days_str)
    section.save()


class Command(BaseCommand):
    help = "Build the wall from config file"

    def handle(self, *args, **options):
        Section.objects.all().delete()
        file_path = os.path.join(settings.BASE_DIR, settings.CONFIG_FILE)
        with open(file_path, "r") as conf_file:
            profile = 1
            for line in conf_file.readlines():
                for section_order, height in enumerate(line.split(" ")):
                    # section_order + 1 since 1-based ordering
                    build_section(profile, section_order + 1, int(height))
                profile += 1
        self.stdout.write("The wall has been built", ending='\n')
