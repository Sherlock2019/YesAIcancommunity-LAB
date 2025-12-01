from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, Callable

import streamlit as st


def _style_base() -> None:
    if st.session_state.get("_neon_table_styles"):
        return
    st.session_state["_neon_table_styles"] = True
    st.markdown(
        """
        <style>
        .neon-table-wrapper {
            border: 1px solid rgba(56,189,248,0.35);
            border-radius: 18px;
            margin: 1.5rem 0;
            box-shadow: 0 18px 40px rgba(15,23,42,0.35);
            overflow: hidden;
        }
        .neon-table-header {
            background: linear-gradient(90deg, rgba(59,130,246,0.4), rgba(14,165,233,0.2));
            padding: 1.2rem;
            border-bottom: 1px solid rgba(56,189,248,0.25);
            color: #e0f2fe;
            font-weight: 700;
            font-size: 1.2rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .neon-table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(15,23,42,0.85);
        }
        .neon-table.light {
            background: rgba(15,23,42,0.9);
        }
        .neon-table th {
            text-align: left;
            padding: 0.9rem 1rem;
            font-size: 0.95rem;
            color: #93c5fd;
            border-bottom: 1px solid rgba(56,189,248,0.25);
        }
        .neon-table td {
            padding: 0.9rem 1rem;
            border-bottom: 1px solid rgba(51,65,85,0.7);
            color: #e2e8f0;
            font-size: 0.94rem;
        }
        .neon-table tr:hover {
            background: rgba(30,64,175,0.15);
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            font-size: 0.8rem;
            padding: 0.15rem 0.65rem;
            border-radius: 999px;
            font-weight: 600;
            letter-spacing: 0.02em;
            box-shadow: 0 0 12px rgba(255,255,255,0.2);
        }
        .status-blue { background: rgba(59,130,246,0.2); color: #38bdf8; border: 1px solid rgba(59,130,246,0.5); }
        .status-green { background: rgba(34,197,94,0.2); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.4); }
        .status-yellow { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(234,179,8,0.45); }
        .status-cyan { background: rgba(45,212,191,0.2); color: #5eead4; border: 1px solid rgba(34,197,94,0.4); }
        .status-red { background: rgba(248,113,113,0.2); color: #fda4af; border: 1px solid rgba(248,113,113,0.35); }
        .rating-stars span {
            font-size: 1rem;
            color: gold;
            margin-right: 1px;
        }
        .neon-table-actions button {
            width: 100%;
        }
        .neon-table-empty {
            padding: 1.5rem;
            text-align: center;
            color: #94a3b8;
        }
        .neon-table-search {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.8rem 1rem;
            background: rgba(15,23,42,0.65);
            border-bottom: 1px solid rgba(56,189,248,0.2);
        }
        .neon-table-search input, .neon-table-search select {
            width: 100%;
        }
        .neon-table-accordion {
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _status_class(status: str) -> str:
    if not status:
        return "status-blue"
    status = status.strip().lower()
    mapping = {
        "new": "status-blue",
        "available": "status-green",
        "mvp": "status-yellow",
        "production ready": "status-cyan",
        "production": "status-cyan",
        "deprecated": "status-red",
        "incubation": "status-blue",
    }
    return mapping.get(status, "status-blue")


def render_neon_table(
    *,
    title: Optional[str] = None,
    columns: Sequence[Tuple[str, str]],
    rows: Sequence[Dict[str, Any]],
    search_enabled: bool = False,
    sort_options: Optional[List[Tuple[str, str]]] = None,
    empty_label: str = "No records found.",
    key: Optional[str] = None,
    group_by: Optional[str] = None,
    on_rate: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> None:
    """
    Render a neon-styled table with optional search and grouping.

    columns: List of tuples (key, label).
    rows: list of dicts with keys matching column keys.
    """
    _style_base()
    table_key = key or f"neon_table_{hash(title)}"
    theme = st.session_state.get("yes_mode", "dark")

    search_term = ""
    sort_key = sort_options[0][0] if sort_options else None
    if search_enabled or sort_options:
        st.markdown("<div class='neon-table-wrapper'>", unsafe_allow_html=True)
        if title:
            st.markdown(f"<div class='neon-table-header'>{title}</div>", unsafe_allow_html=True)
        with st.container():
            cols = []
            if search_enabled:
                cols.append("search")
            if sort_options:
                cols.append("sort")
            if cols:
                ccols = st.columns(len(cols))
                idx = 0
                if "search" in cols:
                    search_term = ccols[idx].text_input("Search", key=f"{table_key}_search")
                    idx += 1
                if sort_options:
                    sort_key = ccols[idx].selectbox(
                        "Sort by",
                        options=[opt[0] for opt in sort_options],
                        format_func=lambda v: dict(sort_options)[v],
                        key=f"{table_key}_sort",
                    )
        filtered = list(rows)
        if search_term:
            lowered = search_term.lower()
            filtered = [
                row
                for row in filtered
                if any(lowered in str(value).lower() for value in row.values())
            ]
        if sort_key:
            filtered.sort(key=lambda r: r.get(sort_key) or "", reverse=False)

        if group_by:
            groups: Dict[str, List[Dict[str, Any]]] = {}
            for row in filtered:
                groups.setdefault(str(row.get(group_by, "Other")), []).append(row)
            for group_name, group_rows in groups.items():
                with st.expander(f"{group_name} ({len(group_rows)})", expanded=False):
                    _render_table_inner(
                        columns=columns,
                        rows=group_rows,
                        empty_label=empty_label,
                        theme=theme,
                        table_key=f"{table_key}_{group_name}",
                        on_rate=on_rate,
                    )
        else:
            _render_table_inner(
                columns=columns,
                rows=filtered,
                empty_label=empty_label,
                theme=theme,
                table_key=table_key,
                on_rate=on_rate,
            )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        _render_table_inner(
            columns=columns,
            rows=rows,
            empty_label=empty_label,
            theme=theme,
            table_key=table_key,
            title=title,
            on_rate=on_rate,
        )


def _render_table_inner(
    *,
    columns: Sequence[Tuple[str, str]],
    rows: Sequence[Dict[str, Any]],
    empty_label: str,
    theme: str,
    table_key: str,
    title: Optional[str] = None,
    on_rate: Optional[Callable[[Dict[str, Any]], None]],
) -> None:
    if title:
        st.markdown(
            f"""
            <div class="neon-table-wrapper">
            <div class="neon-table-header">{title}</div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown("<div class='neon-table-wrapper'>", unsafe_allow_html=True)

    table_class = "neon-table" + (" light" if theme != "dark" else "")
    if not rows:
        st.markdown(f"<div class='neon-table-empty'>{empty_label}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    header_html = "<tr>" + "".join(f"<th>{label}</th>" for _, label in columns) + "</tr>"
    row_html = ""
    for idx, row in enumerate(rows):
        cells = []
        for col_key, _ in columns:
            value = row.get(col_key, "")
            if isinstance(value, dict) and value.get("_type") == "badge":
                badge_class = _status_class(value.get("variant", ""))
                cells.append(f"<td><span class='status-badge {badge_class}'>{value.get('text')}</span></td>")
            elif isinstance(value, dict) and value.get("_type") == "rating":
                rating_num = value.get("value", 0)
                stars = "".join("<span>★</span>" for _ in range(int(round(rating_num))))
                if on_rate:
                    placeholder = f"<button class='stButton'>{stars or 'Rate'}</button>"
                    cells.append(f"<td class='rating-stars'>{placeholder}</td>")
                else:
                    cells.append(f"<td class='rating-stars'>{stars or '—'}</td>")
            elif isinstance(value, dict) and value.get("_type") == "actions":
                actions_html = "<div class='neon-table-actions'>"
                for action in value.get("items", []):
                    btn_key = f"{table_key}_{idx}_{action.get('label')}"
                    if st.button(action.get("label", "Action"), key=btn_key):
                        callback = action.get("on_click")
                        if callable(callback):
                            callback(row)
                    actions_html += "<br/>"
                actions_html += "</div>"
                cells.append(f"<td>{actions_html}</td>")
            else:
                cells.append(f"<td>{value}</td>")
        row_html += "<tr>" + "".join(cells) + "</tr>"
    st.markdown(f"<table class='{table_class}'>" + header_html + row_html + "</table></div>", unsafe_allow_html=True)
