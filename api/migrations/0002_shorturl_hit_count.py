# Generated by Django 4.1.4 on 2022-12-21 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorturl',
            name='hit_count',
            field=models.IntegerField(default=0),
        ),
    ]
