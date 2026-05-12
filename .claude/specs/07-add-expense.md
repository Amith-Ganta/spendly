# Spec: Add Expense

## Overview
Step 7 turns the existing `/expenses/add` stub into a working feature that lets
a signed-in user record a new expense. The page presents a single form
(amount, category, date, optional description); on submit the server validates
the input, inserts a row into the `expenses` table scoped to the current
`session["user_id"]`, and redirects back to `/profile` with a success flash
message so the new expense immediately appears in the recent transactions,
summary stats, and category breakdown. This is the first write path into the
`expenses` table and unblocks the Edit (Step 8) and Delete (Step 9) flows.

## Depends on
- Step 1: Database setup (`expenses` table with `user_id`, `amount`, `category`,
  `date`, `description` columns must exist)
- Step 3: Login and logout (a logged-in `session["user_id"]` is required to
  attribute the new expense)
- Step 5: Backend connection (`/profile` must already read from
  `database/queries.py` so the newly inserted row shows up on redirect)

## Routes
- `GET  /expenses/add` — render the empty add-expense form — logged-in
- `POST /expenses/add` — validate form input, insert into `expenses`, flash
  success message, redirect to `/profile` — logged-in

Both must reject unauthenticated requests (redirect to `/login`, matching the
existing `/profile` pattern).

## Database changes
No database changes. The `expenses` table already has every column this
feature writes to (`user_id`, `amount`, `category`, `date`, `description`,
`created_at`). The `created_at` default (`datetime('now')`) handles itself.

## Templates
- **Create:** `templates/add_expense.html` — extends `base.html`; contains a
  single `<form method="POST" action="{{ url_for('add_expense') }}">` with:
  - `amount` — `<input type="number" step="0.01" min="0.01" required>`
  - `category` — `<select required>` populated from a fixed list (see Rules)
  - `date` — `<input type="date" required>`, defaulting to today
  - `description` — `<textarea>` (optional)
  - Submit button labelled "Add Expense"
  - Cancel link back to `/profile`
  - A flash-message block reusing the styling already used elsewhere
  - On validation error, re-render this template with the user's submitted
    values pre-filled and the relevant error flashed
- **Modify:** `templates/profile.html` — wire the existing "Add Expense" button
  (currently a stub) so its `href` uses `url_for("add_expense")`. If the button
  does not yet exist on the profile page, add it to the page header area.

## Files to change
- `app.py`
  - Replace the placeholder `add_expense()` handler with a real
    `methods=["GET", "POST"]` view:
    - Auth check: if no `session["user_id"]`, redirect to `login`
    - GET: render `add_expense.html` with today's date as the default
    - POST: validate fields (see Rules); on error flash + re-render form with
      submitted values; on success call the new
      `database.db.create_expense(...)` helper, flash a success message, and
      redirect to `url_for("profile")`
- `database/db.py`
  - Add `create_expense(user_id, amount, category, date, description)` —
    parameterised `INSERT` returning the new row id. Description may be
    `None`/empty string; store `None` if blank.
- `templates/profile.html` — point the "Add Expense" button at
  `url_for("add_expense")`

## Files to create
- `templates/add_expense.html` — the form page
- `static/css/add_expense.css` — page-specific styles (form layout, error
  states). Uses CSS variables only — no hardcoded colours.
- `tests/test_07-add-expense.py` — spec-derived tests covering:
  - GET `/expenses/add` requires login
  - GET renders form with today's date pre-filled
  - POST with valid data inserts a row scoped to the session user and
    redirects to `/profile`
  - POST with missing/invalid amount, category, or date re-renders the form
    with a flashed error and no DB write
  - POST with an empty description stores `NULL`
  - Newly inserted expense appears in `/profile` recent transactions and
    summary stats on the redirect

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only via `get_db()`
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with werkzeug (no auth changes in this step)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No inline `<style>` tags; page-specific CSS lives in `static/css/`
- The DB write helper belongs in `database/db.py` (not `queries.py`, which is
  read-side only)
- Categories must be a fixed server-side list matching the seed data:
  `Food, Transport, Bills, Health, Entertainment, Shopping, Other`. Any other
  value is a validation error.
- Amount validation: parse as float; must be `> 0`; reject negatives, zero,
  and non-numeric input.
- Date validation: must parse via `datetime.strptime(value, "%Y-%m-%d")`; on
  failure, flash an error and re-render the form.
- Description is optional; trim whitespace; store `None` if the trimmed value
  is empty.
- The new row's `user_id` MUST come from `session["user_id"]` — never trust a
  form field for ownership.
- On successful insert, flash a single success message
  (e.g. "Expense added.") and redirect to `/profile` (POST/redirect/GET).
- The form `action` must use `url_for("add_expense")` — never a hardcoded path.
- All amounts shown in the UI continue to use the ₹ symbol (Indian Rupee).

## Definition of done
- [ ] `GET /expenses/add` while logged out redirects to `/login`
- [ ] `GET /expenses/add` while logged in renders the form with today's date
  pre-filled in the date field
- [ ] The category dropdown shows the seven allowed categories
- [ ] Submitting the form with valid amount, category, and date inserts one
  row into `expenses` for the logged-in user and redirects to `/profile`
- [ ] The newly created expense is visible in the "Recent Transactions"
  section and counted in the summary stats on the `/profile` page after the
  redirect
- [ ] Submitting with a missing or non-numeric amount re-renders the form,
  flashes an error, and does not insert a row
- [ ] Submitting with amount ≤ 0 re-renders the form, flashes an error, and
  does not insert a row
- [ ] Submitting with an unknown category re-renders the form, flashes an
  error, and does not insert a row
- [ ] Submitting with a malformed or missing date re-renders the form,
  flashes an error, and does not insert a row
- [ ] Submitting with an empty description succeeds and stores `NULL` for
  `description`
- [ ] The "Add Expense" button on the profile page links to `/expenses/add`
- [ ] No raw hex colours appear in `static/css/add_expense.css` — only CSS
  variables
- [ ] `add_expense.html` extends `base.html`
- [ ] All amounts on the form and redirect target render with the ₹ symbol
