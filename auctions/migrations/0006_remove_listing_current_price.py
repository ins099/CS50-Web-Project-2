# Generated by Django 3.0.8 on 2020-07-05 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bid_best_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='current_price',
        ),
    ]
