from django.test import TestCase

from the_wall.entities import UnfinishedSection, BuildingTeam, Schedule


class EndpointsTests(TestCase):

    @staticmethod
    def _get_section() -> UnfinishedSection:
        return UnfinishedSection(
            profile=1,
            order=1,
            height=25,
            area=5
        )

    def test_build_schedule(self):
        team = BuildingTeam(name="1", productivity=7)
        build_schedule = team.get_buid_schedule(self._get_section())
        expected_schedule = {1: 7, 2: 7, 3: 7, 4: 4}
        self.assertEqual(build_schedule, expected_schedule)

    def test_build_schedule_weekend(self):
        work_schedule = Schedule(work_days=5, rest_days=2)
        team = BuildingTeam(name="1", productivity=4, schedule=work_schedule)
        build_schedule = team.get_buid_schedule(self._get_section())
        # day 5 and 6 - weekend
        expected_schedule = {1: 4, 2: 4, 3: 4, 4: 4, 7: 4, 8: 4, 9: 1}
        self.assertEqual(build_schedule, expected_schedule)
