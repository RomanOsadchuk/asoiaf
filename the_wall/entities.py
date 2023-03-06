from dataclasses import dataclass

REQUIRED_HEIGHT = 30
DEFAULT_SECTION_AREA = 195  # amount of yards per foot for section
DEFAULT_PRODUCTIVITY = 195  # how many yards team build per day


@dataclass
class UnfinishedSection:
    height: int  # initial height
    profile: int  # order of profile in the wall (started with 1)
    order: int  # order of section in profile (started with 1)
    area: int = DEFAULT_SECTION_AREA  # yards per foot

    @property
    def yards_to_build(self) -> int:
        return (REQUIRED_HEIGHT - self.height) * self.area


@dataclass
class Schedule:
    work_days: int = 5
    rest_days: int = 0

    def is_working_day(self, day: int) -> bool:
        return day % (self.work_days + self.rest_days) < self.work_days


@dataclass
class BuildingTeam:
    name: str
    day: int = 1
    productivity: int = DEFAULT_PRODUCTIVITY  # yards amount team can build per day
    schedule: Schedule = Schedule()

    def get_buid_schedule(self, section: UnfinishedSection) -> dict[int, int]:
        # returned dict keys: days on which team is building
        # returned dict values: ice amount spent on that day
        result = {}
        yards_to_build = section.yards_to_build
        while yards_to_build > 0:
            if self.schedule.is_working_day(self.day):
                result[self.day] = min(self.productivity, yards_to_build)
                yards_to_build -= result[self.day]
            self.day += 1
        return result
