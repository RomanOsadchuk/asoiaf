from django.db import models


class Section(models.Model):
    profile = models.PositiveIntegerField(help_text="order of profile in the wall")
    order = models.PositiveIntegerField(help_text="order of sectin in profile")
    start_day = models.PositiveIntegerField(help_text="First day of building")
    end_day = models.PositiveIntegerField(help_text="Last day of building")

    class Meta:
        unique_together = ["profile", "order"]

    def __str__(self) -> str:
        return f"Profile {self.profile} Section {self.order}"


class CountDaysByDay(models.Func):
    """
    Returns function that counts how many building days were spent on section
    prior to day from extra params. Therefore - min(end_day, {day})
    """

    def as_sqlite(self, compiler, connection, **extra_context):
        day = self.extra["day"]  # no injection because day is integer
        template = f"min(end_day, {day}) - start_day + 1"
        return super().as_sql(compiler, connection, template=template, **extra_context)
