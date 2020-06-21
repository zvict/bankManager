from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart_query),
    path('chart/query/', views.chart_query),

    path('customer/add/', views.customer_add),
    path('customer/addsucc/', views.customer_add_succ),
    path('customer/all/', views.customer_all),
    path('customer/query/', views.customer_query),
    path('customer/delete/', views.customer_all),
    path('customer/delete/<str:cus_id>/', views.customer_delete),
    path('customer/modify/', views.customer_all),
    path('customer/modify/<str:cus_id>/', views.customer_modify),
    path('customer/modifysucc/<str:cus_id>/', views.customer_modify_succ),

    path('account/add/', views.account_add),
    path('account/add/ajax/getemps/', views.ajax_account_add_get_emps),
    path('account/addsucc/', views.account_add_succ),
    path('account/all/', views.account_all),
    path('account/query/', views.account_query),
    path('account/delete/', views.account_all),
    path('account/delete/<str:acc_id>/', views.account_delete),
    path('account/modify/', views.account_all),
    path('account/modify/<str:acc_id>/', views.account_modify),
    path('account/modifysucc/<str:acc_id>/', views.account_modify_succ),

    path('loan/add/', views.loan_add),
    path('loan/addsucc/', views.loan_add_succ),
    path('loan/all/', views.loan_all),
    path('loan/query/', views.loan_query),
    path('loan/delete/', views.loan_all),
    path('loan/delete/<str:loan_id>/', views.loan_delete),
    path('loan/pay/', views.loan_pay),
    path('loan/pay/ajax/getcusts/', views.ajax_loan_pay_get_custs),
    path('loan/paysucc/', views.loan_pay_succ),
]