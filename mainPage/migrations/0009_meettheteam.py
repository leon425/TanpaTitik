# Generated by Django 4.0.4 on 2024-03-12 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainPage', '0008_alter_customer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetTheTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('division', models.CharField(max_length=200)),
                ('job_desc', models.CharField(max_length=200)),
            ],
        ),
    ]
