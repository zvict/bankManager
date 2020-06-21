# Generated by Django 3.0.3 on 2020-06-21 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_auto_20200621_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='settime',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='customers',
            field=models.ManyToManyField(related_name='loan_cus', through='manager.CusForLoan', to='manager.Customer'),
        ),
    ]
