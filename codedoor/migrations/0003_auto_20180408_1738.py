# Generated by Django 2.0.1 on 2018-04-09 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codedoor', '0002_auto_20180406_0254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.URLField(blank=True, null=True),
        ),
    ]