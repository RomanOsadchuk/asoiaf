from django.db import models

YARDS_PER_FOOT = 195
FEET_PER_DAY = 1
YARDS_PER_DAY = YARDS_PER_FOOT * FEET_PER_DAY
PRICE_PER_YARD = 1900


class LedgerManager(models.Manager):

    def yards_on_day(self, profile: int, day: int) -> int:
        """Counts how many yards were built for a given profile on a given day"""
        query_set = self.filter(section__profile=profile, day=day)
        return query_set.count() * YARDS_PER_DAY

    def cost_by_day(self, profile: int | None, day: int | None) -> int:
        """
        Counts how much was spent on building given profile accumulated by a given day
        If profile is None - counts spends for entire wall
        If day is None - counts total spent for all days
        """
        query_set = self.filter(section__profile=profile) if profile else self.all()
        if day:
            query_set = query_set.filter(day__lte=day)
        return query_set.count() * YARDS_PER_DAY * PRICE_PER_YARD


class Section(models.Model):
    """
    Represents one section in the wall.
    It's order in profile and what profile it belongs to
    """
    order = models.PositiveIntegerField(help_text="Order of section in profile")
    profile = models.PositiveIntegerField(help_text="Order of profile in the wall")

    class Meta:
        unique_together = ["profile", "order"]

    def __str__(self) -> str:
        return f"Profile {self.profile} Section {self.order}"


class Ledger(models.Model):
    """
    Record in ledger represents if section was built on given day
    If NO record for section S and day D - section S was NOT built on day D
    """
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    day = models.PositiveIntegerField()

    class Meta:
        indexes = [models.Index(fields=["day"])]
        unique_together = ["section", "day"]

    objects = LedgerManager()
