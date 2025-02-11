import mimetypes
from django.db import models
from users.models import Account
from django.core.exceptions import ValidationError


def validate_file_type(file):
    valid_mime_types = ['application/pdf', 'image/jpeg', 'image/png', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    valid_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'docx']

    # Get MIME type from uploaded file (if available)
    mime_type = getattr(file, 'content_type', None)
    
    # If `content_type` is not available, use mimetypes.guess_type
    if not mime_type:
        mime_type, _ = mimetypes.guess_type(file.name)

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
    )  # File field for scanned documents, images, or PDFs

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='properties')  # Foreign key to Account table
    total_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in square meters")  # Total area of the land
    reference_point = models.CharField(max_length=255, help_text="Nearest benchmark or fixed point for reference")  # Nearest reference point
    date_surveyed = models.DateField()  # Date the land was surveyed

    def __str__(self):
        return f"{self.land_title} ({self.title_number})"

    class Meta:
        verbose_name_plural = "Properties"

class LandLocation(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='land_location')  # Link to Property
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Latitude coordinate
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Longitude coordinate
    altitude = models.DecimalField(max_digits=9, decimal_places=2)  # Altitude coordinate
    village = models.CharField(max_length=100, null=True, blank=True)
    parish = models.CharField(max_length=100, null=True, blank=True)
    subcounty = models.CharField(max_length=100, null=True, blank=True)
    county = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, default='Uganda', null=True, blank=True)

    def __str__(self):
        return f"Location for {self.property.land_title} ({self.property.title_number})"

    class Meta:
        verbose_name_plural = "Land Locations"
