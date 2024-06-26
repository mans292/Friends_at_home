# Generated by Django 4.2.5 on 2023-09-18 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_klarnaorder_alter_customer_phone_delete_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klarnaorder',
            name='html_snippet',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
