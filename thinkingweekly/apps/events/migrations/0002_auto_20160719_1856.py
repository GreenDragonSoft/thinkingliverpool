# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-19 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='extra_twitter_handle',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='organiser',
            name='twitter_handle',
            field=models.CharField(blank=True, help_text='With the leading @, eg @newsfromnowhere', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='twitter_handle',
            field=models.CharField(blank=True, help_text='With the leading @, eg @LEAFonBoldSt', max_length=16, null=True),
        ),
    ]
