"""
gauges.py — Plotly gauge and bar chart helpers for the dashboard.
"""

import plotly.graph_objects as go


def create_health_gauge(cal_pct: float, gauge_color: str) -> go.Figure:
    """Create the battery health gauge indicator."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=cal_pct,
        number={"suffix": "%", "font": {"size": 20}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": gauge_color},
            "steps": [
                {"range": [0, 70],  "color": "#fee2e2"},
                {"range": [70, 90], "color": "#fef3c7"},
                {"range": [90, 100], "color": "#d1fae5"},
            ],
        },
    ))
    fig.update_layout(
        height=180,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_qvalue_bar(q_values) -> go.Figure:
    """Create the Q-value comparison bar chart."""
    fig = go.Figure(data=[go.Bar(
        x=["Increase", "Maintain", "Decrease"],
        y=q_values.tolist(),
        marker_color=["#10b981", "#f59e0b", "#ef4444"],
    )])
    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


# Health label → gauge colour mapping
GAUGE_COLORS = {
    "Healthy": "#10b981",
    "Moderate": "#f59e0b",
    "Degrading": "#f97316",
    "Severely Degraded": "#ef4444",
}
