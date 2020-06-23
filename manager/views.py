import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import *
from django.db.models import Sum
import datetime


def post_to_dict(post, mode):
    newdict = post.copy()
    outdict = {}
    if mode == 0:  # 添加模式
        for i in newdict.dict().items():
            if i[1] == "":
                outdict[i[0]] = None
            else:
                outdict[i[0]] = i[1]
    elif mode == 1:  # 查询模式
        for i in newdict.dict().items():
            if i[1] != "":
                outdict[i[0]] = i[1]
    elif mode == 2:  # 修改模式
        for i in newdict.dict().items():
            if "id" not in i[0]:
                if i[1] == "":
                    outdict[i[0]] = None
                else:
                    outdict[i[0]] = i[1]
    return outdict


def unique_count(inlist):
    udict = {}
    for obj in (inlist):
        if obj not in udict:
            udict[obj] = 1
        else:
            udict[obj] += 1
    # print(udict)
    return len(udict), udict


# def chart(request):
#     acccnt = []
#     banknames = Bank.objects.values_list("bankname")
#     banknames = [i[0] for i in banknames]
#     savedata = []
#     for bankname in banknames:
#         bank = Bank.objects.get(bankname=bankname)
#         savecnt, _ = unique_count(Accounts.objects.filter(cusforacc__bank=bank, accounttype="0"))
#         savedata.append(savecnt)
#     acccnt.append({
#         'name': "储蓄账户",
#         'data': savedata
#     })
#     checkdata = []
#     for bankname in banknames:
#         bank = Bank.objects.get(bankname=bankname)
#         checkcnt, _ = unique_count(Accounts.objects.filter(cusforacc__bank=bank, accounttype="1"))
#         checkdata.append(checkcnt)
#     acccnt.append({
#         'name': "支票账户",
#         'data': checkdata
#     })
#     cntchart = {
#         'chart': {'type': 'column'},
#         'title': {'text': '客户数量统计'},
#         'xAxis': {'categories': banknames},
#         'series': acccnt
#     }
#     cntdump = json.dumps(cntchart)

#     moneycnt = []
#     savemoney = []
#     for bankname in banknames:
#         bank = Bank.objects.get(bankname=bankname)
#         saveaccs = Accounts.objects.filter(cusforacc__bank=bank, accounttype="0").annotate(sum=Sum("money"))
#         sm = 0
#         for saveacc in saveaccs:
#             sm += saveacc.sum
#         savemoney.append(sm)
#     moneycnt.append({
#         'name': "储蓄总额",
#         'data': savemoney
#     })
#     loanmoney = []
#     for bankname in banknames:
#         bank = Bank.objects.get(bankname=bankname)
#         loanaccs = Loan.objects.filter(bank=bank).annotate(sum=Sum("money"))
#         lm = 0
#         for loanacc in loanaccs:
#             lm += loanacc.sum
#         loanmoney.append(lm)
#     moneycnt.append({
#         'name': "贷款总额",
#         'data': loanmoney
#     })
#     moneychart = {
#         'chart': {'type': 'column'},
#         'title': {'text': '业务金额统计'},
#         'xAxis': {'categories': banknames},
#         'series': moneycnt
#     }
#     moneydump = json.dumps(moneychart)

#     return render(request, 'manager/base.html', {'moneychart': moneydump, 'cntchart':cntdump})


@csrf_exempt
def chart_query(request):
    timeintr = ['']
    if request.method == 'POST':
        timeintr = request.POST.get('timeintr').split(' - ')
    if timeintr == ['']:
        timestart = [1, 1, 1]
        timeend = [9999, 12, 31]
    else:
        timestart = [int(i) for i in timeintr[0].split('-')]
        timeend = [int(i) for i in timeintr[1].split('-')]
    acccnt = []
    banknames = Bank.objects.values_list("bankname")
    banknames = [i[0] for i in banknames]
    savedata = []
    for bankname in banknames:
        bank = Bank.objects.get(bankname=bankname)
        savecnt, _ = unique_count(Accounts.objects.filter(
            cusforacc__bank=bank,
            accounttype="0",
            settime__gte=datetime.date(timestart[0], timestart[1], timestart[2]),
            settime__lte=datetime.date(timeend[0], timeend[1], timeend[2]),
            ))
        savedata.append(savecnt)
    acccnt.append({
        'name': "储蓄账户",
        'data': savedata
    })
    checkdata = []
    for bankname in banknames:
        bank = Bank.objects.get(bankname=bankname)
        checkcnt, _ = unique_count(Accounts.objects.filter(
            cusforacc__bank=bank,
            accounttype="1",
            settime__gte=datetime.date(timestart[0], timestart[1], timestart[2]),
            settime__lte=datetime.date(timeend[0], timeend[1], timeend[2]),
            ))
        checkdata.append(checkcnt)
    acccnt.append({
        'name': "支票账户",
        'data': checkdata
    })
    cntchart = {
        'chart': {'type': 'column'},
        'title': {'text': '客户数量统计'},
        'xAxis': {'categories': banknames},
        'series': acccnt
    }
    cntdump = json.dumps(cntchart)

    moneycnt = []
    savemoney = []
    for bankname in banknames:
        bank = Bank.objects.get(bankname=bankname)
        saveaccs = Accounts.objects.filter(
            cusforacc__bank=bank,
            accounttype="0",
            settime__gte=datetime.date(timestart[0], timestart[1], timestart[2]),
            settime__lte=datetime.date(timeend[0], timeend[1], timeend[2]),
            ).annotate(sum=Sum("money"))
        sm = 0
        for saveacc in saveaccs:
            sm += saveacc.sum
        savemoney.append(sm)
    moneycnt.append({
        'name': "储蓄总额",
        'data': savemoney
    })
    loanmoney = []
    for bankname in banknames:
        bank = Bank.objects.get(bankname=bankname)
        loanaccs = Loan.objects.filter(
            bank=bank,
            settime__gte=datetime.date(timestart[0], timestart[1], timestart[2]),
            settime__lte=datetime.date(timeend[0], timeend[1], timeend[2]),
            ).annotate(sum=Sum("money"))
        lm = 0
        for loanacc in loanaccs:
            lm += loanacc.sum
        loanmoney.append(lm)
    moneycnt.append({
        'name': "贷款总额",
        'data': loanmoney
    })
    moneychart = {
        'chart': {'type': 'column'},
        'title': {'text': '业务金额统计'},
        'xAxis': {'categories': banknames},
        'series': moneycnt
    }
    moneydump = json.dumps(moneychart)

    tabledata = {}
    for i, bankname in enumerate(banknames):
        tabledata[bankname] = {}
        tabledata[bankname]['savenum'] = savedata[i]
        tabledata[bankname]['checknum'] = checkdata[i]
        tabledata[bankname]['savemoney'] = savemoney[i]
        tabledata[bankname]['loanmoney'] = loanmoney[i]
        tabledata[bankname]['nums'] = savedata[i] + checkdata[i]
        tabledata[bankname]['moneys'] = savemoney[i] + loanmoney[i]
    # tabledata = json.dumps(tabledata)
    print(tabledata)

    return render(request, 'manager/base.html', \
        {'moneychart': moneydump, 'cntchart':cntdump, 'tabledata':tabledata, 'banknames':banknames})


def customer_add(request):
    emp_ids = [i[0] for i in Employee.objects.values_list("empid")]
    return render(request, "manager/customer/add.html", locals())


@csrf_exempt
def customer_add_succ(request):
    save_succ = 1
    if request.method == 'POST':
        add_dict = post_to_dict(request.POST, 0)
        loanres = add_dict.pop('loanres')
        accres = add_dict.pop('accres')
        print(add_dict, loanres, accres)
        signal = 1
        try:
            Customer.objects.create(**add_dict)
            signal = 0
            loanemp = Employee.objects.get(empid=loanres)
            accemp = Employee.objects.get(empid=accres)
            cus = Customer.objects.get(cusid=add_dict['cusid'])
            cus.loanres = loanemp
            cus.save()
            cus.accres = accemp
            cus.save()
        except:
            save_succ = 0
            if signal == 0:
                Customer.objects.get(cusid=add_dict['cusid']).delete()
    return render(request, "manager/customer/addSucc.html", {"save_succ":save_succ})


def customer_all(request):
    data = Customer.objects.all()
    return render(request, "manager/customer/query.html", {"data":data})


@csrf_exempt
def customer_query(request):
    data = Customer.objects.all()
    if request.method == 'POST':
        query_dict = post_to_dict(request.POST, 1)
        data = data.filter(**query_dict)
    return render(request, "manager/customer/query.html", {"data":data})


def customer_delete(request, cus_id):
    cus = Customer.objects.get(cusid=cus_id)
    msg = 0
    if (len(cus.loan_cus.all()) != 0) or (len(cus.accounts_set.all()) != 0):
        msg = "有关联账户或贷款，不能删除"
    else:
        cus.delete()
    data = Customer.objects.all()
    return render(request, "manager/customer/query.html", locals())


def customer_modify(request, cus_id):
    customer = Customer.objects.get(cusid=cus_id)
    emp_ids = [i[0] for i in Employee.objects.values_list("empid")]
    return render(request, "manager/customer/modify.html", locals())


@csrf_exempt
def customer_modify_succ(request, cus_id):
    modify_dict = post_to_dict(request.POST, 2)
    modify_succ = 1
    if request.method == 'POST':
        try:
            Customer.objects.filter(cusid=cus_id).update(**modify_dict)
        except:
            modify_succ = 0
    return render(request, "manager/customer/modifySucc.html", {"modify_succ":modify_succ})


def ajax_account_add_get_emps(request):
    bankname = request.GET.get('bankname')
    bank = Bank.objects.get(bankname=bankname)
    deps = bank.department_set.all()
    emp_ids = []
    for dep in deps:
        depart = Department.objects.get(departid=dep.departid)
        emps = depart.employee_set.all()
        for emp in emps:
            emp_ids.append(emp.empid)
    print(emp_ids)
    return JsonResponse({"emp_ids":emp_ids})


def account_add(request):
    cus_ids = Customer.objects.values_list("cusid")
    cus_ids = [i[0] for i in cus_ids]
    bank_names = Bank.objects.values_list("bankname")
    bank_names = [i[0] for i in bank_names]
    return render(request, "manager/account/add.html", locals())


@csrf_exempt
def account_add_succ(request):
    save_succ = 1
    signal = {
        'acc':1,
        'cus':1,
        'sorc':1,
    }
    if request.method == 'POST':
        data = post_to_dict(request.POST, 0)
        cus_ids = data['cusid'].split(',')
        # cus_ids = [i[0]*18 for i in cus_ids]
        print(data)
        try:
            acc = Accounts.objects.create(
                accountid=data['accountid'],
                money=float(data['money']),
                settime=data['settime'],
                accounttype=data['accounttype'],
            )
            print("创建Accounts成功")
            print(acc)
            signal['acc'] = 0
            bank = Bank.objects.get(bankname=data['bankname'])
            acc = Accounts.objects.get(accountid=data['accountid'])
            for cus_id in cus_ids:
                cus = Customer.objects.get(cusid=cus_id)
                # acc.customers.add(cus)
                cusforacc = CusForAcc.objects.create(
                    accountid=acc,
                    bank=bank,
                    cusid=cus,
                    visit=data['settime'],
                    accounttype=data['accounttype'],
                )
                print(cus_id,'done')
            print("创建CusForAcc成功")
            signal['cus'] = 0
            if data['accounttype'] == '0':
                saveacc = SaveAcc.objects.create(
                    accountid=acc,
                    interestrate=float(data['interestrate']),
                    savetype=data['savetype'],
                )
                print("创建SaveAcc成功")
                signal['sorc'] = 0
            elif data['accounttype'] == '1':
                checkacc = CheckAcc.objects.create(
                    accountid=acc,
                    overdraft=float(data['overdraft']),
                )
                print("创建CheckAcc成功")
                signal['sorc'] = 0
        except:
            save_succ = 0
            if signal['acc'] == 0:
                Accounts.objects.get(accountid=data['accountid']).delete()
    return render(request, "manager/account/addSucc.html", {"save_succ":save_succ, "signal":signal})


def account_all(request):
    saveaccs = SaveAcc.objects.all()
    checkaccs = CheckAcc.objects.all()
    return render(request, "manager/account/query.html", locals())


@csrf_exempt
def account_query(request):
    saveaccs = SaveAcc.objects.all()
    checkaccs = CheckAcc.objects.all()
    if request.method == 'POST':
        query_dict = post_to_dict(request.POST, 1)
        if 'overdraft' not in request.POST.dict():  # 储蓄账户
            saveaccs = saveaccs.filter(**query_dict)
        if 'overdraft' in request.POST.dict():  # 支票账户
            checkaccs = checkaccs.filter(**query_dict)
    return render(request, "manager/account/query.html", locals())


def account_delete(request, acc_id):
    Accounts.objects.filter(accountid=acc_id).delete()
    saveaccs = SaveAcc.objects.all()
    checkaccs = CheckAcc.objects.all()
    return render(request, "manager/account/query.html", locals())


def account_modify(request, acc_id):
    try:
        account = SaveAcc.objects.get(accountid=acc_id)
        acctype = "0"
    except:
        account = CheckAcc.objects.get(accountid=acc_id)
        acctype = "1"
    return render(request, "manager/account/modify.html", locals())


@csrf_exempt
def account_modify_succ(request, acc_id):
    try:
        account = SaveAcc.objects.get(accountid=acc_id)
        acctype = "0"
    except:
        account = CheckAcc.objects.get(accountid=acc_id)
        acctype = "1"
    modify_dict = post_to_dict(request.POST, 0)
    modify_dict.pop('accountid')
    modify_succ = 1
    if request.method == 'POST':
        # try:
        if acctype == "0":
            account.interestrate = float(modify_dict['interestrate'])
            account.savetype = modify_dict['savetype']
            account.save()
        if acctype == "1":
            account.overdraft = float(modify_dict['overdraft'])
            account.save()
        Accounts.objects.filter(accountid=acc_id).update(
            money=float(modify_dict['accountid__money']),
            settime=modify_dict['accountid__settime']
        )
        # except:
        #     modify_succ = 0
    return render(request, "manager/account/modifySucc.html", {"modify_succ":modify_succ})


def loan_add(request):
    cus_ids = Customer.objects.values_list("cusid")
    cus_ids = [i[0] for i in cus_ids]
    bank_names = Bank.objects.values_list("bankname")
    bank_names = [i[0] for i in bank_names]
    return render(request, "manager/loan/add.html", locals())


@csrf_exempt
def loan_add_succ(request):
    save_succ = 1
    signal = {
        'loan':1,
        'cus':1,
    }
    if request.method == 'POST':
        data = post_to_dict(request.POST, 0)
        cus_ids = data['cusid'].split(',')
        # cus_ids = [i[0]*18 for i in cus_ids]
        print(data)
        try:
            bank = Bank.objects.get(bankname=data['bankname'])
            loan = Loan.objects.create(
                loanid=data['loanid'],
                money=float(data['money']),
                moneyleft=float(data['money']),
                bank=bank,
                state="0",
                settime=data['settime'],
            )
            print("创建Loan成功")
            print(loan)
            signal['loan'] = 0
            loan = Loan.objects.get(loanid=data['loanid'])
            for cus_id in cus_ids:
                cus = Customer.objects.get(cusid=cus_id)
                # acc.customers.add(cus)
                cusforloan = CusForLoan.objects.create(
                    loanid=loan,
                    cusid=cus,
                )
                print(cus_id,'done')
            print("创建CusForLoan成功")
            signal['cus'] = 0
        except:
            save_succ = 0
            if signal['loan'] == 0:
                Loan.objects.get(laonid=data['laonid']).delete()
    return render(request, "manager/loan/addSucc.html", {"save_succ":save_succ, "signal":signal})


def loan_all(request):
    data = Loan.objects.all()
    statemap = {
        '0': "未发放",
        '1': "发放中",
        '2': "发放完成",
        '3': "异常",
    }
    bank_names = Bank.objects.values_list("bankname")
    bank_names = [i[0] for i in bank_names]
    return render(request, "manager/loan/query.html", locals())


def loan_delete(request, loan_id):
    loan = Loan.objects.get(loanid=loan_id)
    msg = 0
    if loan.state == "1":
        msg = "贷款发放中，不能删除"
    else:
        loan.delete()
    data = Loan.objects.all()
    statemap = {
        '0': "未发放",
        '1': "发放中",
        '2': "发放完成",
        '3': "异常",
    }
    bank_names = Bank.objects.values_list("bankname")
    bank_names = [i[0] for i in bank_names]
    return render(request, "manager/loan/query.html", locals())


@csrf_exempt
def loan_query(request):
    loans = Loan.objects.all()
    bank_names = Bank.objects.values_list("bankname")
    bank_names = [i[0] for i in bank_names]
    statemap = {
        '0': "未发放",
        '1': "发放中",
        '2': "发放完成",
        '3': "异常",
    }
    if request.method == 'POST':
        query_dict = post_to_dict(request.POST, 1)
        data = loans.filter(**query_dict)
    return render(request, "manager/loan/query.html", locals())


def ajax_loan_pay_get_custs(request):
    loanid = request.GET.get('loanid')
    loan = Loan.objects.get(loanid=loanid)
    custs = loan.customers.all()
    cus_ids = []
    for cust in custs:
        cus_ids.append(cust.cusid)
    print(cus_ids)
    return JsonResponse({"cus_ids":cus_ids, "moneyleft":loan.moneyleft})


def loan_pay(request):
    loan_ids = Loan.objects.filter(state__in=["0","1"]).values_list("loanid")
    loan_ids = [i[0] for i in loan_ids]
    return render(request, "manager/loan/pay.html", locals())


@csrf_exempt
def loan_pay_succ(request):
    if request.method == 'POST':
        pay_dict = post_to_dict(request.POST, 0)
        loan = Loan.objects.get(loanid=pay_dict['loanid'])
        cus = Customer.objects.get(cusid=pay_dict['cusid'])
        paymoney = float(pay_dict['money'])
        moneyleft = float(loan.moneyleft)
        msg = "发放成功"
        if paymoney > moneyleft or moneyleft == 0.0:
            msg = "余额不足"
        elif paymoney <= 0.0:
            msg = "发放金额须大于0"
        elif paymoney == moneyleft:
            try:
                payinfo = PayInfo.objects.create(
                    loanid=loan,
                    cusid=cus,
                    money=paymoney,
                    paytime=pay_dict['paytime']
                )
                loan.state = "2"
                loan.moneyleft = 0.0
                loan.save()
            except:
                msg = "发放失败"
        else:
            try:
                payinfo = PayInfo.objects.create(
                    loanid=loan,
                    cusid=cus,
                    money=paymoney,
                    paytime=pay_dict['paytime']
                )
                loan.state = "1"
                loan.moneyleft = moneyleft - paymoney
                loan.save()
            except:
                msg = "发放失败"
    return render(request, "manager/loan/paySucc.html", {"msg":msg})