# Generated by Django 2.2.8 on 2019-12-29 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20191229_2034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='legacy_points',
        ),
    ]
