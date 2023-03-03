from django.test import TestCase

from the_wall.entities import UnfinishedSection
from the_wall.models import Section
from the_wall.use_cases import build_wall


DATA = [
    UnfinishedSection(height=21, profile=1, order=1),
    UnfinishedSection(height=25, profile=1, order=2),
    UnfinishedSection(height=28, profile=1, order=3),
    UnfinishedSection(height=17, profile=2, order=1),
]


class BuildingTests(TestCase):

    def test_wall_building(self):
        build_wall(DATA)

        self.assertEqual(Section.objects.count(), 4)

        section_1_1 = Section.objects.get(profile=1, order=1)
        self.assertEqual(section_1_1.building_days_list, list(range(1, 10)))

        section_1_2 = Section.objects.get(profile=1, order=2)
        self.assertEqual(section_1_2.building_days_list, list(range(1, 6)))

        section_1_3 = Section.objects.get(profile=1, order=3)
        self.assertEqual(section_1_3.building_days_list, list(range(1, 3)))

        section_2_1 = Section.objects.get(profile=2, order=1)
        self.assertEqual(section_2_1.building_days_list, list(range(1, 14)))
