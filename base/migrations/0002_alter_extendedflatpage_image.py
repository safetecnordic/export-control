# Generated by Django 4.1.1 on 2022-10-24 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="extendedflatpage",
            name="image",
            field=models.ImageField(null=True, upload_to="base/img"),
        ),
    ]
