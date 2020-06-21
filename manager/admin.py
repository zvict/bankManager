from django.contrib import admin

from .models import Bank, Accounts, Employee, Department, Customer, Loan

admin.site.register(Bank)
admin.site.register(Accounts)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Customer)
admin.site.register(Loan)
