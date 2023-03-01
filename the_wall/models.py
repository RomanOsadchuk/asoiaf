from django.db import models

YARDS_PER_FOOT = 195
FEET_PER_DAY = 1
YARDS_PER_DAY = YARDS_PER_FOOT * FEET_PER_DAY
PRICE_PER_YARD = 1900


class LedgerManager(models.Manager):

    def yards_on_day(self, profile: int, day: int) -> int:
        query_set = self.filter(section__profile=profile, day=day)
        return query_set.count() * YARDS_PER_DAY

    def cost_by_day(self, profile: int = None, day: int = None) -> int:
        query_set = self.filter(section__profile=profile) if profile else self.all()
        if day:
            query_set = query_set.filter(day__lte=day)
        return query_set.count() * YARDS_PER_DAY * PRICE_PER_YARD


class Section(models.Model):
    profile = models.PositiveIntegerField()
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ['profile', 'order']

    def __str__(self) -> str:
        return f"Profile {self.profile} Section {self.order}"


class Ledger(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    day = models.PositiveIntegerField()

    class Meta:
        indexes = [models.Index(fields=['day'])]
        unique_together = ['section', 'day']

    objects = LedgerManager()
