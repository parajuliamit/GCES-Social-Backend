# Generated by Django 3.2 on 2021-11-09 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_auto_20211109_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='batch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.batch'),
            preserve_default=False,
        ),
    ]
