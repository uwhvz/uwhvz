# Generated by Django 2.0.7 on 2018-07-10 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20180710_0533'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='modifier',
            field=models.IntegerField(default=0),
        ),
    ]
