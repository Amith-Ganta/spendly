# Spec: Login and Logout

## Overview

Implements the full login and logout flow. `GET /login` already renders the form;
this step adds `POST /login` to authenticate the user — look up the email, verify
the password with werkzeug, store `user_id` in the Flask session, and redirect to
the expenses dashboard on success. `GET /logout` clears the session and redirects
to the landing page. A `login_required` helper is also introduced so that stub
routes can guard themselves without duplicating session checks.

## Depends on

- **Step 1 — Database Setup**: `users` table and `get_db()` must exist.
- **Step 2 — Registration**: `create_user()` and password hashing must be in place so there are accounts to log in with.

## Routes

- `POST /login` — validate credentials, set session, redirect to `/` — public
- `GET /logout` — clear session, redirect to `/` — public (no login required to log out)

> `GET /login` already exists; the route function must be updated to handle both
> methods (`methods=["GET", "POST"]`).

## Database changes

No database changes — the `users` table from Step 1 is sufficient.

## Templates

- **Modify** `templates/login.html`:
  - Replace hardcoded `action="/login"` with `action="{{ url_for('login') }}"`
  - The `{% if error %}` block is already present — no change needed there

- **Modify** `templates/base.html`:
  - Add a conditional nav link: show "Sign out" (`/logout`) when `session.user_id`
    is set, otherwise show "Sign in" (`/login`) and "Register" (`/register`)

## Files to change

| File | Change |
|---|---|
| `app.py` | Import `session`, `check_password_hash`; convert `login` to GET+POST; implement `logout`; add `login_required` helper |
| `database/db.py` | Add `get_user_by_email(email)` helper |
| `templates/login.html` | Fix hardcoded form action URL |
| `templates/base.html` | Add session-aware nav links |

## Files to create

None.

## New dependencies

No new dependencies — `werkzeug.security` is already installed.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings or `.format()` in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `login_required` must be a plain helper function (not a decorator) that calls
  `abort(401)` or redirects to `/login` — keep it simple; no `functools.wraps` needed
- Follow Post/Redirect/Get: on success, `redirect()` — never `render_template()` from a POST handler
- `get_user_by_email()` must live in `database/db.py`, not inline in the route
- On bad credentials, re-render `login.html` with `error="Invalid email or password."` — never reveal which field was wrong
- `session.clear()` on logout — don't pop individual keys
- After logout, redirect to `url_for('landing')`
- After login, redirect to `url_for('landing')` — a dashboard route does not exist yet

## Definition of done

- [ ] `GET /login` renders the form (unchanged behaviour)
- [ ] Submitting valid email/password sets `session["user_id"]` and redirects (HTTP 302)
- [ ] Submitting an unknown email re-renders the form with a visible error message
- [ ] Submitting a wrong password re-renders the form with the same generic error message
- [ ] `GET /logout` clears the session and redirects to the landing page
- [ ] After logout, `session["user_id"]` is no longer present
- [ ] The login form action uses `url_for('login')` — no hardcoded URL
- [ ] Base nav shows "Sign in" / "Register" when logged out, and "Sign out" when logged in
