from datetime import datetime
from unittest import skip

from django.test import TestCase
from django.urls import reverse

from the_wall.entities import UnfinishedSection
from the_wall.models import Section
from the_wall.use_cases import build_wall


def generate_data(profiles: int = 100, sections: int = 2000) -> list[UnfinishedSection]:
    result = []
    for i in range(profiles):
        for j in range(sections):
            result.append(UnfinishedSection(
                height=5 + j % 20,
                profile=i + 1,
                order=j + 1
            ))
    return result


class PerformanceTest(TestCase):

    def setUp(self) -> None:
        data = generate_data()
        build_wall(data)

    @skip
    def test_total(self):
        self.assertEqual(Section.objects.count(), 200000)
        url = reverse("total_cost")
        start = datetime.now()
        response = self.client.get(url)
        end = datetime.now()
        duration = (end - start).seconds

        self.assertEqual(response.json(), {"day": None, "cost": 1148550000000})
        self.assertLess(duration, 1)
