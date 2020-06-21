# Generated by Django 2.2 on 2020-06-10 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('accountid', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('money', models.FloatField()),
                ('settime', models.DateField(blank=True, null=True)),
                ('accounttype', models.CharField(max_length=1)),
            ],
            options={
                'verbose_name': '账户',
                'verbose_name_plural': '账户',
                'db_table': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('bankname', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=20)),
                ('money', models.FloatField()),
            ],
            options={
                'verbose_name': '银行',
                'verbose_name_plural': '银行',
                'db_table': 'bank',
            },
        ),
        migrations.CreateModel(
            name='CusForloan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'cusforloan',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cusid', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('cusname', models.CharField(max_length=20)),
                ('cusphone', models.CharField(max_length=11)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_phone', models.CharField(max_length=11)),
                ('contact_name', models.CharField(max_length=20)),
                ('contact_email', models.EmailField(blank=True, max_length=20, null=True)),
                ('contact_relation', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': '客户',
                'verbose_name_plural': '客户',
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('departid', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('departname', models.CharField(max_length=20)),
                ('departtype', models.CharField(blank=True, max_length=15, null=True)),
                ('manager', models.CharField(max_length=18)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Bank')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('loanid', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('money', models.FloatField(blank=True, null=True)),
                ('state', models.CharField(max_length=1)),
                ('bank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='manager.Bank')),
                ('customers', models.ManyToManyField(related_name='loan_cus', through='manager.CusForloan', to='manager.Customer')),
            ],
            options={
                'verbose_name': '贷款',
                'verbose_name_plural': '贷款',
                'db_table': 'loan',
            },
        ),
        migrations.CreateModel(
            name='SaveAcc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interestrate', models.FloatField(blank=True, null=True)),
                ('savetype', models.CharField(blank=True, max_length=1, null=True)),
                ('accountid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Accounts')),
            ],
            options={
                'verbose_name': '储蓄账户',
                'verbose_name_plural': '储蓄账户',
                'db_table': 'saveacc',
            },
        ),
        migrations.CreateModel(
            name='PayInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.FloatField()),
                ('paytime', models.DateField()),
                ('cusid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Customer')),
                ('loanid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Loan')),
            ],
            options={
                'db_table': 'payinfo',
                'unique_together': {('loanid', 'cusid', 'money', 'paytime')},
            },
        ),
        migrations.AddField(
            model_name='loan',
            name='payinfos',
            field=models.ManyToManyField(related_name='loan_pay', through='manager.PayInfo', to='manager.Customer'),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('empid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('empname', models.CharField(max_length=20)),
                ('empphone', models.CharField(blank=True, max_length=11, null=True)),
                ('empaddr', models.CharField(blank=True, max_length=50, null=True)),
                ('emptype', models.CharField(max_length=1)),
                ('empstart', models.DateField()),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='manager.Department')),
            ],
            options={
                'verbose_name': '员工',
                'verbose_name_plural': '员工',
                'db_table': 'employee',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='accres',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_accres', to='manager.Employee'),
        ),
        migrations.AddField(
            model_name='customer',
            name='loanres',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_loanres', to='manager.Employee'),
        ),
        migrations.AddField(
            model_name='cusforloan',
            name='cusid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Customer'),
        ),
        migrations.AddField(
            model_name='cusforloan',
            name='loanid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Loan'),
        ),
        migrations.CreateModel(
            name='CusForAcc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit', models.DateField(blank=True, null=True)),
                ('accounttype', models.CharField(blank=True, max_length=1, null=True)),
                ('accountid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Accounts')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Bank')),
                ('cusid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Customer')),
            ],
            options={
                'db_table': 'cusforacc',
                'unique_together': {('bank', 'cusid', 'accounttype'), ('accountid', 'cusid')},
            },
        ),
        migrations.CreateModel(
            name='CheckAcc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overdraft', models.FloatField(blank=True, null=True)),
                ('accountid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Accounts')),
            ],
            options={
                'verbose_name': '支票账户',
                'verbose_name_plural': '支票账户',
                'db_table': 'checkacc',
            },
        ),
        migrations.AddField(
            model_name='accounts',
            name='customers',
            field=models.ManyToManyField(through='manager.CusForAcc', to='manager.Customer'),
        ),
        migrations.AlterUniqueTogether(
            name='cusforloan',
            unique_together={('loanid', 'cusid')},
        ),
    ]
