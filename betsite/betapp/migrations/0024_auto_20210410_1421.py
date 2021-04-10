# Generated by Django 3.1.1 on 2021-04-10 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betapp', '0023_auto_20210407_2042'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='custommatch',
            options={'verbose_name_plural': 'Custom Matches'},
        ),
        migrations.AddField(
            model_name='winnermatch',
            name='refund',
            field=models.BooleanField(default=False, verbose_name='REFUND ALL BETS!'),
        ),
    ]