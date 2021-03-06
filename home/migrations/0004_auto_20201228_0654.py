# Generated by Django 3.1.3 on 2020-12-28 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0003_auto_20201228_0648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
