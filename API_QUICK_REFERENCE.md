# SACCO API Quick Reference

## API Endpoints Summary

| Endpoint | Method | Purpose | Auth | Role |
|----------|--------|---------|------|------|
| `/api/loan-calculator/` | POST | Calculate loan payments | Yes | Any |
| `/api/withdrawal-apply/` | POST | Submit withdrawal | Yes | Member |
| `/api/loan/<id>/status/` | GET | Get loan details | Yes | Any |
| `/api/loan/<id>/approve/` | POST | Approve loan | Yes | Admin |
| `/api/loan/<id>/reject/` | POST | Reject loan | Yes | Admin |

---

## Quick Examples

### 1. Calculate Loan Repayment
```bash
curl -X POST http://localhost:8000/sacco/api/loan-calculator/ \
  -H "Content-Type: application/json" \
  -d '{
    "loan_amount": 1000000,
    "interest_rate": 12.5,
    "loan_term_months": 24
  }'
```

**Response:**
```json
{
  "success": true,
  "monthly_payment": 46296.96,
  "total_interest": 111137.09,
  "total_repayment": 1111137.09
}
```

---

### 2. Apply for Withdrawal
```bash
curl -X POST http://localhost:8000/sacco/api/withdrawal-apply/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50000,
    "purpose": "School fees",
    "payment_method": "mobile_money"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Withdrawal application submitted successfully",
  "withdrawal_id": 5,
  "status": "pending"
}
```

---

### 3. Check Loan Status
```bash
curl http://localhost:8000/sacco/api/loan/1/status/
```

**Response:**
```json
{
  "success": true,
  "loan_id": 1,
  "member_name": "John Doe",
  "amount": "1000000",
  "status": "approved"
}
```

---

### 4. Approve Loan (Admin Only)
```bash
curl -X POST http://localhost:8000/sacco/api/loan/1/approve/
```

**Response:**
```json
{
  "success": true,
  "message": "Loan approved successfully",
  "status": "approved"
}
```

---

### 5. Reject Loan (Admin Only)
```bash
curl -X POST http://localhost:8000/sacco/api/loan/1/reject/
```

**Response:**
```json
{
  "success": true,
  "message": "Loan rejected successfully",
  "status": "rejected"
}
```

---

## JavaScript Examples

### Loan Calculator
```javascript
async function calculateLoan() {
  const response = await fetch('/sacco/api/loan-calculator/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      loan_amount: 1000000,
      interest_rate: 12.5,
      loan_term_months: 24
    })
  });
  return await response.json();
}
```

### Withdrawal Application
```javascript
async function applyWithdrawal() {
  const response = await fetch('/sacco/api/withdrawal-apply/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      amount: 50000,
      purpose: 'School fees',
      payment_method: 'mobile_money'
    })
  });
  return await response.json();
}
```

### Check Loan Status
```javascript
async function checkLoanStatus(loanId) {
  const response = await fetch(`/sacco/api/loan/${loanId}/status/`);
  return await response.json();
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Not Found |
| 405 | Method Not Allowed |

---

## Common Errors

| Error | Solution |
|-------|----------|
| "Invalid JSON format" | Check JSON syntax |
| "Loan amount and term must be > 0" | Provide positive values |
| "Insufficient balance" | Request amount should not exceed balance |
| "Permission denied" | Login as admin for restricted endpoints |
| "Loan not found" | Verify loan ID exists |

---

## Authentication Flow

1. **Login** → `/sacco/login/` (POST)
2. **Session Set** → Automatic cookie handling
3. **Use APIs** → Include cookie in requests
4. **Logout** → `/sacco/logout/` (POST)

---

## Testing URLs

- **Member Dashboard:** `http://localhost:8000/sacco/`
- **Admin Dashboard:** `http://localhost:8000/sacco/` (as admin)
- **API Base:** `http://localhost:8000/sacco/api/`
- **Django Admin:** `http://localhost:8000/admin/`

---

## Response Format

All responses are JSON with this structure:
```json
{
  "success": true/false,
  "message": "Description",
  "error": "Error description (if failed)"
}
```

---

## Notes

- All endpoints require user to be logged in
- Admin endpoints require staff/superuser role
- Withdrawal amount cannot exceed member's current savings balance
- Notifications are automatically created when loans are approved/rejected
- Loan calculator uses amortization formula for accurate calculations
