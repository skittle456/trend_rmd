# Generated by Django 2.0.3 on 2019-05-26 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0009_googletrend_lang'),
    ]

    operations = [
        migrations.AddField(
            model_name='googletrend',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
