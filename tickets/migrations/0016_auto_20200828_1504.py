# Generated by Django 3.0.8 on 2020-08-28 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0015_auto_20200828_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(blank=True, max_length=2000),
        ),
    ]
