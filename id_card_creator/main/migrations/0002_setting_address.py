# Generated by Django 3.2.12 on 2023-02-15 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='address',
            field=models.CharField(default='', max_length=255),
        ),
    ]
