from django.db import models
from users.models import Account, Location
from django.core.exceptions import ValidationError

def validate_file_type(file):
    valid_mime_types = ['application/pdf', 'image/jpeg', 'image/png', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    valid_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'docx']
    mime_type = file.file.content_type
    extension = file.name.split('.')[-1].lower()
    if mime_type not in valid_mime_types or extension not in valid_extensions:
        raise ValidationError('Unsupported file type. Please upload a PDF, image, or DOCX file.')


class Property(models.Model):
    LAND_TITLE_FILE_TYPES = [
        ('image', 'Image'),
        ('pdf', 'PDF'),
        ('doc', 'Document'),
    ]

    land_title = models.CharField(max_length=255)  # Title of the land
    title_number = models.CharField(max_length=100, unique=True)  # Unique title number
    title_document = models.FileField(
    upload_to='land_titles/',
    validators=[validate_file_type],
    help_text="Upload land title documents (PDF, image, or docx files)."
        )       # File field for scanned documents, images, or PDFs

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='properties')  # Foreign key to the Account table
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='properties')  # Foreign key to Location table
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Latitude coordinate
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Longitude coordinate
    altitude = models.DecimalField(max_digits=9, decimal_places=2)  # Altitude coordinate
    total_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in square meters")  # Total area of the land
    reference_point = models.CharField(max_length=255, help_text="Nearest benchmark or fixed point for reference")  # Nearest reference point
    date_surveyed = models.DateField()  # Date the land was surveyed

    def __str__(self):
        return f"{self.land_title} ({self.title_number})"

    class Meta:
        verbose_name_plural = "Properties"



