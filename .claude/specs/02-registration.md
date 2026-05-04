# Spec: Registration

## Overview

Implements the full user registration flow. `GET /register` already renders the
form template; this step adds `POST /register` to process submissions — validate
inputs, hash the password with werkzeug, insert the new user via a `db.py` helper,
store `user_id` in the Flask session, and redirect on success. It also wires up
Flask's `secret_key` (required for sessions) and fixes the hardcoded form action
URL in the template.

## Depends on

- **Step 1 — Database Setup**: `users` table and `get_db()` must exist.

## Routes

- `POST /register` — validate form data, create user, set session, redirect — public

> `GET /register` already exists; the route function must be updated to handle
> both methods (`methods=["GET", "POST"]`).

## Database changes

No database changes — the `users` table from Step 1 is sufficient.

## Templates

- **Modify** `templates/register.html`:
  - Replace hardcoded `action="/register"` with `action="{{ url_for('register') }}"`
  - The `{% if error %}` block is already in place — no change needed there

## Files to change

| File | Change |
|---|---|
| `app.py` | Add `secret_key`; import `session`, `redirect`, `url_for`, `request`; convert `register` to GET+POST handler |
| `database/db.py` | Add `create_user(name, email, password_hash)` helper |
| `templates/register.html` | Fix hardcoded form action URL |

## Files to create

None.

## New dependencies

No new dependencies — `werkzeug.security` is already installed.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings or `.format()` in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` — never store plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set before any session use (use a hard-coded dev string — no `.env` required for this step)
- Follow the Post/Redirect/Get pattern: on success, `redirect()` — never `render_template()` from a POST handler
- `create_user()` must live in `database/db.py`, not inline in the route
- On duplicate email, catch the `sqlite3.IntegrityError` and re-render the form with `error="An account with that email already exists."`
- Minimum password length: 8 characters — validate server-side and return an error if too short

## Definition of done

- [ ] `GET /register` renders the form (unchanged behaviour)
- [ ] Submitting valid name/email/password creates a row in `users` with a hashed password
- [ ] After successful registration, the browser is redirected (HTTP 302) — not shown a raw response
- [ ] `session["user_id"]` is set immediately after registration
- [ ] Submitting a duplicate email re-renders the form with a visible error message
- [ ] Submitting a password shorter than 8 characters re-renders the form with a visible error message
- [ ] The `users` table never contains a plaintext password
- [ ] The form action uses `url_for()` — no hardcoded URL
