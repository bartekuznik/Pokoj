# Generated by Django 4.2.1 on 2024-01-03 11:02

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PlayerInGame",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("player_id", models.PositiveIntegerField(default=True, unique=True)),
                ("player_nick", models.TextField(max_length=200)),
                ("card_1", models.CharField(max_length=20, null=True)),
                ("card_2", models.CharField(max_length=20, null=True)),
                ("tokens", models.IntegerField(default=0)),
                ("winPercentage", models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cardsOnTable", models.JSONField()),
                ("nextPlayer", models.CharField(max_length=200)),
                ("tokensOnTable", models.PositiveIntegerField(default=0)),
                ("lastCall", models.PositiveIntegerField(default=0)),
            ],
        ),
    ]