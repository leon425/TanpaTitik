# Generated by Django 4.0.4 on 2024-03-12 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainPage', '0009_meettheteam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meettheteam',
            name='division',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='meettheteam',
            name='job_desc',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
