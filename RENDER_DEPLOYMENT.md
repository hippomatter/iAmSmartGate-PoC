# Deploying iAmSmartGate on Render.com - Step-by-Step Guide

## Prerequisites ✅
- [x] Render.com free account created
- [x] GitHub account linked to Render
- [x] Project pushed to GitHub repo
- [x] render.yaml blueprint file configured

---

## Step 1: Prepare Your GitHub Repo

### 1.1 Commit all deployment files:
```bash
cd c:\Users\hipopo\Codes\iAmSmartGate\iAmSmartGate-PoC
git add render.yaml backend/requirements.txt backend/app.py backend/admin_console.py
git add gate-reader-app/index.html user-wallet-app/index.html index.html
git commit -m "Add Render.com blueprint deployment with all services"
git push origin main
```

### 1.2 Verify files exist in GitHub:
- `render.yaml` (root level) - Defines all 4 services
- `backend/requirements.txt` (updated with gunicorn)
- `backend/app.py` (updated with error handling)
- `backend/admin_console.py` (API_BASE points to backend)
- Frontend apps with updated API URLs

---

## Step 2: Deploy Blueprint on Render.com

### 2.1 Go to Render Dashboard
1. Visit https://dashboard.render.com
2. Click **"New +"** button → Select **"Blueprint"**

### 2.2 Connect GitHub Repository
1. Click **"Connect a repository"**
2. Select your GitHub repo: **`iAmSmartGate-PoC`**
3. Click **"Connect"**
4. Render will automatically detect `render.yaml`

### 2.3 Review Blueprint Configuration

Render will show all services defined in render.yaml:

**Service 1: Backend API**
- **Name:** `iAmSmartGate-PoC-Backend`
- **Type:** Web Service
- **Runtime:** Python 3
- **Build:** `pip install -r backend/requirements.txt`
- **Start:** `cd backend && gunicorn app:app`
- **Env Vars:** Auto-generated SECRET_KEY, JWT_SECRET_KEY, etc.

**Service 2: Admin Console**
- **Name:** `iAmSmartGate-PoC-Admin`
- **Type:** Web Service
- **Runtime:** Python 3
- **Build:** `pip install -r backend/requirements.txt`
- **Start:** `cd backend && gunicorn admin_console:app`

**Service 3: Gate Reader App**
- **Name:** `iAmSmartGate-PoC-Gate`
- **Type:** Static Site
- **Publish Path:** `gate-reader-app`

**Service 4: User Wallet App**
- **Name:** `iAmSmartGate-PoC-Wallet`
- **Type:** Static Site
- **Publish Path:** `user-wallet-app`

### 2.4 Environment Variables (Auto-Generated)
Render automatically creates these from render.yaml:

| Key | Value | Service |
|-----|-------|------|
| `DEBUG` | `false` | Backend, Admin |
| `TEST_MODE` | `false` | Backend |
| `ALLOWED_ORIGINS` | `*` | Backend |
| `SECRET_KEY` | (auto-generated) | Backend |
| `JWT_SECRET_KEY` | (auto-generated) | Backend |
| `DATABASE_URL` | `sqlite:///iamsmartgate.db` | Backend |

### 2.5 Deploy All Services
- Review the services
- Click **"Apply"** → **"Create All Services"**
- All 4 services will deploy simultaneously

---

## Step 3: Wait for Deployment

### 3.1 Monitor Build Progress
You'll see logs for each service:

**Backend Service:**
```
=== Building Docker image
=== Installing build runtime
=== Running build command: pip install -r backend/requirements.txt
=== Starting: cd backend && gunicorn app:app
=== Service live at https://iamsmartgate-backend.onrender.com
```

**Admin Console:**
```
=== Starting: cd backend && gunicorn admin_console:app
=== Service live at https://iamsmartgate-poc.onrender.com
```

**Static Sites:**
```
=== Publishing gate-reader-app
=== Service live at https://iamsmartgate-poc-gate.onrender.com

=== Publishing user-wallet-app
=== Service live at https://iamsmartgate-poc-wallet.onrender.com
```

### 3.2 Deployment Complete
All services are **live!** 🎉

---

## Step 4: Test All Services

### 4.1 Test Backend API
```bash
curl https://iamsmartgate-backend.onrender.com/health
```
Expected response:
```json
{"status": "ok", "timestamp": "2026-01-02T..."}
```

### 4.2 Test Admin Console
Open in browser:
```
https://iamsmartgate-poc.onrender.com/
```
You should see the admin dashboard loading data from the backend.

### 4.3 Test Gate Reader App
Open in browser:
```
https://iamsmartgate-poc-gate.onrender.com/
```
Should load the QR code scanner interface.

### 4.4 Test User Wallet App
Open in browser:
```
https://iamsmartgate-poc-wallet.onrender.com/
```
Should load the user wallet interface.

### 4.5 Check Logs
In Render Dashboard:
1. Click each service name
2. Go to **"Logs"** tab
3. View real-time logs
4. Verify no errors

---

## Step 5: Architecture Verification

### 5.1 Frontend API Configuration
All frontend apps are already configured to use production URLs:

**Gate Reader** (`gate-reader-app/index.html`):
```javascript
const API_BASE = 'https://iamsmartgate-backend.onrender.com';

// Replace all API calls:
fetch(`${API_BASE}/api/status`)
  .then(r => r.json())
  .catch(e => console.error(e));
```

Same for `user-wallet-app/index.html`

---

## Step 6: Fix CORS Issues (If Needed)

### If frontend can't reach backend:

**Option A: Open CORS temporarily (Testing)**
1. Go to Render Dashboard → Your service
2. Click **"Environment"** tab
3. Edit `ALLOWED_ORIGINS`:
   ```
   https://your-netlify-app.netlify.app,https://your-other-app.netlify.app
   ```
4. Click **"Save"** (auto-redeploys)

**Option B: Update backend code**
In `backend/config.py`, change:
```python
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
```

In `backend/app.py`, update CORS:
```python
from flask_cors import CORS
import os

allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
CORS(app, resources={r"/*": {"origins": allowed_origins}})
```

Then commit and push - Render auto-redeploys!

---

## Step 7: Monitor & Maintain

### 7.1 View Logs
Render Dashboard → Your service → **"Logs"** tab

### 7.2 Check Metrics
- **CPU Usage**
- **Memory Usage**
- **Network I/O**
(Free tier has basic monitoring)

### 7.3 Restart Service
Click **"Restart"** if needed (in Render Dashboard)

### 7.4 Enable Auto-Deploy
Render automatically redeploys when you push to GitHub (already enabled)

---

## Troubleshooting

### ❌ Build Fails
Check logs for Python import errors:
1. Go to **"Logs"** tab
2. Look for `ModuleNotFoundError` or `ImportError`
3. Update `backend/requirements.txt` with missing packages
4. Commit and push - Render auto-redeploys

### ❌ CORS Errors
Frontend console shows: `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
- Update `ALLOWED_ORIGINS` environment variable
- Or temporarily set to `*` for testing

### ❌ Database Issues
If you use PostgreSQL in production:
1. Add to Render: **"PostgreSQL"** service
2. Copy connection string
3. Set `DATABASE_URL` environment variable
4. Current: SQLite (fine for testing, limited for production)

### ❌ Service Keeps Restarting
1. Check logs for memory leaks
2. Free tier has 512MB RAM limit
3. Upgrade to paid if needed

---

## Production Checklist

Before going public:
- [ ] Set `DEBUG=false`
- [ ] Set `TEST_MODE=false`
- [ ] Generate strong `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Restrict `ALLOWED_ORIGINS` to your domains only
- [ ] Enable HTTPS (automatic on Render)
- [ ] Test all API endpoints
- [ ] Monitor logs regularly
- [ ] Set up error alerts (Render Pro feature)

---

## Your Live URLs

| Service | URL | Status |
|---------|-----|--------|
| Backend API | https://iamsmartgate-backend.onrender.com | ✅ Live |
| Admin Console | https://iamsmartgate-poc.onrender.com | ✅ Live |
| Gate Reader App | https://iamsmartgate-poc-gate.onrender.com | ✅ Live |
| User Wallet App | https://iamsmartgate-poc-wallet.onrender.com | ✅ Live |
| Landing Page | (Deploy index.html separately) | 📝 Optional |

**API Endpoints:**
- Health Check: `https://iamsmartgate-backend.onrender.com/health`
- User API: `https://iamsmartgate-backend.onrender.com/api/*`
- Admin API: `https://iamsmartgate-backend.onrender.com/admin/*`

---

## Blueprint Deployment Benefits

✅ **One-Click Deploy:** All 4 services created simultaneously  
✅ **Auto-Sync:** Push to GitHub → Auto-redeploys all services  
✅ **Environment Isolation:** Each service has its own config  
✅ **Static Site Optimization:** CDN delivery for frontends  
✅ **Consistent URLs:** Service names remain stable  
✅ **Infrastructure as Code:** render.yaml version controlled  

---

## Next Steps

### Immediate (Already Done ✅)
1. ✅ Push render.yaml to GitHub
2. ✅ Deploy via Blueprint on Render
3. ✅ All 4 services deployed
4. ✅ Frontend APIs pointing to backend
5. ✅ Admin console pointing to backend

### Optional Enhancements
- [ ] Deploy landing page (index.html) to GitHub Pages
- [ ] Set up custom domain for services
- [ ] Restrict CORS to specific domains
- [ ] Add PostgreSQL database (if needed)
- [ ] Enable Render monitoring alerts
- [ ] Set up CI/CD for automated testing

### Maintenance
- Monitor logs regularly in Render Dashboard
- Free tier services sleep after 15 min inactivity (normal)
- First request after sleep takes ~30 seconds to wake up
- Consider paid tier ($7/month) for always-on services

**Need help?** Check Render docs: https://render.com/docs

