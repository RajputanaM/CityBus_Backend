# Generated by Django 4.2.4 on 2023-09-21 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_number', models.CharField(max_length=10)),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('price_per_ticket', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='BusStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_tickets', models.PositiveIntegerField()),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking_date_time', models.DateTimeField(auto_now_add=True)),
                ('bus_arrival_time', models.TimeField()),
                ('bus_departure_time', models.TimeField()),
                ('source_station', models.CharField(max_length=255)),
                ('destination_station', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.bus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.profile')),
            ],
        ),
        migrations.AddField(
            model_name='bus',
            name='destination_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_buses', to='bus.busstation'),
        ),
        migrations.AddField(
            model_name='bus',
            name='source_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_buses', to='bus.busstation'),
        ),
    ]
