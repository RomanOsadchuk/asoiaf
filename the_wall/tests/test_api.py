from django.test import TestCase
from django.urls import reverse

from the_wall.utils import build_wall


DATA = [
    [21, 25, 28],
    [17],
    [17, 22, 17, 19, 17, 30],
]


class EndpointsTests(TestCase):

    def setUp(self) -> None:
        build_wall(DATA)

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
