# Generated by Django 3.1.1 on 2020-11-02 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betapp', '0015_auto_20201102_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='points',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=15),
        ),
        migrations.AlterField(
            model_name='winnerbet',
            name='payout',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='winnerbet',
            name='points',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
