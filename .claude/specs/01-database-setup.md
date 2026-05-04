# Step 1 — Database Setup

## Overview

Replace the stub in `database/db.py` with a working SQLite implementation.
This is the **foundation step** — authentication, profiles, and expense tracking all depend on it.

---

## Dependencies

- **Depends on:** Nothing — this is the first step
- **No new routes** — existing placeholder routes in `app.py` remain unchanged

---

## Database Schema

### `users` table

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | Primary key, autoincrement |
| `name` | TEXT | Not null |
| `email` | TEXT | Unique, not null |
| `password_hash` | TEXT | Not null |
| `created_at` | TEXT | Default `datetime('now')` |

### `expenses` table

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | Primary key, autoincrement |
| `user_id` | INTEGER | Foreign key → `users.id`, not null |
| `amount` | REAL | Not null |
| `category` | TEXT | Not null |
| `date` | TEXT | Not null (YYYY-MM-DD format) |
| `description` | TEXT | Nullable |
| `created_at` | TEXT | Default `datetime('now')` |

---

## Functions to Implement (`database/db.py`)

### `get_db()`
- Opens connection to `spendly.db` in project root
- Sets `row_factory = sqlite3.Row` (dictionary-like row access)
- Runs `PRAGMA foreign_keys = ON`
- Returns the connection

### `init_db()`
- Creates both tables using `CREATE TABLE IF NOT EXISTS`
- Safe to call multiple times without error

### `seed_db()`
- Checks if `users` table already has data → returns early if yes (no duplicates)
- Inserts one demo user:
  - name: `Demo User`
  - email: `demo@spendly.com`
  - password: `demo123` (hashed with `werkzeug.security`)
- Inserts 8 sample expenses:
  - All linked to the demo user
  - Cover multiple categories
  - Dates spread across the current month
  - At least one expense per category

---

## Changes to `app.py`

```python
from database.db import get_db, init_db, seed_db

with app.app_context():
    init_db()
    seed_db()
```

---

## Files to Change

| File | Change |
|---|---|
| `database/db.py` | Implement `get_db()`, `init_db()`, `seed_db()` |
| `app.py` | Add imports and startup calls |

**No new files to create.**

---

## Dependencies & Categories

**Packages** — no new installs needed:
- `sqlite3` (standard library)
- `werkzeug.security` (already installed)

**Fixed category list** — use exactly these values:

`Food` · `Transport` · `Bills` · `Health` · `Entertainment` · `Shopping` · `Other`

---

## Rules

- No ORMs (no SQLAlchemy)
- Parameterized queries only — never use f-strings or string formatting in SQL
- `PRAGMA foreign_keys = ON` on every connection
- Store `amount` as `REAL`, not `INTEGER`
- Hash passwords with `werkzeug.security.generate_password_hash`
- Dates must follow `YYYY-MM-DD` format consistently

---

## Expected Behavior

| Function | Expected |
|---|---|
| `get_db()` | Returns connection with dict-like rows and FK enforcement on |
| `init_db()` | Creates tables safely, no error on repeated runs |
| `seed_db()` | Inserts demo data once only, skips if data already exists |
| DB constraints | Rejects duplicate emails and invalid foreign keys |

---

## Error Handling

| Scenario | Expected outcome |
|---|---|
| Duplicate email insert | Fails with `UNIQUE constraint` error |
| Expense with invalid `user_id` | Fails with foreign key constraint error |
| Invalid query | Raises a clear error for debugging |

---

## Definition of Done

- [ ] Database file created on app startup
- [ ] Both tables exist with correct schema and constraints
- [ ] Demo user exists with hashed password
- [ ] 8 sample expenses exist across all categories
- [ ] No duplicate seed data on repeated runs
- [ ] App starts without errors
- [ ] Foreign key enforcement works
- [ ] All queries use parameterized SQL
