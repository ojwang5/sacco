# Loan Status Management & Notifications

## Overview
The loan status management system now includes automatic notifications for both members and admins when loan applications are approved or rejected. Admins can manage loan statuses through two interfaces:
1. Django Admin Interface (recommended for bulk actions)
2. Frontend Web Interface (for individual loan management)

## Loan Status Options

### Status Types
- **Pending** (Default): New loan applications awaiting review
- **Approved**: Loan has been approved by admin
- **Rejected**: Loan has been rejected by admin

## Admin Interfaces for Managing Loans

### 1. Django Admin Interface (Recommended for Bulk Actions)

#### Accessing Django Admin
1. Navigate to `/admin/`
2. Login with admin credentials
3. Click on "Loans" in the admin dashboard

#### Bulk Status Management
The Django admin interface provides quick actions for managing multiple loans at once:

**Approve Loans:**
1. Select one or more pending loans using the checkboxes
2. From the "Action:" dropdown, select "✓ Approve selected loans and notify members"
3. Click "Go"
4. Notifications automatically sent to:
   - The loan applicant (member)
   - All other admins

**Reject Loans:**
1. Select one or more pending loans using the checkboxes
2. From the "Action:" dropdown, select "✗ Reject selected loans and notify members"
3. Click "Go"
4. Notifications automatically sent to:
   - The loan applicant (member)
   - All other admins

#### Features
- Approval/Rejection date automatically set to current date
- Notifications include loan details (amount, interest, term)
- Clean confirmation message showing count of loans processed
- Filtered view by status for easy navigation

### 2. Frontend Web Interface

#### Accessing Loan Management
1. Login as admin
2. Click "Loans" in the navigation menu
3. View the loans list table

#### Loan Status Indicators
- **Yellow Badge - Pending**: Loan awaiting review
- **Green Badge - Approved**: Loan has been approved
- **Red Badge - Rejected**: Loan has been rejected

#### Individual Loan Management
For pending loans, quick action buttons are displayed:
- **Approve Button**: Directly approve the loan (green button with ✓)
- **Reject Button**: Directly reject the loan (red button with ✗)
- **Edit Button**: Open full loan editor for detailed changes
- **Delete Button**: Remove the loan

#### Using the Full Loan Editor
1. Click "Edit" button on any loan row
2. In the loan form:
   - Change the status dropdown (Pending → Approved or Rejected)
   - Update other loan details if needed
3. Click "Save" to update
4. Notifications are automatically created based on status change

#### Action Confirmation
- Status change confirmations show detailed messages
- "Loan updated and approved! Member notified."
- "Loan updated and rejected! Member notified."

## Notification Details

### What Members Receive
When a loan status changes, the member receives a notification with:

**For Approval:**
- Title: "Your Loan Application has been Approved"
- Message includes:
  - Loan amount (UGX)
  - Interest rate (%)
  - Loan term (months)
  - Congratulations message

**For Rejection:**
- Title: "Your Loan Application has been Rejected"
- Message includes:
  - Loan amount
  - Note to contact admin for details

### What Admins Receive
Other admin users receive notifications about loan decisions made by colleagues:

**For Approval:**
- Title: "Loan Approved: [Member Name]"
- Message includes:
  - Approving admin's name
  - Loan ID
  - Member name
  - Loan amount

**For Rejection:**
- Title: "Loan Rejected: [Member Name]"
- Message includes:
  - Rejecting admin's name
  - Loan ID
  - Member name
  - Loan amount

### Accessing Notifications

#### Members
1. Click "Notifications" in the main menu
2. View all pending, read, and resolved notifications
3. Click on any notification to see details and any replies from admins

#### Admins
1. Click "Notifications" in the main menu
2. View the Admin Notifications Dashboard
3. See categorized view (Pending, Read, Resolved)
4. Add replies or internal notes to any notification

## Workflow Example

### Step 1: Member Applies for Loan
- Member fills out loan application form
- Application is submitted
- System creates a "Loan Application" notification
- Admin sees it in the notification dashboard

### Step 2: Admin Reviews Application
- Admin goes to Loans page
- Sees loan in "Pending" status (yellow badge)
- Clicks "Edit" to review details
- Changes status to "Approved" or "Rejected"

### Step 3: Notifications Sent
- Member receives notification of decision
- Other admins are notified of the decision
- Notifications appear in both member and admin notification panels

### Step 4: Member Views Response
- Member checks their Notifications
- Sees the approval/rejection notification
- Can view details of the decision
- Can see any admin comments/replies

## Technical Implementation

### Views Modified
- `edit_loan`: Now tracks status changes and creates notifications
- `delete_loan`: Admin-only access added
- `loans_list`: Enhanced display with status badges and quick actions

### Admin Actions
- `approve_loans`: Bulk approve with automatic notifications
- `reject_loans`: Bulk reject with automatic notifications

### Models Used
- `Notification`: Stores notification records
- `NotificationReply`: Stores admin replies/comments
- `Loan`: Updated approval_date when status changes

### Notification Types
- `loan_application`: Initial loan application
- `loan_approval`: Loan has been approved
- `loan_rejection`: Loan has been rejected

## Best Practices

### For Admins
1. **Review Before Approving**: Click Edit to view full loan details including guarantors
2. **Set Interest Rates**: Ensure interest rate and term are set before approval
3. **Use Internal Notes**: Add comments/notes to notifications for other admins
4. **Bulk Operations**: Use Django admin for efficient bulk approvals
5. **Documentation**: Reject with detailed explanation for member benefit

### For Members
1. **Check Notifications**: Regularly visit Notifications to check application status
2. **Respond Quickly**: If admin requests more information, respond promptly
3. **Review Details**: Read full approval/rejection message for next steps

## Troubleshooting

### Notifications Not Appearing
- **Check Status**: Ensure loan status was actually changed
- **Check Member**: Verify member is properly linked to user account
- **Check Admin Role**: Ensure user has admin/superuser privileges
- **Database**: Run `python manage.py migrate` to ensure tables exist

### Status Won't Change in Frontend
- **Permissions**: Login as admin/superuser user
- **Permission Check**: Verify `request.user.is_staff` or `is_superuser`
- **Form**: Check that status field is not readonly in form

### Members Not Receiving Notifications
- **Member Link**: Verify member record is linked to User account
- **Admin Accounts**: Ensure admin users also have Member records with admin role

## Future Enhancements

Potential features to add:
1. **Loan Approval Conditions**: Add optional conditions to approval
2. **Approval Templates**: Create standard response templates
3. **Scheduled Notifications**: Send reminders for pending applications
4. **Approval Workflow**: Multi-step approval process with different admins
5. **Email Notifications**: Send email when status changes
6. **SMS Notifications**: Send SMS to member's phone
7. **Approval Comments**: Mandatory comment field for rejections

## Support

For issues related to loan status management:
1. Check Django logs: `python manage.py check`
2. Verify migrations: `python manage.py migrate`
3. Test notification creation in admin
4. Check member-user relationship in database
