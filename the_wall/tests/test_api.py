from django.test import TestCase
from django.urls import reverse

from the_wall.entities import UnfinishedSection
from the_wall.use_cases import build_wall, build_section


DATA = [
    UnfinishedSection(height=21, profile=1, order=1),
    UnfinishedSection(height=25, profile=1, order=2),
    UnfinishedSection(height=28, profile=1, order=3),
    UnfinishedSection(height=17, profile=2, order=1),
    UnfinishedSection(height=17, profile=3, order=1),
    UnfinishedSection(height=22, profile=3, order=2),
    UnfinishedSection(height=17, profile=3, order=3),
    UnfinishedSection(height=19, profile=3, order=4),
    UnfinishedSection(height=17, profile=3, order=5),
]


class EndpointsTests(TestCase):

    def setUp(self) -> None:
        build_wall(DATA)

    def test_profile_ice_on_day(self):
        params = [(1, 1, 585), (1, 2, 585), (1, 3, 390), (1, 5, 390), (1, 6, 195), (1, 9, 195), (1, 10, 0)]
        for profile, day, ice_amount in params:
            url = reverse("profile_ice_on_day", args=(profile, day))
            response = self.client.get(url)
            self.assertEqual(response.json(), {"day": day, "ice_amount": ice_amount})

    def test_profile_cost_by_day(self):
        params = [(1, 1, 1111500), (1, 2, 2223000), (1, 3, 2964000), (1, 7, 5187000), (1, 10, 5928000)]
        for profile, day, cost in params:
            url = reverse("profile_cost_by_day", args=(profile, day))
            response = self.client.get(url)
            self.assertEqual(response.json(), {"day": day, "cost": cost})

    def test_total_cost_by_day(self):
        params = [(1, 3334500), (2, 6669000), (3, 9633000), (7, 20748000), (10, 27417000)]
        for day, cost in params:
            url = reverse("total_cost_by_day", args=(day, ))
            response = self.client.get(url)
            self.assertEqual(response.json(), {"day": day, "cost": cost})

    def test_total_cost(self):
        url = reverse("total_cost")
        response = self.client.get(url)
        self.assertEqual(response.json(), {"day": None, "cost": 32233500})


class TestBuildingFromLaterDay(TestCase):

    def setUp(self) -> None:
        section = UnfinishedSection(height=27, profile=1, order=1)
        build_section(section, day=11)

    def test_profile_cost_by_day(self):
        params = [(1, 10, 0), (1, 11, 370500), (1, 13, 1111500), (1, 14, 1111500)]
        for profile, day, cost in params:
            url = reverse("profile_cost_by_day", args=(profile, day))
            response = self.client.get(url)
            self.assertEqual(response.json(), {"day": day, "cost": cost})
