# Generated by Django 3.2 on 2021-11-09 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20211109_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='batch',
            field=models.ManyToManyField(blank=True, to='base.Batch'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='routine',
            field=models.ManyToManyField(blank=True, to='base.Routine'),
        ),
    ]
