"""UI and Visualization Helpers for Streamlit Dashboard.

Provides Plotly score gauges, radar charts, skill category breakdowns,
and sample resume/job description loader utilities.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List
import plotly.graph_objects as go


def load_sample_file(relative_path: str) -> str:
    """Read a sample text or document file from data directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, relative_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""


def create_score_gauge(score: float, tier: str, tier_color: str) -> go.Figure:
    """Generate an interactive Plotly radial gauge for the overall ATS score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>ATS Compatibility: {tier}</b>", 'font': {'size': 16, 'color': '#1e293b'}},
        number={'suffix': "%", 'font': {'size': 44, 'color': tier_color, 'family': "Arial, sans-serif"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
            'bar': {'color': tier_color, 'thickness': 0.3},
            'bgcolor': "#f1f5f9",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': '#fee2e2'},
                {'range': [50, 70], 'color': '#fef3c7'},
                {'range': [70, 85], 'color': '#dbeafe'},
                {'range': [85, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "#0f172a", 'width': 3},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(
        height=260,
        margin=dict(l=25, r=25, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif")
    )
    return fig


def create_category_radar_chart(
    resume_by_cat: Dict[str, List[str]], 
    jd_by_cat: Dict[str, List[str]]
) -> go.Figure:
    """Create a radar/spider chart comparing skills count across technical categories."""
    categories = sorted(list(set(list(resume_by_cat.keys()) + list(jd_by_cat.keys()))))
    if not categories:
        categories = ["General Competencies"]

    resume_counts = [len(resume_by_cat.get(cat, [])) for cat in categories]
    jd_counts = [len(jd_by_cat.get(cat, [])) for cat in categories]

    # Close the radar loop
    radar_cats = categories + [categories[0]]
    r_counts = resume_counts + [resume_counts[0]]
    j_counts = jd_counts + [jd_counts[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=j_counts,
        theta=radar_cats,
        fill='toself',
        fillcolor='rgba(239, 68, 68, 0.15)',
        line=dict(color='#ef4444', width=2),
        name='Job Description Target'
    ))

    fig.add_trace(go.Scatterpolar(
        r=r_counts,
        theta=radar_cats,
        fill='toself',
        fillcolor='rgba(16, 185, 129, 0.25)',
        line=dict(color='#10b981', width=2),
        name='Your Resume'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(r_counts + j_counts, default=1) + 1, 5)],
                tickfont=dict(size=10, color="#64748b")
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#1e293b", family="sans-serif")
            )
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        height=340,
        margin=dict(l=40, r=40, t=20, b=40),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def create_keyword_comparison_bar(top_keywords: List[tuple]) -> go.Figure:
    """Horizontal bar chart showing top keywords extracted from job description."""
    if not top_keywords:
        return go.Figure()

    terms = [t[0] for t in reversed(top_keywords[:10])]
    scores = [round(t[1] * 100, 1) for t in reversed(top_keywords[:10])]

    fig = go.Figure(go.Bar(
        x=scores,
        y=terms,
        orientation='h',
        marker=dict(
            color=scores,
            colorscale='Blues',
            showscale=False
        ),
        text=[f"{s}%" for s in scores],
        textposition='outside'
    ))

    fig.update_layout(
        title="<b>Top Weighted Keywords in Job Description (TF-IDF)</b>",
        title_font=dict(size=14, color="#1e293b"),
        xaxis=dict(title="Relative Importance Weight (%)", showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(autorange="reversed"),
        height=320,
        margin=dict(l=10, r=40, t=40, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig
