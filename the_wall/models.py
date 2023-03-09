from django.db import models
from django.db.models import Sum
from .entities import UnfinishedSection, LedgerRecord


class Section(models.Model):
    """
    Represents one section in the wall.
    It's order in profile and what profile it belongs to
    """
    order = models.PositiveIntegerField(help_text="Order of section in profile")
    profile = models.PositiveIntegerField(help_text="Order of profile in the wall")
    initial_height = models.PositiveIntegerField()
    yards_per_foot = models.PositiveIntegerField(help_text="Area of the section")

    class Meta:
        unique_together = ["profile", "order"]

    def __str__(self) -> str:
        return f"Profile {self.profile} Section {self.order}"

    @classmethod
    def save_entities(cls, section_data: UnfinishedSection, ledger_data: list[LedgerRecord]):
        section = cls.objects.create(
            order=section_data.order,
            profile=section_data.profile,
            initial_height=section_data.height,
            yards_per_foot=section_data.area
        )
        Ledger.objects.bulk_create(
            Ledger(section=section, day=ld.day, team=ld.team_name, ice_used=ld.ice_used)
            for ld in ledger_data
        )

    @classmethod
    def check_profile(cls, profile: int) -> bool:
        return cls.objects.filter(profile=profile).exists()


class Ledger(models.Model):
    """
    Record in ledger represents if section was built on given day
    If NO record for section S and day D - section S was NOT built on day D
    """
    day = models.PositiveIntegerField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    team = models.CharField(max_length=50)
    ice_used = models.PositiveIntegerField()

    class Meta:
        indexes = [models.Index(fields=["day"])]
        unique_together = ["section", "day"]

    @classmethod
    def count_ice_on_day(cls, profile: int | None, day: int) -> int:
        """Ice amount spent on profile or entire wall (if profile arg is None) on a given day"""
        query_set = cls.objects.filter(day=day)
        if profile:
            query_set = query_set.filter(section__profile=profile)
        return query_set.aggregate(total=Sum("ice_used"))["total"] or 0

    @classmethod
    def count_ice_by_day(cls, profile: int | None, day: int | None) -> int:
        """
        Ice amount spent on building given profile accumulated by a given day
        If profile is None - counts spends for entire wall
        If day is None - counts total spent for all days
        """
        query_set = cls.objects.all()
        if profile:
            query_set = query_set.filter(section__profile=profile)
        if day:
            query_set = query_set.filter(day__lte=day)
        return query_set.aggregate(total=Sum("ice_used"))["total"] or 0
