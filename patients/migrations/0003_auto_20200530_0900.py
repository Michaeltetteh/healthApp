# Generated by Django 3.0.2 on 2020-05-30 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_auto_20200530_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pulsemodel',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
