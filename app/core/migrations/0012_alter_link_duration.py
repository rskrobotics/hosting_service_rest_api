# Generated by Django 3.2.5 on 2021-09-15 18:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_link_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(30000)]),
        ),
    ]
