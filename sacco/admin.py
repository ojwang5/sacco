from django.contrib import admin
from django.utils import timezone
from . import models
from .models import Member, Notification, Loan, Savings, Payment, Withdrawal, NotificationReply, OTP

class MemberAdmin(admin.ModelAdmin):
    list_display = ['member_id', 'name', 'id_number', 'phone', 'email', 'join_date', 'user']
    search_fields = ['name', 'id_number', 'phone', 'email']
    list_filter = ['join_date']
    readonly_fields = ['member_id']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'id_number', 'phone', 'email', 'address')
        }),
        ('Account Information', {
            'fields': ('user',),
            'description': 'Link to Django user account for login'
        }),
        ('System Fields', {
            'fields': ('member_id', 'join_date'),
            'classes': ('collapse',)
        }),
    )
    class Media:
        css = {
            'all': ('admin/css/bootstrap.min.css',)
        }

class SavingsAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'member', 'amount', 'transaction_type', 'transaction_date']
    search_fields = ['member__name', 'transaction_type']
    list_filter = ['transaction_type', 'transaction_date']
    class Media:
        css = {
            'all': ('admin/css/bootstrap.min.css',)
        }

class LoanAdmin(admin.ModelAdmin):
    list_display = ['loan_id', 'member', 'amount', 'interest_rate', 'term_months', 'status', 'application_date', 'approval_date']
    search_fields = ['member__name', 'purpose']
    list_filter = ['status', 'application_date']
    readonly_fields = ['loan_id', 'application_date']
    fieldsets = (
        ('Loan Information', {
            'fields': ('loan_id', 'member', 'amount', 'interest_rate', 'term_months', 'purpose')
        }),
        ('Guarantors', {
            'fields': ('guarantor1', 'guarantor2'),
        }),
        ('Status & Dates', {
            'fields': ('status', 'application_date', 'approval_date')
        }),
    )
    actions = ['approve_loans', 'reject_loans']

    def approve_loans(self, request, queryset):
        """Approve selected loans and create notifications"""
        count = 0
        for loan in queryset:
            if loan.status != 'approved':
                loan.status = 'approved'
                loan.approval_date = timezone.now().date()
                loan.save()
                count += 1
                
                # Create notification for member
                Notification.objects.create(
                    member=loan.member,
                    notification_type='loan_approval',
                    title=f'Your Loan Application has been Approved',
                    message=f'Congratulations! Your loan application for UGX {loan.amount} at {loan.interest_rate}% interest for {loan.term_months} months has been APPROVED.',
                    loan=loan,
                    admin_user=request.user,
                    status='unread'
                )
                
                # Create notification for admins (notification to the approver)
                admin_members = Member.objects.filter(role__in=['admin', 'superadmin'])
                for admin_member in admin_members:
                    if admin_member.user != request.user:  # Don't notify the approver
                        Notification.objects.create(
                            member=admin_member,
                            notification_type='loan_approval',
                            title=f'Loan Approved: {loan.member.name}',
                            message=f'Admin {request.user.first_name or request.user.username} has APPROVED loan #{loan.loan_id} for {loan.member.name} (UGX {loan.amount}).',
                            loan=loan,
                            admin_user=request.user,
                            status='unread'
                        )
        
        self.message_user(request, f"{count} loan(s) approved successfully. Notifications sent.")
    
    approve_loans.short_description = "✓ Approve selected loans and notify members"

    def reject_loans(self, request, queryset):
        """Reject selected loans and create notifications"""
        count = 0
        for loan in queryset:
            if loan.status != 'rejected':
                loan.status = 'rejected'
                loan.approval_date = timezone.now().date()
                loan.save()
                count += 1
                
                # Create notification for member
                Notification.objects.create(
                    member=loan.member,
                    notification_type='loan_rejection',
                    title=f'Your Loan Application has been Rejected',
                    message=f'Unfortunately, your loan application for UGX {loan.amount} has been REJECTED. Please contact admin for more details.',
                    loan=loan,
                    admin_user=request.user,
                    status='unread'
                )
                
                # Create notification for admins
                admin_members = Member.objects.filter(role__in=['admin', 'superadmin'])
                for admin_member in admin_members:
                    if admin_member.user != request.user:  # Don't notify the rejecter
                        Notification.objects.create(
                            member=admin_member,
                            notification_type='loan_rejection',
                            title=f'Loan Rejected: {loan.member.name}',
                            message=f'Admin {request.user.first_name or request.user.username} has REJECTED loan #{loan.loan_id} for {loan.member.name} (UGX {loan.amount}).',
                            loan=loan,
                            admin_user=request.user,
                            status='unread'
                        )
        
        self.message_user(request, f"{count} loan(s) rejected successfully. Notifications sent.")
    
    reject_loans.short_description = "✗ Reject selected loans and notify members"

    class Media:
        css = {
            'all': ('admin/css/bootstrap.min.css',)
        }

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'loan', 'amount', 'payment_date']
    search_fields = ['loan__member__name']
    list_filter = ['payment_date']
    class Media:
        css = {
            'all': ('admin/css/bootstrap.min.css',)
        }

class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['withdrawal_id', 'member', 'amount', 'status', 'application_date', 'approval_date', 'approved_by']
    search_fields = ['member__name', 'purpose']
    list_filter = ['status', 'application_date', 'payment_method']
    readonly_fields = ['withdrawal_id', 'application_date']
    actions = ['approve_withdrawals', 'reject_withdrawals']

    def approve_withdrawals(self, request, queryset):
        queryset.update(status='approved', approval_date=timezone.now().date(), approved_by=request.user)
        self.message_user(request, f"{queryset.count()} withdrawal(s) approved.")
    approve_withdrawals.short_description = "Approve selected withdrawals"

    def reject_withdrawals(self, request, queryset):
        queryset.update(status='rejected', approval_date=timezone.now().date(), approved_by=request.user)
        self.message_user(request, f"{queryset.count()} withdrawal(s) rejected.")
    reject_withdrawals.short_description = "Reject selected withdrawals"

    class Media:
        css = {
            'all': ('admin/css/bootstrap.min.css',)
        }


class NotificationReplyInline(admin.TabularInline):
    model = models.NotificationReply
    extra = 1
    readonly_fields = ['created_at', 'admin_user']
    fields = ['admin_user', 'reply_message', 'is_internal', 'created_at']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_id', 'member', 'notification_type', 'status', 'created_at', 'admin_user']
    search_fields = ['member__name', 'title', 'message']
    list_filter = ['notification_type', 'status', 'created_at']
    readonly_fields = ['notification_id', 'created_at', 'updated_at']
    inlines = [NotificationReplyInline]
    actions = ['mark_as_resolved', 'mark_as_read']

    fieldsets = (
        ('Notification Information', {
            'fields': ('notification_id', 'member', 'notification_type', 'title', 'message')
        }),
        ('Related Objects', {
            'fields': ('loan', 'withdrawal'),
        }),
        ('Status & Admin', {
            'fields': ('status', 'admin_user', 'created_at', 'updated_at')
        }),
    )

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved', admin_user=request.user)
        self.message_user(request, f"{queryset.count()} notification(s) marked as resolved.")
    mark_as_resolved.short_description = "Mark as resolved"

    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
        self.message_user(request, f"{queryset.count()} notification(s) marked as read.")
    mark_as_read.short_description = "Mark as read"

    class Media:
        css = {
            'all': ('admin/css/bootstrap.min.css',)
        }


class NotificationReplyAdmin(admin.ModelAdmin):
    list_display = ['reply_id', 'notification', 'admin_user', 'is_internal', 'created_at']
    search_fields = ['notification__title', 'admin_user__username', 'reply_message']
    list_filter = ['is_internal', 'created_at']
    readonly_fields = ['reply_id', 'created_at', 'notification']

    class Media:
        css = {
            'all': ('admin/css/bootstrap.min.css',)
        }

# Register only if model exists to avoid import/name mismatches causing server 500
_registration_map = {
    'Member': MemberAdmin,
    'Savings': SavingsAdmin,
    'Loan': LoanAdmin,
    'Payment': PaymentAdmin,
    'Withdrawal': WithdrawalAdmin,
    'Notification': NotificationAdmin,
    'NotificationReply': NotificationReplyAdmin,
    'OTP': None,  # OTP model doesn't need admin interface
}

for model_name, admin_cls in _registration_map.items():
    model = getattr(models, model_name, None)
    if not model:
        # model not defined exactly with this name in sacco.models — skip safely
        continue
    try:
        admin.site.register(model, admin_cls)
    except admin.sites.AlreadyRegistered:
        admin.site.unregister(model)
        admin.site.register(model, admin_cls)
