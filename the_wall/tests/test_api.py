from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from the_wall.models import Section


def days_from_height(height: int) -> str:
    result = ""
    day = 1
    while height < settings.WALL_HEIGHT:
        result += f"{day},"
        height += 1
        day += 1
    return result[:-1]


def create_sections(data: list[list[int]]):
    for i, profile in enumerate(data):
        for j, height in enumerate(profile):
            days_str = days_from_height(int(height))
            section = Section(profile=i+1, order=j+1, building_days_str=days_str)
            section.save()


DATA = [
    [21, 25, 28],
    [17],
    [17, 22, 17, 19, 17],
]


class EndpointsTests(TestCase):

    def setUp(self) -> None:
        create_sections(DATA)

    def test_profile_ice_on_day(self):
        params = [(1, 1, 585), (1, 2, 585), (1, 3, 390), (1, 5, 390), (1, 6, 195), (1, 9, 195), (1, 10, 0)]
        for profile, day, ice_amount in params:
            url = reverse('profile_ice_on_day', args=(profile, day))
            response = self.client.get(url)
            self.assertEqual(response.json(), {"day": day, "ice_amount": ice_amount})

    def test_profile_cost_by_day(self):
        params = [(1, 1, 1111500), (1, 2, 2223000), (1, 3, 2964000), (1, 7, 5187000), (1, 10, 5928000)]
        for profile, day, cost in params:
            url = reverse('profile_cost_by_day', args=(profile, day))
            response = self.client.get(url)
            self.assertEqual(response.json(), {"day": day, "cost": cost})

    def test_total_cost_by_day(self):
        params = [(1, 3334500), (2, 6669000), (3, 9633000), (7, 20748000), (10, 27417000)]
        for day, cost in params:
            url = reverse('total_cost_by_day', args=(day, ))
            response = self.client.get(url)
            self.assertEqual(response.json(), {"day": day, "cost": cost})

    def test_total_cost(self):
        url = reverse('total_cost')
        response = self.client.get(url)
        self.assertEqual(response.json(), {"day": None, "cost": 32233500})
