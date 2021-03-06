# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-22 07:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cache_id', models.CharField(max_length=100)),
                ('cache', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='UserCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aiml_kernel', models.CharField(max_length=102400)),
            ],
        ),
        migrations.AddField(
            model_name='requestcache',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='HRBot.UserCache'),
        ),
    ]
