# Generated by Django 5.0.6 on 2024-07-14 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_store', '0011_cart_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='back_cam',
            name='back_cam',
            field=models.CharField(choices=[('16px', '16px'), ('32px', '32px'), ('64px', '64px'), ('108px', '108px')], default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='front_cam',
            name='front_cam',
            field=models.CharField(choices=[('8px', '8px'), ('16px', '16px')], default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='Process',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='description',
            field=models.TextField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='discountPrice',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='network',
            name='mobile_network',
            field=models.CharField(choices=[('4G', '4G'), ('5G', '5G')], default=None, max_length=10),
        ),
        migrations.AlterField(
            model_name='ram',
            name='ram',
            field=models.CharField(choices=[('4GB', '4GB'), ('6GB', '6GB'), ('8GB', '8GB')], default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='rom',
            name='rom',
            field=models.CharField(choices=[('64GB', '64GB'), ('128GB', '128GB'), ('256GB', '256GB')], default=None, max_length=100),
        ),
    ]
