# Generated by Django 4.1.1 on 2022-10-24 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("flatpages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExtendedFlatPage",
            fields=[
                (
                    "flatpage_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="flatpages.flatpage",
                    ),
                ),
                ("image", models.ImageField(upload_to="base/img")),
            ],
            bases=("flatpages.flatpage",),
        ),
    ]
