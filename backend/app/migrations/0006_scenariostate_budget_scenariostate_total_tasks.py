# Generated by Django 4.0.5 on 2022-06-26 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenariostate',
            name='budget',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scenariostate',
            name='total_tasks',
            field=models.IntegerField(default=0),
        ),
    ]
