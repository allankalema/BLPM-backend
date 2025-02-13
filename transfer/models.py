from django.db import models
from django.conf import settings  # Import the settings to use AUTH_USER_MODEL
from property.models import Property  # Importing Property model

class Transfer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('rejected', 'Rejected'),
    ]
    
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='transfers_from', 
        on_delete=models.CASCADE,
        null=True
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='transfers_to', 
        on_delete=models.CASCADE,
        null=True
    )
    land_title = models.ForeignKey(Property, null=True, related_name='transfers', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )
    transfer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer of {self.land_title.land_title} from {self.from_user.username} to {self.to_user.username} - {self.status}"

    class Meta:
        verbose_name = "Land Transfer"
        verbose_name_plural = "Land Transfers"
        ordering = ['-transfer_date']
