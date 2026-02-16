from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=120, unique=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "name")
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="districts")
    name = models.CharField(max_length=120)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("region__order", "order", "name")
        constraints = [
            models.UniqueConstraint(fields=["region", "name"], name="uq_district_region_name")
        ]
        indexes = [
            models.Index(fields=["region", "name"]),
        ]

    def __str__(self):
        return f"{self.region.name} / {self.name}"
