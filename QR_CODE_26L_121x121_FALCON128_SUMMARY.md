# QR Code Configuration Summary for MM-Falcon PQC Signature

## Project Overview
This project implements **Quantum-Safe Digital Signatures** using MM-Falcon (a post-quantum cryptography algorithm) with QR code encoding for email verification and verification purposes.

---

## QR Code Version Used

### **Version 26** - Primary Configuration
- **Module Dimensions**: 121 × 121 pixels
- **Physical Size (with settings)**: 1,250 × 1,250 pixels
  - Box size: 10 pixels per module
  - Border: 4 pixels

### Error Correction Level
- **Level: L (Low)**
  - ~7% error correction capability
  - Provides good balance between capacity and reliability

---

## Payload Capacity - Version 26

| Data Type | Capacity |
|-----------|----------|
| **Numeric** | 7,089 characters |
| **Alphanumeric** | 4,296 characters |
| **Byte/Binary** | 2,953 bytes |
| **Kanji** | 1,817 characters |

---

## Implementation Details

### Quantum-Safe Algorithm
- **Algorithm**: `ckm-icc-shake256-mm-falcon`
- **Signature Size**: 690 bytes
- **Hash Function**: SHAKE256

### Python Implementation (sig2qr.py)
```python
# URL QR Code
qr = qrcode.QRCode(
    version=26,  # Fixed Version 26
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Signature QR Code
qr = qrcode.QRCode(
    version=1,  # Auto-fit to content
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.make(fit=True)  # Auto-size to fit the data
```

### JavaScript/HTML Implementation (appQsQRSig.html & sig2qr.html)
```javascript
// URL QR Code
QRCode.toCanvas(canvas, url, {
    errorCorrectionLevel: 'L',
    version: 26,  // Force Version 26
    width: 1250,
    margin: 4
});

// Signature QR Code
QRCode.toCanvas(canvas, data, {
    errorCorrectionLevel: 'L',
    version: undefined,  // Auto-fit
    width: 1250,
    margin: 4
});
```

---

## Data Padding Strategy

### URL QR Code
- **Target Length**: 1,273 characters (safe Version 26 'L' capacity)
- **Padding Method**: Query parameter `?padding=xxxx...`
- **Purpose**: Ensure consistent QR code size for both URL and signature codes

### Signature QR Code
- **Max Capacity**: 1,852 alphanumeric characters (Version 26 'L')
- **Actual Data**: 690 bytes (binary signature data in hex = 1,380 hex characters)
- **Padding**: 472 '0' characters appended to reach 1,852 capacity

---

## File Locations in Project

| File | Purpose | Key Configuration |
|------|---------|-------------------|
| [appQsQRSig.html](public/appQsQRSig.html) | Main web application | Version 26 for URLs, auto-fit for signatures |
| [sig2qr.html](public/sig2qr.html) | HTML QR converter | Version 26 forced for both QR codes |
| [sig2qr.py](public/sig2qr.py) | Python QR converter | Version 26 for URLs, Version 1 for signatures |
| [appQsQRSig (deployed) 20250413.html](public/appQsQRSig%20\(deployed\)%2020250413.html) | Production version | Same as appQsQRSig.html |

---

## QR Code Output

### Combined QR Code Structure
```
[URL QR Code (Version 26)]  [Signature QR Code (Auto-fit)]
     1,250×1,250 px            1,250×1,250 px
```

- **Combined Dimensions**: 2,500 × 1,250 pixels (side-by-side)
- **Format**: PNG image
- **Output File**: `signature.png`

---

## Capacity Analysis

### Available Capacity (Version 26, ERROR_CORRECT_L)
- **Binary Mode**: 2,953 bytes

### Actual Usage
- **MM-Falcon Signature**: 690 bytes
- **Utilization**: 23.3% of available capacity
- **Remaining Capacity**: 2,263 bytes for future expansion

### Safety Margin
- ✅ Large headroom for signature growth
- ✅ Robust error correction with Level L
- ✅ Consistent QR code sizing across implementations

---

## Key Design Decisions

1. **Fixed Version 26 for URLs**: Ensures consistent QR code dimensions for visual alignment and display purposes

2. **Auto-fit for Signatures**: Allows flexible signature encoding without wasting space, but maintains 1,250×1,250px display size through padding

3. **Error Correction Level L**: Balances between:
   - Maximum data capacity
   - Reasonable error tolerance (~7%)
   - Practical scanning requirements

4. **Binary Padding**: Uses '0' padding for signatures and '?padding=x' for URLs to maintain consistent QR code versions across different data types

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **QR Code Version (URL)** | 26 |
| **QR Code Version (Signature)** | Auto-fit (typically 24-26) |
| **Error Correction** | L (Low) |
| **Signature Algorithm** | MM-Falcon (NIST PQC candidate) |
| **Signature Size** | 690 bytes |
| **Max QR Capacity** | 2,953 bytes (binary) |
| **Utilization** | ~23.3% |
| **Output Format** | PNG (1,250×1,250 px each) |
| **Use Case** | Email verification with quantum-safe signatures |

---

*Last Updated: January 22, 2026*
*Project: QuantumSafe QR Code Signature Generation*
