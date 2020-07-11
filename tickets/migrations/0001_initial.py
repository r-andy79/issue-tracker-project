# Generated by Django 3.0.8 on 2020-07-11 18:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Ticket title')),
                ('create_date', models.DateTimeField(verbose_name='Date created')),
                ('ticket_author', models.CharField(max_length=60)),
                ('description', models.TextField(blank=True)),
                ('ticket_type', models.CharField(choices=[('bug', 'Bug'), ('feature', 'Feature')], max_length=10)),
                ('ticket_status', models.CharField(choices=[('T', 'To do'), ('D', 'Doing'), ('C', 'Completed')], default='T', max_length=1)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
