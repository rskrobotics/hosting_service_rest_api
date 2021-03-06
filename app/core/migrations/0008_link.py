# Generated by Django 3.2.5 on 2021-09-15 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_user_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_str', models.CharField(max_length=50)),
                ('available_until', models.DateTimeField(null=True)),
                ('thumbnail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.thumbnail')),
            ],
        ),
    ]
