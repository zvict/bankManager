from django.db import models

# Create your models here.

class Bank(models.Model):
    bankname = models.CharField(primary_key=True, max_length=20)
    city = models.CharField(max_length=20)
    money = models.FloatField()

    class Meta:
        db_table = 'bank'
        verbose_name = verbose_name_plural = '银行'


class Department(models.Model):
    departid = models.CharField(primary_key=True, max_length=4)
    departname = models.CharField(max_length=20)
    departtype = models.CharField(max_length=15, blank=True, null=True)
    manager = models.CharField(max_length=18)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

    class Meta:
        db_table = 'department'
        verbose_name = verbose_name_plural = '部门'


class Employee(models.Model):
    empid = models.CharField(primary_key=True, max_length=8)
    empname = models.CharField(max_length=20)
    empphone = models.CharField(max_length=11, blank=True, null=True)
    empaddr = models.CharField(max_length=50, blank=True, null=True)
    emptype = models.CharField(max_length=1)  # 0-经理, 1-普通员工
    empstart = models.DateField()
    depart = models.ForeignKey(Department, on_delete=models.PROTECT)

    class Meta:
        db_table = 'employee'
        verbose_name = verbose_name_plural = '员工'


class Customer(models.Model):
    cusid = models.CharField(primary_key=True, max_length=18)
    cusname = models.CharField(max_length=20)
    cusphone = models.CharField(max_length=11)
    address = models.CharField(max_length=50, blank=True, null=True)
    contact_phone = models.CharField(max_length=11)
    contact_name = models.CharField(max_length=20)
    contact_email = models.EmailField(max_length=20, blank=True, null=True)  # EmailField
    contact_relation = models.CharField(max_length=10)
    loanres = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name="customer_loanres")
    accres = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name="customer_accres")

    class Meta:
        db_table = 'customer'
        verbose_name = verbose_name_plural = '客户'


class Accounts(models.Model):
    accountid = models.CharField(primary_key=True, max_length=6)
    money = models.FloatField()
    settime = models.DateField(blank=True, null=True)
    accounttype = models.CharField(max_length=1)  # 0-储蓄账户, 1-支票账户
    customers = models.ManyToManyField(Customer, through='CusForAcc', through_fields=('accountid','cusid'))

    class Meta:
        db_table = 'accounts'
        verbose_name = verbose_name_plural = '账户'


class CheckAcc(models.Model):
    accountid = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    # accountid = models.OneToOneField(Accounts, on_delete=models.CASCADE, primary_key=True)
    overdraft = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'checkacc'
        verbose_name = verbose_name_plural = '支票账户'


class SaveAcc(models.Model):
    accountid = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    # accountid = models.OneToOneField(Accounts, on_delete=models.CASCADE, primary_key=True)
    interestrate = models.FloatField(blank=True, null=True)
    savetype = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'saveacc'
        verbose_name = verbose_name_plural = '储蓄账户'


class CusForAcc(models.Model):
    # accountid = models.OneToOneField(Accounts, models.DO_NOTHING, primary_key=True)
    accountid = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    cusid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    visit = models.DateField(blank=True, null=True)
    accounttype = models.CharField(max_length=1, blank=True, null=True)  # 0-储蓄账户, 1-支票账户

    class Meta:
        db_table = 'cusforacc'
        unique_together = (('accountid', 'cusid'), ('bank', 'cusid', 'accounttype'),)


class Loan(models.Model):
    loanid = models.CharField(primary_key=True, max_length=4)
    money = models.FloatField(blank=True, null=True)
    moneyleft = models.FloatField(blank=True, null=True)
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, blank=True, null=True)
    settime = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=1)  # 0-未发放, 1-发放中, 2-发放完, 3-异常
    customers = models.ManyToManyField(Customer, through='CusForLoan', through_fields=('loanid', 'cusid'), related_name='loan_cus')
    payinfos = models.ManyToManyField(Customer, through='PayInfo', through_fields=('loanid', 'cusid'), related_name='loan_pay')

    class Meta:
        db_table = 'loan'
        verbose_name = verbose_name_plural = '贷款'


class CusForLoan(models.Model):
    # loanid = models.ForeignKey('Loan', models.DO_NOTHING, db_column='loanID', primary_key=True)
    loanid = models.ForeignKey(Loan, on_delete=models.CASCADE)
    cusid = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cusforloan'
        unique_together = (('loanid', 'cusid'),)


class PayInfo(models.Model):
    # loanid = models.ForeignKey(Loan, models.DO_NOTHING, db_column='loanID', primary_key=True)
    loanid = models.ForeignKey(Loan, on_delete=models.CASCADE)
    cusid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    money = models.FloatField()
    paytime = models.DateField()

    class Meta:
        db_table = 'payinfo'
        unique_together = (('loanid', 'cusid', 'money', 'paytime'),)