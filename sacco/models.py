from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

class Member(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('superadmin', 'Super Admin'),
    ]

    member_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    join_date = models.DateField(default=timezone.now)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.member_id})"

    class Meta:
        ordering = ['name']

class Savings(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    transaction_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    transaction_date = models.DateField(default=timezone.now)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.member.name} - UGX {self.amount}"

    class Meta:
        ordering = ['-transaction_date']

class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    loan_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    term_months = models.PositiveIntegerField()
    purpose = models.TextField()
    application_date = models.DateField(default=timezone.now)
    approval_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    guarantor1 = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='guarantor1_loans')
    guarantor2 = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True, related_name='guarantor2_loans')

    def __str__(self):
        return f"Loan #{self.loan_id} - {self.member.name} - UGX {self.amount}"

    class Meta:
        ordering = ['-application_date']

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    payment_id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')

    def __str__(self):
        return f"Payment - Loan #{self.loan.loan_id} - UGX {self.amount}"

    class Meta:
        ordering = ['-payment_date']

class Withdrawal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    withdrawal_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    purpose = models.TextField()
    application_date = models.DateField(default=timezone.now)
    approval_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='approved_withdrawals')

    def __str__(self):
        return f"Withdrawal #{self.withdrawal_id} - {self.member.name} - UGX {self.amount}"

    class Meta:
        ordering = ['-application_date']

class OTP(models.Model):
    phone = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    purpose = models.CharField(max_length=20, choices=[
        ('password_reset', 'Password Reset'),
        ('account_creation', 'Account Creation'),
    ])

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.phone} - {self.purpose}"

    class Meta:
        ordering = ['-created_at']


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('loan_application', 'Loan Application'),
        ('withdrawal_application', 'Withdrawal Application'),
        ('loan_approval', 'Loan Approval'),
        ('withdrawal_approval', 'Withdrawal Approval'),
        ('loan_rejection', 'Loan Rejection'),
        ('withdrawal_rejection', 'Withdrawal Rejection'),
        ('admin_message', 'Admin Message'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('read', 'Read'),
        ('resolved', 'Resolved'),
    ]

    notification_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Foreign keys to related objects (one will be null depending on type)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, blank=True, null=True)
    withdrawal = models.ForeignKey(Withdrawal, on_delete=models.CASCADE, blank=True, null=True)
    
    # Admin who processed/replied to the notification
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='processed_notifications')

    def __str__(self):
        return f"{self.notification_type} - {self.member.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['member', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]


class NotificationReply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='replies')
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notification_replies')
    reply_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_internal = models.BooleanField(default=False)  # True if only visible to admins

    def __str__(self):
        return f"Reply to {self.notification.title} by {self.admin_user.username if self.admin_user else 'Unknown'}"

    class Meta:
        ordering = ['created_at']

