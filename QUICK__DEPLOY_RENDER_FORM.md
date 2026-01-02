# Quick Render.com Deployment Checklist

## Pre-Deployment (Do This Now)

```bash
# 1. Navigate to project
cd c:\Users\hipopo\Codes\iAmSmartGate\iAmSmartGate-PoC

# 2. Check Git status
git status

# 3. Commit all deployment files
git add render.yaml backend/requirements.txt backend/app.py backend/admin_console.py index.html
git commit -m "Prepare for Render.com blueprint deployment"

# 4. Push to GitHub
git push origin main

# 5. Verify on GitHub (open browser)
# Visit your repo and confirm files are there
```

---

## Render.com Blueprint Deployment (3 minutes)

### Step 1: Deploy via Blueprint
```
🌐 Go to: https://dashboard.render.com
📍 Click: "New +" → "Blueprint"
🔗 Select: Your GitHub repo
✅ Click: "Connect"
✅ Render will read render.yaml and create ALL services automatically
```

### Step 2: Review Services (Auto-Created)
```
Render will create 4 services from render.yaml:

1. Backend API Service
   Name: iAmSmartGate-PoC-Backend
   Type: Web Service (Python + Gunicorn)
   
2. Admin Console Service
   Name: iAmSmartGate-PoC-Admin
   Type: Web Service (Python + Gunicorn)
   
3. Gate Reader App
   Name: iAmSmartGate-PoC-Gate
   Type: Static Site
   
4. User Wallet App
   Name: iAmSmartGate-PoC-Wallet
   Type: Static Site
```

### Step 3: Auto-Generated Environment Variables
```
Render automatically generates:
- SECRET_KEY (for Backend)
- JWT_SECRET_KEY (for Backend)
- DEBUG=false (for both services)
- TEST_MODE=false (for Backend)
- ALLOWED_ORIGINS=* (for Backend)
```

### Step 4: Deploy All Services
```
Click "Apply" → "Create All Services"
⏳ Wait 3-5 minutes for all deployments
✅ All 4 services will be live!
```

### Step 5: Verify All Services
```bash
# Test Backend API
curl https://iamsmartgate-backend.onrender.com/health
# Expected: {"status":"ok","timestamp":"..."}

# Test Admin Console
curl https://iamsmartgate-poc.onrender.com/
# Expected: HTML admin console page

# Test Gate Reader (open in browser)
https://iamsmartgate-poc-gate.onrender.com/

# Test User Wallet (open in browser)
https://iamsmartgate-poc-wallet.onrender.com/
```

---

## Your Live URLs
```
Backend API:       https://iamsmartgate-backend.onrender.com
Admin Console:     https://iamsmartgate-poc.onrender.com
Gate Reader:       https://iamsmartgate-poc-gate.onrender.com
User Wallet:       https://iamsmartgate-poc-wallet.onrender.com
Landing Page:      (Deploy index.html separately or use GitHub Pages)
```

All frontend apps already point to the correct backend URLs!

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Add missing package to `backend/requirements.txt` → Push |
| CORS Error | Already set to `ALLOWED_ORIGINS=*` in render.yaml |
| Service won't start | Check logs in Render Dashboard → Fix → Push |
| Database error | SQLite works fine (file stored in service disk) |
| Free tier sleeps | Services sleep after 15 min inactivity (normal) |
| Static site 404 error | Use `static_site` type (not `web`) in render.yaml |
| Admin can't reach backend | Verify admin_console.py API_BASE points to backend URL |

---

## Architecture Overview

```
┌─────────────────────┐
│   Landing Page      │  (index.html - deploy to GitHub Pages)
│   (Program Selector)│
└──────────┬──────────┘
           │
    ┌──────┴──────┬──────────────┬──────────────┐
    │             │              │              │
┌───▼────┐  ┌────▼─────┐  ┌─────▼──────┐  ┌───▼──────┐
│Backend │  │  Admin   │  │Gate Reader │  │  User    │
│  API   │◄─┤ Console  │  │    App     │  │ Wallet   │
│        │  │          │  │  (Static)  │  │ (Static) │
└────────┘  └──────────┘  └─────┬──────┘  └────┬─────┘
                                 │              │
                                 └──────┬───────┘
                                        │
                                        ▼
                               Backend API calls
```

---

## File Changes Made

✅ Created: `render.yaml` - Blueprint config for 4 services
✅ Updated: `backend/requirements.txt` - Added gunicorn
✅ Updated: `backend/app.py` - Added error handling & root endpoint
✅ Updated: `backend/admin_console.py` - API_BASE points to backend
✅ Updated: `gate-reader-app/index.html` - API_BASE updated
✅ Updated: `user-wallet-app/index.html` - API_BASE updated
✅ Created: `index.html` - Landing page with program selector
✅ Created: `RENDER_DEPLOYMENT.md` - Full guide
✅ Created: This checklist

All ready to deploy with one click! 🚀
