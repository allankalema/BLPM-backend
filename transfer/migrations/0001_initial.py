# Generated by Django 5.1.3 on 2025-01-27 14:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property', '0002_alter_property_title_document'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('transfer_date', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_from', to=settings.AUTH_USER_MODEL)),
                ('land_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to='property.property')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Land Transfer',
                'verbose_name_plural': 'Land Transfers',
                'ordering': ['-transfer_date'],
            },
        ),
    ]
