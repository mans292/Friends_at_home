# Generated by Django 4.2.5 on 2023-09-24 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_klarnaorder_html_snippet_alter_order_customer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='klarnaorder',
            name='order_id',
        ),
        migrations.AlterField(
            model_name='klarnaorder',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.klarnaorder')),
            ],
        ),
    ]
