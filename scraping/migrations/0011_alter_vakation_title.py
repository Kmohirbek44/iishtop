# Generated by Django 3.2.6 on 2022-06-05 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0010_alter_resume_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vakation',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
