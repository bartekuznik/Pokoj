# Generated by Django 5.0 on 2024-01-21 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0003_playeringame_ip_address_room_isfinished'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playeringame',
            name='ip_address',
            field=models.CharField(default='', max_length=15, null=True),
        ),
    ]
