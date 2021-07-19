# Generated by Django 3.1.5 on 2021-06-29 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210628_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='votes',
            name='vote_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='votes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='votes',
            unique_together={('user', 'answer', 'vote_type')},
        ),
        migrations.RemoveField(
            model_name='votes',
            name='vote',
        ),
    ]
