# Generated by Django 2.0.1 on 2019-02-18 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codedoor', '0005_fix_avg_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='codebucks',
            field=models.IntegerField(default=0),
        ),
    ]
