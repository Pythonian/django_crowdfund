# Generated by Django 3.1.1 on 2020-12-12 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfund', '0015_order_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Phone Number (Optional)'),
        ),
    ]