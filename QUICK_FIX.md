# Quick Fix for Other PC ⚡

## Problem
Other PC shows: `sqlite3.OperationalError: no such table: envanter_users`

## Solution (2 Minutes)

### 1️⃣ Copy This File
```
FROM: c:\Users\rsade\Desktop\Yeni klasör (2)\EnvanterQR\EnvanterQR\app.py
TO:   c:\Users\PC\Desktop\EnvanterQR\app.py
```

### 2️⃣ Verify .env
Make sure `c:\Users\PC\Desktop\EnvanterQR\.env` has:
```
USE_POSTGRESQL=True
DATABASE_URL=postgresql://neondb_owner:npg_5wAMYQxOi9ZW@ep-sparkling-tooth-ag2jhfzt.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require
```

### 3️⃣ Restart App
```bash
python app.py
```

### 4️⃣ Test
- Open: `http://localhost:5000`
- Login with admin credentials
- ✅ Should work!

---

## Why This Works

| Issue | Before | After |
|-------|--------|-------|
| **Flag** | Hardcoded `False` | Reads from `.env` |
| **Login** | Raw SQLite | SQLAlchemy ORM |
| **Database** | Wrong connection | Correct PostgreSQL |

**Result:** App connects to PostgreSQL instead of empty local SQLite file ✅

---

## What Was Updated in app.py

1. **Line 75-81:** Reads `USE_POSTGRESQL` from `.env` instead of hardcoding
2. **Line 2153:** Login function uses ORM instead of raw SQL
3. **Line 945:** Database init uses ORM for both modes

---

**Done!** Both PCs now share PostgreSQL data. 🎉
