# Generated by Django 2.2.28 on 2025-03-20 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songeek_project', '0008_auto_20250320_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ImageField(blank=True, upload_to='album_covers'),
        ),
    ]
