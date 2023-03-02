from django.db import models


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
