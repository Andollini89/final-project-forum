# Generated by Django 3.1.5 on 2021-06-28 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210628_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votes',
            name='vote',
            field=models.IntegerField(default=0),
        ),
    ]
