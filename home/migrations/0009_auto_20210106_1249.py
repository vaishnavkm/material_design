# Generated by Django 3.1.3 on 2021-01-06 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20210106_1233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Payments',
            new_name='Payment',
        ),
    ]
