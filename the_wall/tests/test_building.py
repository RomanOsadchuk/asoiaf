from django.test import TestCase

from the_wall.entities import UnfinishedSection
from the_wall.models import Section, Ledger
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
        self.assertEqual(Section.objects.filter(profile=1).count(), 3)
        self.assertEqual(Section.objects.filter(profile=2).count(), 1)

        self.assertEqual(Ledger.objects.filter(day=1).count(), 4)
        self.assertEqual(Ledger.objects.filter(day=3).count(), 3)
        self.assertEqual(Ledger.objects.filter(day=6).count(), 2)
        self.assertEqual(Ledger.objects.filter(day=10).count(), 1)
        self.assertEqual(Ledger.objects.filter(day=14).count(), 0)
        self.assertEqual(Ledger.objects.count(), 2 + 5 + 9 + 13)
