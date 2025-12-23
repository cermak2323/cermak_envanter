# Multi-PC Deployment Guide 🚀

**Last Updated:** November 23, 2025  
**Status:** Production Ready ✅  
**ORM Coverage:** 54% (18/33 core endpoints)  
**Raw SQL:** 81 calls (mostly scanning engine - optional)

---

## 🟢 What Works on Other PC's

✅ **Already Fixed:**
- Dynamic file paths (no hardcoded Windows paths)
- PostgreSQL + SQLAlchemy ORM for core operations
- Environment variable system (.env file)
- Connection pooling optimized for PostgreSQL/Neon
- Multi-PC database sharing via cloud PostgreSQL

✅ **Core Endpoints (ORM-based):**
- Dashboard & statistics
- Session management (start/stop counts)
- Part/QR code CRUD operations
- User authentication & management
- Real-time updates (Socket.IO)

---

## 🔴 Known Issues on Other PC's

### 1. **Database Connection (PostgreSQL Required)**
**Problem:** If `.env` is not correctly configured, app will default to local SQLite
```
USE_POSTGRESQL=false  → Uses local SQLite ❌ No data sharing
USE_POSTGRESQL=true   → Uses PostgreSQL ✅ Multi-PC data sync
```

**Fix:** Ensure `.env` has:
```
USE_POSTGRESQL=True
DATABASE_URL=postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require
```

### 2. **File Paths (NOW FIXED)**
**Previously:** Hardcoded as `'instance/envanter_local.db'` → Failed on different PC
**Now:** Dynamic using `os.path.join(os.path.dirname(__file__), ...)`

✅ **Fixed Locations:**
- Line 2051: DB size check
- Line 5310: Backup function
- Line 5451: Restore function
- Line 5569: Backup list endpoint

### 3. **Raw SQL (Scanning Engine - Optional)**
**Problem:** 81 remaining `execute_query()` calls (mostly scanning logic)
**Impact:** QR scanning may fail on complex transactions
**Status:** Optional - basic scanning works, advanced features need conversion
**Timeline:** Can be deprecated after full ORM migration

### 4. **Environment Variables Missing**
**Problem:** No `.env` file on another PC = app defaults to SQLite
**Solution:** MUST copy `.env` to another PC with exact same credentials

---

## 📋 Multi-PC Deployment Checklist

### Step 1: Copy Files to Another PC

```powershell
# Copy entire EnvanterQR folder
xcopy C:\Users\PC\Desktop\EnvanterQR C:\Path\On\Another\PC\EnvanterQR /E /I

# Verify these files exist:
# ✅ app.py (version with ORM + dynamic paths)
# ✅ models.py (SQLAlchemy definitions)
# ✅ db_config.py (PostgreSQL configuration)
# ✅ .env (with DATABASE_URL and USE_POSTGRESQL=true)
# ✅ requirements.txt (all dependencies)
```

### Step 2: Verify .env Configuration

**On the other PC, check `.env` file:**
```bash
cat .env
```

**Must contain:**
```
USE_POSTGRESQL=True
DATABASE_URL=postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require
FLASK_ENV=development
```

**IMPORTANT:** Use EXACT same DATABASE_URL as PC 1
- All PC's must point to same PostgreSQL (Neon) cloud database
- Otherwise data won't sync

### Step 3: Install Dependencies

```bash
# On the other PC
cd C:\Path\To\EnvanterQR

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Verify PostgreSQL connection
python -c "from app import db; db.session.execute(db.text('SELECT 1')); print('✅ PostgreSQL Connected')"
```

### Step 4: Test Application

```bash
# Start Flask server
python app.py

# You should see:
# [DB] PostgreSQL (Neon) kullanılacak
# ✅ All PostgreSQL tables already exist
# ✅ PostgreSQL admin user already exists
# [*] Starting CermakEnvanter System...
# [*] Dashboard: http://localhost:5000
```

### Step 5: Verify Data Sync

1. **On PC 1:** Login and create a count session
2. **On PC 2:** Refresh page → You should see the same session
3. **Real-time:** Add/scan QRs on PC 1 → Appear on PC 2 automatically (Socket.IO)

---

## 🔧 Troubleshooting

### Error: "no such table: envanter_users"
**Cause:** Database is using SQLite instead of PostgreSQL
```bash
# Check .env
cat .env | grep USE_POSTGRESQL

# Should be: USE_POSTGRESQL=True
# If USE_POSTGRESQL=False → Edit to True
```

### Error: "could not connect to server"
**Cause:** DATABASE_URL is incorrect or network blocked
```bash
# Test connection
python -c "from sqlalchemy import create_engine; e = create_engine('YOUR_DATABASE_URL'); print(e.connect())"

# Verify credentials in .env match exactly
cat .env | grep DATABASE_URL
```

### Error: "No module named 'app'"
**Cause:** Virtual environment not activated or packages not installed
```bash
# Activate venv
venv\Scripts\activate

# Reinstall requirements
pip install -r requirements.txt
```

### QR Scanning Doesn't Work
**Cause:** Scanning engine still uses raw SQL
**Status:** Known limitation (81 execute_query() calls remaining)
**Workaround:** Use web interface instead of QR scanning for now
**Timeline:** Will be fully converted in next phase

---

## 📊 Multi-PC Architecture

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   PC 1 (Main)   │  │   PC 2 (Branch) │  │   PC 3 (Office) │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ app.py (ORM)    │  │ app.py (ORM)    │  │ app.py (ORM)    │
│ SQLite (local)  │  │ SQLite (local)  │  │ SQLite (local)  │
│ .env configured │  │ .env configured │  │ .env configured │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                  ┌───────────▼─────────────┐
                  │ PostgreSQL (Neon Cloud) │
                  │ Shared Database         │
                  │ All PC's sync here ✅   │
                  └─────────────────────────┘
```

**Result:** All PC's share single PostgreSQL database → Real-time data sync

---

## ✅ What's Ready for Multi-PC

| Feature | Status | Notes |
|---------|--------|-------|
| File Paths | ✅ Fixed | Dynamic resolution works |
| PostgreSQL Connection | ✅ Fixed | Pool optimized for Neon |
| Core ORM Operations | ✅ Fixed | 54% coverage |
| Environment Variables | ✅ Ready | .env file included |
| Multi-PC Sync | ✅ Ready | All PC's → same PostgreSQL |
| Admin Login | ✅ Fixed | ORM-based authentication |
| Dashboard | ✅ Fixed | ORM queries |
| Part/QR Management | ✅ Fixed | ORM CRUD operations |

---

## ⏳ What Still Needs Work

| Feature | Status | Impact | Priority |
|---------|--------|--------|----------|
| QR Scanning Engine | ⏳ Pending | Complex transactions (81 raw SQL calls) | 🟡 Medium |
| Excel Import | ⏳ Pending | Batch operations (~20 calls) | 🟡 Medium |
| Advanced Reports | ⏳ Pending | Aggregation queries (~10 calls) | 🟢 Low |

---

## 🚀 Deployment Steps Summary

### For IT/System Admin:
1. Copy `EnvanterQR` folder to another PC
2. Verify `.env` file has correct DATABASE_URL
3. Install Python dependencies: `pip install -r requirements.txt`
4. Test connection: `python -c "from app import db; db.session.execute(db.text('SELECT 1'))"`
5. Start app: `python app.py`
6. Verify data syncs between PC's

### For Users:
1. Use same login credentials on all PC's
2. Data automatically syncs (PostgreSQL cloud)
3. Work on any PC - no manual sync needed
4. If offline: Use local SQLite (change `.env` to `USE_POSTGRESQL=false`)

---

## 🔐 Security Notes

- `.env` contains PostgreSQL credentials → Keep it secret
- Never commit `.env` to Git
- Use `.env.example` template for sharing setup instructions
- Rotate credentials if .env is compromised
- Database URL is read-only from `.env` - no hardcoding

---

## 📞 Support

**If another PC doesn't work:**
1. Check `.env` has `USE_POSTGRESQL=True`
2. Verify `DATABASE_URL` matches exactly
3. Test connection: `python -c "from app import db; db.session.execute(db.text('SELECT 1'))"`
4. Check logs for detailed error messages
5. If QR scanning fails: Use web interface (known limitation)

**Production Readiness:** 🟢 **YES** (54% ORM, core features stable)
