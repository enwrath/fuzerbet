# Generated by Django 3.1.1 on 2021-04-04 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('betapp', '0019_auto_20210404_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomBet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('payout', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('winner', models.IntegerField(default=0)),
                ('resolved', models.BooleanField(default=False)),
                ('won', models.BooleanField(default=False)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='betapp.custommatch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
