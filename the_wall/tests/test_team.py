from django.test import TestCase

from the_wall.entities import UnfinishedSection, BuildingTeam, LedgerRecord


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
        build_data = team.get_buid_data(self._get_section())
        expected_data = [
            LedgerRecord(team_name="1", ice_used=7, day=1),
            LedgerRecord(team_name="1", ice_used=7, day=2),
            LedgerRecord(team_name="1", ice_used=7, day=3),
            LedgerRecord(team_name="1", ice_used=4, day=4),
        ]
        self.assertEqual(build_data, expected_data)
