# Generated by Django 5.1.5 on 2025-02-18 14:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0001_initial'),
        ('voting', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('voter', 'election', 'candidate')},
        ),
    ]
