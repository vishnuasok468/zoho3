# Generated by Django 4.2.3 on 2023-11-24 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0002_retaineritems_itemname_retaineritems_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='retaineritems',
            name='rate',
            field=models.IntegerField(null=True),
        ),
    ]
