# Generated by Django 5.0.6 on 2024-09-21 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_testresult_test_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresult',
            name='test_type',
        ),
    ]
