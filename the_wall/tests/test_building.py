from django.test import TestCase

from the_wall.utils import build_wall
from the_wall.models import Section, Ledger


DATA = [
    [21, 25, 28],
    [17],
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
