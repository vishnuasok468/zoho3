# Generated by Django 4.2.3 on 2023-11-21 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='retaineritems',
            name='itemname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='retaineritems',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
