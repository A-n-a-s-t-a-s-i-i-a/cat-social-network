# Generated by Django 5.1.3 on 2024-11-21 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cat_network", "0002_alter_catuser_age"),
    ]

    operations = [
        migrations.AlterField(
            model_name="catuser",
            name="age",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
