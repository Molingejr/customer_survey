# Generated by Django 2.1.5 on 2019-02-09 02:48

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20190207_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cellphone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128),
        ),
    ]
