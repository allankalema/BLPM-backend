from django.db import models

class Location(models.Model):
    village = models.CharField(max_length=100)
    parish = models.CharField(max_length=100)
    subcounty = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Uganda')

    def __str__(self):
        return f"{self.village}, {self.parish}, {self.subcounty}, {self.county}, {self.district}, {self.country}"

    class Meta:
        verbose_name_plural = "Locations"
