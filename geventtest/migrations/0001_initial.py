# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_url', models.URLField(blank=True)),
                ('image', models.FileField(upload_to=b'/testpath')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
