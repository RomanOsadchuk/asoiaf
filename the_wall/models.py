from django.db import models

YARDS_PER_FOOT = 195
PRICE_PER_YARD = 1900


class SectionManager(models.Manager):

    def yards_on_day(self, profile: int, day: int) -> int:
        query_set = self.filter(profile=profile)
        return sum(section.yards_on_day(day) for section in query_set)

    def cost_by_day(self, profile: int = None, day: int = None) -> int:
        query_set = self.filter(profile=profile) if profile else self.all()
        if not day:
            return sum(section.cost_total() for section in query_set)
        return sum(section.cost_by_day(day) for section in query_set)


class Section(models.Model):
    profile = models.PositiveIntegerField()
    order = models.PositiveIntegerField()
    building_days_str = models.CharField(max_length=100)

    objects = SectionManager()

    class Meta:
        unique_together = ['profile', 'order']

    def __str__(self) -> str:
        return f"Profile {self.profile} Section {self.order}"

    @property
    def building_days_list(self) -> list[int]:
        return [int(d) for d in self.building_days_str.split(",")]

    def yards_on_day(self, day: int) -> int:
        return YARDS_PER_FOOT if day in self.building_days_list else 0

    def yards_by_day(self, day: int) -> int:
        return sum(YARDS_PER_FOOT for d in self.building_days_list if d <= day)

    def cost_by_day(self, day: int) -> int:
        return PRICE_PER_YARD * self.yards_by_day(day)

    def yards_total(self) -> int:
        return YARDS_PER_FOOT * len(self.building_days_list)

    def cost_total(self) -> int:
        return PRICE_PER_YARD * self.yards_total()
