# Generated by Django 4.2.3 on 2023-09-28 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_manager', '0002_company_company_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Company',
        ),
    ]