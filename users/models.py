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


class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    nin = models.CharField(max_length=20, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # Foreign key to Location

    # Role fields
    land_owner = models.BooleanField(default=False)
    surveyor = models.BooleanField(default=False)
    govt_official = models.BooleanField(default=False)
    law_enforcement = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        verbose_name_plural = "Accounts"