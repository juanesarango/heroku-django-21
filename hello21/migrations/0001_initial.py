# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('value', models.CharField(max_length=100, null=True, default=None)),
                ('redeemed', models.BooleanField(default=False)),
            ],
        ),
    ]
