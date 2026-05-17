from django.urls import path
from . import views

app_name = 'sacco'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/<str:phone>/', views.verify_otp, name='verify_otp'),
    path('set-password/<str:phone>/', views.set_password, name='set_password'),
    path('settings/', views.settings, name='settings'),
    path('reports/', views.reports, name='reports'),
    path('contact/', views.contact, name='contact'),
    path('reports/export-members/', views.export_members_report, name='export_members_report'),
    path('export/<str:model_name>/<str:format_type>/', views.export_data, name='export_data'),

    path('members/', views.members_list, name='members_list'),
    path('members/add/', views.add_member, name='add_member'),
    path('members/<int:member_id>/edit/', views.edit_member, name='edit_member'),
    path('members/<int:member_id>/delete/', views.delete_member, name='delete_member'),

    path('loans/', views.loans_list, name='loans_list'),
    path('loans/add/', views.add_loan, name='add_loan'),
    path('loans/<int:loan_id>/edit/', views.edit_loan, name='edit_loan'),
    path('loans/<int:loan_id>/delete/', views.delete_loan, name='delete_loan'),
    path('loans/<int:loan_id>/approve/', views.approve_loan, name='approve_loan'),
    path('loans/<int:loan_id>/reject/', views.reject_loan, name='reject_loan'),

    path('savings/', views.savings_list, name='savings_list'),
    path('savings/add/', views.add_savings, name='add_savings'),
    path('savings/<int:transaction_id>/edit/', views.edit_savings, name='edit_savings'),
    path('savings/<int:transaction_id>/delete/', views.delete_savings, name='delete_savings'),

    path('payments/', views.payments_list, name='payments_list'),
    path('payments/add/', views.add_payment, name='add_payment'),
    path('apply-loan/', views.apply_loan, name='apply_loan'),
    path('make-payment/', views.make_payment, name='make_payment'),

    path('withdrawals/', views.withdrawals_list, name='withdrawals_list'),
    path('withdrawals/add/', views.add_withdrawal, name='add_withdrawal'),
    path('withdrawals/<int:withdrawal_id>/edit/', views.edit_withdrawal, name='edit_withdrawal'),
    path('withdrawals/<int:withdrawal_id>/delete/', views.delete_withdrawal, name='delete_withdrawal'),
    path('withdrawals/apply/', views.apply_withdrawal, name='apply_withdrawal'),
    path('withdrawals/my/', views.my_withdrawals, name='my_withdrawals'),

    # Notification URLs
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/admin/', views.admin_notifications, name='admin_notifications'),
    path('notifications/superadmin/', views.superadmin_notifications, name='superadmin_notifications'),
    path('notifications/create/', views.create_notification, name='create_notification'),
    path('notifications/<int:notification_id>/', views.notification_detail, name='notification_detail'),
    path('notifications/<int:notification_id>/resolve/', views.mark_notification_resolved, name='mark_notification_resolved'),

    # Calculator UI
    path('loan-calculator/', views.loan_calculator, name='loan_calculator'),

    # API Endpoints
    path('api/loan-calculator/', views.api_loan_calculator, name='api_loan_calculator'),
    path('api/withdrawal-apply/', views.api_withdrawal_apply, name='api_withdrawal_apply'),

    path('api/loan/<int:loan_id>/status/', views.api_loan_status, name='api_loan_status'),
    path('api/loan/<int:loan_id>/approve/', views.api_loan_status_approve, name='api_loan_approve'),
    path('api/loan/<int:loan_id>/reject/', views.api_loan_status_reject, name='api_loan_reject'),
]
