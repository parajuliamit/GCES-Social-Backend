# Generated by Django 3.2 on 2021-11-10 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_auto_20211110_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='is_approved',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='teacher_comment',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]