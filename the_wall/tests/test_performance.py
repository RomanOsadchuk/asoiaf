from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from the_wall.models import Section
from the_wall.utils import build_wall


def generate_data(profiles: int = 100, sections: int = 2000) -> list[list[int]]:
    result = []
    for i in range(profiles):
        result.append([5 + j % 20 for j in range(sections)])
    return result


class PerformanceTest(TestCase):

    def setUp(self) -> None:
        data = generate_data()
        build_wall(data)

    def test_total(self):
        self.assertEqual(Section.objects.count(), 200000)
        url = reverse('total_cost')
        start = datetime.now()
        response = self.client.get(url)
        end = datetime.now()
        duration = (end - start).seconds

        self.assertEqual(response.json(), {"day": None, "cost": 1148550000000})
        self.assertLess(duration, 1)
