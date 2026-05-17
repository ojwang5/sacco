# SACCO System API Endpoints Documentation

## Overview
The SACCO system now includes RESTful API endpoints for loan calculations, withdrawal applications, and loan status management. All endpoints require authentication via Django session/login.

---

## API Endpoints

### 1. Loan Calculator API

**Endpoint:** `POST /sacco/api/loan-calculator/`

**Authentication:** Required (Login)

**Purpose:** Calculate loan repayment details (monthly payment, total interest, total repayment)

**Request Format:**
```json
{
  "loan_amount": 1000000,
  "interest_rate": 12.5,
  "loan_term_months": 24
}
```

**Request Parameters:**
- `loan_amount` (float, required): Loan amount in UGX
- `interest_rate` (float, required): Annual interest rate (%)
- `loan_term_months` (int, required): Loan duration in months

**Success Response (200):**
```json
{
  "success": true,
  "monthly_payment": 46296.96,
  "total_interest": 111137.09,
  "total_repayment": 1111137.09,
  "loan_amount": 1000000,
  "interest_rate": 12.5,
  "loan_term_months": 24
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Loan amount and term must be greater than 0"
}
```

**Example cURL Request:**
```bash
curl -X POST http://localhost:8000/sacco/api/loan-calculator/ \
  -H "Content-Type: application/json" \
  -d '{
    "loan_amount": 1000000,
    "interest_rate": 12.5,
    "loan_term_months": 24
  }'
```

**Example JavaScript/Fetch:**
```javascript
const calculateLoan = async () => {
  const response = await fetch('/sacco/api/loan-calculator/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      loan_amount: 1000000,
      interest_rate: 12.5,
      loan_term_months: 24
    })
  });
  
  const data = await response.json();
  if (data.success) {
    console.log('Monthly Payment:', data.monthly_payment);
    console.log('Total Interest:', data.total_interest);
    console.log('Total Repayment:', data.total_repayment);
  } else {
    console.error('Error:', data.error);
  }
};
```

---

### 2. Withdrawal Application API

**Endpoint:** `POST /sacco/api/withdrawal-apply/`

**Authentication:** Required (Member Login)

**Purpose:** Submit a withdrawal application

**Request Format:**
```json
{
  "amount": 50000,
  "purpose": "School fees for children",
  "payment_method": "mobile_money"
}
```

**Request Parameters:**
- `amount` (decimal, required): Withdrawal amount in UGX
- `purpose` (string, required): Purpose of withdrawal
- `payment_method` (string, required): Payment method (cash, mobile_money, bank_transfer)

**Success Response (201):**
```json
{
  "success": true,
  "message": "Withdrawal application submitted successfully",
  "withdrawal_id": 5,
  "amount": "50000",
  "status": "pending",
  "purpose": "School fees for children",
  "payment_method": "mobile_money",
  "application_date": "2026-04-03"
}
```

**Error Responses:**

Insufficient Balance (400):
```json
{
  "success": false,
  "error": "Insufficient balance. Current balance: UGX 30000.00"
}
```

Not a Member (403):
```json
{
  "success": false,
  "error": "You are not a registered member"
}
```

Invalid Data (400):
```json
{
  "success": false,
  "error": "Purpose is required"
}
```

**Example cURL Request:**
```bash
curl -X POST http://localhost:8000/sacco/api/withdrawal-apply/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50000,
    "purpose": "School fees",
    "payment_method": "mobile_money"
  }'
```

**Example JavaScript/Fetch:**
```javascript
const applyWithdrawal = async () => {
  const response = await fetch('/sacco/api/withdrawal-apply/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      amount: 50000,
      purpose: 'School fees for children',
      payment_method: 'mobile_money'
    })
  });
  
  const data = await response.json();
  if (data.success) {
    console.log('Withdrawal ID:', data.withdrawal_id);
    console.log('Status:', data.status);
    console.log('Application Date:', data.application_date);
  } else {
    console.error('Error:', data.error);
  }
};
```

---

### 3. Get Loan Status API

**Endpoint:** `GET /sacco/api/loan/<loan_id>/status/`

**Authentication:** Required (Login)

**Purpose:** Get detailed loan information and current status

**URL Parameters:**
- `loan_id` (int, required): Loan ID

**Success Response (200):**
```json
{
  "success": true,
  "loan_id": 1,
  "member_name": "John Doe",
  "amount": "1000000",
  "interest_rate": "12.50",
  "term_months": 24,
  "purpose": "Business expansion",
  "status": "approved",
  "application_date": "2026-03-15",
  "approval_date": "2026-03-20"
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "Loan not found"
}
```

**Permission Denied (403):**
```json
{
  "success": false,
  "error": "Permission denied"
}
```

**Example cURL Request:**
```bash
curl http://localhost:8000/sacco/api/loan/1/status/
```

**Example JavaScript/Fetch:**
```javascript
const getLoanStatus = async (loanId) => {
  const response = await fetch(`/sacco/api/loan/${loanId}/status/`);
  const data = await response.json();
  
  if (data.success) {
    console.log('Loan Status:', data.status);
    console.log('Amount:', data.amount);
  } else {
    console.error('Error:', data.error);
  }
};
```

---

### 4. Approve Loan API

**Endpoint:** `POST /sacco/api/loan/<loan_id>/approve/`

**Authentication:** Required (Admin/Superadmin Only)

**Purpose:** Approve a pending loan application

**URL Parameters:**
- `loan_id` (int, required): Loan ID to approve

**Success Response (200):**
```json
{
  "success": true,
  "message": "Loan approved successfully",
  "loan_id": 1,
  "status": "approved",
  "approval_date": "2026-04-03"
}
```

**Error Responses:**

Already Approved (400):
```json
{
  "success": false,
  "error": "Loan is already approved"
}
```

Loan Not Found (404):
```json
{
  "success": false,
  "error": "Loan not found"
}
```

Permission Denied (403):
```json
{
  "success": false,
  "error": "Permission denied. Admin access required"
}
```

**Example cURL Request:**
```bash
curl -X POST http://localhost:8000/sacco/api/loan/1/approve/
```

**Example JavaScript/Fetch:**
```javascript
const approveLoan = async (loanId) => {
  const response = await fetch(`/sacco/api/loan/${loanId}/approve/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }
  });
  
  const data = await response.json();
  if (data.success) {
    console.log('Loan approved on:', data.approval_date);
  } else {
    console.error('Error:', data.error);
  }
};
```

**Automatic Actions:**
- Sets loan status to "approved"
- Sets approval_date to current date
- Creates notification for member
- Notifies all other admin users

---

### 5. Reject Loan API

**Endpoint:** `POST /sacco/api/loan/<loan_id>/reject/`

**Authentication:** Required (Admin/Superadmin Only)

**Purpose:** Reject a pending loan application

**URL Parameters:**
- `loan_id` (int, required): Loan ID to reject

**Success Response (200):**
```json
{
  "success": true,
  "message": "Loan rejected successfully",
  "loan_id": 1,
  "status": "rejected",
  "approval_date": "2026-04-03"
}
```

**Error Responses:**

Already Rejected (400):
```json
{
  "success": false,
  "error": "Loan is already rejected"
}
```

Loan Not Found (404):
```json
{
  "success": false,
  "error": "Loan not found"
}
```

Permission Denied (403):
```json
{
  "success": false,
  "error": "Permission denied. Admin access required"
}
```

**Example cURL Request:**
```bash
curl -X POST http://localhost:8000/sacco/api/loan/1/reject/
```

**Example JavaScript/Fetch:**
```javascript
const rejectLoan = async (loanId) => {
  const response = await fetch(`/sacco/api/loan/${loanId}/reject/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }
  });
  
  const data = await response.json();
  if (data.success) {
    console.log('Loan rejected on:', data.approval_date);
  } else {
    console.error('Error:', data.error);
  }
};
```

**Automatic Actions:**
- Sets loan status to "rejected"
- Sets approval_date to current date
- Creates notification for member
- Notifies all other admin users

---

## Common Response Structure

All API endpoints follow this response structure:

### Success Response
```json
{
  "success": true,
  "message": "Operation description",
  "data": {}
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error description"
}
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success (GET, POST) |
| 201 | Created (Resource created) |
| 400 | Bad Request (Invalid parameters) |
| 403 | Forbidden (Permission denied) |
| 404 | Not Found |
| 405 | Method Not Allowed |

---

## Authentication

All API endpoints require authentication. You must be logged in via Django session.

**How to authenticate:**
1. Make a POST request to `/sacco/login/` with credentials
2. The session cookie will be automatically set
3. Use this cookie in subsequent API requests

---

## Error Handling

Always check the `success` field in responses. If `success` is `false`, read the `error` field for details.

**Example Error Handling:**
```javascript
const apiCall = async (url, options = {}) => {
  try {
    const response = await fetch(url, options);
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error);
    }
    
    return data;
  } catch (error) {
    console.error('API Error:', error.message);
    // Handle error appropriately
  }
};
```

---

## Rate Limiting

Currently no rate limiting is implemented. It is recommended to implement rate limiting in production.

---

## CSRF Protection

Django's CSRF protection is enabled. When making POST requests, include the CSRF token:

```javascript
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

const response = await fetch('/sacco/api/loan-calculator/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken,
  },
  body: JSON.stringify(data)
});
```

---

## Testing the APIs

### Using cURL

**Test Loan Calculator:**
```bash
curl -X POST http://localhost:8000/sacco/api/loan-calculator/ \
  -H "Content-Type: application/json" \
  -d '{"loan_amount": 1000000, "interest_rate": 12.5, "loan_term_months": 24}'
```

**Test Withdrawal Application:**
```bash
curl -X POST http://localhost:8000/sacco/api/withdrawal-apply/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 50000, "purpose": "Personal need", "payment_method": "mobile_money"}'
```

**Test Get Loan Status:**
```bash
curl http://localhost:8000/sacco/api/loan/1/status/
```

**Test Approve Loan:**
```bash
curl -X POST http://localhost:8000/sacco/api/loan/1/approve/
```

**Test Reject Loan:**
```bash
curl -X POST http://localhost:8000/sacco/api/loan/1/reject/
```

---

## Integration Examples

### Mobile App Integration
Use these endpoints to build mobile applications:
- Login endpoint for authentication
- Loan calculator for real-time calculations
- Withdrawal application for easy application submission
- Loan status for tracking application progress

### Web Dashboard Integration
- Embed loan calculator widget in member dashboard
- Show withdrawal status with notifications
- Admin loan management interface

### Third-Party Integration
- Export loan data via APIs
- Integrate with payment gateways
- Sync with external accounting systems

---

## Future Enhancements

Planned API improvements:
- Pagination for list endpoints
- Filtering and search capabilities
- Bulk operations
- Webhooks for real-time updates
- API key authentication (optional)
- Rate limiting
- API usage analytics
- Swagger/OpenAPI documentation

---

## Support & Troubleshooting

### Common Issues

**401 Unauthorized**
- Ensure you are logged in
- Check session cookie is valid

**403 Forbidden**
- Check user role/permissions
- Admin endpoints require staff/superuser status

**400 Bad Request**
- Verify JSON format is correct
- Check all required parameters are provided
- Validate parameter types and values

**404 Not Found**
- Verify loan/withdrawal ID exists
- Check ID is correct and resource hasn't been deleted

---

## Version History

- **v1.0** (2026-04-03) - Initial API release
  - Loan calculator endpoint
  - Withdrawal application endpoint
  - Loan status management endpoints
  - Notification integration
