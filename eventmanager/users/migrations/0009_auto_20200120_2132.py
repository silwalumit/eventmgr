# Generated by Django 2.2.7 on 2020-01-20 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
        ('users', '0008_auto_20191226_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='events',
            field=models.ManyToManyField(through='event.SavedEvent', to='event.Event', verbose_name='Events'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', related_query_name='subscriber', to='users.Organizer', verbose_name='Organizer')),
                ('volunteer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', related_query_name='subscription', to='users.Volunteer', verbose_name='Volunteer')),
            ],
        ),
        migrations.AddField(
            model_name='volunteer',
            name='organizers',
            field=models.ManyToManyField(through='users.Subscription', to='users.Organizer', verbose_name='Organizers'),
        ),
    ]
