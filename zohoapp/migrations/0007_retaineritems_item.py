# Generated by Django 4.2.3 on 2023-12-06 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0006_salesorder_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='retaineritems',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='zohoapp.additem'),
        ),
    ]