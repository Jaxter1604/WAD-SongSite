# Generated by Django 2.2.28 on 2025-03-22 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songeek_project', '0010_auto_20250322_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ImageField(default='album_covers/default.jpeg', upload_to='album_covers'),
        ),
    ]
