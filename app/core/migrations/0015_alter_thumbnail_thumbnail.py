# Generated by Django 3.2.7 on 2021-09-16 21:09

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_thumbnail_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbnail',
            name='thumbnail',
            field=models.ImageField(upload_to=core.models.thumbnail_file_path),
        ),
    ]
