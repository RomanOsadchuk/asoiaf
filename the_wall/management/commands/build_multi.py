from django.core.management.base import BaseCommand

from the_wall.models import Section
from the_wall.multiprocess_build import build_wall_multiprocess
from the_wall.utils import parse_input_file


class Command(BaseCommand):
    help = "Build the wall from config file"

    def add_arguments(self, parser):
        parser.add_argument("teams_count", type=int)

    def handle(self, *args, **options):
        Section.objects.all().delete()
        teams_count = options["teams_count"]
        unfinished_sections = parse_input_file()
        build_wall_multiprocess(unfinished_sections, teams_count)
        self.stdout.write("The wall has been built", ending='\n')
