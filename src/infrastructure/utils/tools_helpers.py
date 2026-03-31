import datetime
from datetime import datetime, timedelta

def resolve_period(period: str, now: datetime) -> tuple[datetime, datetime]:
    """"""
    if period == "this_week":
        start: datetime = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return start, now
    if period == "last_week":
        end = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        start = end - timedelta(weeks=1)
        return start, end
    if period == "this_month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return start, now
    if period == "last_30_days":
        return now - timedelta(days=30), now
    if period == "last_90_days":
        return now - timedelta(days=90), now

def prev_numeric(week_values: list[tuple[str, float | None]], current_idx: int) -> float | None:
    """"""
    for i in range(current_idx - 1, -1, -1):
        if week_values[i][1] is not None:
            return week_values[i][1]
    return None

def format_delta(val: float, prev: float | None, metric: str) -> str:
    """"""
    if prev is None or prev == 0:
        return ""

    pct = (val - prev) / prev * 100

    # For pace, a negative delta is actually an improvement
    if metric == "pace":
        label = "faster" if pct < 0 else "slower"
        return f"  ({pct:+.1f}%  {label})"

    return f"  ({pct:+.1f}%)"

def overall_trend(values: list[float], metric: str) -> str:
    if len(values) < 2:
        return "Overall trend: insufficient data."

    mid = max(len(values) // 2, 1)
    first_avg = sum(values[:mid]) / mid
    second_avg = sum(values[mid:]) / max(len(values) - mid, 1)

    if first_avg == 0:
        return "Overall trend: stable (no baseline data)."

    change_pct = (second_avg - first_avg) / first_avg * 100

    if metric == "pace":
        if change_pct < -5:
            direction = f"IMPROVING ({change_pct:+.1f}%  faster)"
        elif change_pct > 5:
            direction = f"DECLINING ({change_pct:+.1f}%  slower)"
        else:
            direction = f"STABLE ({change_pct:+.1f}%)"
    else:
        if change_pct > 5:
            direction = f"INCREASING ({change_pct:+.1f}%)"
        elif change_pct < -5:
            direction = f"DECREASING ({change_pct:+.1f}%)"
        else:
            direction = f"STABLE ({change_pct:+.1f}%)"

    return f"Overall trend: {direction}"

def stats(activities: list) -> dict:
    if not activities:
        return {
            "count": 0,
            "distance_km": 0.0,
            "time_min": 0.0,
            "elevation_m": 0.0,
            "avg_hr": None,
            "avg_pace": None,
            "total_load": 0.0,
        }

    hr_readings = [a.average_heartrate for a in activities if a.average_heartrate]
    pace_readings = [a.pace_min_per_km for a in activities if a.pace_min_per_km]

    return {
        "count": len(activities),
        "distance_km": sum(a.distance_km for a in activities),
        "time_min": sum(a.moving_time_minutes for a in activities),
        "elevation_m": sum(a.total_elevation_gain for a in activities),
        "avg_hr": sum(hr_readings) / len(hr_readings) if hr_readings else None,
        "avg_pace": sum(pace_readings) / len(pace_readings) if pace_readings else None,
        "total_load": float(sum(a.suffer_score or 0 for a in activities)),
    }

def _row(
        label: str,
        val_b: float | None,
        val_a: float | None,
        fmt: str = ".1f",
        unit: str = "",
        invert: bool = False,
) -> str:
    b_str = f"{val_b:{fmt}}{unit}" if val_b is not None else "—"
    a_str = f"{val_a:{fmt}}{unit}" if val_a is not None else "—"

    if val_a is not None and val_b is not None and val_b != 0:
        delta_abs = val_a - val_b
        delta_pct = delta_abs / val_b * 100
        sign = "+" if delta_abs >= 0 else ""

        if invert:
            arrow = "↑" if delta_abs < 0 else ("↓" if delta_abs > 0 else "→")
        else:
            arrow = "↑" if delta_abs > 0 else ("↓" if delta_abs < 0 else "→")

        delta_str = f"{sign}{delta_abs:{fmt}}{unit}  ({sign}{delta_pct:.1f}%)  {arrow}"
    else:
        delta_str = "—"

    return f"  {label:<20}  {'':>12}  {b_str:>14}  {a_str:>14}  {delta_str:>12}"