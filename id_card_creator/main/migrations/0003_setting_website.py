# Generated by Django 3.2.12 on 2023-02-15 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_setting_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='website',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]