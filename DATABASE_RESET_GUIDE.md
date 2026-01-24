# Database Reset Guide

## ✅ Database Schema Updates

The Pass table has been updated with a new field:
- **`signature_method`** - Stores the QR signature method (RSA-2048 or FALCON-128)
  - Default value: `FALCON-128`
  - Allows backward compatibility (old records default to RSA-2048)

System state table includes:
- **`signature_method`** - Global setting for newly approved passes

---

## 🔄 How to Reset Database

### Method 1: Using Batch Script (Windows)

**Quick Reset:**
```batch
reset_database.bat
```

This will:
1. Stop any running servers
2. Delete the existing database file
3. Prepare for fresh database creation

Then start the system:
```batch
start.bat
```

---

### Method 2: Using Python Script (Cross-platform)

```bash
python reset_database.py
```

This provides more detailed output and works on all platforms.

---

### Method 3: Manual Reset

**Step 1: Stop servers**
- Close all terminal windows running the backend/admin console
- Or press `Ctrl+C` in each terminal

**Step 2: Delete database**

Windows:
```batch
del backend\instance\iamsmartgate.db
```

Linux/Mac:
```bash
rm backend/instance/iamsmartgate.db
```

**Step 3: Restart system**
```batch
start.bat
```

The database will be automatically recreated with the new schema when the backend starts.

---

## 📊 Database Location

**SQLite Database File:**
```
backend/instance/iamsmartgate.db
```

**Configuration:**
- Defined in `backend/config.py`
- Environment variable: `DATABASE_URL` (optional)
- Default: SQLite local file

---

## 🆕 New Schema Fields

### Pass Table
```sql
CREATE TABLE passes (
    pass_id VARCHAR(100) PRIMARY KEY,
    iamsmart_id VARCHAR(100) NOT NULL,
    site_id VARCHAR(50) NOT NULL,
    purpose_id VARCHAR(50) NOT NULL,
    visit_date_time DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'In Process',
    qr_signature TEXT,
    signature_method VARCHAR(20) DEFAULT 'FALCON-128',  -- ✨ NEW FIELD
    created_timestamp DATETIME,
    approved_timestamp DATETIME,
    used_timestamp DATETIME,
    expiry_timestamp DATETIME,
    used_flag BOOLEAN DEFAULT 0,
    revoked_flag BOOLEAN DEFAULT 0,
    device_id VARCHAR(100)
);
```

### System State Table
```sql
CREATE TABLE system_state (
    key VARCHAR(50) PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME
);

-- New entry for signature method
INSERT INTO system_state (key, value) VALUES ('signature_method', 'FALCON-128');
```

---

## 🔍 Verify Database Schema

After reset, you can verify the new schema:

**Using Python:**
```bash
cd backend
python -c "from models import db, Pass; from app import create_app; app = create_app(); print('Pass columns:', [c.name for c in Pass.__table__.columns])"
```

Expected output should include `signature_method` in the list.

---

## 🎯 Testing New Features

1. **Reset database** (use any method above)
2. **Start system**: `start.bat`
3. **Open Admin Console**: http://localhost:5001
4. **Check Dashboard**: Should show "🦅 Quantum FALCON-128" as default
5. **System Control**: Switch between RSA-2048 and FALCON-128
6. **Approve a pass**: New passes will use the selected method
7. **User Wallet**: Generate QR codes with the selected signature method
8. **Gate Reader**: Scan and verify with appropriate method

---

## ⚠️ Important Notes

- **Data Loss**: Resetting the database deletes all existing passes, users, and audit logs
- **Backward Compatibility**: Old databases without `signature_method` field will default to RSA-2048
- **No Migration Needed**: SQLAlchemy will auto-create tables on first run
- **Test Data**: The system creates test gates automatically (GATE001-GATE004)

---

## 🐛 Troubleshooting

**Issue: "Database is locked"**
```bash
# Stop all Python processes
taskkill /F /IM python.exe

# Then reset database
```

**Issue: "Table already exists"**
```bash
# Delete instance folder completely
rmdir /S /Q backend\instance

# Restart system
start.bat
```

**Issue: "signature_method column not found"**
```bash
# Reset database to recreate with new schema
reset_database.bat
```

---

## 📝 Development Workflow

For development with frequent schema changes:

1. Make changes to `backend/models.py`
2. Run `reset_database.bat` or `reset_database.py`
3. Run `start.bat` to recreate with new schema
4. Test new features

---

*Last Updated: January 24, 2026*
