# Generated by Django 2.0.3 on 2019-05-26 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0010_googletrend_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='googletrend',
            name='summary',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='googletrend',
            name='title_detail',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
