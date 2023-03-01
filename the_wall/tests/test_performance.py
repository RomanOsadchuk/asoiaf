from datetime import datetime

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
        sections = []
        for j, height in enumerate(profile):
            days_str = days_from_height(int(height))
            section = Section(profile=i+1, order=j+1, building_days_str=days_str)
            sections.append(section)
        Section.objects.bulk_create(sections)


def generate_data(profiles: int = 500, sections: int = 2000) -> list[list[int]]:
    result = []
    for i in range(profiles):
        result.append([5 + j % 20 for j in range(sections)])
    return result


class SomeTests(TestCase):

    def setUp(self) -> None:
        data = generate_data()
        create_sections(data)

    def test_total(self):
        self.assertEqual(Section.objects.count(), 1000000)
        url = reverse('total_cost')
        start = datetime.now()
        response = self.client.get(url)
        end = datetime.now()
        duration = (end - start).seconds

        self.assertEqual(response.json(), {"day": None, "cost": 5742750000000})
        self.assertLess(duration, 11)
