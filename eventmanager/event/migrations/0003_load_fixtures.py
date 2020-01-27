# Generated by Django 2.2.7 on 2020-01-25 14:47

from django.db import migrations, models 

def load_event_types(apps, schema_editor):
    from django.core.management import call_command
    call_command("loaddata", "event_type")

def delete_event_types(apps, schema_editor):
    Type = apps.get_model("event", "Type")
    Type.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_event_location'),
    ]

    operations = [
        migrations.RunPython(load_event_types, delete_event_types)
    ]
