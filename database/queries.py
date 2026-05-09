from datetime import datetime

from .db import get_db


def _initials(name):
    parts = [p for p in name.split() if p]
    return "".join(p[0].upper() for p in parts)[:2]


def _format_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{dt.day} {dt:%b %Y}"


def _format_member_since(created_at):
    dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%B %Y")


def get_user_by_id(user_id):
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT name, email, created_at FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        return None
    return {
        "name": row["name"],
        "email": row["email"],
        "member_since": _format_member_since(row["created_at"]),
        "initials": _initials(row["name"]),
    }


def get_summary_stats(user_id):
    conn = get_db()
    try:
        totals = conn.execute(
            "SELECT COUNT(*) AS n, COALESCE(SUM(amount), 0) AS total "
            "FROM expenses WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        top = conn.execute(
            "SELECT category FROM expenses WHERE user_id = ? "
            "GROUP BY category ORDER BY SUM(amount) DESC, category ASC LIMIT 1",
            (user_id,),
        ).fetchone()
    finally:
        conn.close()

    count = totals["n"] if totals else 0
    if count == 0:
        return {"total_spent": "0.00", "transaction_count": 0, "top_category": "—"}
    return {
        "total_spent": f"{totals['total']:.2f}",
        "transaction_count": count,
        "top_category": top["category"],
    }


def get_recent_transactions(user_id, limit=10):
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT date, description, category, amount FROM expenses "
            "WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    finally:
        conn.close()

    return [
        {
            "date": _format_date(r["date"]),
            "description": r["description"],
            "category": r["category"],
            "amount": f"{r['amount']:.2f}",
        }
        for r in rows
    ]


def get_category_breakdown(user_id):
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT category AS name, SUM(amount) AS total FROM expenses "
            "WHERE user_id = ? GROUP BY category ORDER BY total DESC, category ASC",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        return []

    grand = sum(r["total"] for r in rows)
    if grand == 0:
        return [
            {"name": r["name"], "total": f"{r['total']:.2f}", "pct": 0}
            for r in rows
        ]

    pcts = [round(r["total"] / grand * 100) for r in rows]
    delta = 100 - sum(pcts)
    pcts[0] += delta

    return [
        {"name": r["name"], "total": f"{r['total']:.2f}", "pct": pcts[i]}
        for i, r in enumerate(rows)
    ]
