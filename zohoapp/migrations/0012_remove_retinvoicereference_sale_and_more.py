# Generated by Django 4.2.3 on 2023-12-07 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0011_rename_customer_retinvoicereference_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='retinvoicereference',
            name='sale',
        ),
        migrations.RemoveField(
            model_name='salesorderreference',
            name='sale',
        ),
    ]