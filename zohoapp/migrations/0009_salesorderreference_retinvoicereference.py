# Generated by Django 4.2.3 on 2023-12-07 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0008_sales_item_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='salesOrderReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.BigIntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zohoapp.customer')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zohoapp.salesorder')),
            ],
        ),
        migrations.CreateModel(
            name='retInvoiceReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.BigIntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zohoapp.customer')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zohoapp.retainerinvoice')),
            ],
        ),
    ]
