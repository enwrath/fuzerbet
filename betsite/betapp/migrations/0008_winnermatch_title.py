# Generated by Django 3.1.1 on 2020-09-09 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betapp', '0007_auto_20200907_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='winnermatch',
            name='title',
            field=models.CharField(default='showmatch', max_length=200),
            preserve_default=False,
        ),
    ]
