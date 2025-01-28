# Generated by Django 5.1.5 on 2025-01-28 20:23

import property.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('land_title', models.CharField(max_length=255)),
                ('title_number', models.CharField(max_length=100, unique=True)),
                ('title_document', models.FileField(help_text='Upload land title documents (PDF, image, or docx files).', upload_to='land_titles/', validators=[property.models.validate_file_type])),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('altitude', models.DecimalField(decimal_places=2, max_digits=9)),
                ('total_area', models.DecimalField(decimal_places=2, help_text='Area in square meters', max_digits=10)),
                ('reference_point', models.CharField(help_text='Nearest benchmark or fixed point for reference', max_length=255)),
                ('date_surveyed', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Properties',
            },
        ),
    ]
