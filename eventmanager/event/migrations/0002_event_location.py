# Generated by Django 2.2.7 on 2020-01-20 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='locations.Location'),
        ),
    ]
