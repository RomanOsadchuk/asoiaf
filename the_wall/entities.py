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
class LedgerRecord:
    day: int
    ice_used: int
    team_name: str


@dataclass
class BuildingTeam:
    name: str
    day: int = 1
    productivity: int = DEFAULT_PRODUCTIVITY  # yards amount team can build per day

    def get_buid_data(self, section: UnfinishedSection) -> list[LedgerRecord]:
        result = []
        yards_to_build = section.yards_to_build
        while yards_to_build > 0:
            ice_used = min(self.productivity, yards_to_build)
            result.append(LedgerRecord(
                team_name=self.name,
                day=self.day,
                ice_used=ice_used,
            ))
            yards_to_build -= ice_used
            self.day += 1
        return result
