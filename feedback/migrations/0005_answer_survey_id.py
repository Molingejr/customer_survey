# Generated by Django 2.1.5 on 2019-02-10 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_answer_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='survey_id',
            field=models.IntegerField(default=1),
        ),
    ]