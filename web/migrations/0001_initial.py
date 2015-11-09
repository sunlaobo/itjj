# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=30, verbose_name=b'IP')),
                ('port', models.IntegerField(verbose_name=b'\xe7\xab\xaf\xe5\x8f\xa3')),
                ('type', models.CharField(default=b'http', max_length=10, verbose_name=b'\xe4\xbb\xa3\xe7\x90\x86\xe7\xb1\xbb\xe5\x9e\x8b')),
                ('country', models.CharField(default=b'', max_length=b'100', null=True, verbose_name=b'\xe5\x9c\xb0\xe5\x8c\xba')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x85\xa5\xe5\xba\x93\xe6\x97\xb6\xe9\x97\xb4')),
            ],
        ),
    ]
