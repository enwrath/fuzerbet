# Generated by Django 3.1.1 on 2020-09-06 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betapp', '0003_auto_20200906_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='winnerbet',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]
