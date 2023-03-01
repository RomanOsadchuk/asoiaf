from django.core.management.base import BaseCommand
from the_wall.models import Section
from the_wall.utils import build_wall, parse_input_file


class Command(BaseCommand):
    help = "Build the wall from config file"

    def handle(self, *args, **options):
        Section.objects.all().delete()
        input_data = parse_input_file()
        build_wall(input_data)
        self.stdout.write("The wall has been built", ending='\n')
