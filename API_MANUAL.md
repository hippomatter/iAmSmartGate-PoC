# iAmSmartGate API Manual

**Version:** 1.0  
**Last Updated:** January 25, 2026  
**Base URL (Production):** `https://iamsmartgate-backend.onrender.com`  
**Base URL (Localhost):** `http://localhost:5000`

---

## Quick Reference

| Method | Endpoint | Description | Auth | Section |
|--------|----------|-------------|------|---------|
| **Wallet APIs** |
| POST | `/api/login` | User authentication with iAmSmart eID | ❌ | [→](#1-user-login) |
| POST | `/api/apply-pass` | Submit site visit pass application | ✅ | [→](#2-apply-for-pass) |
| GET | `/api/my-passes` | Get user's passes | ✅ | [→](#3-get-my-passes) |
| GET | `/api/get-qr/<pass_id>` | Generate time-limited signed QR code | ✅ | [→](#4-generate-qr-code) |
| GET | `/api/user-info` | Get user profile information | ✅ | [→](#5-get-user-info) |
| GET | `/api/sites` | Get available access sites | ❌ | [→](#6-get-available-sites) |
| GET | `/api/purposes` | Get visit purposes | ❌ | [→](#7-get-visit-purposes) |
| **Gate APIs** |
| POST | `/api/gate-login` | Gate reader authentication | ❌ | [→](#1-gate-login) |
| POST | `/api/scan-qr` | Validate and verify QR code | ✅ | [→](#2-scan-qr-code) |
| **Admin APIs** |
| GET | `/admin/pending-passes` | Get pending pass applications | 🔐 | [→](#1-get-pending-passes) |
| GET | `/admin/all-passes` | Get all passes with filters | 🔐 | [→](#2-get-all-passes) |
| POST | `/admin/approve-pass/<pass_id>` | Approve pending pass | 🔐 | [→](#3-approve-pass) |
| POST | `/admin/reject-pass/<pass_id>` | Reject pending pass | 🔐 | [→](#4-reject-pass) |
| POST | `/admin/revoke-pass/<pass_id>` | Revoke active pass | 🔐 | [→](#5-revoke-pass) |
| POST | `/admin/set-signature-method` | Set QR signature method (RSA/FALCON) | 🔐 | [→](#6-set-signature-method) |
| POST | `/admin/pause-system` | Pause/resume entire system | 🔐 | [→](#7-pause-system) |
| POST | `/admin/pause-site` | Pause/resume specific site | 🔐 | [→](#8-pause-site) |
| GET | `/admin/system-status` | Get system status and signature method | 🔐 | [→](#9-get-system-status) |
| GET | `/admin/statistics` | Get system usage statistics | 🔐 | [→](#10-get-statistics) |
| GET | `/admin/audit-logs` | Get audit trail logs | 🔐 | [→](#11-get-audit-logs) |
| POST | `/admin/register-gate` | Register new gate reader | 🔐 | [→](#12-register-gate) |
| GET | `/admin/hsm/signature-logs` | Get quantum-safe HSM logs | 🔐 | [→](#13-get-hsm-signature-logs) |

**Legend:** ❌ No auth required | ✅ JWT token (User/Gate) | 🔐 Admin access

---

## Table of Contents

1. [Authentication](#authentication)
2. [Wallet APIs](#wallet-apis)
3. [Gate APIs](#gate-apis)
4. [Admin APIs](#admin-apis)
5. [Error Codes](#error-codes)

---

## Authentication

### JWT Token Authentication

Most endpoints require JWT token authentication. After successful login, include the token in request headers:

```
Authorization: Bearer <your_jwt_token>
```

**Token Expiration:** 24 hours

---

## Wallet APIs

Base path: `/api`

### 1. User Login

**Endpoint:** `POST /api/login`

**Description:** Authenticate user with iAmSmart eID credentials. Creates new user account if first login.

**Request Body:**
```json
{
  "iamsmart_id": "A123456(7)",
  "password": "user123",
  "device_id": "mobile-device-uuid"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "iamsmart_id": "A123456(7)",
    "public_key": "-----BEGIN PUBLIC KEY-----\n...",
    "device_id": "mobile-device-uuid",
    "created_at": "2026-01-25T10:30:00Z"
  },
  "message": "Login successful"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Missing credentials"
}
```

---

### 2. Apply for Pass

**Endpoint:** `POST /api/apply-pass`

**Description:** Submit a site visit pass application.

**Authentication:** Required (JWT Bearer token)

**Request Body:**
```json
{
  "site_id": "SITE001",
  "purpose_id": "MEETING",
  "visit_date_time": "2026-01-26T14:00:00Z",
  "device_id": "mobile-device-uuid"
}
```

**Response (201 Created):**
```json
{
  "pass": {
    "pass_id": "PASS12AB34CD56EF",
    "iamsmart_id": "A123456(7)",
    "site_id": "SITE001",
    "purpose_id": "MEETING",
    "status": "In Process",
    "visit_date_time": "2026-01-26T14:00:00Z",
    "created_timestamp": "2026-01-25T10:35:00Z"
  },
  "message": "Pass application submitted"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Missing required fields"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid or expired token"
}
```

---

### 3. Get My Passes

**Endpoint:** `GET /api/my-passes`

**Description:** Retrieve all passes for the authenticated user.

**Authentication:** Required (JWT Bearer token)

**Query Parameters:**
- `status` (optional): Filter by status (`In Process`, `Pass`, `Used`, `No Pass`, `Revoked`)

**Response (200 OK):**
```json
{
  "passes": [
    {
      "pass_id": "PASS12AB34CD56EF",
      "iamsmart_id": "A123456(7)",
      "site_id": "SITE001",
      "purpose_id": "MEETING",
      "status": "Pass",
      "signature_method": "FALCON-128",
      "visit_date_time": "2026-01-26T14:00:00Z",
      "approved_timestamp": "2026-01-25T11:00:00Z",
      "expiry_timestamp": "2026-01-26T11:00:00Z",
      "used_flag": false,
      "revoked_flag": false
    }
  ]
}
```

---

### 4. Generate QR Code

**Endpoint:** `GET /api/get-qr/<pass_id>`

**Description:** Generate a time-limited (60s) digitally signed QR code payload for an approved pass.

**Authentication:** Required (JWT Bearer token)

**URL Parameters:**
- `pass_id`: Pass ID (e.g., `PASS12AB34CD56EF`)

**Response (200 OK):**
```json
{
  "qr_payload": "{\"p\":\"PASS12AB34CD56EF\",\"t\":\"2026-01-25T12:00:00.000000\",\"s\":\"base64_signature_string...\"}",
  "signature_method": "FALCON-128",
  "expires_in": 60,
  "message": "QR code generated"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Pass not found"
}
```

**Response (403 Forbidden):**
```json
{
  "error": "Pass not approved (status: In Process)"
}
```

```json
{
  "error": "Pass already used"
}
```

```json
{
  "error": "Pass has been revoked"
}
```

```json
{
  "error": "Pass has expired"
}
```

---

### 5. Get User Info

**Endpoint:** `GET /api/user-info`

**Description:** Get authenticated user's profile information.

**Authentication:** Required (JWT Bearer token)

**Response (200 OK):**
```json
{
  "user": {
    "iamsmart_id": "A123456(7)",
    "public_key": "-----BEGIN PUBLIC KEY-----\n...",
    "device_id": "mobile-device-uuid",
    "created_at": "2026-01-25T10:30:00Z"
  }
}
```

---

### 6. Get Available Sites

**Endpoint:** `GET /api/sites`

**Description:** Get list of available access sites.

**Authentication:** Not required

**Response (200 OK):**
```json
{
  "sites": [
    {"site_id": "SITE001", "name": "Main Campus Gate"},
    {"site_id": "SITE002", "name": "Student Halls Entrance"},
    {"site_id": "SITE003", "name": "Research Center"},
    {"site_id": "SITE004", "name": "Library Access"}
  ]
}
```

---

### 7. Get Visit Purposes

**Endpoint:** `GET /api/purposes`

**Description:** Get list of available visit purposes.

**Authentication:** Not required

**Response (200 OK):**
```json
{
  "purposes": [
    {"purpose_id": "MEETING", "name": "Meeting"},
    {"purpose_id": "DELIVERY", "name": "Delivery"},
    {"purpose_id": "MAINTENANCE", "name": "Maintenance"},
    {"purpose_id": "VISITOR", "name": "Visitor"}
  ]
}
```

---

## Gate APIs

Base path: `/api`

> **🔒 Security Notice:** Gate API endpoints require HTTPS in production environments. HTTP requests will be rejected with `403 Forbidden`. Localhost development allows HTTP for testing purposes.

### 1. Gate Login

**Endpoint:** `POST /api/gate-login`

**Description:** Authenticate gate reader device. **Requires HTTPS in production.**

**Request Body:**
```json
{
  "tablet_id": "GATE001",
  "password": "gate123",
  "site_id": "SITE001"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "gate": {
    "tablet_id": "GATE001",
    "site_id": "SITE001",
    "location": "Main Campus Gate",
    "created_at": "2026-01-20T08:00:00Z"
  },
  "message": "Gate login successful"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

---

### 2. Scan QR Code

**Endpoint:** `POST /api/scan-qr`

**Description:** Validate and verify scanned QR code. Marks pass as used upon successful verification. **Requires HTTPS in production.**

**Authentication:** Required (JWT Bearer token - Gate)

**Request Body:**
```json
{
  "qr_payload": "{\"p\":\"PASS12AB34CD56EF\",\"t\":\"2026-01-25T12:00:00.000000\",\"s\":\"base64_signature_string...\"}"
}
```

**Response (200 OK) - Access Granted:**
```json
{
  "result": "Pass",
  "signature_method": "FALCON-128",
  "pass_details": {
    "pass_id": "PASS12AB34CD56EF",
    "user": "A123456(7)",
    "site": "SITE001",
    "purpose": "MEETING"
  },
  "message": "Access granted"
}
```

**Response (200 OK) - Access Denied:**
```json
{
  "result": "No Pass",
  "reason": "Pass already used"
}
```

**Possible Denial Reasons:**
- `"Invalid QR format"`
- `"Pass not found"`
- `"User not found"`
- `"Invalid signature"`
- `"QR code expired"` (>60 seconds old)
- `"System is paused"`
- `"Site is paused"`
- `"Pass not approved"`
- `"Pass already used"`
- `"Pass expired"`

**Response (200 OK) - Revoked Pass:**
```json
{
  "result": "Revoked",
  "reason": "Pass has been revoked"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Missing QR payload"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid or expired token"
}
```

---

## Admin APIs

Base path: `/admin`

### 1. Get Pending Passes

**Endpoint:** `GET /admin/pending-passes`

**Description:** Get all pass applications pending approval.

**Authentication:** Admin access required

**Response (200 OK):**
```json
{
  "passes": [
    {
      "pass_id": "PASS12AB34CD56EF",
      "iamsmart_id": "A123456(7)",
      "site_id": "SITE001",
      "purpose_id": "MEETING",
      "status": "In Process",
      "visit_date_time": "2026-01-26T14:00:00Z",
      "created_timestamp": "2026-01-25T10:35:00Z"
    }
  ]
}
```

---

### 2. Get All Passes

**Endpoint:** `GET /admin/all-passes`

**Description:** Get all passes with optional filtering.

**Authentication:** Admin access required

**Query Parameters:**
- `status` (optional): Filter by status
- `site_id` (optional): Filter by site

**Example:** `/admin/all-passes?status=Pass&site_id=SITE001`

**Response (200 OK):**
```json
{
  "passes": [
    {
      "pass_id": "PASS12AB34CD56EF",
      "iamsmart_id": "A123456(7)",
      "site_id": "SITE001",
      "purpose_id": "MEETING",
      "status": "Pass",
      "signature_method": "FALCON-128",
      "visit_date_time": "2026-01-26T14:00:00Z",
      "created_timestamp": "2026-01-25T10:35:00Z",
      "approved_timestamp": "2026-01-25T11:00:00Z",
      "expiry_timestamp": "2026-01-26T11:00:00Z"
    }
  ]
}
```

---

### 3. Approve Pass

**Endpoint:** `POST /admin/approve-pass/<pass_id>`

**Description:** Approve a pending pass application. Automatically assigns current system signature method.

**Authentication:** Admin access required

**URL Parameters:**
- `pass_id`: Pass ID to approve

**Request Body (Optional):**
```json
{
  "expiry_hours": 24
}
```

**Default:** 24 hours if not specified

**Response (200 OK):**
```json
{
  "message": "Pass approved",
  "pass": {
    "pass_id": "PASS12AB34CD56EF",
    "status": "Pass",
    "signature_method": "FALCON-128",
    "approved_timestamp": "2026-01-25T11:00:00Z",
    "expiry_timestamp": "2026-01-26T11:00:00Z"
  }
}
```

**Response (404 Not Found):**
```json
{
  "error": "Pass not found"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Pass cannot be approved (status: Pass)"
}
```

---

### 4. Reject Pass

**Endpoint:** `POST /admin/reject-pass/<pass_id>`

**Description:** Reject a pending pass application.

**Authentication:** Admin access required

**URL Parameters:**
- `pass_id`: Pass ID to reject

**Response (200 OK):**
```json
{
  "message": "Pass rejected",
  "pass": {
    "pass_id": "PASS12AB34CD56EF",
    "status": "No Pass"
  }
}
```

---

### 5. Revoke Pass

**Endpoint:** `POST /admin/revoke-pass/<pass_id>`

**Description:** Revoke an approved pass.

**Authentication:** Admin access required

**URL Parameters:**
- `pass_id`: Pass ID to revoke

**Response (200 OK):**
```json
{
  "message": "Pass revoked",
  "pass": {
    "pass_id": "PASS12AB34CD56EF",
    "status": "Revoked",
    "revoked_flag": true
  }
}
```

---

### 6. Set Signature Method

**Endpoint:** `POST /admin/set-signature-method`

**Description:** Set system-wide QR code signature method. Affects all newly approved passes.

**Authentication:** Admin access required

**Request Body:**
```json
{
  "method": "FALCON-128"
}
```

**Supported Methods:**
- `"RSA-2048"` - Classic RSA-2048 cryptography
- `"FALCON-128"` - Post-quantum FALCON-128 cryptography

**Response (200 OK):**
```json
{
  "message": "Signature method set to FALCON-128",
  "method": "FALCON-128"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Invalid signature method. Must be RSA-2048 or FALCON-128"
}
```

---

### 7. Pause System

**Endpoint:** `POST /admin/pause-system`

**Description:** Pause or resume the entire access control system.

**Authentication:** Admin access required

**Request Body:**
```json
{
  "paused": true
}
```

**Response (200 OK):**
```json
{
  "message": "System paused",
  "paused": true
}
```

---

### 8. Pause Site

**Endpoint:** `POST /admin/pause-site`

**Description:** Pause or resume a specific site.

**Authentication:** Admin access required

**Request Body:**
```json
{
  "site_id": "SITE001",
  "paused": true
}
```

**Response (200 OK):**
```json
{
  "message": "Site SITE001 paused",
  "site_id": "SITE001",
  "paused": true
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Missing site_id"
}
```

---

### 9. Get System Status

**Endpoint:** `GET /admin/system-status`

**Description:** Get current system status including pause states and signature method.

**Authentication:** Admin access required

**Response (200 OK):**
```json
{
  "global_pause": false,
  "site_pauses": {
    "SITE001": false,
    "SITE002": true
  },
  "signature_method": "FALCON-128"
}
```

---

### 10. Get Statistics

**Endpoint:** `GET /admin/statistics`

**Description:** Get system usage statistics.

**Authentication:** Admin access required

**Response (200 OK):**
```json
{
  "total_users": 145,
  "total_gates": 8,
  "passes_in_process": 12,
  "passes_pass": 234,
  "passes_used": 189,
  "passes_revoked": 5,
  "passes_rejected": 23
}
```

---

### 11. Get Audit Logs

**Endpoint:** `GET /admin/audit-logs`

**Description:** Get system audit trail logs.

**Authentication:** Admin access required

**Query Parameters:**
- `limit` (optional): Number of logs to return (default: 100)

**Example:** `/admin/audit-logs?limit=50`

**Response (200 OK):**
```json
{
  "logs": [
    {
      "id": 1234,
      "timestamp": "2026-01-25T12:00:00Z",
      "event_type": "scan",
      "result": "PASS",
      "user_id": "A123456(7)",
      "pass_id": "PASS12AB34CD56EF",
      "gate_id": "GATE001",
      "details": "Site: SITE001, Purpose: MEETING"
    }
  ]
}
```

**Event Types:**
- `login` - User/gate authentication
- `application` - Pass application submission
- `approval` - Pass approval
- `rejection` - Pass rejection
- `revocation` - Pass revocation
- `scan` - QR code scan at gate
- `pause` - System/site pause toggle
- `config_change` - Configuration changes

---

### 12. Register Gate

**Endpoint:** `POST /admin/register-gate`

**Description:** Register a new gate reader device.

**Authentication:** Admin access required

**Request Body:**
```json
{
  "tablet_id": "GATE005",
  "password": "gate123",
  "site_id": "SITE001",
  "location": "Building A Entrance"
}
```

**Response (201 Created):**
```json
{
  "message": "Gate registered successfully",
  "gate": {
    "tablet_id": "GATE005",
    "site_id": "SITE001",
    "location": "Building A Entrance",
    "created_at": "2026-01-25T12:30:00Z"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Missing required fields"
}
```

**Response (409 Conflict):**
```json
{
  "error": "Gate already exists"
}
```

---

### 13. Get HSM Signature Logs

**Endpoint:** `GET /admin/hsm/signature-logs`

**Description:** Get quantum-safe HSM signature generation logs.

**Authentication:** Admin access required

**Query Parameters:**
- `filter` (optional): Filter by signature method (`all`, `FALCON-128`, `RSA-2048`)

**Example:** `/admin/hsm/signature-logs?filter=FALCON-128`

**Response (200 OK):**
```json
{
  "logs": [
    {
      "id": 1,
      "timestamp": "2026-01-25T12:00:00Z",
      "user_id": "A123456(7)",
      "pass_id": "PASS12AB34CD56EF",
      "signature_method": "FALCON-128",
      "payload_size": 14916,
      "status": "SUCCESS"
    }
  ]
}
```

---

## Error Codes

| HTTP Code | Description |
|-----------|-------------|
| **200 OK** | Request successful |
| **201 Created** | Resource created successfully |
| **400 Bad Request** | Invalid request format or missing parameters |
| **401 Unauthorized** | Invalid or missing authentication token |
| **403 Forbidden** | Valid token but insufficient permissions |
| **404 Not Found** | Requested resource not found |
| **409 Conflict** | Resource already exists |
| **500 Internal Server Error** | Server-side error |

---

## Common Response Formats

### Success Response
```json
{
  "message": "Operation successful",
  "data": { ... }
}
```

### Error Response
```json
{
  "error": "Error description"
}
```

---

## Security Features

### HTTPS Enforcement for Gate APIs

**Production Environment:**
- Gate API endpoints (`/api/gate-login` and `/api/scan-qr`) **require HTTPS**
- HTTP requests will be rejected with `403 Forbidden` response:
  ```json
  {
    "error": "HTTPS required for gate operations",
    "message": "Gate API endpoints must use secure HTTPS connection"
  }
  ```

**Development Environment:**
- Localhost (`localhost` or `127.0.0.1`) allows HTTP for testing
- Security checks are logged but not enforced

**Rationale:**
Gate operations involve critical access control decisions. HTTPS ensures:
- Encrypted communication between gate readers and backend
- Protection against man-in-the-middle attacks
- Secure transmission of authentication tokens and QR data

### JWT Token Security

- Tokens expire after 24 hours
- Include tokens in Authorization header: `Bearer <token>`
- Tokens are validated on every protected endpoint

---

## Rate Limiting

Currently no rate limiting is implemented in this PoC version.

---

## CORS Policy

All origins are allowed in demo mode:
```
Access-Control-Allow-Origin: *
```

---

## Notes

1. **Signature Methods:**
   - `RSA-2048`: Classic cryptography (payload ~1,000 bytes)
   - `FALCON-128`: Post-quantum cryptography (payload ~15,000 bytes, requires QR Version 26)

2. **QR Code Expiration:**
   - QR codes expire 60 seconds after generation
   - Enforced during scan-qr validation

3. **Pass Expiration:**
   - Default pass validity: 24 hours from approval
   - Configurable during approval

4. **Atomic Operations:**
   - Pass usage is atomic (single-use enforcement)
   - Uses database row locking to prevent race conditions

5. **Environment Detection:**
   - Admin Console, User Wallet, and Gate Reader apps automatically detect localhost vs production
   - No manual configuration needed for local development

---

## Support

For issues or questions:
- Check backend logs: `backend/server.log`
- Check browser console for frontend errors
- Review audit logs via `/admin/audit-logs` endpoint

---

**End of API Manual**
