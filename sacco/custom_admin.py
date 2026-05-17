from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path

class CustomAdminSite(admin.AdminSite):
    site_header = 'Sacco Management System'
    site_title = 'Sacco Admin'
    index_title = 'Site Administration'

    def index(self, request, extra_context=None):
        app_list = self.get_app_list(request)
        context = {
            **self.each_context(request),
            'app_list': app_list,
        }
        if extra_context:
            context.update(extra_context)
        return TemplateResponse(request, 'admin/site_admin.html', context)

custom_admin_site = CustomAdminSite(name='custom_admin')

# Import custom ModelAdmin classes
from sacco.admin import MemberAdmin, SavingsAdmin, LoanAdmin, PaymentAdmin

# Register your models with custom_admin_site using the custom admin classes
from sacco.models import Member, Savings, Loan, Payment
custom_admin_site.register(Member, MemberAdmin)
custom_admin_site.register(Savings, SavingsAdmin)
custom_admin_site.register(Loan, LoanAdmin)
custom_admin_site.register(Payment, PaymentAdmin)

urlpatterns = custom_admin_site.urls
