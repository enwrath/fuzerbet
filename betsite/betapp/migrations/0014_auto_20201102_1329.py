# Generated by Django 3.1.1 on 2020-11-02 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betapp', '0013_auto_20200916_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='points',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnerbet',
            name='payout',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnerbet',
            name='points',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='bestof',
            field=models.IntegerField(choices=[(0, 'No betting on score'), (3, 'Bo3'), (5, 'Bo5'), (7, 'Bo7')], default=3),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='p1maps',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0, verbose_name='Map wins: Player 1 (if Bo3+)'),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='p2maps',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0, verbose_name='Map wins: Player 2 (if Bo3+)'),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='player1odds',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='player2odds',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='resL0',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='resL1',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='resL2',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='resL3',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='resW0',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='resW1',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='resW2',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='winnermatch',
            name='resW3',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=11),
        ),
    ]
