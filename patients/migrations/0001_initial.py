# Generated by Django 3.0.2 on 2020-05-29 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_userprofile_gender'),
        ('doctors', '0002_auto_20200126_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.UserProfile')),
                ('device_serial', models.CharField(max_length=50)),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='PulseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('pulse_bpm', models.FloatField(max_length=5)),
                ('device_serial_number', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='patients.Patient')),
            ],
        ),
    ]
