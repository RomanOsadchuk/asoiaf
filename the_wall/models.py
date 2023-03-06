from django.db import models
from .entities import UnfinishedSection


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
    def create_from_entity(cls, data: UnfinishedSection):
        return cls.objects.create(
            order=data.order,
            profile=data.profile,
            initial_height=data.height,
            yards_per_foot=data.area
        )


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
