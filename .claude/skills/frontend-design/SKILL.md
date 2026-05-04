---
name: spendly-ui-designer
description: >
  Generates modern, production-ready UI components and pages for Spendly, a Flask-based personal
  expense tracker (https://github.com/campusx-official/spendly). Use this skill whenever the user
  wants to design, build, create, redesign, improve, or style any Spendly page, screen, section,
  or component — including phrasings like "design the X page", "create UI for X", "build a
  component for X", "make X look better", "redesign X", or any request about Spendly's frontend,
  layout, CSS, or visual polish — even when Spendly isn't named explicitly if the conversation
  context is clearly about it. Also trigger when the user shares a screenshot or description of an
  existing Spendly page and asks for improvements. Do NOT wait for the user to say "use the Spendly
  skill" — if the request is about Spendly UI, use this skill automatically.
---

# Spendly UI Designer

You are designing frontend UI for **Spendly**, a personal expense tracker. Spendly is a Flask app
with server-rendered Jinja2 templates, vanilla CSS, and a sprinkle of vanilla JS. Generate UI that
feels like it belongs in a polished, modern fintech product — not generic Bootstrap-era output, and
not React/Tailwind output that doesn't match the stack.

**Stack summary:**
- Backend: Flask (`app.py`), SQLite or similar
- Templates: Jinja2 in `templates/` (e.g. `base.html`, `dashboard.html`, `add_expense.html`)
- Styles: vanilla CSS in `static/css/` — no Tailwind, no preprocessors
- Scripts: small vanilla JS in `static/js/` for interactions (toggles, modals, chart init)
- Icons: Lucide via CDN, used as `<i data-lucide="icon-name">`, initialized with `lucide.createIcons()`

Do not introduce React, Vue, Tailwind, shadcn, or Bootstrap unless the user explicitly asks.

---

## Before You Design: Check What Already Exists

If the user's project files are available (shared repo, uploaded files, or you're in the codebase),
open `base.html`, the main CSS file, and one or two existing templates before generating anything.
Look for and reuse:

- CSS custom properties (`--color-primary`, `--color-bg`, `--color-surface`, spacing tokens, etc.)
- Existing component classes: `.card`, `.btn`, `.input`, `.badge`, `.table`
- The base layout — sidebar? topbar? container width? Follow it.
- Font family and type scale

If you can't see existing files and the request is non-trivial, ask:
> "Do you have a screenshot or a snippet of the existing Spendly UI? It'll help me match the style."

One screenshot saves three rounds of revision.

---

## Design Language

When you have no existing reference, default to this clean, fintech-leaning aesthetic — close in
spirit to Linear, Notion, or modern banking apps.

### Colors (defaults — override to match existing)
- **Background:** `#F7F8FA` (near-white neutral)
- **Surface (cards):** `#FFFFFF` with soft border `#E5E7EB` and/or subtle shadow
- **Text primary:** `#111827` · **Text secondary:** `#6B7280`
- **Primary accent:** one confident color — indigo `#6366F1`, emerald `#10B981`, or similar. Pick one, stick with it.
- **Semantic:** green `#10B981` (income/positive), red `#EF4444` (expense/negative), amber `#F59E0B` (warnings)

### Spacing
8px grid. Use multiples of 4px or 8px for padding, gap, margin. No arbitrary values like 13px or 27px.

### Radius
- `8px` — inputs, small elements
- `12px` — cards
- `16px` — modals
- Fully rounded — pills, badges

### Shadows
Subtle only. `0 1px 2px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.06)` is the ceiling. No glows, no heavy drops.

### Typography
System stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` (or Inter if the project uses it).
Type scale: 12 / 14 / 16 / 20 / 24 / 32px. Weights: 400 body, 500 medium, 600 semibold for headings.
**Amounts and numbers:** always use `font-variant-numeric: tabular-nums` so columns align.

### Layout Patterns
- Card-based composition — group related info in surfaces, don't sprawl
- Generous whitespace — tight layouts read as cluttered in finance apps
- Left-aligned with clear hierarchy; centered only for empty states and auth
- Tables: always row hover, right-align numeric columns, horizontal scroll on mobile
- Forms: label above input, helper text below, error state in red with icon

### Icons (Lucide)
Load once in `base.html`:
```html
<script src="https://unpkg.com/lucide@1.14.0/dist/umd/lucide.js"></script>
```
Call `lucide.createIcons()` after DOM ready (and after any dynamic DOM insert). Use in templates:
```html
<i data-lucide="wallet"></i>
```
Size via CSS: 16px inline with text, 20px in buttons, 24px for section headers.

**Spendly-appropriate icon picks:**
- Expense/spend: `arrow-down-right`, `shopping-bag`, `credit-card`
- Income: `arrow-up-right`, `wallet`, `trending-up`
- Budget: `target`, `pie-chart`
- Category: `tag`, `folder`
- Add/new: `plus`, `plus-circle`
- Settings: `settings`, `sliders-horizontal`
- Date: `calendar` · Search: `search` · Filter: `filter`

**Icon density:** one per button, one per section heading, one per table row action. Don't sprinkle icons everywhere.

---

## Output Structure

### 1. Short UI Plan (2–5 bullets)
Name the key sections/components and any notable UX decisions. This is orientation, not a spec.
State any assumptions you're making up front — one line each, no long preamble.

### 2. The Code

**Template** (`templates/...html`):
- Use `{% extends "base.html" %}` and `{% block content %}` unless building `base.html` itself
- Use Jinja2 control flow (`{% for %}`, `{% if %}`) with sensible placeholder variable names
- Add a comment at the top: `{# expects: list of expense dicts with keys: id, title, amount, date, category #}`
- Semantic HTML: `<main>`, `<section>`, `<article>`, `<header>`, `<nav>` where appropriate
- Accessible: `aria-label` on icon-only buttons, proper `<label>` for all inputs

**CSS** (`static/css/...css`):
- Scope all rules with a page/component prefix (`.dashboard-...`, `.tx-table-...`) to prevent leakage
- No inline styles except dynamic Jinja values (e.g. `style="width: {{ pct }}%"`)
- Mobile-first: `@media (min-width: 768px)` for wider layouts
- Group logically: layout → typography → colors → states → responsive

**JS** (only if needed):
- Vanilla only, no frameworks
- Minimal — prefer CSS for animations/transitions
- Add as `<script>` block at the bottom of the template, or reference `static/js/...js`

Put each file in its own fenced code block with a path annotation comment.

### 3. Integration Note (1–3 lines)
Which Flask route renders it, what variables the template expects, any sidebar link or route to add.

---

## Handling Ambiguity

If the request is under-specified ("design the reports page"), make reasonable assumptions and state
them in the UI plan. Don't pepper the user with questions for things you can decide reasonably.

Do ask when the answer genuinely changes the output:
> "Is this a standalone page or a modal on top of the dashboard?"

---

## What to Avoid

- ❌ Generic/dated looks — no sharp-cornered boxes, no default browser styles, no Bootstrap-blue buttons
- ❌ Code dumps without structure — always use labeled blocks (template / CSS / JS)
- ❌ Over-styling — solid beats gradient; border beats shadow when either works. Restraint = quality.
- ❌ Inconsistent spacing — if card padding is 16px in one place, it's 16px everywhere
- ❌ Random color accents — one primary, semantic colors for meaning, everything else neutral
- ❌ Mystery icons — a labeled button beats an unlabeled icon in a finance app
- ❌ Mobile afterthought — stack cards vertically and make tables scrollable below ~768px

---

## Worked Example

**Request:** "Design the add expense form"

**UI plan:**
- Modal dialog (not a full page) — users add expenses inline from the dashboard
- Fields: amount (large, prominent with currency prefix), category (pill selector), date (defaults to today), note (optional)
- Primary "Add expense" button anchors bottom-right; cancel is a subtle text button
- Amount uses `tabular-nums` and a currency symbol prefix

**Code:** `templates/partials/add_expense_modal.html` — extends nothing, included via `{% include %}`. Reuses existing `.input`, `.btn-primary`, `.modal` classes from `base.css` if present; adds new `.category-pill-selector` to `static/css/components.css`.

**JS:** small inline script to open/close modal and reset form on close.