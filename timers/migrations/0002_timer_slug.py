# Generated by Django 2.1.2 on 2018-10-30 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("timers", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="timer",
            name="slug",
            field=models.SlugField(default="default", max_length=250),
            preserve_default=False,
        )
    ]
