# Generated by Django 3.1.1 on 2020-11-02 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betapp', '0014_auto_20201102_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='points',
            field=models.FloatField(default=100),
        ),
        migrations.AlterField(
            model_name='winnerbet',
            name='payout',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='winnerbet',
            name='points',
            field=models.FloatField(default=0),
        ),
    ]