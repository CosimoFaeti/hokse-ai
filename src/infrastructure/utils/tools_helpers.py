from datetime import datetime, timedelta


def resolve_period(period: str, now: datetime) -> tuple[datetime, datetime]:
	""""""
	if period == "this_week":
		start: datetime = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
		return start, now
	if period == "last_week":
		end = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
		start = end - timedelta(weeks=1)
		return start, end
	if period == "this_month":
		start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
		return start, now
	if period == "last_30_days":
		return now - timedelta(days=30), now
	if period == "last_90_days":
		return now - timedelta(days=90), now
