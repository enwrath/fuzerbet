# Generated by Django 3.1.1 on 2021-04-07 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betapp', '0021_auto_20210404_1736'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiscData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]