# Generated by Django 4.2.4 on 2023-09-28 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0006_alter_formscore_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='formscore',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
