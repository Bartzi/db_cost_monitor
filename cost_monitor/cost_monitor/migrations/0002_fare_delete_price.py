# Generated by Django 4.0.4 on 2022-06-06 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cost_monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('fare', models.FloatField()),
                ('connection', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='fares', to='cost_monitor.connection')),
            ],
        ),
        migrations.DeleteModel(
            name='Price',
        ),
    ]